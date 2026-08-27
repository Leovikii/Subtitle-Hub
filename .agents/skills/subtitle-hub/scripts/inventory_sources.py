#!/usr/bin/env python3
"""Inventory declared target videos and subtitle evidence without modifying inputs."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

VIDEO_EXTENSIONS = {".mkv", ".mp4", ".m2ts", ".ts", ".webm", ".mov"}
SUBTITLE_EXTENSIONS = {".ass", ".ssa", ".srt", ".vtt", ".sup", ".mks"}
ALLOWED_ROLES = {
    "candidate-baseline",
    "source-text-reference",
    "timing-reference",
    "translation-reference",
    "forced-signs-reference",
    "style-layout-reference",
    "secondary-language-release-source",
}


def files_from(path: Path, extensions: set[str]) -> list[Path]:
    path = path.resolve()
    if path.is_file():
        return [path] if path.suffix.lower() in extensions else []
    if path.is_dir():
        return sorted(p for p in path.rglob("*") if p.is_file() and p.suffix.lower() in extensions)
    raise ValueError(f"path does not exist: {path}")


def sha256_prefix(path: Path, limit: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        digest.update(handle.read(limit))
    return digest.hexdigest()


def probe_video(path: Path, ffprobe: str | None) -> dict[str, object]:
    item: dict[str, object] = {
        "basename": path.name,
        "size": path.stat().st_size,
        "sha256_first_mib": sha256_prefix(path),
    }
    if not ffprobe:
        item["probe"] = "unavailable"
        return item
    command = [
        ffprobe,
        "-v",
        "error",
        "-show_entries",
        "format=duration:stream=index,codec_type,codec_name,width,height:stream_tags=language,title",
        "-of",
        "json",
        str(path),
    ]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True, encoding="utf-8")
        item["probe"] = json.loads(result.stdout)
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        item["probe"] = "failed"
        item["probe_error"] = str(error)
    return item


def inspect_subtitle(path: Path) -> dict[str, object]:
    item: dict[str, object] = {
        "basename": path.name,
        "format": path.suffix.lower().lstrip("."),
        "size": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }
    if path.suffix.lower() in {".ass", ".ssa", ".srt", ".vtt"}:
        try:
            text = path.read_text(encoding="utf-8-sig")
            item["text_readable"] = True
            if path.suffix.lower() in {".ass", ".ssa"}:
                item["ass_sections"] = [
                    section for section in ("[Script Info]", "[V4+ Styles]", "[Events]") if section in text
                ]
                item["event_count"] = sum(
                    1 for line in text.splitlines() if line.startswith(("Dialogue:", "Comment:"))
                )
            else:
                item["cue_count_estimate"] = sum(1 for line in text.splitlines() if "-->" in line)
        except UnicodeDecodeError:
            item["text_readable"] = False
    return item


def parse_declared(spec: str) -> tuple[Path, str, list[str]]:
    parts = spec.split("|", 2)
    if len(parts) != 3:
        raise ValueError("subtitle declaration must be PATH|LANGUAGE|ROLE[,ROLE]")
    path, language, roles_text = parts
    roles = [role.strip() for role in roles_text.split(",") if role.strip()]
    unknown = sorted(set(roles) - ALLOWED_ROLES)
    if not language or language == "und":
        raise ValueError(f"subtitle language is unresolved for {path}; ask the user before assigning roles")
    if not roles or unknown:
        raise ValueError(f"invalid roles for {path}: {unknown or roles}")
    return Path(path), language, roles


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-video", action="append", default=[], help="Target video file or directory")
    parser.add_argument(
        "--subtitle",
        action="append",
        default=[],
        metavar="PATH|LANGUAGE|ROLES",
        help="Declared subtitle file/directory and evidence roles",
    )
    parser.add_argument("--source-language", required=True, help="Actual dialogue/source language")
    parser.add_argument("--renderer-ready", action="store_true")
    parser.add_argument("--fonts-ready", action="store_true")
    parser.add_argument("--output", type=Path, help="Write JSON inventory; stdout is used otherwise")
    args = parser.parse_args()

    try:
        videos = sorted({file for raw in args.target_video for file in files_from(Path(raw), VIDEO_EXTENSIONS)})
        declarations = [parse_declared(spec) for spec in args.subtitle]
        subtitle_groups = []
        for declared_path, language, roles in declarations:
            files = files_from(declared_path, SUBTITLE_EXTENSIONS)
            if not files:
                raise ValueError(f"no supported subtitles found: {declared_path}")
            subtitle_groups.append(
                {
                    "declared_path": str(declared_path.resolve()),
                    "language": language,
                    "roles": roles,
                    "files": [inspect_subtitle(file) for file in files],
                }
            )
    except ValueError as error:
        parser.error(str(error))

    ffprobe = shutil.which("ffprobe")
    roles = {role for group in subtitle_groups for role in group["roles"]}
    has_baseline = "candidate-baseline" in roles
    has_source_text = "source-text-reference" in roles
    structure = "ready" if has_baseline else "blocked"
    timing = "ready" if videos else "blocked"
    language = "ready" if videos and has_source_text else ("limited" if videos else "blocked")
    visual = "ready" if videos and args.renderer_ready and args.fonts_ready else ("limited" if videos else "blocked")
    report = {
        "schema_version": 1,
        "source_language": args.source_language,
        "target_videos": [probe_video(file, ffprobe) for file in videos],
        "subtitle_groups": subtitle_groups,
        "readiness": {
            "structure": structure,
            "language": language,
            "timing": timing,
            "visual": visual,
            "release": "blocked",
        },
        "notes": [
            "Absolute paths are inventory-session data and must not be copied into project.yaml.",
            "Language and roles are declarations; conflicting or ambiguous embedded-track metadata requires user confirmation.",
            "Release remains blocked until project initialization, review, and release QC are complete.",
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
