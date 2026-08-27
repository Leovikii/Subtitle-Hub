#!/usr/bin/env python3
"""Probe target media and subtitle evidence, then emit a disposable intake manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

VIDEO_EXTENSIONS = {".mkv", ".mp4", ".m2ts", ".ts", ".webm", ".mov"}
TEXT_EVIDENCE_EXTENSIONS = {".ass", ".ssa", ".srt", ".vtt", ".txt", ".md"}
SUBTITLE_EXTENSIONS = TEXT_EVIDENCE_EXTENSIONS | {".sup", ".mks"}
BASELINE_EXTENSIONS = {".ass", ".ssa", ".srt", ".vtt"}
TEXT_SUBTITLE_CODECS = {"ass", "ssa", "subrip", "srt", "webvtt", "mov_text", "text"}
ALLOWED_ROLES = {
    "candidate-baseline",
    "source-text-reference",
    "timing-reference",
    "translation-reference",
    "forced-signs-reference",
    "style-layout-reference",
    "secondary-language-release-source",
}
LANGUAGE_ALIASES = {
    "ja": "ja", "jpn": "ja", "jp": "ja", "japanese": "ja", "日语": "ja", "日本語": "ja",
    "en": "en", "eng": "en", "english": "en", "英语": "en",
    "zh": "zh-Hans", "zho": "zh-Hans", "chi": "zh-Hans", "chs": "zh-Hans", "sc": "zh-Hans",
    "zh-cn": "zh-Hans", "zh-hans": "zh-Hans", "简中": "zh-Hans", "简体": "zh-Hans",
    "cht": "zh-Hant", "tc": "zh-Hant", "zh-tw": "zh-Hant", "zh-hant": "zh-Hant", "繁中": "zh-Hant",
    "ko": "ko", "kor": "ko", "korean": "ko", "韩语": "ko",
    "fr": "fr", "fra": "fr", "fre": "fr", "de": "de", "deu": "de", "ger": "de",
    "es": "es", "spa": "es", "it": "it", "ita": "it", "ru": "ru", "rus": "ru",
}
EPISODE_PATTERNS = (
    re.compile(r"(?i)\bS(\d{1,2})[ ._-]*E(\d{1,3})\b"),
    re.compile(r"(?i)\b(?:EP?|episode)[ ._-]*(\d{1,3})\b"),
)


def files_from(path: Path, extensions: set[str]) -> list[Path]:
    resolved = path.expanduser().resolve()
    if resolved.is_file():
        return [resolved] if resolved.suffix.lower() in extensions else []
    if resolved.is_dir():
        return sorted(p for p in resolved.rglob("*") if p.is_file() and p.suffix.lower() in extensions)
    raise ValueError(f"path does not exist: {path}")


def sha256_prefix(path: Path, limit: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        digest.update(handle.read(limit))
    return digest.hexdigest()


def normalize_language(raw: object, *, aliases_only: bool = False) -> str | None:
    if raw is None:
        return None
    value = str(raw).strip().lower().replace("_", "-")
    if not value or value in {"und", "unknown", "none", "null"}:
        return None
    if value in LANGUAGE_ALIASES:
        return LANGUAGE_ALIASES[value]
    if aliases_only:
        return None
    if re.fullmatch(r"[a-z]{2,3}(?:-[a-z0-9]{2,8})*", value):
        parts = value.split("-")
        return parts[0] + "".join("-" + (part.title() if len(part) == 4 else part.upper() if len(part) == 2 else part) for part in parts[1:])
    return None


def language_from_filename(path: Path) -> tuple[str | None, str]:
    tokens = re.split(r"[^A-Za-z0-9-]+", path.stem)
    for token in reversed(tokens):
        language = normalize_language(token, aliases_only=True)
        if language:
            return language, f"filename token {token!r}"
    return None, "no recognized filename language token"


def language_from_text(path: Path) -> tuple[str | None, str]:
    if path.suffix.lower() not in TEXT_EVIDENCE_EXTENSIONS:
        return None, "binary subtitle evidence"
    try:
        raw_sample = path.read_text(encoding="utf-8-sig")[:20000]
    except (OSError, UnicodeDecodeError):
        return None, "text sample unavailable"
    if path.suffix.lower() in {".ass", ".ssa"}:
        sample = "\n".join(
            line.split(",", 9)[-1]
            for line in raw_sample.splitlines()
            if line.startswith(("Dialogue:", "Comment:")) and line.count(",") >= 9
        )
    elif path.suffix.lower() in {".srt", ".vtt"}:
        sample = "\n".join(
            line for line in raw_sample.splitlines()
            if not re.fullmatch(r"\s*\d+\s*", line)
            and "-->" not in line
            and line.strip() != "WEBVTT"
        )
    else:
        sample = raw_sample
    sample = re.sub(r"\{[^}]*\}|<[^>]*>", "", sample)
    kana = len(re.findall(r"[\u3040-\u30ff]", sample))
    hangul = len(re.findall(r"[\uac00-\ud7af]", sample))
    latin = len(re.findall(r"[A-Za-z]", sample))
    cjk = len(re.findall(r"[\u3400-\u9fff]", sample))
    if kana >= 8:
        return "ja", "sample contains Japanese kana"
    if hangul >= 8:
        return "ko", "sample contains Hangul"
    if latin >= 40 and latin > cjk * 2:
        return "en", "sample is predominantly Latin text"
    if cjk >= 20:
        return None, "CJK sample cannot safely distinguish Simplified/Traditional Chinese or Japanese kanji"
    return None, "text sample is insufficient"


def detect_external_language(path: Path) -> tuple[str | None, str]:
    language, basis = language_from_filename(path)
    if language:
        return language, basis
    return language_from_text(path)


def roles_for(language: str | None, source_language: str, suffix: str, embedded_codec: str | None = None) -> list[str]:
    is_timed = suffix.lower() in {".ass", ".ssa", ".srt", ".vtt", ".sup", ".mks"} or embedded_codec is not None
    is_text = suffix.lower() in TEXT_EVIDENCE_EXTENSIONS or (embedded_codec or "").lower() in TEXT_SUBTITLE_CODECS
    roles: list[str] = []
    if language == source_language and is_text:
        roles.append("source-text-reference")
    elif language:
        roles.append("translation-reference")
    if is_timed:
        roles.append("timing-reference")
        roles.append("style-layout-reference")
    if embedded_codec and embedded_codec.lower() not in TEXT_SUBTITLE_CODECS:
        roles.append("forced-signs-reference")
    return list(dict.fromkeys(roles))


def parse_source_spec(spec: str) -> tuple[Path, str | None, list[str] | None]:
    parts = spec.split("|", 2)
    path = Path(parts[0])
    language = normalize_language(parts[1]) if len(parts) >= 2 and parts[1].strip() else None
    roles = None
    if len(parts) == 3 and parts[2].strip():
        roles = [role.strip() for role in parts[2].split(",") if role.strip()]
        unknown = sorted(set(roles) - ALLOWED_ROLES)
        if unknown:
            raise ValueError(f"invalid source roles for {path}: {unknown}")
    return path, language, roles


def parse_track_override(spec: str) -> tuple[str, int, str]:
    parts = spec.split("|", 2)
    if len(parts) != 3 or not parts[1].isdigit():
        raise ValueError("track override must be VIDEO|STREAM_INDEX|LANGUAGE")
    language = normalize_language(parts[2])
    if not language:
        raise ValueError(f"invalid track language: {parts[2]!r}")
    return str(Path(parts[0]).expanduser().resolve()), int(parts[1]), language


def load_probe_cache(path: Path | None) -> dict[str, object]:
    if not path:
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("probe cache must be a JSON object keyed by absolute path or basename")
    return data


def raw_probe(path: Path, ffprobe: str | None, cache: dict[str, object]) -> tuple[str, dict[str, object] | None, str | None]:
    cached = cache.get(str(path.resolve()), cache.get(path.name))
    if isinstance(cached, dict):
        return "ok", cached, None
    if not ffprobe:
        return "unavailable", None, "ffprobe was not found"
    command = [
        ffprobe, "-v", "error", "-show_entries",
        "format=duration,format_name:stream=index,codec_type,codec_name,width,height:stream_tags=language,title:stream_disposition=default,forced",
        "-of", "json", str(path),
    ]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True, encoding="utf-8")
        return "ok", json.loads(result.stdout), None
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        return "failed", None, str(error)


def stream_language(stream: dict[str, object], video: Path, overrides: dict[tuple[str, int], str]) -> tuple[str | None, str]:
    index = int(stream.get("index", -1))
    override = overrides.get((str(video.resolve()), index))
    if override:
        return override, "user/developer track override"
    tags = stream.get("tags") if isinstance(stream.get("tags"), dict) else {}
    language = normalize_language(tags.get("language"))
    if language:
        return language, "container language tag"
    title = str(tags.get("title", ""))
    for token in re.split(r"[^A-Za-z0-9\u4e00-\u9fff]+", title):
        language = normalize_language(token, aliases_only=True)
        if language:
            return language, "container track title"
    return None, "container language metadata unresolved"


def probe_video(
    path: Path,
    ffprobe: str | None,
    cache: dict[str, object],
    overrides: dict[tuple[str, int], str],
    audio_selections: dict[str, int],
    source_language: str,
) -> dict[str, object]:
    status, payload, error = raw_probe(path, ffprobe, cache)
    item: dict[str, object] = {
        "id": "",
        "path": str(path.resolve()),
        "basename": path.name,
        "stem": path.stem,
        "size": path.stat().st_size,
        "sha256_first_mib": sha256_prefix(path),
        "probe_status": status,
        "duration_seconds": None,
        "format": None,
        "streams": [],
        "suggested_audio_stream": None,
    }
    if error:
        item["probe_error"] = error
    if status != "ok" or not payload:
        return item
    format_data = payload.get("format") if isinstance(payload.get("format"), dict) else {}
    try:
        item["duration_seconds"] = round(float(format_data.get("duration")), 3)
    except (TypeError, ValueError):
        pass
    item["format"] = format_data.get("format_name")
    normalized_streams = []
    source_audio = []
    for raw in payload.get("streams", []):
        if not isinstance(raw, dict):
            continue
        language, basis = stream_language(raw, path, overrides)
        stream = {
            "index": int(raw.get("index", -1)),
            "type": raw.get("codec_type"),
            "codec": raw.get("codec_name"),
            "language": language,
            "language_basis": basis,
            "title": (raw.get("tags") or {}).get("title") if isinstance(raw.get("tags"), dict) else None,
            "default": bool((raw.get("disposition") or {}).get("default")) if isinstance(raw.get("disposition"), dict) else False,
            "forced": bool((raw.get("disposition") or {}).get("forced")) if isinstance(raw.get("disposition"), dict) else False,
        }
        if raw.get("width") is not None:
            stream["width"] = raw.get("width")
            stream["height"] = raw.get("height")
        normalized_streams.append(stream)
        if stream["type"] == "audio" and language == source_language:
            source_audio.append(stream["index"])
    item["streams"] = normalized_streams
    selected = audio_selections.get(str(path.resolve()))
    if selected is not None:
        matching = [
            stream for stream in normalized_streams
            if stream["type"] == "audio" and stream["index"] == selected
        ]
        if len(matching) != 1:
            raise ValueError(f"selected audio stream {selected} is absent from {path.name}")
        if matching[0]["language"] != source_language:
            raise ValueError(
                f"selected audio stream {selected} for {path.name} is {matching[0]['language']!r}, "
                f"not source language {source_language!r}"
            )
        item["suggested_audio_stream"] = selected
        item["audio_selection_basis"] = "user/developer audio-stream selection"
    elif len(source_audio) == 1:
        item["suggested_audio_stream"] = source_audio[0]
        item["audio_selection_basis"] = "only source-language audio stream"
    return item


def parse_audio_selection(spec: str) -> tuple[str, int]:
    parts = spec.rsplit("|", 1)
    if len(parts) != 2 or not parts[1].isdigit():
        raise ValueError("audio selection must be VIDEO|STREAM_INDEX")
    return str(Path(parts[0]).expanduser().resolve()), int(parts[1])


def episode_hint(path: Path, project_type: str | None) -> str | None:
    stem = path.stem
    match = EPISODE_PATTERNS[0].search(stem)
    if match:
        return f"S{int(match.group(1)):02d}E{int(match.group(2)):02d}"
    match = EPISODE_PATTERNS[1].search(stem)
    if match:
        number = int(match.group(1))
        if project_type == "ova":
            return f"OVA{number:02d}"
        if project_type == "special":
            return f"SP{number:02d}"
        return f"S01E{number:02d}"
    if project_type == "movie":
        return "MOVIE"
    return None


def external_group(
    group_id: str,
    path: Path,
    language: str | None,
    roles: list[str] | None,
    source_language: str,
    baseline: bool,
    project_type: str | None,
) -> dict[str, object]:
    files = files_from(path, BASELINE_EXTENSIONS if baseline else SUBTITLE_EXTENSIONS)
    if not files:
        raise ValueError(f"no supported subtitle/script evidence found: {path}")
    detected = []
    bases = []
    for file in files:
        detected_language, basis = detect_external_language(file)
        detected.append(detected_language)
        bases.append(basis)
    resolved_language = "zh-Hans" if baseline else language
    language_basis = "candidate baseline declaration" if baseline else "explicit declaration" if language else ""
    if not resolved_language:
        known = {value for value in detected if value}
        if len(known) == 1 and all(value in known for value in detected):
            resolved_language = known.pop()
            language_basis = "; ".join(sorted(set(bases)))
    resolved_roles = ["candidate-baseline", "timing-reference", "style-layout-reference"] if baseline else roles
    if resolved_roles is None:
        resolved_roles = roles_for(resolved_language, source_language, files[0].suffix)
    return {
        "id": group_id,
        "declared_path": str(path.expanduser().resolve()),
        "kind": "candidate-baseline" if baseline else "external-evidence",
        "language": resolved_language,
        "language_basis": language_basis or "unresolved",
        "roles": resolved_roles,
        "files": [
            {
                "id": f"{group_id}-f{index:03d}",
                "path": str(file),
                "basename": file.name,
                "format": file.suffix.lower().lstrip("."),
                "size": file.stat().st_size,
                "sha256": hashlib.sha256(file.read_bytes()).hexdigest(),
                "episode_hint": episode_hint(file, project_type),
            }
            for index, file in enumerate(files, start=1)
        ],
    }


def propose_relationships(videos: list[dict[str, object]], baselines: list[dict[str, object]], project_type: str) -> list[dict[str, object]]:
    baseline_files = [file for group in baselines for file in group["files"]]
    if len(videos) == len(baseline_files) == 1:
        episode = "MOVIE" if project_type == "movie" else episode_hint(Path(videos[0]["basename"]), project_type) or episode_hint(Path(baseline_files[0]["basename"]), project_type) or "S01E01"
        return [{
            "episode": episode,
            "video_id": videos[0]["id"],
            "video": videos[0]["path"],
            "baseline_file_id": baseline_files[0]["id"],
            "subtitle": baseline_files[0]["path"],
            "audio_stream": videos[0]["suggested_audio_stream"],
            "confidence": "high" if videos[0]["suggested_audio_stream"] is not None else "limited",
            "basis": "single video and single baseline",
        }]
    by_episode: dict[str, list[dict[str, object]]] = {}
    for file in baseline_files:
        hint = episode_hint(Path(file["basename"]), project_type)
        if hint:
            by_episode.setdefault(hint, []).append(file)
    result = []
    for video in videos:
        hint = episode_hint(Path(video["basename"]), project_type)
        matches = by_episode.get(hint or "", [])
        result.append({
            "episode": hint,
            "video_id": video["id"],
            "video": video["path"],
            "baseline_file_id": matches[0]["id"] if len(matches) == 1 else None,
            "subtitle": matches[0]["path"] if len(matches) == 1 else None,
            "audio_stream": video["suggested_audio_stream"],
            "confidence": "high" if hint and len(matches) == 1 and video["suggested_audio_stream"] is not None else "unresolved",
            "basis": "matching episode token" if hint and len(matches) == 1 else "episode pairing requires confirmation",
        })
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-video", "--media", action="append", default=[], dest="target_video", help="Target video file or directory")
    parser.add_argument("--candidate-baseline", action="append", default=[], required=True, help="Chinese subtitle baseline file or directory")
    parser.add_argument("--optional-source", "--subtitle", action="append", default=[], dest="optional_source", metavar="PATH[|LANGUAGE|ROLES]")
    parser.add_argument("--source-language", required=True, help="Actual dialogue language (BCP 47)")
    parser.add_argument("--project-type", choices=("tv", "movie", "ova", "ona", "special"))
    parser.add_argument("--track-language", action="append", default=[], metavar="VIDEO|INDEX|LANGUAGE", help="Resolve missing/conflicting container language metadata")
    parser.add_argument("--audio-stream", action="append", default=[], metavar="VIDEO|INDEX", help="Select the intended source-language dialogue stream when probing finds multiple candidates")
    parser.add_argument("--ffprobe", help="Explicit ffprobe executable")
    parser.add_argument("--probe-cache", type=Path, help="Optional JSON cache of raw ffprobe responses")
    parser.add_argument("--renderer-ready", action="store_true")
    parser.add_argument("--fonts-ready", action="store_true")
    parser.add_argument("--output", type=Path, help="Write intake JSON; stdout is used otherwise")
    args = parser.parse_args()

    source_language = normalize_language(args.source_language)
    if not source_language:
        parser.error("--source-language must be a resolvable BCP 47 language tag")
    try:
        videos = sorted({file for raw in args.target_video for file in files_from(Path(raw), VIDEO_EXTENSIONS)})
        if not videos:
            raise ValueError("at least one target video is required")
        overrides_raw = [parse_track_override(spec) for spec in args.track_language]
        overrides = {(path, index): language for path, index, language in overrides_raw}
        audio_selection_raw = [parse_audio_selection(spec) for spec in args.audio_stream]
        audio_selections = dict(audio_selection_raw)
        if len(audio_selections) != len(audio_selection_raw):
            raise ValueError("each target video may have only one explicit audio-stream selection")
        cache = load_probe_cache(args.probe_cache)
        ffprobe = args.ffprobe or shutil.which("ffprobe")
        video_items = [probe_video(file, ffprobe, cache, overrides, audio_selections, source_language) for file in videos]
        for index, item in enumerate(video_items, start=1):
            item["id"] = f"video-{index:03d}"
        baseline_groups = [
            external_group("zh-Hans-candidate-baseline" if len(args.candidate_baseline) == 1 else f"zh-Hans-candidate-baseline-{index:02d}", Path(raw), "zh-Hans", None, source_language, True, args.project_type)
            for index, raw in enumerate(args.candidate_baseline, start=1)
        ]
        optional_groups = []
        for index, raw in enumerate(args.optional_source, start=1):
            path, language, roles = parse_source_spec(raw)
            optional_groups.append(external_group(f"optional-source-{index:03d}", path, language, roles, source_language, False, args.project_type))
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))

    embedded = []
    blocking_questions = []
    for video in video_items:
        if video["probe_status"] != "ok":
            blocking_questions.append(f"Provide a probe-readable target video or ffprobe for {video['basename']}: {video.get('probe_error', video['probe_status'])}")
            continue
        audio_streams = [stream for stream in video["streams"] if stream["type"] == "audio"]
        if video["suggested_audio_stream"] is None:
            blocking_questions.append(f"Confirm the intended {source_language} dialogue audio stream for {video['basename']}; detected audio streams: {[(s['index'], s['language'], s['title']) for s in audio_streams]}")
        for stream in video["streams"]:
            if stream["type"] != "subtitle":
                continue
            language = stream["language"]
            if not language:
                blocking_questions.append(f"Confirm language for embedded subtitle {video['basename']} stream {stream['index']} ({stream['codec']}, {stream['title']})")
            embedded.append({
                "id": f"embedded-{video['id']}-s{stream['index']}",
                "video_id": video["id"],
                "container": video["basename"],
                "stream_index": stream["index"],
                "codec": stream["codec"],
                "language": language,
                "language_basis": stream["language_basis"],
                "roles": roles_for(language, source_language, "", str(stream["codec"] or "")) if language else [],
            })
    for group in optional_groups:
        if not group["language"]:
            blocking_questions.append(f"Confirm language and roles for optional source {group['declared_path']}")

    relationships = propose_relationships(video_items, baseline_groups, args.project_type or "tv")
    required_confirmations = [
        "Approve the final episode/video/baseline/audio-stream map; resolve every low-confidence proposal there",
        "Choose and approve a short lowercase project name before any project directory is created",
    ]
    optional_requests = [
        "Provide a source-language subtitle/script for stronger language review"
        if not any(group["language"] == source_language for group in optional_groups)
        and not any(track["language"] == source_language for track in embedded)
        else ""
    ]
    optional_requests = [request for request in optional_requests if request]
    probe_ready = all(video["probe_status"] == "ok" for video in video_items)
    audio_ready = all(video["suggested_audio_stream"] is not None for video in video_items)
    source_text_ready = any(group["language"] == source_language and "source-text-reference" in group["roles"] for group in optional_groups) or any(track["language"] == source_language and "source-text-reference" in track["roles"] for track in embedded)
    report = {
        "schema_version": 2,
        "skill_version": "1.1.2",
        "created_at": date.today().isoformat(),
        "source_language": source_language,
        "project_type": args.project_type,
        "target_videos": video_items,
        "external_source_groups": baseline_groups + optional_groups,
        "embedded_subtitle_tracks": embedded,
        "proposed_episode_map": relationships,
        "blocking_questions": blocking_questions,
        "required_confirmations": required_confirmations,
        "optional_requests": optional_requests,
        "readiness": {
            "structure": "ready" if baseline_groups else "blocked",
            "language": "ready" if probe_ready and audio_ready and source_text_ready else "limited" if probe_ready and audio_ready else "blocked",
            "timing": "ready" if probe_ready and audio_ready else "blocked",
            "visual": "ready" if probe_ready and args.renderer_ready and args.fonts_ready else "limited" if probe_ready else "blocked",
            "release": "blocked",
        },
        "questions": blocking_questions + required_confirmations + [f"Optional: {request}" for request in optional_requests],
        "notes": [
            "This intake manifest is disposable and may contain local absolute paths; init_project.py folds durable facts into project.yaml and local paths into ignored project/local.paths.yaml.",
            "Proposed relationships and detected languages are not user approval. Create an approved episode map after resolving the questions.",
            "Embedded non-source-language subtitles are timing and auxiliary translation evidence, never source-text authority.",
        ],
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
