#!/usr/bin/env python3
"""Isolated behavioral tests for the Subtitle Hub Skill 1.0 toolchain."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_ROOT = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_ROOT.parent
REPOSITORY_ROOT = SKILL_ROOT.parents[2]
PACKAGE_SCRIPT = REPOSITORY_ROOT / ".github" / "scripts" / "build_subtitle_packages.py"


def run_path(path: Path, *args: str, expect: int = 0) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["PYTHONUTF8"] = "1"
    result = subprocess.run(
        [sys.executable, "-B", str(path), *args], capture_output=True, text=True, encoding="utf-8",
        env=environment,
    )
    if result.returncode != expect:
        raise AssertionError(
            f"{path.name} exited {result.returncode}, expected {expect}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def run(script: str, *args: str, expect: int = 0) -> subprocess.CompletedProcess[str]:
    return run_path(SCRIPT_ROOT / script, *args, expect=expect)


def write_srt(path: Path, text: str = "测试") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"1\n00:00:01,000 --> 00:00:02,000\n{text}\n", encoding="utf-8")


def baseline_ass_bytes(text: str = "测试") -> bytes:
    return (
        "[Script Info]\nScriptType: v4.00+\nWrapStyle: 0\nScaledBorderAndShadow: yes\n"
        "PlayResX: 1920\nPlayResY: 1080\nYCbCr Matrix: TV.709\n\n[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
        "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding\n"
        "Style: CN-Main,Noto Sans CJK SC,62,&H00FFFFFF,&H000000FF,&H00101010,&H80000000,0,0,0,0,"
        "100,100,0,0,1,3,1,2,90,90,54,1\n\n[Events]\n"
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
        f"Dialogue: 0,0:00:01.00,0:00:02.00,CN-Main,,0,0,0,,{text}\n"
    ).encode("utf-8")


def probe_payload(*, extra_audio: bool = False, embedded: str | None = None) -> dict[str, object]:
    streams: list[dict[str, object]] = [
        {"index": 0, "codec_type": "video", "codec_name": "av1", "width": 1920, "height": 1080},
        {"index": 1, "codec_type": "audio", "codec_name": "opus", "tags": {"language": "jpn"}},
    ]
    if extra_audio:
        streams.append({"index": 2, "codec_type": "audio", "codec_name": "aac", "tags": {"language": "ja"}})
    if embedded == "unknown":
        streams.append({"index": 3, "codec_type": "subtitle", "codec_name": "subrip", "tags": {"title": "Signs"}})
    elif embedded:
        streams.append({"index": 3, "codec_type": "subtitle", "codec_name": "ass", "tags": {"language": embedded}})
    return {"format": {"duration": "1440.125", "format_name": "matroska"}, "streams": streams}


def make_materials(
    root: Path, *, movie: bool = False, ass: bool = False, video_name: str | None = None,
    extra_audio: bool = False, embedded: str | None = None,
) -> tuple[Path, Path, Path]:
    video = root / (video_name or ("movie-source.mkv" if movie else "episode-S01E01.mkv"))
    subtitle = root / ("movie.zh-Hans.ass" if ass else "episode-S01E01.zh-Hans.srt")
    video.parent.mkdir(parents=True, exist_ok=True)
    video.write_bytes(("video:" + str(video)).encode("utf-8"))
    if ass:
        subtitle.parent.mkdir(parents=True, exist_ok=True)
        subtitle.write_bytes(baseline_ass_bytes())
    else:
        write_srt(subtitle, "<i>测试</i><br>下一行")
    cache = root / "probe-cache.json"
    cache.write_text(
        json.dumps({str(video.resolve()): probe_payload(extra_audio=extra_audio, embedded=embedded)}, ensure_ascii=False),
        encoding="utf-8",
    )
    return video, subtitle, cache


def inventory(
    root: Path, video: Path, subtitle: Path, cache: Path, *, project_type: str = "tv",
    extra: list[str] | None = None,
) -> tuple[Path, dict[str, object]]:
    output = root / "intake.json"
    args = [
        "--target-video", str(video), "--candidate-baseline", str(subtitle),
        "--source-language", "ja", "--project-type", project_type,
        "--probe-cache", str(cache), "--output", str(output),
    ]
    if extra:
        args.extend(extra)
    run("inventory_sources.py", *args)
    return output, json.loads(output.read_text(encoding="utf-8"))


def make_repository(root: Path) -> tuple[Path, Path]:
    repository = root / "repository"
    series = repository / "works" / "test-series"
    series.mkdir(parents=True)
    (series / "series-guide.md").write_text("# Test series\n", encoding="utf-8")
    (repository / "catalog.yaml").write_text("schema_version: 3\n\nworks:\n", encoding="utf-8")
    return repository, series


def write_snapshot(root: Path, *, subject_id: int = 100, project_type: str = "tv", total: int = 1) -> Path:
    snapshot = root / f"bangumi-{subject_id}.json"
    platform = {"tv": "TV", "movie": "Movie", "ova": "OVA", "ona": "Web", "special": "Special"}[project_type]
    snapshot.write_text(
        json.dumps({
            "id": subject_id, "name": "テスト作品", "name_cn": "测试作品", "date": "2026-01-01",
            "platform": platform, "total_episodes": total,
        }, ensure_ascii=False), encoding="utf-8",
    )
    return snapshot


def write_episode_map(path: Path, rows: list[tuple[str, Path, Path, int, str]]) -> Path:
    lines = ["episode\tvideo\tsubtitle\taudio_stream\taudio_language"]
    lines.extend(f"{episode}\t{video}\t{subtitle}\t{audio}\t{language}" for episode, video, subtitle, audio, language in rows)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def init_arguments(
    repository: Path, series: Path, snapshot: Path, intake_path: Path, episode_map: Path, *,
    project_name: str = "test-tv", project_type: str = "tv", work_id: str | None = None,
    subject_id: str = "100", secondary: str | None = None,
) -> list[str]:
    args = [
        "--series-dir", str(series), "--repository-root", str(repository),
        "--project-name", project_name, "--project-name-approved-by", "test-owner",
        "--type", project_type, "--bangumi-id", subject_id, "--bangumi-snapshot", str(snapshot),
        "--scope-approved-by", "test-owner", "--intake", str(intake_path),
        "--intake-approved-by", "test-owner", "--episode-map", str(episode_map),
    ]
    if work_id:
        args.extend(["--work-id", work_id])
    if secondary:
        args.extend(["--secondary-language", secondary])
    return args


def initialize_project(
    root: Path, *, movie: bool = False, ass: bool = False, video_name: str | None = None,
    secondary: str | None = None,
) -> tuple[Path, Path, Path, Path, list[str]]:
    repository, series = make_repository(root)
    project_type = "movie" if movie else "tv"
    video, subtitle, cache = make_materials(root / "materials", movie=movie, ass=ass, video_name=video_name)
    intake_path, _ = inventory(root, video, subtitle, cache, project_type=project_type)
    episode = "MOVIE" if movie else "S01E01"
    episode_map = write_episode_map(root / "episode-map.tsv", [(episode, video, subtitle, 1, "ja")])
    snapshot = write_snapshot(root, project_type=project_type)
    project_name = "test-movie" if movie else "test-tv"
    args = init_arguments(
        repository, series, snapshot, intake_path, episode_map, project_name=project_name,
        project_type=project_type, secondary=secondary,
    )
    return repository, series, video, subtitle, args


def release_ass(subject_id: int, title: str, episode: str, version: str = "1.0.0") -> str:
    return (
        "[Script Info]\n" f"; Subtitle-Hub-Version: {version}\n"
        "; Subtitle-Hub-Languages: zh-Hans\n; Subtitle-Hub-Primary-Language: zh-Hans\n"
        f"Title: bgm{subject_id} - {title} - {episode}\n"
        "ScriptType: v4.00+\nWrapStyle: 0\nScaledBorderAndShadow: yes\n"
        "PlayResX: 1920\nPlayResY: 1080\nYCbCr Matrix: TV.709\n\n[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
        "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding\n"
        "Style: CN-Main,Noto Sans CJK SC,62,&H00FFFFFF,&H000000FF,&H00101010,&H80000000,0,0,0,0,"
        "100,100,0,0,1,3,1,2,90,90,54,1\n\n[Events]\n"
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
        "Dialogue: 0,0:00:01.00,0:00:02.00,CN-Main,,0,0,0,,测试\n"
    )


class SkillStructureTests(unittest.TestCase):
    def test_skill_frontmatter_contract(self) -> None:
        text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        frontmatter = text.split("---\n", 2)[1]
        top_level = {
            match.group(1)
            for match in re.finditer(r"(?m)^([a-z][a-z0-9-]*):(?:\s|$)", frontmatter)
        }
        self.assertEqual(top_level, {"name", "description", "metadata"})
        self.assertRegex(frontmatter, r"(?m)^name: subtitle-hub$")
        self.assertRegex(frontmatter, r'(?m)^  version: "1\.0\.0"$')
        self.assertNotIn("[TODO:", text)

    def test_skill_local_markdown_links_resolve(self) -> None:
        missing = []
        for markdown in [SKILL_ROOT / "SKILL.md", *sorted((SKILL_ROOT / "references").glob("*.md"))]:
            for raw in re.findall(r"\[[^\]]+\]\(([^)]+)\)", markdown.read_text(encoding="utf-8")):
                target = raw.split("#", 1)[0]
                if target and "://" not in target and not target.startswith("#"):
                    if not (markdown.parent / target).resolve().exists():
                        missing.append(f"{markdown.relative_to(SKILL_ROOT)} -> {raw}")
        self.assertEqual(missing, [])

    def test_rule_ids_are_unique_and_project_refs_resolve(self) -> None:
        rule_sources: dict[str, str] = {}
        duplicates = []
        for markdown in [SKILL_ROOT / "SKILL.md", *sorted((SKILL_ROOT / "references").glob("*.md"))]:
            for rule_id in re.findall(r"(?m)^#{2,4}\s+(SH-[A-Z]+-\d{3})\b", markdown.read_text(encoding="utf-8")):
                if rule_id in rule_sources:
                    duplicates.append(f"{rule_id}: {rule_sources[rule_id]} and {markdown.name}")
                rule_sources[rule_id] = markdown.name
        self.assertEqual(duplicates, [])
        unresolved = []
        for guide in (REPOSITORY_ROOT / "works").glob("**/docs/project-guide.md"):
            for rule_id in re.findall(r"`(SH-[A-Z]+-\d{3})`", guide.read_text(encoding="utf-8")):
                if rule_id not in rule_sources:
                    unresolved.append(f"{guide.relative_to(REPOSITORY_ROOT)}: {rule_id}")
        self.assertEqual(unresolved, [])

    def test_no_parallel_root_docs_standard_remains(self) -> None:
        old_docs = REPOSITORY_ROOT / "docs"
        remaining = sorted(path for path in old_docs.rglob("*") if path.is_file()) if old_docs.exists() else []
        self.assertEqual(remaining, [])

    def test_active_repository_markdown_links_resolve(self) -> None:
        markdown_files = [REPOSITORY_ROOT / "README.md", REPOSITORY_ROOT / "CATALOG.md", REPOSITORY_ROOT / "AGENTS.md",
                          *sorted((REPOSITORY_ROOT / "works").glob("**/*.md"))]
        missing = []
        for markdown in markdown_files:
            if "project/archive" in markdown.as_posix() or not markdown.is_file():
                continue
            for raw in re.findall(r"\[[^\]]+\]\(([^)]+)\)", markdown.read_text(encoding="utf-8")):
                target = raw.split("#", 1)[0]
                if target and "://" not in target and not target.startswith("#"):
                    if not (markdown.parent / target).resolve().exists():
                        missing.append(f"{markdown.relative_to(REPOSITORY_ROOT)} -> {raw}")
        self.assertEqual(missing, [])


class InventoryTests(unittest.TestCase):
    def test_binary_subtitle_cannot_be_the_chinese_working_baseline(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            video, _, cache = make_materials(root)
            baseline = root / "baseline.sup"
            baseline.write_bytes(b"pgs")
            result = run(
                "inventory_sources.py", "--target-video", str(video),
                "--candidate-baseline", str(baseline), "--source-language", "ja",
                "--project-type", "tv", "--probe-cache", str(cache), expect=2,
            )
            self.assertIn("no supported", result.stderr)

    def test_probe_cache_reports_tracks_roles_and_layered_readiness(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            video, subtitle, cache = make_materials(root, embedded="en")
            _, data = inventory(root, video, subtitle, cache)
            self.assertEqual(data["schema_version"], 2)
            self.assertEqual(data["readiness"]["timing"], "ready")
            self.assertEqual(data["readiness"]["language"], "limited")
            self.assertEqual(data["readiness"]["visual"], "limited")
            self.assertEqual(data["blocking_questions"], [])
            track = data["embedded_subtitle_tracks"][0]
            self.assertEqual(track["language"], "en")
            self.assertIn("timing-reference", track["roles"])
            self.assertIn("translation-reference", track["roles"])
            self.assertNotIn("source-text-reference", track["roles"])

    def test_source_text_and_local_rendering_unlock_dimensions(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            video, subtitle, cache = make_materials(root)
            source = root / "episode.ja.srt"
            write_srt(source, "テストです")
            _, data = inventory(root, video, subtitle, cache, extra=[
                "--optional-source", f"{source}|ja|source-text-reference,timing-reference",
                "--renderer-ready", "--fonts-ready",
            ])
            self.assertEqual(data["readiness"]["language"], "ready")
            self.assertEqual(data["readiness"]["visual"], "ready")

    def test_unreadable_probe_blocks_timing(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            video, subtitle, _ = make_materials(root)
            result = run(
                "inventory_sources.py", "--target-video", str(video), "--candidate-baseline", str(subtitle),
                "--source-language", "ja", "--project-type", "tv", "--ffprobe", str(root / "missing-ffprobe"),
            )
            data = json.loads(result.stdout)
            self.assertEqual(data["readiness"]["timing"], "blocked")
            self.assertTrue(data["blocking_questions"])

    def test_multiple_source_audio_tracks_require_and_accept_selection(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            video, subtitle, cache = make_materials(root, extra_audio=True)
            _, blocked = inventory(root, video, subtitle, cache)
            self.assertEqual(blocked["readiness"]["timing"], "blocked")
            self.assertTrue(any("audio stream" in item for item in blocked["blocking_questions"]))
            _, ready = inventory(root, video, subtitle, cache, extra=["--audio-stream", f"{video}|2"])
            self.assertEqual(ready["readiness"]["timing"], "ready")
            self.assertEqual(ready["target_videos"][0]["suggested_audio_stream"], 2)

    def test_unknown_embedded_language_is_blocking_until_overridden(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            video, subtitle, cache = make_materials(root, embedded="unknown")
            _, blocked = inventory(root, video, subtitle, cache)
            self.assertTrue(any("embedded subtitle" in item for item in blocked["blocking_questions"]))
            _, ready = inventory(root, video, subtitle, cache, extra=["--track-language", f"{video}|3|en"])
            self.assertEqual(ready["blocking_questions"], [])
            self.assertEqual(ready["embedded_subtitle_tracks"][0]["language"], "en")

    def test_filename_language_detection_rejects_arbitrary_bcp47_like_token(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            video, subtitle, cache = make_materials(root)
            optional = root / "car.ass"
            optional.write_bytes(baseline_ass_bytes("123"))
            _, data = inventory(root, video, subtitle, cache, extra=["--optional-source", str(optional)])
            self.assertIsNone(data["external_source_groups"][-1]["language"])
            self.assertTrue(any("optional source" in item for item in data["blocking_questions"]))


class InitializationTests(unittest.TestCase):
    def test_dry_run_rejects_unparseable_chinese_baseline(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            repository, series = make_repository(root)
            video, subtitle, cache = make_materials(root / "materials")
            subtitle.write_text("not a subtitle\n", encoding="utf-8")
            intake_path, _ = inventory(root, video, subtitle, cache)
            episode_map = write_episode_map(root / "map.tsv", [("S01E01", video, subtitle, 1, "ja")])
            args = init_arguments(repository, series, write_snapshot(root), intake_path, episode_map)
            self.assertIn("no parseable dialogue cues", run("init_project.py", *args, "--dry-run", expect=2).stderr)

    def test_existing_series_requires_its_single_series_guide(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _, series, _, _, args = initialize_project(root)
            (series / "series-guide.md").unlink()
            self.assertIn("lacks series-guide.md", run("init_project.py", *args, expect=2).stderr)

    def test_tv_dry_run_initialization_and_ready_validation(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _, series, _, _, args = initialize_project(root)
            dry = run("init_project.py", *args, "--dry-run")
            self.assertIn('"project_name": "test-tv"', dry.stdout)
            self.assertFalse((series / "SH0001--test-tv").exists())
            run("init_project.py", *args)
            project = series / "SH0001--test-tv"
            result = run("validate_project.py", str(project), "--ready-for-proofreading", "--json")
            self.assertTrue(json.loads(result.stdout)["valid"])
            metadata = (project / "project.yaml").read_text(encoding="utf-8")
            self.assertNotIn(str(root), metadata)
            self.assertIn('project_name: "test-tv"', metadata)
            self.assertIn('intake_approved_by: "test-owner"', metadata)
            self.assertFalse((project / "subtitles" / "current").exists())
            for obsolete in ("progress.yaml", "issues.tsv", "change-log.tsv", "README.md"):
                self.assertFalse((project / "docs" / obsolete).exists())
            self.assertTrue((project / "README.md").is_file())

    def test_movie_uses_movie_episode_id(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _, series, _, _, args = initialize_project(root, movie=True)
            run("init_project.py", *args)
            project = series / "SH0001--test-movie"
            self.assertIn('MOVIE: "movie-source.mkv"', (project / "project.yaml").read_text(encoding="utf-8"))
            run("validate_project.py", str(project), "--ready-for-proofreading")

    def test_srt_conversion_uses_noto_fallback_and_preserves_markup(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _, series, _, _, args = initialize_project(root)
            run("init_project.py", *args)
            master = (series / "SH0001--test-tv" / "project/workspace/episodes/S01E01/master.ass").read_text(encoding="utf-8")
            self.assertIn("Noto Sans CJK SC", master)
            self.assertIn(r"{\i1}测试{\i0}\N下一行", master)

    def test_ass_baseline_master_is_byte_preserving(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _, series, _, subtitle, args = initialize_project(root, ass=True)
            original = subtitle.read_bytes()
            run("init_project.py", *args)
            master = series / "SH0001--test-tv/project/workspace/episodes/S01E01/master.ass"
            self.assertEqual(master.read_bytes(), original)

    def test_project_name_approval_is_mandatory(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _, _, _, _, args = initialize_project(root)
            position = args.index("--project-name-approved-by")
            del args[position:position + 2]
            self.assertIn("--project-name-approved-by", run("init_project.py", *args, expect=2).stderr)

    def test_unresolved_intake_cannot_initialize(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            repository, series = make_repository(root)
            video, subtitle, cache = make_materials(root / "materials", embedded="unknown")
            intake_path, _ = inventory(root, video, subtitle, cache)
            episode_map = write_episode_map(root / "map.tsv", [("S01E01", video, subtitle, 1, "ja")])
            args = init_arguments(repository, series, write_snapshot(root), intake_path, episode_map)
            self.assertIn("blocking questions", run("init_project.py", *args, expect=2).stderr)

    def test_unsafe_episode_id_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            repository, series, video, subtitle, args = initialize_project(root)
            episode_map = write_episode_map(root / "unsafe.tsv", [("../../escape", video, subtitle, 1, "ja")])
            args[args.index("--episode-map") + 1] = str(episode_map)
            self.assertIn("unsafe or invalid", run("init_project.py", *args, expect=2).stderr)
            self.assertFalse((repository.parent / "escape").exists())
            self.assertFalse((series / "SH0001--test-tv").exists())

    def test_duplicate_release_stems_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            repository, series = make_repository(root)
            video1, video2 = root / "a/same.mkv", root / "b/same.mkv"
            for video in (video1, video2):
                video.parent.mkdir(parents=True)
                video.write_bytes(str(video).encode("utf-8"))
            subtitles = root / "baselines"
            sub1, sub2 = subtitles / "S01E01.zh-Hans.srt", subtitles / "S01E02.zh-Hans.srt"
            write_srt(sub1)
            write_srt(sub2)
            cache = root / "cache.json"
            cache.write_text(json.dumps({str(video1.resolve()): probe_payload(), str(video2.resolve()): probe_payload()}), encoding="utf-8")
            intake_path = root / "intake.json"
            run("inventory_sources.py", "--target-video", str(video1), "--target-video", str(video2),
                "--candidate-baseline", str(subtitles), "--source-language", "ja", "--project-type", "tv",
                "--probe-cache", str(cache), "--output", str(intake_path))
            episode_map = write_episode_map(root / "map.tsv", [
                ("S01E01", video1, sub1, 1, "ja"), ("S01E02", video2, sub2, 1, "ja")])
            args = init_arguments(repository, series, write_snapshot(root, total=2), intake_path, episode_map)
            self.assertIn("duplicate release filename", run("init_project.py", *args, expect=2).stderr)

    def test_duplicate_work_and_bangumi_ids_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _, series, _, _, args = initialize_project(root)
            run("init_project.py", *args)
            duplicate_work = [*args, "--work-id", "SH0001"]
            duplicate_work[duplicate_work.index("--project-name") + 1] = "another-project"
            self.assertIn("work ID already exists", run("init_project.py", *duplicate_work, expect=2).stderr)
            duplicate_subject = [*args, "--work-id", "SH0002"]
            duplicate_subject[duplicate_subject.index("--project-name") + 1] = "another-project"
            self.assertIn("Bangumi subject already exists", run("init_project.py", *duplicate_subject, expect=2).stderr)
            self.assertEqual(len(list(series.glob("SH*"))), 1)

    def test_new_series_is_rolled_back_after_late_source_collision(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            repository = root / "repository"
            (repository / "works").mkdir(parents=True)
            (repository / "catalog.yaml").write_text("schema_version: 3\nworks:\n", encoding="utf-8")
            video, _, cache = make_materials(root / "materials")
            baseline_root = root / "duplicate-baselines"
            sub1, sub2 = baseline_root / "a/same.srt", baseline_root / "b/same.srt"
            write_srt(sub1)
            write_srt(sub2, "另一条")
            intake_path = root / "intake.json"
            run("inventory_sources.py", "--target-video", str(video), "--candidate-baseline", str(baseline_root),
                "--source-language", "ja", "--project-type", "tv", "--probe-cache", str(cache), "--output", str(intake_path))
            episode_map = write_episode_map(root / "map.tsv", [("S01E01", video, sub1, 1, "ja")])
            new_series = repository / "works/new-series"
            args = init_arguments(repository, new_series, write_snapshot(root), intake_path, episode_map)
            args.extend(["--create-series", "--series-title", "新系列", "--series-name-approved-by", "test-owner"])
            result = run("init_project.py", *args, expect=1)
            self.assertIn("duplicate source basename", result.stderr)
            self.assertFalse(new_series.exists())

    def test_ready_gate_detects_missing_local_video(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _, series, video, _, args = initialize_project(root)
            run("init_project.py", *args)
            project = series / "SH0001--test-tv"
            video.unlink()
            result = run("validate_project.py", str(project), "--ready-for-proofreading", "--json", expect=1)
            self.assertIn("not readable", "\n".join(json.loads(result.stdout)["errors"]))


class CatalogAndPackagingTests(unittest.TestCase):
    def test_catalog_contains_only_released_projects(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            repository, series, _, _, args = initialize_project(root)
            run("init_project.py", *args)
            run("sync_catalog.py", "--repository-root", str(repository))
            self.assertNotIn("SH0001", (repository / "catalog.yaml").read_text(encoding="utf-8"))
            current = series / "SH0001--test-tv/subtitles/current"
            current.mkdir(parents=True)
            (current / "VERSION").write_text("1.0.0\n", encoding="utf-8")
            (current / "placeholder.zh-Hans.ass").write_text("placeholder\n", encoding="utf-8")
            run("sync_catalog.py", "--repository-root", str(repository), "--check", expect=1)
            run("sync_catalog.py", "--repository-root", str(repository))
            run("sync_catalog.py", "--repository-root", str(repository), "--check")
            self.assertIn("SH0001", (repository / "catalog.yaml").read_text(encoding="utf-8"))

    def test_package_builder_maps_video_stem_without_episode_token(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            repository, series, _, _, args = initialize_project(root, video_name="custom-cut-name.mkv")
            run("init_project.py", *args)
            current = series / "SH0001--test-tv/subtitles/current"
            current.mkdir(parents=True)
            (current / "VERSION").write_text("1.0.0\n", encoding="utf-8")
            (current / "custom-cut-name.zh-Hans.ass").write_text(
                release_ass(100, "测试作品", "S01E01"), encoding="utf-8", newline="\n")
            self.assertIn("valid", run_path(PACKAGE_SCRIPT, "--repository-root", str(repository), "--check").stdout)
            run_path(PACKAGE_SCRIPT, "--repository-root", str(repository))
            packages = list((repository / "packages").glob("*.zip"))
            self.assertEqual(len(packages), 1)
            self.assertIn("bgm100 - 测试作品 [v1.0.0]", packages[0].name)


if __name__ == "__main__":
    unittest.main()
