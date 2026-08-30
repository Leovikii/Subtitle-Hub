#!/usr/bin/env python3
"""Create a transactionally initialized Subtitle Hub 1.4.0 proofreading project."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

SKILL_VERSION = "1.4.0"
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
TEXT_BASELINES = {".ass", ".ssa", ".srt", ".vtt"}
SAFE_COMPONENT_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
SC_FONT = "Noto Sans CJK SC"
JP_FONT = "Noto Sans CJK JP"
JAPANESE_KANA = re.compile(r"[\u3040-\u30ff]")
JAPANESE_STYLE = re.compile(r"(?:日文|日本|日语|日語|原文|原語|(?:^|[-_ ])(?:ja|jp|jpn)(?:$|[-_ ]))", re.IGNORECASE)
INLINE_FONT = re.compile(r"\\fn([^\\}]*)")


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
    if data.get("schema_version") != 4 or data.get("skill_version") != SKILL_VERSION:
        raise ValueError(f"intake must use schema_version 4 and skill_version {SKILL_VERSION}")
    if not data.get("external_source_groups"):
        raise ValueError("intake lacks subtitle source groups")
    if data.get("blocking_questions"):
        raise ValueError(f"intake still has blocking questions: {data['blocking_questions']}")
    if not data.get("episode_map"):
        raise ValueError("intake lacks an approved episode map")
    for track in data.get("embedded_subtitle_tracks", []):
        if not track.get("ignored", False) and (not track.get("language") or not track.get("roles")):
            raise ValueError(
                f"selected embedded subtitle {track.get('id', '<unknown>')} requires confirmed language and roles"
            )
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


def video_locator(raw: str) -> str:
    value = raw.strip()
    if value.startswith("ssh://"):
        parsed = urlparse(value)
        if parsed.scheme != "ssh" or parsed.password is not None or not parsed.hostname or not parsed.username or not parsed.path or parsed.query or parsed.fragment:
            raise ValueError("SSH video locator must contain host, user and path but no password")
        return value
    return str(Path(value).expanduser().resolve())


def load_episode_map(intake: dict[str, object], work_type: str, source_language: str) -> list[dict[str, object]]:
    videos_by_path = {video_locator(str(item["path"])): item for item in intake["target_videos"]}
    baseline_files = {
        str(Path(file["path"]).resolve()): file
        for group in intake["external_source_groups"]
        if "candidate-baseline" in group.get("roles", [])
        for file in group["files"]
    }
    rows: list[dict[str, object]] = []
    seen_episodes: set[str] = set()
    seen_outputs: set[str] = set()
    for raw in intake["episode_map"]:
        episode = str(raw.get("episode") or "").strip()
        if not valid_episode(episode, work_type) or episode in seen_episodes:
            raise ValueError(f"unsafe, missing, or duplicate {work_type} episode ID: {episode!r}")
        raw_video = str(raw.get("video") or "").strip()
        video_path = video_locator(raw_video) if raw_video else ""
        subtitle_path = str(Path(str(raw.get("subtitle") or "")).expanduser().resolve())
        if video_path and video_path not in videos_by_path:
            raise ValueError(f"episode map video is absent from intake: {video_path}")
        if subtitle_path not in baseline_files:
            raise ValueError(f"episode map baseline is absent from intake: {subtitle_path}")
        video_file = Path(video_path) if video_path and not video_path.startswith("ssh://") else None
        subtitle_file = Path(subtitle_path)
        if video_file and (not video_file.is_file() or video_file.stat().st_size != int(videos_by_path[video_path]["size"]) or first_mib_sha256(video_file) != videos_by_path[video_path]["sha256_first_mib"]):
            raise ValueError(f"target video changed or is unreadable after intake: {video_file}")
        if not subtitle_file.is_file() or file_sha256(subtitle_file) != baseline_files[subtitle_path]["sha256"]:
            raise ValueError(f"candidate baseline changed or is unreadable after intake: {subtitle_file}")
        validate_baseline_source(subtitle_file)
        video = videos_by_path.get(video_path)
        audio_index = raw.get("audio_stream")
        audio_language = str(raw.get("audio_language") or "").strip()
        if video and not isinstance(audio_index, int):
            raise ValueError(f"audio_stream must be an integer for {episode}")
        if not video and (audio_index is not None or audio_language):
            raise ValueError(f"audio fields must be null for text-only episode {episode}")
        if video and (not LANGUAGE_RE.fullmatch(audio_language) or audio_language.split("-", 1)[0] != source_language.split("-", 1)[0]):
            raise ValueError(f"audio_language {audio_language!r} does not match {source_language!r}")
        streams = [stream for stream in video.get("streams", []) if stream.get("type") == "audio" and stream.get("index") == audio_index] if video else []
        if video and len(streams) != 1:
            raise ValueError(f"selected audio stream {audio_index} is absent from {video['basename']}")
        target_basename = str(raw.get("target_basename") or (video["basename"] if video else "")).strip()
        timing_authority = str(raw.get("timing_authority") or "").strip()
        if not target_basename or Path(target_basename).name != target_basename:
            raise ValueError(f"safe target_basename is required for {episode}")
        if not timing_authority:
            raise ValueError(f"timing_authority is required for {episode}")
        output_name = f"{Path(target_basename).stem}.zh-Hans.ass"
        if output_name.casefold() in seen_outputs:
            raise ValueError(f"duplicate release filename: {output_name}")
        seen_episodes.add(episode)
        seen_outputs.add(output_name.casefold())
        rows.append({
            "episode": episode, "video": video, "subtitle": baseline_files[subtitle_path],
            "subtitle_path": subtitle_path, "audio_stream": audio_index,
            "audio_language": audio_language, "audio_codec": streams[0].get("codec") if streams else None,
            "target_basename": target_basename, "timing_authority": timing_authority, "output_name": output_name,
        })
    if work_type == "movie" and (len(rows) != 1 or rows[0]["episode"] != "MOVIE"):
        raise ValueError("a movie project must map exactly one MOVIE entry")
    return rows


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
        f"Style: CN-Main,{SC_FONT},62,&H00FFFFFF,&H000000FF,&H00101010,&H00000000,0,0,0,0,100,100,0,0,1,3,0,2,96,96,70,1", "",
        "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    lines.extend(f"Dialogue: 0,{start},{end},CN-Main,,0,0,0,,{text}" for start, end, text in cues)
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")


def normalize_ass_master(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff")
    if "[V4+ Styles]\n" not in text or "[Events]\n" not in text:
        raise ValueError("ASS working master requires V4+ Styles and Events sections")
    defaults = {
        "ScriptType": "v4.00+", "WrapStyle": "0", "ScaledBorderAndShadow": "yes",
        "PlayResX": "1920", "PlayResY": "1080", "YCbCr Matrix": "TV.709",
    }
    if not text.startswith("[Script Info]\n"):
        text = "[Script Info]\n" + "\n".join(f"{key}: {value}" for key, value in defaults.items()) + "\n\n" + text
    else:
        next_section = re.search(r"(?m)^\[[^\n]+\]$", text[len("[Script Info]\n"):])
        if not next_section:
            raise ValueError("ASS Script Info has no following section")
        end = len("[Script Info]\n") + next_section.start()
        head, tail = text[:end], text[end:]
        existing = {m.group(1) for m in re.finditer(r"(?m)^([^;\s][^:]*):", head)}
        additions = "".join(f"{key}: {value}\n" for key, value in defaults.items() if key not in existing)
        text = head.rstrip("\n") + "\n" + additions + "\n" + tail.lstrip("\n")

    events_start = text.index("[Events]\n")
    japanese_styles: set[str] = set()
    for line in text[events_start:].splitlines():
        if not line.startswith(("Dialogue:", "Comment:")):
            continue
        parts = line.split(",", 9)
        if len(parts) == 10 and JAPANESE_KANA.search(re.sub(r"\{[^}]*\}", "", parts[9])):
            japanese_styles.add(parts[3].strip() or "Default")

    style_start = text.index("[V4+ Styles]\n")
    head, styles, events = text[:style_start], text[style_start:events_start], text[events_start:]
    targets: dict[str, str] = {}
    style_output: list[str] = []
    for line in styles.splitlines(keepends=True):
        if not line.startswith("Style:"):
            style_output.append(line)
            continue
        fields = line.removesuffix("\n").split(":", 1)[1].lstrip().split(",")
        if len(fields) < 2:
            raise ValueError("malformed ASS style definition")
        name = fields[0]
        target = JP_FONT if name in japanese_styles or JAPANESE_STYLE.search(name) else SC_FONT
        targets[name] = target
        fields[1] = target
        style_output.append("Style: " + ",".join(fields) + ("\n" if line.endswith("\n") else ""))

    event_output: list[str] = []
    for line in events.splitlines(keepends=True):
        if not line.startswith(("Dialogue:", "Comment:")):
            event_output.append(line)
            continue
        bare = line.removesuffix("\n")
        parts = bare.split(",", 9)
        if len(parts) != 10:
            raise ValueError("malformed ASS event")
        target = targets.get(parts[3].strip() or "Default", SC_FONT)
        parts[9] = INLINE_FONT.sub(lambda match: f"\\fn{JP_FONT if JAPANESE_KANA.search(parts[9]) else target}" if match.group(1).strip() else match.group(0), parts[9])
        event_output.append(",".join(parts) + ("\n" if line.endswith("\n") else ""))
    result = head + "".join(style_output) + "".join(event_output)
    return result if result.endswith("\n") else result + "\n"


def prepare_master(source: Path, destination: Path) -> str:
    suffix = source.suffix.lower()
    if suffix in {".ass", ".ssa"}:
        normalized = normalize_ass_master(source.read_text(encoding="utf-8-sig"))
        destination.write_text(normalized, encoding="utf-8", newline="\n")
        return "content-preserving ASS working-master normalization"
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


def source_block(groups: list[dict[str, object]], embedded: list[dict[str, object]], rows: list[dict[str, object]]) -> str:
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
        lines.append(f"    evidence: {quote(group.get('language_basis', 'approved intake'))}")
    for track in embedded:
        if not track.get("language") or not track.get("roles"):
            continue
        embedded_scope = ",".join(
            str(row["episode"]) for row in rows if row["video"] and row["video"].get("id") == track.get("video_id")
        ) or "ALL"
        lines.extend([
            f"  - id: {track['id']}", f"    language: {track['language']}", "    kind: embedded-subtitle-track",
            f"    container: {quote(track['container'])}", f"    stream_index: {track['stream_index']}",
            f"    codec: {quote(track.get('codec'))}", f"    scope: {quote(embedded_scope)}", "    roles:",
        ])
        lines.extend(f"      - {role}" for role in track["roles"])
        lines.append(f"    evidence: {quote(track.get('language_basis', 'container probe and approved intake'))}")
    return "\n".join(lines)


def video_block(rows: list[dict[str, object]]) -> str:
    has_video = any(row["video"] for row in rows)
    accesses = {str(row["video"].get("access", "local")) for row in rows if row["video"]}
    medium = "not-provided" if not has_video else "user-provided-ssh-video" if accesses == {"ssh"} else "user-provided-local-video" if accesses == {"local"} else "user-provided-mixed-video"
    lines = ["video_sources:", "  target-video:", f"    medium: {medium}", "    files:"]
    for row in rows:
        lines.append(f"      {row['episode']}: {quote(row['target_basename'])}")
    lines.append("    timing_authority:")
    for row in rows:
        lines.append(f"      {row['episode']}: {quote(row['timing_authority'])}")
    if not has_video:
        lines.extend(["    inventory_status: not-provided", "    fingerprints: {}", "    selected_audio: {}"])
        return "\n".join(lines)
    lines.append("    fingerprints:")
    for row in rows:
        video = row["video"]
        if not video:
            continue
        lines.extend([
            f"      {row['episode']}:", f"        size: {video['size']}",
            f"        sha256_first_mib: {video['sha256_first_mib']}",
            f"        duration_seconds: {video.get('duration_seconds') if video.get('duration_seconds') is not None else 'null'}",
        ])
    lines.append("    selected_audio:")
    for row in rows:
        if not row["video"]:
            continue
        lines.extend([
            f"      {row['episode']}:", f"        stream_index: {row['audio_stream']}",
            f"        language: {row['audio_language']}", f"        codec: {quote(row.get('audio_codec'))}",
        ])
    return "\n".join(lines)


def local_paths_text(rows: list[dict[str, object]]) -> str:
    lines = ["schema_version: 1", "videos:"]
    lines.extend(f"  {row['episode']}: {quote(row['video']['path'])}" for row in rows if row["video"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--series-dir", required=True, type=Path)
    parser.add_argument("--create-series", action="store_true")
    parser.add_argument("--series-title")
    parser.add_argument("--project-name", required=True, help="User-approved short lowercase developer-facing name")
    parser.add_argument("--approved-by", required=True, help="Approver for identity, scope, mappings, roles, languages, and names")
    parser.add_argument("--work-id", help="Optional explicit ID; otherwise allocate the next repository SH number")
    parser.add_argument("--repository-root", type=Path)
    parser.add_argument("--type", required=True, choices=("tv", "movie", "ova", "ona", "special"))
    parser.add_argument("--bangumi-id", required=True)
    parser.add_argument("--bangumi-snapshot", required=True, type=Path)
    parser.add_argument("--intake", required=True, type=Path)
    parser.add_argument("--secondary-language", help="Optional release secondary language")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    project_name = args.project_name.strip()
    if not PROJECT_NAME_RE.fullmatch(project_name) or not 3 <= len(project_name) <= 48:
        parser.error("--project-name must be 3-48 lowercase ASCII letters/digits/hyphens")
    if not args.approved_by.strip():
        parser.error("--approved-by requires an identified approver")
    if args.secondary_language and not LANGUAGE_RE.fullmatch(args.secondary_language):
        parser.error("--secondary-language must be a BCP 47 language tag")
    try:
        snapshot = load_snapshot(args.bangumi_snapshot, args.bangumi_id)
        intake = load_intake(args.intake)
        if intake.get("project_type") and intake["project_type"] != args.type:
            raise ValueError(f"intake project_type {intake['project_type']!r} conflicts with --type {args.type!r}")
        source_language = str(intake["source_language"])
        rows = load_episode_map(intake, args.type, source_language)
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
        if not args.create_series or not args.series_title:
            parser.error("a new series directory requires --create-series and --series-title")
        if not PROJECT_NAME_RE.fullmatch(series_dir.name):
            parser.error("new series directory name must be lowercase ASCII letters/digits/hyphens")
    elif not series_dir.is_dir():
        parser.error(f"series path is not a directory: {series_dir}")

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
        "BANGUMI_ID": args.bangumi_id,
        "TITLE_JA_YAML": quote(str(snapshot["name"])), "TITLE_ZH_HANS_YAML": quote(str(snapshot["name_cn"])),
        "BANGUMI_DATE_YAML": quote(str(snapshot["date"])), "BANGUMI_PLATFORM_YAML": quote(str(snapshot["platform"])),
        "BANGUMI_TOTAL_EPISODES": str(snapshot["_total_episodes"]),
        "APPROVED_BY_YAML": quote(args.approved_by),
        "VERIFIED_AT": verified_at, "SOURCE_LANGUAGE": source_language,
        "SECONDARY_LANGUAGE_YAML": quote(args.secondary_language) if args.secondary_language else "null",
        "SUBTITLE_PROFILE": "zh-bilingual" if args.secondary_language else "zh-mono",
        "SECONDARY_STYLES_YAML": "\n      - JP-Main" if args.secondary_language else "[]",
        "SCOPE": scope, "UPDATED_AT": verified_at,
        "EPISODES_YAML": "\n".join(f"  {row['episode']}: {{ status: not-started }}" for row in rows),
        "MACHINE_COVERAGE": ("ffprobe media/track inventory; " if any(row["video"] for row in rows) else "text-only inventory; ") + "source hashes; project structure and master parsing",
        "HUMAN_COVERAGE": f"project name, identity scope, episode map, timing authority, languages, and material roles approved by {args.approved_by}",
        "INITIALIZATION_SUMMARY": f"Prepared {len(rows)} writable master(s) from immutable Chinese baseline sources.",
        "EVIDENCE_TIER": str(intake.get("evidence_tier") or "D"),
        "TIMING_AUTHORITY_YAML": quote("; ".join(f"{row['episode']}={row['timing_authority']}" for row in rows)),
    }
    project_text = render(template_root / "project.yaml", values)
    project_text = project_text.replace("subtitle_sources: []", source_block(intake["external_source_groups"], intake.get("embedded_subtitle_tracks", []), rows))
    project_text = project_text.replace("video_sources: {}", video_block(rows))
    limitations = list(dict.fromkeys(str(value) for value in intake.get("limitations", []) if str(value).strip()))
    if limitations:
        project_text = project_text.replace("limitations: []", "limitations:\n" + "\n".join(f"  - {quote(value)}" for value in limitations))
    planned = {
        "skill_version": SKILL_VERSION, "target": str(target), "work_id": work_id, "project_name": project_name,
        "approved_by": args.approved_by, "episodes": [row["episode"] for row in rows],
        "release_filenames": [row["output_name"] for row in rows],
        "videos_recorded_by_basename_only": [row["video"]["basename"] for row in rows if row["video"]],
        "evidence_tier": intake.get("evidence_tier"),
        "timing_authorities": {row["episode"]: row["timing_authority"] for row in rows},
        "masters_to_prepare": [{"episode": row["episode"], "source": row["subtitle_path"]} for row in rows],
        "limitations": limitations,
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
        review_text = render(template_root / "review.md", values)
        fingerprints = "  master_sha256:\n" + "\n".join(
            f"    {row['episode']}: {file_sha256(staging / 'project' / 'workspace' / 'episodes' / str(row['episode']) / 'master.ass')}"
            for row in rows
        )
        review_text = review_text.replace("  master_sha256: {}", fingerprints)
        (staging / "review.md").write_text(review_text, encoding="utf-8")
        if any(row["video"] for row in rows):
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
            raise ValueError(f"initialized project failed proofreading gate: {validation.stdout or validation.stderr}")
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
