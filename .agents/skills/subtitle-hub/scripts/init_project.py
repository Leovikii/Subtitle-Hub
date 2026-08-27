#!/usr/bin/env python3
"""Initialize a Subtitle Hub proofreading work from verified identity and an episode map."""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

TEXT_SUBTITLE_EXTENSIONS = {".ass", ".ssa", ".srt", ".vtt"}
WORK_ID_RE = re.compile(r"SH\d{4,}")


def quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def render(template: Path, values: dict[str, str]) -> str:
    text = template.read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    unresolved = sorted(set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", text)))
    if unresolved:
        raise ValueError(f"unresolved template values in {template.name}: {unresolved}")
    return text


def load_snapshot(path: Path, expected_id: str) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    required = ("id", "name", "name_cn")
    missing = [key for key in required if not data.get(key)]
    if missing:
        raise ValueError(f"Bangumi snapshot lacks required values: {missing}")
    if str(data["id"]) != expected_id:
        raise ValueError(f"Bangumi snapshot id {data['id']} does not match --bangumi-id {expected_id}")
    return data


def load_map(path: Path) -> list[dict[str, Path | str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames != ["episode", "video", "subtitle"]:
            raise ValueError("episode map header must be: episode<TAB>video<TAB>subtitle")
        rows = []
        seen: set[str] = set()
        for row in reader:
            episode = row["episode"].strip()
            video = Path(row["video"]).expanduser().resolve()
            subtitle = Path(row["subtitle"]).expanduser().resolve()
            if not episode or episode in seen:
                raise ValueError(f"missing or duplicate episode id: {episode!r}")
            if not video.is_file():
                raise ValueError(f"target video is not readable: {video}")
            if not subtitle.is_file() or subtitle.suffix.lower() not in TEXT_SUBTITLE_EXTENSIONS:
                raise ValueError(f"candidate Chinese subtitle is not supported/readable: {subtitle}")
            seen.add(episode)
            rows.append({"episode": episode, "video": video, "subtitle": subtitle})
    if not rows:
        raise ValueError("episode map is empty")
    return rows


def source_block(rows: list[dict[str, Path | str]]) -> str:
    names = [Path(row["subtitle"]).name for row in rows]
    episode_scope = str(rows[0]["episode"]) if len(rows) == 1 else f"{rows[0]['episode']}-{rows[-1]['episode']}"
    return "\n".join(
        [
            "subtitle_sources:",
            "  - id: zh-Hans-candidate-baseline",
            "    language: zh-Hans",
            "    kind: imported-proofreading-baseline",
            "    path: project/sources/subtitles/zh-Hans/candidate-baseline",
            f"    file_count: {len(names)}",
            f"    scope: {quote(episode_scope)}",
            "    roles:",
            "      - candidate-baseline",
            "      - style-layout-reference",
            "    classification:",
            "      status: declared",
            "      confirmed_by: initializer-input",
            f"      confirmed_at: {date.today().isoformat()}",
            "      evidence: explicit proofreading episode map",
        ]
    )


def video_block(rows: list[dict[str, Path | str]]) -> str:
    lines = ["video_sources:", "  target-video:", "    medium: user-provided-local-video", "    timing_reference: true", "    files:"]
    for row in rows:
        lines.append(f"      {row['episode']}: {quote(Path(row['video']).name)}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--series-dir", required=True, type=Path)
    parser.add_argument("--work-id", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--type", required=True, choices=("tv", "movie", "ova", "ona", "special"))
    parser.add_argument("--bangumi-id", required=True)
    parser.add_argument("--bangumi-snapshot", required=True, type=Path)
    parser.add_argument("--episode-map", required=True, type=Path)
    parser.add_argument("--source-language", required=True)
    parser.add_argument("--secondary-language", help="Optional release secondary language")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not WORK_ID_RE.fullmatch(args.work_id):
        parser.error("--work-id must match SH followed by at least four digits")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.slug):
        parser.error("--slug must use lowercase letters, digits, and hyphens")
    try:
        snapshot = load_snapshot(args.bangumi_snapshot, args.bangumi_id)
        rows = load_map(args.episode_map)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))
    subtitle_names = [Path(row["subtitle"]).name.casefold() for row in rows]
    if len(subtitle_names) != len(set(subtitle_names)):
        parser.error("candidate subtitles contain duplicate basenames; rename or separate them before initialization")

    target = args.series_dir.resolve() / f"{args.work_id}--{args.slug}"
    if target.exists():
        parser.error(f"target already exists: {target}")
    skill_root = Path(__file__).resolve().parents[1]
    template_root = skill_root / "assets" / "templates"
    scope = "MOVIE" if args.type == "movie" and len(rows) == 1 else f"{len(rows)} mapped episodes"
    values = {
        "WORK_ID": args.work_id,
        "SLUG": args.slug,
        "WORK_TYPE": args.type,
        "EPISODE_COUNT": str(len(rows)),
        "BANGUMI_ID": args.bangumi_id,
        "TITLE_JA": str(snapshot["name"]),
        "TITLE_ZH_HANS": str(snapshot["name_cn"]),
        "TITLE_JA_YAML": quote(str(snapshot["name"])),
        "TITLE_ZH_HANS_YAML": quote(str(snapshot["name_cn"])),
        "VERIFIED_AT": date.today().isoformat(),
        "SOURCE_LANGUAGE": args.source_language,
        "SECONDARY_LANGUAGE_YAML": quote(args.secondary_language) if args.secondary_language else "null",
        "SECONDARY_LANGUAGE_DISPLAY": args.secondary_language or "无（单语中文字幕）",
        "SCOPE": scope,
        "UPDATED_AT": date.today().isoformat(),
    }
    project_text = render(template_root / "project.yaml", values)
    project_text = project_text.replace("subtitle_sources: []", source_block(rows))
    project_text = project_text.replace("video_sources: {}", video_block(rows))

    planned = {
        "target": str(target),
        "episodes": [str(row["episode"]) for row in rows],
        "videos_recorded_by_basename_only": [Path(row["video"]).name for row in rows],
        "subtitles_to_copy": [str(row["subtitle"]) for row in rows],
    }
    if args.dry_run:
        print(json.dumps(planned, ensure_ascii=False, indent=2))
        return 0

    directories = [
        target / "docs",
        target / "project" / "sources" / "subtitles" / "zh-Hans" / "candidate-baseline",
        target / "project" / "workspace" / "temp" / "tools",
        target / "project" / "workspace" / "temp" / "intermediate",
        target / "project" / "workspace" / "temp" / "review" / "attachments",
        target / "project" / "workspace" / "temp" / "logs",
        target / "project" / "workspace" / "build",
        target / "project" / "archive",
        target / "subtitles" / "current",
    ]
    for row in rows:
        directories.append(target / "project" / "workspace" / "episodes" / str(row["episode"]))
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=False)
    for directory in (
        target / "project" / "workspace" / "temp" / "tools",
        target / "project" / "workspace" / "temp" / "intermediate",
        target / "project" / "workspace" / "temp" / "review",
        target / "project" / "workspace" / "temp" / "logs",
        target / "project" / "workspace" / "build",
    ):
        (directory / ".gitignore").write_text("*\n!.gitignore\n", encoding="utf-8")

    (target / "project.yaml").write_text(project_text, encoding="utf-8")
    (target / "docs" / "project-guide.md").write_text(render(template_root / "project-guide.md", values), encoding="utf-8")
    (target / "docs" / "progress.yaml").write_text(render(template_root / "progress.yaml", values), encoding="utf-8")
    shutil.copyfile(template_root / "issues.tsv", target / "docs" / "issues.tsv")
    shutil.copyfile(template_root / "change-log.tsv", target / "docs" / "change-log.tsv")
    destination = target / "project" / "sources" / "subtitles" / "zh-Hans" / "candidate-baseline"
    for row in rows:
        source = Path(row["subtitle"])
        output = destination / source.name
        shutil.copy2(source, output)
    print(json.dumps(planned, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
