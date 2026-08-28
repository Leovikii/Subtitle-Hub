#!/usr/bin/env python3
"""Independently verify a 1.2.0 ASS candidate against workspace masters."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

from build_subtitle_packages import PackageError, validate_release_dir, yaml_scalar

EVENTS = "[Events]\n"
STYLES = "[V4+ Styles]\n"
EPISODE_ID = re.compile(r"S\d{2}E\d{2,3}")
STYLE = re.compile(r"^Style:\s*(.*)$")
RESET = re.compile(r"\\r([^\\}]*)")
INLINE_FONT = re.compile(r"\\fn([^\\}]*)")
OVERRIDE = re.compile(r"\{[^}]*\}")
KANA = re.compile(r"[\u3040-\u30ff]")
JP_LABEL = re.compile(r"(?:日文|日本|日语|日語|原文|原語|(?<![0-9A-Za-z])(?:ja|jp|jpn)(?![0-9A-Za-z]))", re.I)
WORKING_FONTS = {"Microsoft YaHei UI", "Yu Gothic UI"}
SC_FONT = "Noto Sans CJK SC"
JP_FONT = "Noto Sans CJK JP"


class CandidateError(RuntimeError):
    pass


def section(text: str, marker: str) -> str:
    start = text.find(marker)
    if start < 0:
        raise CandidateError(f"missing {marker.strip()} section")
    match = re.search(r"(?m)^\[[^\n]+\]$", text[start + len(marker):])
    end = start + len(marker) + match.start() if match else len(text)
    return text[start:end]


def style_map(text: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for line in section(text, STYLES).splitlines():
        match = STYLE.match(line)
        if not match:
            continue
        fields = match.group(1).split(",")
        if len(fields) < 2 or fields[0] in result:
            raise CandidateError(f"malformed or duplicate style {fields[0]!r}")
        result[fields[0]] = fields
    return result


def rendered_events(text: str) -> tuple[str, int]:
    output: list[str] = []
    removed = 0
    for line in section(text, EVENTS).splitlines(keepends=True):
        if line.startswith("Comment:"):
            removed += 1
        else:
            output.append(line)
    return "".join(output), removed


def references(events: str) -> set[str]:
    result: set[str] = set()
    for line in events.splitlines():
        if not line.startswith("Dialogue:"):
            continue
        parts = line.split(",", 9)
        if len(parts) != 10:
            raise CandidateError(f"malformed event line: {line[:80]}")
        result.add(parts[3].strip() or "Default")
        result.update(value.strip() for value in RESET.findall(parts[9]) if value.strip())
    return result


def font_targets(events: str, refs: set[str]) -> dict[str, str]:
    targets = {name: JP_FONT if JP_LABEL.search(name) else SC_FONT for name in refs}
    for line in events.splitlines():
        if not line.startswith("Dialogue:"):
            continue
        parts = line.split(",", 9)
        active_inline = False
        base: list[str] = []
        cursor = 0
        for block in OVERRIDE.finditer(parts[9]):
            if not active_inline:
                base.append(parts[9][cursor:block.start()])
            tags = block.group(0)
            if RESET.search(tags):
                active_inline = False
            if any(value.strip() for value in INLINE_FONT.findall(tags)):
                active_inline = True
            cursor = block.end()
        if not active_inline:
            base.append(parts[9][cursor:])
        if KANA.search("".join(base)):
            names = [parts[3].strip() or "Default", *[value.strip() for value in RESET.findall(parts[9]) if value.strip()]]
            for name in names:
                targets[name] = JP_FONT
    return targets


def map_inline(events: str, targets: dict[str, str]) -> tuple[str, int]:
    output: list[str] = []
    changes = 0
    for line in events.splitlines(keepends=True):
        if not line.startswith("Dialogue:"):
            output.append(line)
            continue
        parts = line.removesuffix("\n").split(",", 9)
        style_target = targets[parts[3].strip() or "Default"]
        blocks = list(OVERRIDE.finditer(parts[9]))
        rebuilt: list[str] = []
        cursor = 0
        for index, block in enumerate(blocks):
            rebuilt.append(parts[9][cursor:block.start()])
            next_start = blocks[index + 1].start() if index + 1 < len(blocks) else len(parts[9])
            following = parts[9][block.end():next_start]
            target = JP_FONT if KANA.search(following) else style_target

            def replace(match: re.Match[str]) -> str:
                nonlocal changes
                old = match.group(1).strip()
                if not old:
                    return match.group(0)
                if old not in WORKING_FONTS:
                    raise CandidateError(f"unapproved working inline font {old!r}")
                changes += 1
                return f"\\fn{target}"

            rebuilt.append(INLINE_FONT.sub(replace, block.group(0)))
            cursor = block.end()
        rebuilt.append(parts[9][cursor:])
        parts[9] = "".join(rebuilt)
        output.append(",".join(parts) + ("\n" if line.endswith("\n") else ""))
    return "".join(output), changes


def verify_file(master: Path, candidate: Path) -> tuple[int, int, int, int]:
    source = master.read_text(encoding="utf-8-sig")
    output = candidate.read_text(encoding="utf-8")
    source_events, comments_removed = rendered_events(source)
    refs = references(source_events)
    targets = font_targets(source_events, refs)
    expected_events, inline_changes = map_inline(source_events, targets)
    output_events = section(output, EVENTS)
    if output_events != expected_events:
        expected_hash = hashlib.sha256(expected_events.encode()).hexdigest()
        output_hash = hashlib.sha256(output_events.encode()).hexdigest()
        raise CandidateError(f"{candidate}: rendered Events differ beyond allowed cleanup/font mapping (expected {expected_hash}, got {output_hash})")

    source_styles = style_map(source)
    output_styles = style_map(output)
    if set(output_styles) != refs:
        raise CandidateError(f"{candidate}: retained styles differ; expected {sorted(refs)}, got {sorted(output_styles)}")
    changed = 0
    for name in refs:
        if name not in source_styles:
            raise CandidateError(f"{master}: undefined referenced style {name!r}")
        expected = source_styles[name].copy()
        old_font = expected[1].strip()
        if old_font not in WORKING_FONTS:
            raise CandidateError(f"{master}: unapproved working style font {old_font!r}")
        expected[1] = targets[name]
        if output_styles[name] != expected:
            raise CandidateError(f"{candidate}: style {name!r} changed beyond Fontname mapping")
        changed += 1
    return len(set(source_styles) - refs), changed, inline_changes, comments_removed


def verify_project(project_root: Path) -> None:
    project_root = project_root.resolve()
    candidate_dir = project_root / "project/workspace/build/current-candidate"
    version, candidates = validate_release_dir(candidate_dir, project_root)
    metadata = (project_root / "project.yaml").read_text(encoding="utf-8")
    project_type = yaml_scalar(metadata, "type", 0)
    totals = [0, 0, 0, 0]
    for candidate in candidates:
        match = EPISODE_ID.search(candidate.name)
        episode = match.group(0) if match else "MOVIE" if project_type == "movie" else None
        if episode is None:
            raise CandidateError(f"{candidate}: cannot determine episode ID")
        master = project_root / "project/workspace/episodes" / episode / "master.ass"
        totals = [a + b for a, b in zip(totals, verify_file(master, candidate))]
    print(f"verified {project_root.name} {version}: {len(candidates)} subtitles; removed {totals[0]} styles/{totals[3]} Comments; mapped {totals[1]} style/{totals[2]} inline fonts; rendered Events otherwise identical")


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
