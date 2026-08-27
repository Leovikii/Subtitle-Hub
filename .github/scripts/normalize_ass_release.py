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
LEGACY_SECONDARY_SUFFIX = re.compile(r"\.(zh-Hans)\.(ja|en)\.ass\Z")
PRIMARY_SUFFIX = re.compile(r"\.(zh-Hans)\.ass\Z")
EPISODE_ID = re.compile(r"S\d{2}E\d{2}")
STYLE_RESET = re.compile(r"\\r([^\\}]*)")
INLINE_FONT = re.compile(r"\\fn([^\\}]*)")
STYLE_DEFINITION = re.compile(r"^Style:\s*(.*)$")
REQUIRED_SCRIPT_INFO = (
    "ScriptType",
    "WrapStyle",
    "ScaledBorderAndShadow",
    "PlayResX",
    "PlayResY",
    "YCbCr Matrix",
)
FONT_MAP = {
    "Microsoft YaHei UI": "Noto Sans CJK SC",
    "DengXian": "Noto Sans CJK SC",
    "KaiTi": "Noto Sans CJK SC",
    "SimHei": "Noto Sans CJK SC",
    "Yu Gothic UI": "Noto Sans CJK JP",
}
STANDARD_FONTS = {"Noto Sans CJK SC", "Noto Sans CJK JP"}
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
    languages = yaml_block(metadata, "languages", 0)
    release = yaml_block(languages, "release", 2)
    primary = yaml_scalar(release, "primary", 4)
    secondary = yaml_scalar(release, "secondary", 4)
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


def normalize_styles(
    style_section: str, references: set[str]
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
            new_font = FONT_MAP.get(old_font, old_font)
            if new_font not in STANDARD_FONTS:
                raise NormalizeError(
                    f"style {name!r} uses unsupported font {old_font!r}; "
                    "record a project exception or extend the approved mapping"
                )
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


def normalize_inline_fonts(events_tail: str) -> tuple[str, int]:
    changes = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal changes
        old_font = match.group(1).strip()
        if not old_font:
            return match.group(0)
        new_font = FONT_MAP.get(old_font, old_font)
        if new_font not in STANDARD_FONTS:
            raise NormalizeError(
                f"event override uses unsupported font {old_font!r}; "
                "record a project exception or extend the approved mapping"
            )
        replacement = f"\\fn{new_font}"
        if replacement != match.group(0):
            changes += 1
        return replacement

    return INLINE_FONT.sub(replace, events_tail), changes


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

    fields, comments = script_info(source)
    style_section = ass_section(source, STYLE_SECTION)
    events_tail = ass_section(source, EVENTS_SECTION)
    events_without_metadata, event_source_credits, metadata_removed = (
        normalize_source_metadata(events_tail)
    )
    references = event_style_references(events_without_metadata)
    normalized_styles, removed, style_font_changes = normalize_styles(
        style_section, references
    )
    normalized_events, inline_font_changes = normalize_inline_fonts(events_without_metadata)

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
    release_dir = project_root / "subtitles/current"
    workspace_episodes = project_root / "project/workspace/episodes"
    output_dir = project_root / "project/workspace/build/current-candidate"
    if output_dir.exists():
        raise NormalizeError(f"refusing to overwrite existing candidate: {output_dir}")
    output_dir.mkdir(parents=True)

    subject_id, _, title_zh_hans, _ = bangumi_identity(project_root)
    primary, secondary = project_languages(project_root)
    metadata = (project_root / "project.yaml").read_text(encoding="utf-8")
    project_type = yaml_scalar(metadata, "type", 0)
    release_templates = sorted(release_dir.glob("*.ass"), key=lambda path: path.name)
    if not release_templates:
        raise NormalizeError(f"{release_dir}: contains no ASS files")

    total_removed = 0
    total_style_font_changes = 0
    total_inline_font_changes = 0
    total_source_metadata_removed = 0
    try:
        for release_template in release_templates:
            legacy_match = LEGACY_SECONDARY_SUFFIX.search(release_template.name)
            primary_match = PRIMARY_SUFFIX.search(release_template.name)
            if legacy_match:
                if legacy_match.group(1) != primary or legacy_match.group(2) != secondary:
                    raise NormalizeError(
                        f"{release_template}: does not match current language metadata"
                    )
            elif not primary_match or primary_match.group(1) != primary:
                raise NormalizeError(
                    f"{release_template}: does not match current language metadata"
                )
            episode_match = EPISODE_ID.search(release_template.name)
            if episode_match:
                episode_id = episode_match.group(0)
            elif project_type == "movie":
                episode_id = "MOVIE"
            else:
                raise NormalizeError(
                    f"{release_template}: cannot determine workspace episode ID"
                )
            source_path = workspace_episodes / episode_id / "master.ass"
            if not source_path.is_file():
                raise NormalizeError(f"missing workspace master: {source_path}")
            output_name = (
                LEGACY_SECONDARY_SUFFIX.sub(f".{primary}.ass", release_template.name)
                if legacy_match
                else release_template.name
            )
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
        f"built {output_dir} ({len(release_templates)} subtitles; "
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
