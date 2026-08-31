#!/usr/bin/env python3
"""Build a structurally normalized ASS release candidate."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

from build_subtitle_packages import (
    PackageError,
    bangumi_identity,
    is_high_confidence_credit_fragment,
    validate_release_dir,
    yaml_block,
    yaml_scalar,
)


STYLE_SECTION = "[V4+ Styles]"
EVENTS_SECTION = "[Events]"
STYLE_RESET = re.compile(r"\\r([^\\}]*)")
INLINE_FONT = re.compile(r"\\fn([^\\}]*)")
OVERRIDE_BLOCK = re.compile(r"\{[^}]*\}")
STYLE_DEFINITION = re.compile(r"^Style:\s*(.*)$")
REQUIRED_SCRIPT_INFO = (
    "ScriptType",
    "WrapStyle",
    "ScaledBorderAndShadow",
    "PlayResX",
    "PlayResY",
    "YCbCr Matrix",
)
SC_FONT = "Noto Sans CJK SC"
JP_FONT = "Noto Sans CJK JP"
JAPANESE_KANA = re.compile(r"[\u3040-\u30ff]")
JAPANESE_STYLE_LABEL = re.compile(
    r"(?:日文|日本|日语|日語|原文|原語|(?<![0-9A-Za-z])(?:ja|jp|jpn)(?![0-9A-Za-z]))",
    re.IGNORECASE,
)
SOURCE_METADATA_PREFIX = "[源字幕信息]"
SUBTITLE_GROUP_IN_TEXT = re.compile(
    r"([0-9A-Za-z_\u3040-\u30ff\u3400-\u9fff·&＋+ -]{1,48}字幕组)"
)
SOURCE_PROVENANCE_MARKERS = (
    "中文底稿",
    "日文原本",
    "版本校验",
    "时间轴与特效参考",
)
SOURCE_DISCLAIMER_MARKERS = ("仅供", "不得用于", "禁止用于", "违法", "欢迎访问")


class NormalizeError(RuntimeError):
    pass


def project_languages(project_root: Path) -> tuple[str, str | None]:
    metadata = (project_root / "project.yaml").read_text(encoding="utf-8")
    if yaml_scalar(metadata, "schema_version", 0) != "9":
        raise NormalizeError("upgrade project to schema_version 9 before building a candidate")
    release = yaml_block(metadata, "release_languages", 0)
    primary = yaml_scalar(release, "primary", 2)
    secondary = yaml_scalar(release, "secondary", 2)
    return primary, None if secondary == "null" else secondary


def script_info(source: str) -> tuple[dict[str, str], list[str]]:
    if not source.startswith("[Script Info]\n"):
        raise NormalizeError("ASS must begin with [Script Info]")
    next_section = re.search(r"(?m)^\[[^\n]+\]$", source[len("[Script Info]\n") :])
    if not next_section:
        raise NormalizeError("ASS contains no section after [Script Info]")
    end = len("[Script Info]\n") + next_section.start()
    fields: dict[str, str] = {}
    comments: list[str] = []
    for line in source[len("[Script Info]\n") : end].splitlines():
        if line.startswith(";"):
            comments.append(line)
        elif ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    for field in REQUIRED_SCRIPT_INFO:
        if not fields.get(field):
            raise NormalizeError(f"missing required Script Info field {field}")
    return fields, comments


def ass_section(source: str, header: str) -> str:
    marker = f"{header}\n"
    start = source.find(marker)
    if start < 0:
        raise NormalizeError(f"missing {header} section")
    next_section = re.search(r"(?m)^\[[^\n]+\]$", source[start + len(marker) :])
    end = (
        start + len(marker) + next_section.start()
        if next_section
        else len(source)
    )
    return source[start:end]


def event_style_references(events_tail: str) -> set[str]:
    references: set[str] = set()
    in_events = False
    for line in events_tail.splitlines():
        if line.startswith("[") and line.endswith("]"):
            in_events = line == EVENTS_SECTION
            continue
        if not in_events or not line.startswith(("Dialogue:", "Comment:")):
            continue
        parts = line.split(",", 9)
        if len(parts) != 10:
            raise NormalizeError(f"malformed event line: {line[:80]}")
        style = parts[3].strip()
        references.add(style or "Default")
        for reset in STYLE_RESET.findall(parts[9]):
            reset_style = reset.strip()
            if reset_style:
                references.add(reset_style)
    return references


def font_targets_by_style(events_tail: str, references: set[str]) -> dict[str, str]:
    targets = {
        style: JP_FONT if JAPANESE_STYLE_LABEL.search(style) else SC_FONT
        for style in references
    }
    in_events = False
    for line in events_tail.splitlines():
        if line.startswith("[") and line.endswith("]"):
            in_events = line == EVENTS_SECTION
            continue
        if not in_events or not line.startswith(("Dialogue:", "Comment:")):
            continue
        parts = line.split(",", 9)
        if len(parts) != 10:
            raise NormalizeError(f"malformed event line: {line[:80]}")
        active_inline_font = False
        base_text: list[str] = []
        cursor = 0
        for block in OVERRIDE_BLOCK.finditer(parts[9]):
            if not active_inline_font:
                base_text.append(parts[9][cursor:block.start()])
            tags = block.group(0)
            if STYLE_RESET.search(tags):
                active_inline_font = False
            if any(value.strip() for value in INLINE_FONT.findall(tags)):
                active_inline_font = True
            cursor = block.end()
        if not active_inline_font:
            base_text.append(parts[9][cursor:])
        if not JAPANESE_KANA.search("".join(base_text)):
            continue
        styles = [parts[3].strip() or "Default"]
        styles.extend(reset.strip() for reset in STYLE_RESET.findall(parts[9]) if reset.strip())
        for style in styles:
            targets[style] = JP_FONT
    return targets


def normalize_styles(
    style_section: str, references: set[str], font_targets: dict[str, str]
) -> tuple[str, list[str], int]:
    defined: set[str] = set()
    removed: list[str] = []
    output: list[str] = []
    font_changes = 0
    for line in style_section.splitlines(keepends=True):
        style_match = STYLE_DEFINITION.match(line.removesuffix("\n"))
        if not style_match:
            output.append(line)
            continue
        name = style_match.group(1).split(",", 1)[0]
        if name in defined:
            raise NormalizeError(f"duplicate style definition: {name!r}")
        defined.add(name)
        if name in references:
            line_ending = "\n" if line.endswith("\n") else ""
            fields = style_match.group(1).split(",")
            if len(fields) < 2:
                raise NormalizeError(f"malformed style line: {line[:80]}")
            old_font = fields[1].strip()
            new_font = font_targets[name]
            if new_font != old_font:
                font_changes += 1
            fields[1] = new_font
            output.append("Style: " + ",".join(fields) + line_ending)
        else:
            removed.append(name)
    missing = sorted(references - defined)
    if missing:
        raise NormalizeError(f"events reference undefined styles: {', '.join(missing)}")
    retained = defined - set(removed)
    missing_after = sorted(references - retained)
    if missing_after:
        raise NormalizeError(f"style pruning removed referenced styles: {', '.join(missing_after)}")
    return "".join(output), removed, font_changes


def normalize_inline_fonts(
    events_tail: str, font_targets: dict[str, str]
) -> tuple[str, int]:
    changes = 0
    output: list[str] = []
    in_events = False
    for line in events_tail.splitlines(keepends=True):
        bare = line.removesuffix("\n")
        if bare.startswith("[") and bare.endswith("]"):
            in_events = bare == EVENTS_SECTION
        if not in_events or not bare.startswith(("Dialogue:", "Comment:")):
            output.append(line)
            continue
        parts = bare.split(",", 9)
        if len(parts) != 10:
            raise NormalizeError(f"malformed event line: {bare[:80]}")
        style = parts[3].strip() or "Default"
        target = font_targets[style]

        text = parts[9]
        blocks = list(OVERRIDE_BLOCK.finditer(text))
        if blocks:
            rebuilt: list[str] = []
            cursor = 0
            for index, block in enumerate(blocks):
                rebuilt.append(text[cursor:block.start()])
                next_start = blocks[index + 1].start() if index + 1 < len(blocks) else len(text)
                following_text = text[block.end():next_start]
                inline_target = JP_FONT if JAPANESE_KANA.search(following_text) else target

                def replace(match: re.Match[str]) -> str:
                    nonlocal changes
                    if not match.group(1).strip():
                        return match.group(0)
                    replacement = f"\\fn{inline_target}"
                    if replacement != match.group(0):
                        changes += 1
                    return replacement

                rebuilt.append(INLINE_FONT.sub(replace, block.group(0)))
                cursor = block.end()
            rebuilt.append(text[cursor:])
            parts[9] = "".join(rebuilt)
        output.append(",".join(parts) + ("\n" if line.endswith("\n") else ""))
    return "".join(output), changes


def assert_rendered_regression(
    source_styles: str,
    candidate_styles: str,
    source_events: str,
    candidate_events: str,
    references: set[str],
) -> None:
    def styles(text: str) -> dict[str, list[str]]:
        result: dict[str, list[str]] = {}
        for line in text.splitlines():
            match = STYLE_DEFINITION.match(line)
            if match:
                fields = match.group(1).split(",")
                result[fields[0]] = fields
        return result

    before = styles(source_styles)
    after = styles(candidate_styles)
    if set(after) != references:
        raise NormalizeError("candidate retained-style set differs from rendered references")
    for name in references:
        if name not in before:
            raise NormalizeError(f"source lacks referenced style {name!r}")
        if before[name] != after[name]:
            raise NormalizeError(f"candidate changed master style {name!r}")

    if source_events != candidate_events:
        raise NormalizeError("candidate changed rendered Events")


def source_credit_from_metadata(text: str) -> str | None:
    value = text.removeprefix(SOURCE_METADATA_PREFIX).strip()
    if any(marker in value for marker in SOURCE_PROVENANCE_MARKERS):
        return None
    if any(marker in value for marker in SOURCE_DISCLAIMER_MARKERS):
        group_match = SUBTITLE_GROUP_IN_TEXT.search(value.removeprefix("本字幕由"))
        return group_match.group(1).strip() if group_match else None
    return value if is_high_confidence_credit_fragment(value) else None


def normalize_source_metadata(events_tail: str) -> tuple[str, list[str], int]:
    output: list[str] = []
    credits: list[str] = []
    removed = 0
    in_events = False
    for line in events_tail.splitlines(keepends=True):
        bare = line.removesuffix("\n")
        if bare.startswith("[") and bare.endswith("]"):
            in_events = bare == EVENTS_SECTION
        if in_events and bare.startswith("Comment:"):
            parts = bare.split(",", 9)
            if len(parts) != 10:
                raise NormalizeError(f"malformed event line: {bare[:80]}")
            if parts[4].strip() == "Source-Metadata" and parts[9].startswith(
                SOURCE_METADATA_PREFIX
            ):
                credit = source_credit_from_metadata(parts[9])
                if credit and credit not in credits:
                    credits.append(credit)
            removed += 1
            continue
        output.append(line)
    return "".join(output), credits, removed


def normalized_header(
    *,
    fields: dict[str, str],
    comments: list[str],
    version: str,
    primary: str,
    secondary: str | None,
    subject_id: str,
    title_zh_hans: str,
    episode_id: str,
    event_source_credits: list[str],
) -> str:
    timing_notes = [
        line.removeprefix("; ")
        for line in comments
        if line.startswith("; Target MKV mux lead")
    ]
    source_credits: list[str] = []
    for line in comments:
        if not line.startswith(
            ("; Original fansub credit (metadata only):", "; Subtitle-Hub-Source-Credit:")
        ):
            continue
        raw_credit = line.split(":", 1)[1].strip()
        for credit in raw_credit.split("；"):
            credit = " ".join(credit.split())
            if (
                is_high_confidence_credit_fragment(credit)
                and credit not in source_credits
            ):
                source_credits.append(credit)
    for credit in event_source_credits:
        if credit not in source_credits:
            source_credits.append(credit)
    if len(timing_notes) > 1:
        raise NormalizeError("multiple timing notes require manual review")

    language_list = primary if secondary is None else f"{primary}, {secondary}"
    lines = [
        "[Script Info]",
        f"; Subtitle-Hub-Version: {version}",
        f"; Subtitle-Hub-Languages: {language_list}",
        f"; Subtitle-Hub-Primary-Language: {primary}",
    ]
    if secondary is not None:
        lines.append(f"; Subtitle-Hub-Secondary-Language: {secondary}")
    if timing_notes:
        lines.append(f"; Subtitle-Hub-Timing-Note: {timing_notes[0]}")
    if source_credits:
        lines.append(f"; Subtitle-Hub-Source-Credit: {'；'.join(source_credits)}")
    lines.extend(
        [
            f"Title: bgm{subject_id} - {title_zh_hans} - {episode_id}",
            f"ScriptType: {fields['ScriptType']}",
            f"WrapStyle: {fields['WrapStyle']}",
            f"ScaledBorderAndShadow: {fields['ScaledBorderAndShadow']}",
            f"PlayResX: {fields['PlayResX']}",
            f"PlayResY: {fields['PlayResY']}",
            f"YCbCr Matrix: {fields['YCbCr Matrix']}",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def normalize_file(
    source_path: Path,
    output_path: Path,
    *,
    version: str,
    primary: str,
    secondary: str | None,
    subject_id: str,
    title_zh_hans: str,
    episode_id: str,
) -> tuple[list[str], int, int, int]:
    source = source_path.read_text(encoding="utf-8-sig")
    if "\r" in source:
        raise NormalizeError(f"{source_path}: expected normalized LF line endings")
    style_start = source.find(f"{STYLE_SECTION}\n")
    events_start = source.find(f"{EVENTS_SECTION}\n")
    if style_start < 0 or events_start <= style_start:
        raise NormalizeError(f"{source_path}: invalid Styles/Events section order")
    master_fonts = {
        match.group(1).strip()
        for match in re.finditer(r"(?m)^Style:\s*[^,]+,([^,]+)", source)
    }
    master_fonts.update(value.strip() for value in INLINE_FONT.findall(source) if value.strip())
    unsupported = sorted(master_fonts - {SC_FONT, JP_FONT})
    if unsupported:
        raise NormalizeError(
            f"{source_path}: master has non-Noto fonts: {', '.join(unsupported)}"
        )

    fields, comments = script_info(source)
    style_section = ass_section(source, STYLE_SECTION)
    events_tail = ass_section(source, EVENTS_SECTION)
    events_without_metadata, event_source_credits, metadata_removed = (
        normalize_source_metadata(events_tail)
    )
    references = event_style_references(events_without_metadata)
    font_targets = font_targets_by_style(events_without_metadata, references)
    normalized_styles, removed, style_font_changes = normalize_styles(
        style_section, references, font_targets
    )
    normalized_events, inline_font_changes = normalize_inline_fonts(
        events_without_metadata, font_targets
    )
    if style_font_changes or inline_font_changes:
        raise NormalizeError(f"{source_path}: master is not already Noto-normalized")
    assert_rendered_regression(
        style_section,
        normalized_styles,
        events_without_metadata,
        normalized_events,
        references,
    )

    header = normalized_header(
        fields=fields,
        comments=comments,
        version=version,
        primary=primary,
        secondary=secondary,
        subject_id=subject_id,
        title_zh_hans=title_zh_hans,
        episode_id=episode_id,
        event_source_credits=event_source_credits,
    )
    output = header + normalized_styles + normalized_events
    if output[output.find(f"{EVENTS_SECTION}\n") :] != normalized_events:
        raise NormalizeError(f"{source_path}: unexpected Events mutation")
    output_path.write_text(output, encoding="utf-8", newline="\n")
    return removed, style_font_changes, inline_font_changes, metadata_removed


def build_candidate(project_root: Path, version: str) -> None:
    project_root = project_root.resolve()
    metadata = (project_root / "project.yaml").read_text(encoding="utf-8")
    initialization = yaml_block(metadata, "initialization", 0)
    if (
        yaml_scalar(metadata, "schema_version", 0) != "9"
        or yaml_scalar(initialization, "skill_version", 2) != "1.4.2"
    ):
        raise NormalizeError("upgrade project to the Skill 1.4.2 contract before building a candidate")
    workspace_episodes = project_root / "project/workspace/episodes"
    output_dir = project_root / "project/workspace/build/current-candidate"
    if output_dir.exists():
        raise NormalizeError(f"refusing to overwrite existing candidate: {output_dir}")
    output_dir.mkdir(parents=True)

    subject_id, _, title_zh_hans, _ = bangumi_identity(project_root)
    primary, secondary = project_languages(project_root)
    project_type = yaml_scalar(metadata, "type", 0)
    video_sources = yaml_block(metadata, "video_sources", 0)
    target_video = yaml_block(video_sources, "target-video", 2)
    files_block = yaml_block(target_video, "files", 4)
    release_targets = [
        (match.group(1), f"{Path(match.group(2).strip().strip(chr(34) + chr(39))).stem}.{primary}.ass")
        for match in re.finditer(r"(?m)^      ([A-Za-z0-9]+):\s*(.*?)\s*$", files_block)
    ]
    if not release_targets:
        raise NormalizeError(f"{project_root / 'project.yaml'}: target-video map is empty")

    total_removed = 0
    total_style_font_changes = 0
    total_inline_font_changes = 0
    total_source_metadata_removed = 0
    try:
        for episode_id, output_name in release_targets:
            if project_type == "movie" and episode_id != "MOVIE":
                raise NormalizeError(f"{project_root}: movie target map must use MOVIE")
            source_path = workspace_episodes / episode_id / "master.ass"
            if not source_path.is_file():
                raise NormalizeError(f"missing workspace master: {source_path}")
            removed, style_font_changes, inline_font_changes, metadata_removed = normalize_file(
                source_path,
                output_dir / output_name,
                version=version,
                primary=primary,
                secondary=secondary,
                subject_id=subject_id,
                title_zh_hans=title_zh_hans,
                episode_id=episode_id,
            )
            total_removed += len(removed)
            total_style_font_changes += style_font_changes
            total_inline_font_changes += inline_font_changes
            total_source_metadata_removed += metadata_removed
        (output_dir / "VERSION").write_text(f"{version}\n", encoding="utf-8", newline="\n")
        validate_release_dir(output_dir, project_root)
    except Exception:
        shutil.rmtree(output_dir)
        raise
    print(
        f"built {output_dir} ({len(release_targets)} subtitles; "
        f"removed {total_removed} unused style definitions; "
        f"removed {total_source_metadata_removed} non-rendering comment events; "
        f"changed {total_style_font_changes} style fonts and "
        f"{total_inline_font_changes} inline fonts)"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="work project root")
    parser.add_argument("--version", required=True, help="candidate SemVer")
    args = parser.parse_args()
    build_candidate(args.project, args.version)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (NormalizeError, PackageError, OSError, UnicodeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
