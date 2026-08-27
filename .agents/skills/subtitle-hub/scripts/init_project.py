#!/usr/bin/env python3
"""Create a transactionally initialized Subtitle Hub 1.1.0 proofreading project."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

SKILL_VERSION = "1.1.0"
WORK_ID_RE = re.compile(r"SH\d{4,}")
PROJECT_NAME_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
LANGUAGE_RE = re.compile(r"[a-z]{2,3}(?:-[A-Za-z0-9]{2,8})*")
EPISODE_PATTERNS = {
    "tv": re.compile(r"S\d{2}E\d{2,3}"),
    "ona": re.compile(r"S\d{2}E\d{2,3}"),
    "ova": re.compile(r"OVA\d{2,3}"),
    "special": re.compile(r"SP\d{2,3}"),
    "movie": re.compile(r"MOVIE"),
}
EPISODE_MAP_HEADER = ["episode", "video", "subtitle", "audio_stream", "audio_language"]
TEXT_BASELINES = {".ass", ".ssa", ".srt", ".vtt"}
SAFE_COMPONENT_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


def quote(value: object) -> str:
    return json.dumps(value, ensure_ascii=False)


def render(template: Path, values: dict[str, str]) -> str:
    text = template.read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    unresolved = sorted(set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", text)))
    if unresolved:
        raise ValueError(f"unresolved template values in {template.name}: {unresolved}")
    return text


def find_repository_root(start: Path) -> Path | None:
    for candidate in [start.resolve(), *start.resolve().parents]:
        if (candidate / "catalog.yaml").is_file() and (candidate / "works").is_dir():
            return candidate
    return None


def yaml_scalar(text: str, name: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(name)}:\s*[\"']?([^\s\"']+)", text)
    return match.group(1) if match else None


def existing_identities(repository: Path | None) -> tuple[dict[str, Path], dict[str, Path]]:
    work_ids: dict[str, Path] = {}
    subject_ids: dict[str, Path] = {}
    if not repository:
        return work_ids, subject_ids
    for metadata in repository.glob("works/**/project.yaml"):
        text = metadata.read_text(encoding="utf-8-sig")
        work_id = yaml_scalar(text, "id")
        identity = re.search(r"(?ms)^identity:\s*$.*?^  id:\s*[\"']?([^\s\"']+)", text)
        if work_id:
            work_ids[work_id] = metadata.parent
        if identity:
            subject_ids[identity.group(1)] = metadata.parent
    return work_ids, subject_ids


def allocate_work_id(existing: dict[str, Path]) -> str:
    numbers = [int(value[2:]) for value in existing if WORK_ID_RE.fullmatch(value)]
    return f"SH{(max(numbers, default=0) + 1):04d}"


def load_snapshot(path: Path, expected_id: str) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    required = ("id", "name", "name_cn", "date", "platform")
    missing = [key for key in required if data.get(key) in (None, "")]
    total = data.get("total_episodes", data.get("eps"))
    if total in (None, ""):
        missing.append("total_episodes/eps")
    if missing:
        raise ValueError(f"Bangumi snapshot lacks required identity/scope values: {missing}")
    if str(data["id"]) != expected_id:
        raise ValueError(f"Bangumi snapshot id {data['id']} does not match --bangumi-id {expected_id}")
    try:
        data["_total_episodes"] = int(total)
    except (TypeError, ValueError) as error:
        raise ValueError(f"Bangumi episode count is not an integer: {total!r}") from error
    if data["_total_episodes"] <= 0:
        raise ValueError("Bangumi episode count must be positive")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(data["date"])):
        raise ValueError(f"Bangumi date is not an ISO date: {data['date']!r}")
    return data


def load_intake(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 2 or data.get("skill_version") != SKILL_VERSION:
        raise ValueError(f"intake must use schema_version 2 and skill_version {SKILL_VERSION}")
    if not data.get("target_videos") or not data.get("external_source_groups"):
        raise ValueError("intake lacks target videos or source groups")
    if data.get("readiness", {}).get("timing") != "ready":
        raise ValueError("intake timing readiness is not ready; resolve probing/audio questions before initialization")
    if data.get("blocking_questions"):
        raise ValueError(f"intake still has blocking questions: {data['blocking_questions']}")
    return data


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def first_mib_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        digest.update(handle.read(1024 * 1024))
    return digest.hexdigest()


def valid_episode(episode: str, work_type: str) -> bool:
    return bool(EPISODE_PATTERNS[work_type].fullmatch(episode))


def load_episode_map(path: Path, intake: dict[str, object], work_type: str, source_language: str) -> list[dict[str, object]]:
    videos_by_path = {str(Path(item["path"]).resolve()): item for item in intake["target_videos"]}
    baseline_files = {
        str(Path(file["path"]).resolve()): file
        for group in intake["external_source_groups"]
        if "candidate-baseline" in group.get("roles", [])
        for file in group["files"]
    }
    rows: list[dict[str, object]] = []
    seen_episodes: set[str] = set()
    seen_outputs: set[str] = set()
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames != EPISODE_MAP_HEADER:
            raise ValueError("approved episode map header must be: episode<TAB>video<TAB>subtitle<TAB>audio_stream<TAB>audio_language")
        for raw in reader:
            episode = raw["episode"].strip()
            if not valid_episode(episode, work_type):
                raise ValueError(f"unsafe or invalid {work_type} episode ID: {episode!r}")
            if episode in seen_episodes:
                raise ValueError(f"duplicate episode ID: {episode}")
            video_path = str(Path(raw["video"]).expanduser().resolve())
            subtitle_path = str(Path(raw["subtitle"]).expanduser().resolve())
            if video_path not in videos_by_path:
                raise ValueError(f"episode map video is absent from intake: {video_path}")
            if subtitle_path not in baseline_files:
                raise ValueError(f"episode map baseline is absent from intake: {subtitle_path}")
            video_file = Path(video_path)
            subtitle_file = Path(subtitle_path)
            if not video_file.is_file():
                raise ValueError(f"target video is not readable: {video_file}")
            if not subtitle_file.is_file():
                raise ValueError(f"candidate baseline is not readable: {subtitle_file}")
            video = videos_by_path[video_path]
            if video_file.stat().st_size != int(video["size"]) or first_mib_sha256(video_file) != video["sha256_first_mib"]:
                raise ValueError(f"target video changed after intake: {video_file}")
            baseline = baseline_files[subtitle_path]
            if file_sha256(subtitle_file) != baseline["sha256"]:
                raise ValueError(f"candidate baseline changed after intake: {subtitle_file}")
            validate_baseline_source(subtitle_file)
            if not raw["audio_stream"].isdigit():
                raise ValueError(f"audio_stream must be an integer for {episode}")
            audio_index = int(raw["audio_stream"])
            audio_language = raw["audio_language"].strip()
            if not LANGUAGE_RE.fullmatch(audio_language) or audio_language.split("-", 1)[0] != source_language.split("-", 1)[0]:
                raise ValueError(f"audio_language {audio_language!r} does not match source language {source_language!r}")
            streams = [stream for stream in video.get("streams", []) if stream.get("type") == "audio" and stream.get("index") == audio_index]
            if len(streams) != 1:
                raise ValueError(f"selected audio stream {audio_index} is not present in {video['basename']}")
            output_name = f"{Path(video['basename']).stem}.zh-Hans.ass"
            folded = output_name.casefold()
            if folded in seen_outputs:
                raise ValueError(f"target video stems produce a duplicate release filename: {output_name}")
            seen_episodes.add(episode)
            seen_outputs.add(folded)
            rows.append({
                "episode": episode,
                "video": video,
                "subtitle": baseline_files[subtitle_path],
                "subtitle_path": subtitle_path,
                "audio_stream": audio_index,
                "audio_language": audio_language,
                "audio_codec": streams[0].get("codec"),
                "output_name": output_name,
            })
    if not rows:
        raise ValueError("approved episode map is empty")
    if work_type == "movie" and (len(rows) != 1 or rows[0]["episode"] != "MOVIE"):
        raise ValueError("a movie project must map exactly one MOVIE entry")
    return rows


def validate_scope(snapshot: dict[str, object], rows: list[dict[str, object]], work_type: str, scope_approved_by: str) -> str:
    platform = str(snapshot["platform"])
    expected_tokens = {
        "tv": ("tv",), "movie": ("movie", "剧场", "劇場"), "ova": ("ova",),
        "ona": ("web", "ona"), "special": ("special", "sp", "特别", "特別"),
    }[work_type]
    platform_match = any(token.casefold() in platform.casefold() for token in expected_tokens)
    count_match = len(rows) == int(snapshot["_total_episodes"])
    if not scope_approved_by.strip():
        raise ValueError("--scope-approved-by is required after identity/type/episode-scope review")
    if platform_match and count_match:
        return "api-fields-and-user-confirmed"
    return f"user-confirmed-exception: platform={platform!r}, api_total={snapshot['_total_episodes']}, mapped={len(rows)}"


def ass_time(raw: str) -> str:
    match = re.fullmatch(r"(?:(\d+):)?(\d{2}):(\d{2})[,.](\d{3})", raw.strip())
    if not match:
        raise ValueError(f"invalid subtitle timestamp: {raw!r}")
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2))
    seconds = int(match.group(3))
    if minutes >= 60 or seconds >= 60:
        raise ValueError(f"invalid subtitle timestamp: {raw!r}")
    centiseconds = (int(match.group(4)) + 5) // 10
    total_centiseconds = ((hours * 60 + minutes) * 60 + seconds) * 100 + centiseconds
    total_seconds, centiseconds = divmod(total_centiseconds, 100)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}:{minutes:02d}:{seconds:02d}.{centiseconds:02d}"


def subtitle_text_to_ass(text: str) -> str:
    value = html.unescape(text.strip())
    value = re.sub(r"(?i)<br\s*/?>", r"\\N", value)
    value = re.sub(r"(?i)<i>", r"{\\i1}", value)
    value = re.sub(r"(?i)</i>", r"{\\i0}", value)
    value = re.sub(r"(?i)<b>", r"{\\b1}", value)
    value = re.sub(r"(?i)</b>", r"{\\b0}", value)
    value = re.sub(r"<[^>]+>", "", value)
    value = value.replace("\r", "").replace("\n", r"\N")
    return value


def parse_srt(text: str) -> list[tuple[str, str, str]]:
    cues = []
    for block in re.split(r"\n\s*\n", text.replace("\r\n", "\n").strip()):
        lines = block.splitlines()
        time_index = next((index for index, line in enumerate(lines) if "-->" in line), None)
        if time_index is None:
            continue
        start, end = [part.strip().split(" ", 1)[0] for part in lines[time_index].split("-->", 1)]
        cues.append((ass_time(start), ass_time(end), subtitle_text_to_ass("\n".join(lines[time_index + 1 :]))))
    return cues


def parse_vtt(text: str) -> list[tuple[str, str, str]]:
    cleaned = text.replace("\r\n", "\n").lstrip("\ufeff")
    if cleaned.startswith("WEBVTT"):
        cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else ""
    return parse_srt(cleaned)


def validate_baseline_source(source: Path) -> None:
    suffix = source.suffix.lower()
    if suffix not in TEXT_BASELINES:
        raise ValueError(f"candidate baseline cannot create a working master: {source}")
    try:
        text = source.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as error:
        raise ValueError(f"candidate baseline is not UTF-8 text: {source}") from error
    if suffix == ".srt":
        cues = parse_srt(text)
    elif suffix == ".vtt":
        cues = parse_vtt(text)
    else:
        if "[Events]" not in text or not re.search(r"(?m)^Format:.*Start.*End.*Text\s*$", text):
            raise ValueError(f"ASS/SSA candidate baseline lacks a parseable Events section: {source}")
        cues = [()] if re.search(r"(?m)^Dialogue:", text) else []
    if not cues:
        raise ValueError(f"candidate baseline contains no parseable dialogue cues: {source}")


def write_ass_from_cues(destination: Path, cues: list[tuple[str, str, str]]) -> None:
    if not cues:
        raise ValueError("baseline conversion produced zero cues")
    lines = [
        "[Script Info]", "ScriptType: v4.00+", "WrapStyle: 0", "ScaledBorderAndShadow: yes",
        "PlayResX: 1920", "PlayResY: 1080", "YCbCr Matrix: TV.709", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: CN-Main,Noto Sans CJK SC,62,&H00FFFFFF,&H000000FF,&H00101010,&H00000000,0,0,0,0,100,100,0,0,1,3,0,2,96,96,70,1", "",
        "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    lines.extend(f"Dialogue: 0,{start},{end},CN-Main,,0,0,0,,{text}" for start, end, text in cues)
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")


def prepare_master(source: Path, destination: Path) -> str:
    suffix = source.suffix.lower()
    if suffix in {".ass", ".ssa"}:
        shutil.copy2(source, destination)
        return "byte-preserving ASS/SSA baseline copy"
    text = source.read_text(encoding="utf-8-sig")
    if suffix == ".srt":
        write_ass_from_cues(destination, parse_srt(text))
        return "deterministic SRT-to-ASS fallback conversion"
    if suffix == ".vtt":
        write_ass_from_cues(destination, parse_vtt(text))
        return "deterministic VTT-to-ASS fallback conversion"
    raise ValueError(f"unsupported working-baseline format: {source}")


def source_scope(group: dict[str, object], rows: list[dict[str, object]]) -> str:
    group_paths = {str(Path(file["path"]).resolve()) for file in group["files"]}
    episodes = [str(row["episode"]) for row in rows if row["subtitle_path"] in group_paths]
    if episodes:
        return ",".join(episodes)
    mapped_episodes = {str(row["episode"]) for row in rows}
    hinted = sorted({str(file.get("episode_hint")) for file in group["files"] if file.get("episode_hint") in mapped_episodes})
    return ",".join(hinted) if hinted else "ALL"


def source_block(groups: list[dict[str, object]], embedded: list[dict[str, object]], rows: list[dict[str, object]], approved_by: str, verified_at: str) -> str:
    lines = ["subtitle_sources:"]
    for group in groups:
        language = group.get("language")
        roles = group.get("roles") or []
        if not language or not roles:
            raise ValueError(f"source group {group['id']} has unresolved language or roles; rerun intake with explicit declarations")
        path = f"project/sources/subtitles/{language}/{group['id']}"
        lines.extend([
            f"  - id: {group['id']}", f"    language: {language}", f"    kind: {group['kind']}",
            f"    path: {path}", f"    file_count: {len(group['files'])}", f"    scope: {quote(source_scope(group, rows))}", "    roles:",
        ])
        lines.extend(f"      - {role}" for role in roles)
        lines.extend([
            "    classification:", "      status: user-confirmed", f"      confirmed_by: {quote(approved_by)}",
            f"      confirmed_at: {verified_at}", f"      evidence: {quote(group.get('language_basis', 'approved intake'))}",
        ])
    for track in embedded:
        if not track.get("language") or not track.get("roles"):
            continue
        embedded_scope = ",".join(
            str(row["episode"]) for row in rows if row["video"].get("id") == track.get("video_id")
        ) or "ALL"
        lines.extend([
            f"  - id: {track['id']}", f"    language: {track['language']}", "    kind: embedded-subtitle-track",
            f"    container: {quote(track['container'])}", f"    stream_index: {track['stream_index']}",
            f"    codec: {quote(track.get('codec'))}", f"    scope: {quote(embedded_scope)}", "    roles:",
        ])
        lines.extend(f"      - {role}" for role in track["roles"])
        lines.extend([
            "    classification:", "      status: verified", f"      confirmed_by: {quote(approved_by)}",
            f"      confirmed_at: {verified_at}", f"      evidence: {quote(track.get('language_basis', 'container probe and approved intake'))}",
        ])
    return "\n".join(lines)


def video_block(rows: list[dict[str, object]]) -> str:
    lines = ["video_sources:", "  target-video:", "    medium: user-provided-local-video", "    files:"]
    for row in rows:
        lines.append(f"      {row['episode']}: {quote(row['video']['basename'])}")
    lines.append("    fingerprints:")
    for row in rows:
        video = row["video"]
        lines.extend([
            f"      {row['episode']}:", f"        size: {video['size']}",
            f"        sha256_first_mib: {video['sha256_first_mib']}",
            f"        duration_seconds: {video.get('duration_seconds') if video.get('duration_seconds') is not None else 'null'}",
        ])
    lines.append("    selected_audio:")
    for row in rows:
        lines.extend([
            f"      {row['episode']}:", f"        stream_index: {row['audio_stream']}",
            f"        language: {row['audio_language']}", f"        codec: {quote(row.get('audio_codec'))}",
        ])
    return "\n".join(lines)


def local_paths_text(rows: list[dict[str, object]]) -> str:
    lines = ["schema_version: 1", "videos:"]
    lines.extend(f"  {row['episode']}: {quote(row['video']['path'])}" for row in rows)
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--series-dir", required=True, type=Path)
    parser.add_argument("--create-series", action="store_true")
    parser.add_argument("--series-title")
    parser.add_argument("--series-name-approved-by")
    parser.add_argument("--project-name", required=True, help="User-approved short lowercase developer-facing name")
    parser.add_argument("--project-name-approved-by", required=True)
    parser.add_argument("--work-id", help="Optional explicit ID; otherwise allocate the next repository SH number")
    parser.add_argument("--repository-root", type=Path)
    parser.add_argument("--type", required=True, choices=("tv", "movie", "ova", "ona", "special"))
    parser.add_argument("--bangumi-id", required=True)
    parser.add_argument("--bangumi-snapshot", required=True, type=Path)
    parser.add_argument("--scope-approved-by", required=True)
    parser.add_argument("--intake", required=True, type=Path)
    parser.add_argument("--intake-approved-by", required=True)
    parser.add_argument("--episode-map", required=True, type=Path)
    parser.add_argument("--secondary-language", help="Optional release secondary language")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    project_name = args.project_name.strip()
    if not PROJECT_NAME_RE.fullmatch(project_name) or not 3 <= len(project_name) <= 48:
        parser.error("--project-name must be 3-48 lowercase ASCII letters/digits/hyphens")
    if not args.project_name_approved_by.strip() or not args.intake_approved_by.strip():
        parser.error("project name and intake require an identified approver")
    if args.secondary_language and not LANGUAGE_RE.fullmatch(args.secondary_language):
        parser.error("--secondary-language must be a BCP 47 language tag")
    try:
        snapshot = load_snapshot(args.bangumi_snapshot, args.bangumi_id)
        intake = load_intake(args.intake)
        if intake.get("project_type") and intake["project_type"] != args.type:
            raise ValueError(f"intake project_type {intake['project_type']!r} conflicts with --type {args.type!r}")
        source_language = str(intake["source_language"])
        rows = load_episode_map(args.episode_map, intake, args.type, source_language)
        scope_basis = validate_scope(snapshot, rows, args.type, args.scope_approved_by)
        group_ids: set[str] = set()
        for group in intake["external_source_groups"]:
            group_id = str(group.get("id", ""))
            language = str(group.get("language", ""))
            if not SAFE_COMPONENT_RE.fullmatch(group_id) or not LANGUAGE_RE.fullmatch(language):
                raise ValueError(f"unsafe source group id/language: {group_id!r}/{language!r}")
            if group_id.casefold() in group_ids:
                raise ValueError(f"duplicate source group id: {group_id}")
            group_ids.add(group_id.casefold())
            for file in group.get("files", []):
                source = Path(str(file.get("path", ""))).expanduser().resolve()
                if not source.is_file() or file_sha256(source) != file.get("sha256"):
                    raise ValueError(f"source evidence changed or is unreadable after intake: {source}")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))

    series_dir = args.series_dir.expanduser().resolve()
    repository = args.repository_root.resolve() if args.repository_root else find_repository_root(series_dir)
    work_ids, subject_ids = existing_identities(repository)
    work_id = args.work_id or allocate_work_id(work_ids)
    if not WORK_ID_RE.fullmatch(work_id):
        parser.error("--work-id must match SH followed by at least four digits")
    if work_id in work_ids:
        parser.error(f"work ID already exists at {work_ids[work_id]}")
    if args.bangumi_id in subject_ids:
        parser.error(f"Bangumi subject already exists at {subject_ids[args.bangumi_id]}")
    if not series_dir.exists():
        if not args.create_series or not args.series_title or not args.series_name_approved_by:
            parser.error("a new series directory requires --create-series, --series-title, and --series-name-approved-by")
        if not PROJECT_NAME_RE.fullmatch(series_dir.name):
            parser.error("new series directory name must be lowercase ASCII letters/digits/hyphens")
    elif not series_dir.is_dir():
        parser.error(f"series path is not a directory: {series_dir}")
    elif not (series_dir / "series-guide.md").is_file():
        parser.error(f"existing series directory lacks series-guide.md: {series_dir}")

    target = series_dir / f"{work_id}--{project_name}"
    staging = series_dir / f".{work_id}--{project_name}.initializing"
    if target.exists() or staging.exists():
        parser.error(f"target or staging path already exists: {target}")
    skill_root = Path(__file__).resolve().parents[1]
    template_root = skill_root / "assets" / "templates"
    verified_at = date.today().isoformat()
    scope = "MOVIE" if args.type == "movie" else f"{len(rows)} mapped episodes"
    values = {
        "WORK_ID": work_id, "PROJECT_NAME": project_name, "WORK_TYPE": args.type, "EPISODE_COUNT": str(len(rows)),
        "BANGUMI_ID": args.bangumi_id, "TITLE_JA": str(snapshot["name"]), "TITLE_ZH_HANS": str(snapshot["name_cn"]),
        "TITLE_JA_YAML": quote(str(snapshot["name"])), "TITLE_ZH_HANS_YAML": quote(str(snapshot["name_cn"])),
        "BANGUMI_DATE_YAML": quote(str(snapshot["date"])), "BANGUMI_PLATFORM_YAML": quote(str(snapshot["platform"])),
        "BANGUMI_TOTAL_EPISODES": str(snapshot["_total_episodes"]), "IDENTITY_SCOPE_BASIS_YAML": quote(scope_basis),
        "SCOPE_APPROVED_BY_YAML": quote(args.scope_approved_by), "PROJECT_NAME_APPROVED_BY_YAML": quote(args.project_name_approved_by),
        "VERIFIED_AT": verified_at, "SOURCE_LANGUAGE": source_language,
        "SECONDARY_LANGUAGE_YAML": quote(args.secondary_language) if args.secondary_language else "null",
        "SUBTITLE_PROFILE": "zh-bilingual" if args.secondary_language else "zh-mono",
        "SECONDARY_STYLES_YAML": "\n      - JP-Main" if args.secondary_language else "[]",
        "SECONDARY_LANGUAGE_DISPLAY": args.secondary_language or "无（单语中文字幕）", "SCOPE": scope, "UPDATED_AT": verified_at,
        "EPISODES_YAML": "\n".join(f"  {row['episode']}: {{ status: not-started }}" for row in rows),
        "MACHINE_COVERAGE": "ffprobe media/track inventory; source hashes; project structure and master parsing",
        "HUMAN_COVERAGE": f"project name, identity scope, episode map and material roles approved by {args.intake_approved_by}",
        "INITIALIZATION_SUMMARY": f"Prepared {len(rows)} writable master(s) from immutable Chinese baseline sources.",
        "INTAKE_APPROVED_BY_YAML": quote(args.intake_approved_by),
    }
    project_text = render(template_root / "project.yaml", values)
    project_text = project_text.replace("subtitle_sources: []", source_block(intake["external_source_groups"], intake.get("embedded_subtitle_tracks", []), rows, args.intake_approved_by, verified_at))
    project_text = project_text.replace("video_sources: {}", video_block(rows))
    planned = {
        "skill_version": SKILL_VERSION, "target": str(target), "work_id": work_id, "project_name": project_name,
        "project_name_approved_by": args.project_name_approved_by, "episodes": [row["episode"] for row in rows],
        "release_filenames": [row["output_name"] for row in rows],
        "videos_recorded_by_basename_only": [row["video"]["basename"] for row in rows],
        "masters_to_prepare": [{"episode": row["episode"], "source": row["subtitle_path"]} for row in rows],
        "optional_limitations": [question for question in intake.get("questions", []) if question.startswith("Optional:")],
    }
    if args.dry_run:
        print(json.dumps(planned, ensure_ascii=False, indent=2))
        return 0

    created_series = False
    promoted_target = False
    try:
        if not series_dir.exists():
            series_dir.mkdir(parents=True, exist_ok=False)
            created_series = True
            series_values = {"SERIES_TITLE": args.series_title}
            (series_dir / "series-guide.md").write_text(render(template_root / "series-guide.md", series_values), encoding="utf-8")
        directories = [staging / "project" / "sources" / "subtitles"]
        directories.extend(staging / "project" / "workspace" / "episodes" / str(row["episode"]) for row in rows)
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=False)
        for group in intake["external_source_groups"]:
            destination = staging / "project" / "sources" / "subtitles" / str(group["language"]) / str(group["id"])
            destination.mkdir(parents=True, exist_ok=False)
            seen_names: set[str] = set()
            for file in group["files"]:
                source = Path(file["path"])
                if source.name.casefold() in seen_names:
                    raise ValueError(f"duplicate source basename in group {group['id']}: {source.name}")
                seen_names.add(source.name.casefold())
                shutil.copy2(source, destination / source.name)
        methods = {}
        for row in rows:
            source = Path(row["subtitle_path"])
            master = staging / "project" / "workspace" / "episodes" / str(row["episode"]) / "master.ass"
            methods[str(row["episode"])] = prepare_master(source, master)
        (staging / "project.yaml").write_text(project_text, encoding="utf-8")
        (staging / "review.md").write_text(render(template_root / "review.md", values), encoding="utf-8")
        (staging / "project" / "local.paths.yaml").write_text(local_paths_text(rows), encoding="utf-8")
        planned["master_preparation"] = methods
        staging.rename(target)
        promoted_target = True
        validator = Path(__file__).resolve().with_name("validate_project.py")
        validation = subprocess.run(
            [sys.executable, str(validator), str(target), "--ready-for-proofreading", "--json"],
            capture_output=True, text=True, encoding="utf-8",
        )
        if validation.returncode != 0:
            raise ValueError(f"initialized project failed readiness validation: {validation.stdout or validation.stderr}")
        planned["validation"] = "ready-for-proofreading"
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        if promoted_target and target.exists():
            shutil.rmtree(target)
        if created_series and series_dir.exists():
            shutil.rmtree(series_dir)
        raise
    print(json.dumps(planned, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
