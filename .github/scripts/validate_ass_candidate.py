#!/usr/bin/env python3
"""Independently verify a normalized ASS candidate against workspace masters."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

from build_subtitle_packages import PackageError, validate_release_dir, yaml_scalar


EVENTS_SECTION = "[Events]\n"
STYLES_SECTION = "[V4+ Styles]\n"
EPISODE_ID = re.compile(r"S\d{2}E\d{2}")
INLINE_FONT = re.compile(r"\\fn([^\\}]*)")
STYLE_DEFINITION = re.compile(r"^Style:\s*(.*)$")
FONT_MAP = {
    "Microsoft YaHei UI": "Noto Sans CJK SC",
    "DengXian": "Noto Sans CJK SC",
    "KaiTi": "Noto Sans CJK SC",
    "SimHei": "Noto Sans CJK SC",
    "Yu Gothic UI": "Noto Sans CJK JP",
}


class CandidateError(RuntimeError):
    pass


def events_tail(text: str) -> str:
    index = text.find(EVENTS_SECTION)
    if index < 0:
        raise CandidateError("missing Events section")
    return text[index:]


def style_map(text: str) -> dict[str, list[str]]:
    start = text.find(STYLES_SECTION)
    end = text.find(EVENTS_SECTION)
    if start < 0 or end <= start:
        raise CandidateError("invalid Styles/Events order")
    styles: dict[str, list[str]] = {}
    for line in text[start:end].splitlines():
        match = STYLE_DEFINITION.match(line)
        if not match:
            continue
        fields = match.group(1).split(",")
        if len(fields) < 2 or fields[0] in styles:
            raise CandidateError(f"malformed or duplicate style {fields[0]!r}")
        styles[fields[0]] = fields
    return styles


def expected_events(source_events: str) -> tuple[str, int]:
    changes = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal changes
        old_font = match.group(1).strip()
        if not old_font:
            return match.group(0)
        if old_font not in FONT_MAP:
            raise CandidateError(f"unapproved source inline font {old_font!r}")
        changes += 1
        return f"\\fn{FONT_MAP[old_font]}"

    return INLINE_FONT.sub(replace, source_events), changes


def verify_file(master: Path, candidate: Path) -> tuple[int, int, int]:
    source = master.read_text(encoding="utf-8-sig")
    output = candidate.read_text(encoding="utf-8")
    source_events = events_tail(source)
    output_events = events_tail(output)
    expected, inline_changes = expected_events(source_events)
    if output_events != expected:
        expected_hash = hashlib.sha256(expected.encode()).hexdigest()
        output_hash = hashlib.sha256(output_events.encode()).hexdigest()
        raise CandidateError(
            f"{candidate}: Events differ beyond approved inline font mapping "
            f"(expected {expected_hash}, got {output_hash})"
        )

    source_styles = style_map(source)
    output_styles = style_map(output)
    changed_styles = 0
    for name, output_fields in output_styles.items():
        if name not in source_styles:
            raise CandidateError(f"{candidate}: unexpected new style {name!r}")
        expected_fields = source_styles[name].copy()
        old_font = expected_fields[1].strip()
        if old_font not in FONT_MAP:
            raise CandidateError(f"{master}: unapproved source style font {old_font!r}")
        expected_fields[1] = FONT_MAP[old_font]
        if output_fields != expected_fields:
            raise CandidateError(
                f"{candidate}: style {name!r} changed beyond approved Fontname mapping"
            )
        changed_styles += 1

    removed = set(source_styles) - set(output_styles)
    return len(removed), changed_styles, inline_changes


def verify_project(project_root: Path) -> None:
    project_root = project_root.resolve()
    candidate_dir = project_root / "project/workspace/build/current-candidate"
    version, candidates = validate_release_dir(candidate_dir, project_root)
    metadata = (project_root / "project.yaml").read_text(encoding="utf-8")
    project_type = yaml_scalar(metadata, "type", 0)
    totals = [0, 0, 0]
    for candidate in candidates:
        match = EPISODE_ID.search(candidate.name)
        episode_id = match.group(0) if match else "MOVIE" if project_type == "movie" else None
        if episode_id is None:
            raise CandidateError(f"{candidate}: cannot determine episode ID")
        master = project_root / "project/workspace/episodes" / episode_id / "master.ass"
        result = verify_file(master, candidate)
        totals = [left + right for left, right in zip(totals, result)]
    print(
        f"verified {project_root.name} {version}: {len(candidates)} subtitles; "
        f"removed {totals[0]} styles; mapped {totals[1]} retained style fonts and "
        f"{totals[2]} inline fonts; Events otherwise byte-identical"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("projects", nargs="+", type=Path)
    args = parser.parse_args()
    for project in args.projects:
        verify_project(project)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CandidateError, PackageError, OSError, UnicodeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
