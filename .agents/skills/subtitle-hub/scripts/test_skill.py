#!/usr/bin/env python3
"""Isolated behavioral tests for the Subtitle Hub Skill 1.4.0 toolchain."""

from __future__ import annotations

import json
import hashlib
import os
import re
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import unquote, urlparse

SCRIPT_ROOT = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_ROOT.parent
REPOSITORY_ROOT = SKILL_ROOT.parents[2]
PACKAGE_SCRIPT = REPOSITORY_ROOT / ".github" / "scripts" / "build_subtitle_packages.py"
CATALOG_SCRIPT = REPOSITORY_ROOT / ".github" / "scripts" / "sync_catalog.py"
NORMALIZE_SCRIPT = REPOSITORY_ROOT / ".github" / "scripts" / "normalize_ass_release.py"
TEST_REPOSITORY_SLUG = "example/repo"
sys.path.insert(0, str(PACKAGE_SCRIPT.parent))
sys.path.insert(0, str(SCRIPT_ROOT))
from build_subtitle_packages import (  # noqa: E402
    PackageError,
    is_high_confidence_credit_fragment,
    validated_source_credit_parts,
)
from normalize_ass_release import (  # noqa: E402
    SC_FONT,
    JP_FONT,
    NormalizeError,
    assert_rendered_regression,
    ass_section,
    font_targets_by_style,
    normalize_inline_fonts,
    normalize_source_metadata,
    normalize_styles,
)
import sync_bangumi_metadata  # noqa: E402
import remote_media  # noqa: E402


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
    (repository / "catalog.yaml").write_text("schema_version: 6\n\nworks:\n", encoding="utf-8")
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


def approve_intake(
    path: Path, episode: str, subtitle: Path, *, video: Path | str | None = None,
    audio: int | None = None, language: str | None = None,
    target_basename: str | None = None, timing_authority: str = "Chinese baseline",
) -> Path:
    data = json.loads(path.read_text(encoding="utf-8"))
    data["blocking_questions"] = []
    data["episode_map"] = [{
        "episode": episode, "video_id": "video-001" if video else None,
        "video": str(video.resolve()) if isinstance(video, Path) else video,
        "target_basename": target_basename or (
            video.name if isinstance(video, Path) else Path(unquote(urlparse(video).path)).name if video else f"{episode}.mkv"
        ),
        "baseline_file_id": data["external_source_groups"][0]["files"][0]["id"],
        "subtitle": str(subtitle.resolve()), "audio_stream": audio,
        "audio_language": language, "timing_authority": timing_authority,
    }]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def init_arguments(
    repository: Path, series: Path, snapshot: Path, intake_path: Path, *,
    project_name: str = "test-tv", project_type: str = "tv", work_id: str | None = None,
    subject_id: str = "100", secondary: str | None = None,
) -> list[str]:
    args = [
        "--series-dir", str(series), "--repository-root", str(repository),
        "--project-name", project_name, "--approved-by", "test-owner",
        "--type", project_type, "--bangumi-id", subject_id, "--bangumi-snapshot", str(snapshot),
        "--intake", str(intake_path),
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
    approve_intake(intake_path, episode, subtitle, video=video, audio=1, language="ja")
    snapshot = write_snapshot(root, project_type=project_type)
    project_name = "test-movie" if movie else "test-tv"
    args = init_arguments(
        repository, series, snapshot, intake_path, project_name=project_name,
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


def mark_review_release_ready(project: Path) -> None:
    path = project / "review.md"
    text = path.read_text(encoding="utf-8")
    replacements = {
        "status: planning": "status: released",
        "  evidence_tier: null": "  evidence_tier: D",
        "  master_sha256: {}": "  master_sha256:\n    S01E01: " + hashlib.sha256((project / "project/workspace/episodes/S01E01/master.ass").read_bytes()).hexdigest(),
        "  chinese_in_scope: 0": "  chinese_in_scope: 1",
        "  chinese_reviewed: 0": "  chinese_reviewed: 1",
        "  static_layout_checked: 0": "  static_layout_checked: 1",
        "  human_source_fidelity_review: not-required": "  human_source_fidelity_review: verified",
        "  human_release_review: pending": "  human_release_review: verified",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")


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
        self.assertRegex(frontmatter, r'(?m)^  version: "1\.4\.0"$')
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

    def test_skill_has_four_routed_references_and_one_style_basis(self) -> None:
        references = {path.name for path in (SKILL_ROOT / "references").glob("*.md")}
        self.assertEqual(references, {
            "project-initialization.md", "proofreading-and-approval.md",
            "timing-style-and-qc.md", "release-and-workspace.md",
        })
        style = (SKILL_ROOT / "references" / "timing-style-and-qc.md").read_text(encoding="utf-8")
        self.assertIn("Netflix", style)
        self.assertIn("Subtitle Hub engineering adaptations", style)
        for unrelated in ("BBC", "DCMP", "EBU"):
            self.assertNotIn(unrelated, style)

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
        for metadata in (REPOSITORY_ROOT / "works").glob("**/project.yaml"):
            for rule_id in re.findall(r"(?:global_ref:\s*|`)(SH-[A-Z]+-\d{3})", metadata.read_text(encoding="utf-8")):
                if rule_id not in rule_sources:
                    unresolved.append(f"{metadata.relative_to(REPOSITORY_ROOT)}: {rule_id}")
        self.assertEqual(unresolved, [])

    def test_no_parallel_root_docs_standard_remains(self) -> None:
        old_docs = REPOSITORY_ROOT / "docs"
        remaining = sorted(path for path in old_docs.rglob("*") if path.is_file()) if old_docs.exists() else []
        self.assertEqual(remaining, [])

    def test_projects_use_two_file_control_plane(self) -> None:
        for metadata in (REPOSITORY_ROOT / "works").glob("**/project.yaml"):
            project = metadata.parent
            self.assertTrue((project / "review.md").is_file())
            self.assertFalse((project / "README.md").exists())
            self.assertFalse((project / "docs").exists())
            text = metadata.read_text(encoding="utf-8")
            schema = re.search(r"(?m)^schema_version: (\d+)$", text)
            self.assertIsNotNone(schema)
            self.assertIn("subtitle_design:", text)
            if schema.group(1) == "9":
                self.assertIn("release_languages:", text)
                self.assertNotIn("  review: review.md", text)
            else:
                result = run("validate_project.py", str(project), "--json", expect=1)
                self.assertIn("upgrade required before processing", result.stdout)

    def test_active_repository_markdown_links_resolve(self) -> None:
        markdown_files = [REPOSITORY_ROOT / "README.md", REPOSITORY_ROOT / "CATALOG.md", REPOSITORY_ROOT / "AGENTS.md",
                          *sorted((REPOSITORY_ROOT / "works").glob("**/*.md"))]
        missing = []
        for markdown in markdown_files:
            if not markdown.is_file():
                continue
            for raw in re.findall(r"\[[^\]]+\]\(([^)]+)\)", markdown.read_text(encoding="utf-8")):
                target = raw.split("#", 1)[0]
                if target and "://" not in target and not target.startswith("#"):
                    if not (markdown.parent / target).resolve().exists():
                        missing.append(f"{markdown.relative_to(REPOSITORY_ROOT)} -> {raw}")
        self.assertEqual(missing, [])


class RemoteMediaTests(unittest.TestCase):
    def connection(self, **values: object) -> SimpleNamespace:
        defaults = {
            "ssh": "ssh", "host": "10.9.6.2", "port": 22, "user": "media_reader",
            "connect_timeout": 10, "client_timeout": 75, "action": "probe",
        }
        defaults.update(values)
        return SimpleNamespace(**defaults)

    def test_probe_uses_strict_password_ssh_and_returns_password_free_locators(self) -> None:
        payload = json.dumps(probe_payload(), ensure_ascii=False)
        stdout = (
            f"{remote_media.MARKER.format(1)}\n123456\n{'a' * 64}\n{payload}\n"
            f"{remote_media.MARKER.format(2)}\n234567\n{'b' * 64}\n{payload}\n"
        ).encode()
        args = self.connection(path=["/srv/media/O'Brien 作品 S01E01.mkv", "/srv/media/作品 S01E02.mkv"])
        with mock.patch.object(remote_media.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, stdout)) as runner:
            remote_media.validate_connection(args)
            result = remote_media.probe(args)
        command = runner.call_args.args[0]
        self.assertIn("ClearAllForwardings=yes", command)
        self.assertIn("PermitLocalCommand=no", command)
        self.assertIn("PreferredAuthentications=password,keyboard-interactive", command)
        self.assertIn("PubkeyAuthentication=no", command)
        self.assertIn("StrictHostKeyChecking=ask", command)
        self.assertNotIn("example-secret", " ".join(command))
        remote_command = command[-1]
        for forbidden in ("sudo ", "apt ", "docker ", "mktemp", "touch "):
            self.assertNotIn(forbidden, remote_command)
        self.assertIn("'\"'\"'", remote_command)
        self.assertEqual(runner.call_count, 1)
        self.assertEqual(len(result["media"]), 2)
        media = result["media"][0]
        self.assertEqual(media["size"], 123456)
        self.assertEqual(media["basename"], "O'Brien 作品 S01E01.mkv")
        self.assertTrue(media["path"].startswith("ssh://media_reader@10.9.6.2:22/"))
        self.assertNotIn("password", json.dumps(result).lower())

    def test_remote_paths_and_local_outputs_are_bounded(self) -> None:
        for unsafe in ("relative.mkv", "/srv/../etc/passwd", "/srv/bad\nname.mkv"):
            with self.assertRaises(remote_media.RemoteMediaError):
                remote_media.remote_path(unsafe)
        with self.assertRaises(remote_media.RemoteMediaError):
            remote_media.validate_connection(self.connection(host="10.9.6.2;id"))
        frame_command = remote_media.ssh_command(self.connection(action="frame"), "fixed")
        self.assertIn("StrictHostKeyChecking=yes", frame_command)
        with tempfile.TemporaryDirectory() as raw:
            output = Path(raw) / "frame.jpg"
            args = self.connection(path="/srv/media/episode.mkv", output=str(output))
            with mock.patch.object(remote_media, "run_ssh", return_value=b"jpeg"):
                result = remote_media.write_remote_output(args, "frame", "fixed read-only command", ".jpg")
            self.assertEqual(output.read_bytes(), b"jpeg")
            self.assertEqual(result["bytes"], 4)
        outside = self.connection(path="/srv/media/episode.mkv", output=str(REPOSITORY_ROOT / "frame.jpg"))
        with self.assertRaises(remote_media.RemoteMediaError):
            remote_media.write_remote_output(outside, "frame", "fixed read-only command", ".jpg")


class InventoryTests(unittest.TestCase):
    def test_text_only_inventory_is_tier_b_with_source_text_and_never_calls_ffprobe(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            baseline = root / "episode.S01E01.zh.srt"
            source = root / "episode.S01E01.ja.srt"
            write_srt(baseline, "测试")
            write_srt(source, "テスト")
            result = run(
                "inventory_sources.py", "--candidate-baseline", str(baseline),
                "--optional-source", f"{source}|ja|source-text-reference",
                "--source-language", "ja", "--project-type", "tv",
                "--ffprobe", str(root / "must-not-run"),
            )
            data = json.loads(result.stdout)
            self.assertEqual(data["evidence_tier"], "B")
            self.assertEqual(data["target_videos"], [])
            self.assertNotIn("readiness", data)
            self.assertTrue(any("video not provided" in item for item in data["limitations"]))
            self.assertEqual(data["blocking_questions"], [])

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

    def test_probe_cache_reports_tracks_roles_without_parallel_readiness(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            video, subtitle, cache = make_materials(root, embedded="en")
            _, data = inventory(root, video, subtitle, cache)
            self.assertEqual(data["schema_version"], 4)
            self.assertEqual(data["skill_version"], "1.4.0")
            self.assertNotIn("readiness", data)
            self.assertEqual(data["blocking_questions"], [])
            self.assertEqual(data["external_source_groups"][0]["roles"], ["candidate-baseline"])
            track = data["embedded_subtitle_tracks"][0]
            self.assertEqual(track["language"], "en")
            self.assertIn("timing-reference", track["roles"])
            self.assertIn("translation-reference", track["roles"])
            self.assertNotIn("source-text-reference", track["roles"])

    def test_ssh_probe_inventory_guides_initialization_without_copying_video(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            repository, series = make_repository(root)
            baseline = root / "Target.S01E01.zh-Hans.srt"
            write_srt(baseline)
            locator = "ssh://media_reader@10.9.6.2:22/srv/media/Target.S01E01.mkv"
            remote_probe = root / "remote-probe.json"
            remote_probe.write_text(json.dumps({
                "schema_version": 1,
                "action": "probe",
                "connection": {"host": "10.9.6.2", "port": 22, "user": "media_reader"},
                "media": [{
                    "access": "ssh", "path": locator, "remote_path": "/srv/media/Target.S01E01.mkv",
                    "basename": "Target.S01E01.mkv", "size": 123456,
                    "sha256_first_mib": "a" * 64, "probe": probe_payload(),
                }],
            }, ensure_ascii=False), encoding="utf-8")
            intake = root / "intake.json"
            run(
                "inventory_sources.py", "--ssh-video-probe", str(remote_probe),
                "--candidate-baseline", str(baseline), "--source-language", "ja",
                "--project-type", "tv", "--output", str(intake),
            )
            data = json.loads(intake.read_text(encoding="utf-8"))
            self.assertEqual(data["target_videos"][0]["access"], "ssh")
            self.assertEqual(data["target_videos"][0]["path"], locator)
            self.assertEqual(data["blocking_questions"], [])
            approve_intake(intake, "S01E01", baseline, video=locator, audio=1, language="ja")
            run("init_project.py", *init_arguments(repository, series, write_snapshot(root), intake))
            project = series / "SH0001--test-tv"
            local_paths = (project / "project/local.paths.yaml").read_text(encoding="utf-8")
            self.assertIn(locator, local_paths)
            metadata = (project / "project.yaml").read_text(encoding="utf-8")
            self.assertIn("medium: user-provided-ssh-video", metadata)
            self.assertNotIn("/srv/media", metadata)
            run("validate_project.py", str(project), "--ready-for-proofreading")
            unsafe = json.loads(remote_probe.read_text(encoding="utf-8"))
            unsafe["media"][0]["path"] = "ssh://media_reader:secret@10.9.6.2:22/srv/media/Target.S01E01.mkv"
            remote_probe.write_text(json.dumps(unsafe), encoding="utf-8")
            result = run(
                "inventory_sources.py", "--ssh-video-probe", str(remote_probe),
                "--candidate-baseline", str(baseline), "--source-language", "ja",
                "--project-type", "tv", expect=2,
            )
            self.assertIn("locator and connection metadata conflict", result.stderr)

    def test_source_text_sets_tier_without_renderer_or_font_flags(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            video, subtitle, cache = make_materials(root)
            source = root / "episode.ja.srt"
            write_srt(source, "テストです")
            _, data = inventory(root, video, subtitle, cache, extra=[
                "--optional-source", f"{source}|ja|source-text-reference,timing-reference",
            ])
            self.assertEqual(data["evidence_tier"], "B")
            self.assertNotIn("readiness", data)

    def test_unreadable_probe_blocks_timing(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            video, subtitle, _ = make_materials(root)
            result = run(
                "inventory_sources.py", "--target-video", str(video), "--candidate-baseline", str(subtitle),
                "--source-language", "ja", "--project-type", "tv", "--ffprobe", str(root / "missing-ffprobe"),
            )
            data = json.loads(result.stdout)
            self.assertTrue(data["blocking_questions"])

    def test_multiple_source_audio_tracks_require_and_accept_selection(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            video, subtitle, cache = make_materials(root, extra_audio=True)
            _, blocked = inventory(root, video, subtitle, cache)
            self.assertTrue(any("audio stream" in item for item in blocked["blocking_questions"]))
            _, ready = inventory(root, video, subtitle, cache, extra=["--audio-stream", f"{video}|2"])
            self.assertEqual(ready["blocking_questions"], [])
            self.assertEqual(ready["target_videos"][0]["suggested_audio_stream"], 2)

    def test_unknown_embedded_language_is_ignored_until_selected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            video, subtitle, cache = make_materials(root, embedded="unknown")
            _, ignored = inventory(root, video, subtitle, cache)
            self.assertEqual(ignored["blocking_questions"], [])
            self.assertTrue(ignored["embedded_subtitle_tracks"][0]["ignored"])
            _, ready = inventory(root, video, subtitle, cache, extra=["--track-language", f"{video}|3|en"])
            self.assertEqual(ready["blocking_questions"], [])
            self.assertEqual(ready["embedded_subtitle_tracks"][0]["language"], "en")
            self.assertFalse(ready["embedded_subtitle_tracks"][0]["ignored"])

    def test_initializer_rejects_selected_embedded_track_without_language_or_roles(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            repository, series = make_repository(root)
            video, subtitle, cache = make_materials(root / "materials", embedded="unknown")
            intake_path, data = inventory(root, video, subtitle, cache)
            approve_intake(intake_path, "S01E01", subtitle, video=video, audio=1, language="ja")
            data = json.loads(intake_path.read_text(encoding="utf-8"))
            data["embedded_subtitle_tracks"][0]["ignored"] = False
            intake_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            snapshot = write_snapshot(root)
            result = run(
                "init_project.py",
                *init_arguments(repository, series, snapshot, intake_path),
                "--dry-run",
                expect=2,
            )
            self.assertIn("requires confirmed language and roles", result.stderr)

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
    def test_bangumi_sync_compares_remote_total_to_identity_not_project_scope(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            repository, series, video, subtitle, args = initialize_project(root)
            snapshot = write_snapshot(root, total=16)
            position = args.index("--bangumi-snapshot")
            args[position + 1] = str(snapshot)
            run("init_project.py", *args)
            project = series / "SH0001--test-tv"
            payload = {
                "id": 100, "type": 2, "platform": "TV", "total_episodes": 16,
                "name": "テスト作品", "name_cn": "测试作品",
            }
            with mock.patch.object(sync_bangumi_metadata, "fetch_json", return_value=payload):
                self.assertEqual(sync_bangumi_metadata.remote_identity(project), ("テスト作品", "测试作品"))

    def test_text_only_project_uses_target_basename_and_creates_no_local_paths(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            repository, series = make_repository(root)
            baseline = root / "episode.S01E01.zh.srt"
            source = root / "episode.S01E01.ja.srt"
            write_srt(baseline, "测试")
            write_srt(source, "テスト")
            intake = root / "intake.json"
            run(
                "inventory_sources.py", "--candidate-baseline", str(baseline),
                "--optional-source", f"{source}|ja|source-text-reference",
                "--source-language", "ja", "--project-type", "tv", "--output", str(intake),
            )
            approve_intake(intake, "S01E01", baseline, target_basename="Target.S01E01.mkv")
            args = init_arguments(repository, series, write_snapshot(root), intake)
            run("init_project.py", *args)
            project = series / "SH0001--test-tv"
            self.assertFalse((project / "project/local.paths.yaml").exists())
            self.assertIn('S01E01: "Target.S01E01.mkv"', (project / "project.yaml").read_text(encoding="utf-8"))
            run("validate_project.py", str(project), "--ready-for-proofreading")

    def test_dry_run_rejects_unparseable_chinese_baseline(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            repository, series = make_repository(root)
            video, subtitle, cache = make_materials(root / "materials")
            subtitle.write_text("not a subtitle\n", encoding="utf-8")
            intake_path, _ = inventory(root, video, subtitle, cache)
            approve_intake(intake_path, "S01E01", subtitle, video=video, audio=1, language="ja")
            args = init_arguments(repository, series, write_snapshot(root), intake_path)
            self.assertIn("no parseable dialogue cues", run("init_project.py", *args, "--dry-run", expect=2).stderr)

    def test_existing_series_does_not_require_empty_series_guide(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _, series, _, _, args = initialize_project(root)
            (series / "series-guide.md").unlink()
            run("init_project.py", *args, "--dry-run")

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
            self.assertIn('approved_by: "test-owner"', metadata)
            self.assertIn("schema_version: 9", metadata)
            self.assertFalse((project / "subtitles" / "current").exists())
            self.assertTrue((project / "review.md").is_file())
            self.assertFalse((project / "README.md").exists())
            self.assertFalse((project / "docs").exists())
            self.assertFalse((project / "project/archive").exists())
            self.assertFalse((project / "project/workspace/build").exists())
            self.assertFalse((project / "project/workspace/temp").exists())

    def test_movie_uses_movie_episode_id(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _, series, _, _, args = initialize_project(root, movie=True)
            run("init_project.py", *args)
            project = series / "SH0001--test-movie"
            self.assertIn('MOVIE: "movie-source.mkv"', (project / "project.yaml").read_text(encoding="utf-8"))
            run("validate_project.py", str(project), "--ready-for-proofreading")

    def test_srt_conversion_uses_noto_and_preserves_markup(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _, series, _, _, args = initialize_project(root)
            run("init_project.py", *args)
            master = (series / "SH0001--test-tv" / "project/workspace/episodes/S01E01/master.ass").read_text(encoding="utf-8")
            self.assertIn("Noto Sans CJK SC", master)
            self.assertIn(",62,&H00FFFFFF,&H000000FF,&H00101010,&H00000000", master)
            self.assertIn(",2,96,96,70,1", master)
            self.assertIn(r"{\i1}测试{\i0}\N下一行", master)

    def test_ass_baseline_source_is_immutable_and_master_contract_is_prepared(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _, series, _, subtitle, args = initialize_project(root, ass=True)
            original = subtitle.read_bytes()
            run("init_project.py", *args)
            master = series / "SH0001--test-tv/project/workspace/episodes/S01E01/master.ass"
            self.assertEqual(subtitle.read_bytes(), original)
            prepared = master.read_text(encoding="utf-8")
            self.assertIn("WrapStyle:", prepared)
            self.assertIn("Noto Sans CJK SC", prepared)

    def test_project_name_approval_is_mandatory(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _, _, _, _, args = initialize_project(root)
            position = args.index("--approved-by")
            del args[position:position + 2]
            self.assertIn("--approved-by", run("init_project.py", *args, expect=2).stderr)

    def test_unresolved_intake_cannot_initialize(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            repository, series = make_repository(root)
            video, subtitle, cache = make_materials(root / "materials", extra_audio=True)
            intake_path, _ = inventory(root, video, subtitle, cache)
            approve_intake(intake_path, "S01E01", subtitle, video=video, audio=1, language="ja")
            data = json.loads(intake_path.read_text(encoding="utf-8"))
            data["blocking_questions"] = ["select source audio"]
            intake_path.write_text(json.dumps(data), encoding="utf-8")
            args = init_arguments(repository, series, write_snapshot(root), intake_path)
            self.assertIn("blocking questions", run("init_project.py", *args, expect=2).stderr)

    def test_unsafe_episode_id_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            repository, series, video, subtitle, args = initialize_project(root)
            intake_path = Path(args[args.index("--intake") + 1])
            approve_intake(intake_path, "../../escape", subtitle, video=video, audio=1, language="ja")
            self.assertIn("unsafe, missing, or duplicate", run("init_project.py", *args, expect=2).stderr)
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
            data = json.loads(intake_path.read_text(encoding="utf-8"))
            data["blocking_questions"] = []
            data["episode_map"] = [
                {"episode": "S01E01", "video": str(video1.resolve()), "target_basename": "same.mkv", "subtitle": str(sub1.resolve()), "audio_stream": 1, "audio_language": "ja", "timing_authority": "Chinese baseline"},
                {"episode": "S01E02", "video": str(video2.resolve()), "target_basename": "same.mkv", "subtitle": str(sub2.resolve()), "audio_stream": 1, "audio_language": "ja", "timing_authority": "Chinese baseline"},
            ]
            intake_path.write_text(json.dumps(data), encoding="utf-8")
            args = init_arguments(repository, series, write_snapshot(root, total=2), intake_path)
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
            (repository / "catalog.yaml").write_text("schema_version: 6\nworks:\n", encoding="utf-8")
            video, _, cache = make_materials(root / "materials")
            baseline_root = root / "duplicate-baselines"
            sub1, sub2 = baseline_root / "a/same.srt", baseline_root / "b/same.srt"
            write_srt(sub1)
            write_srt(sub2, "另一条")
            intake_path = root / "intake.json"
            run("inventory_sources.py", "--target-video", str(video), "--candidate-baseline", str(baseline_root),
                "--source-language", "ja", "--project-type", "tv", "--probe-cache", str(cache), "--output", str(intake_path))
            approve_intake(intake_path, "S01E01", sub1, video=video, audio=1, language="ja")
            new_series = repository / "works/new-series"
            args = init_arguments(repository, new_series, write_snapshot(root), intake_path)
            args.extend(["--create-series", "--series-title", "新系列"])
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

    def test_existing_project_must_upgrade_skill_contract_before_processing(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _, series, _, _, args = initialize_project(root)
            run("init_project.py", *args)
            project = series / "SH0001--test-tv"
            metadata = project / "project.yaml"
            metadata.write_text(
                metadata.read_text(encoding="utf-8").replace(
                    'skill_version: "1.4.0"', 'skill_version: "1.3.0"'
                ),
                encoding="utf-8",
            )
            result = run("validate_project.py", str(project), "--json", expect=1)
            self.assertIn("upgrade before processing", result.stdout)


class CatalogAndPackagingTests(unittest.TestCase):
    def test_action_catalog_adds_release_and_package_after_package_exists(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            repository, series, _, _, args = initialize_project(root)
            run("init_project.py", *args)
            current = series / "SH0001--test-tv/subtitles/current"
            current.mkdir(parents=True)
            (current / "VERSION").write_text("1.0.0\n", encoding="utf-8")
            (current / "placeholder.zh-Hans.ass").write_text("placeholder\n", encoding="utf-8")
            package = repository / "packages/bgm100 - 测试作品 [v1.0.0].zip"
            package.parent.mkdir()
            package.write_bytes(b"action-output")
            mismatch = run_path(
                CATALOG_SCRIPT, "--repository-root", str(repository),
                "--repository-slug", TEST_REPOSITORY_SLUG,
                "--check-package-links", expect=1,
            )
            self.assertIn("stale package links", mismatch.stderr)
            run_path(CATALOG_SCRIPT, "--repository-root", str(repository), "--repository-slug", TEST_REPOSITORY_SLUG)
            run_path(CATALOG_SCRIPT, "--repository-root", str(repository), "--repository-slug", TEST_REPOSITORY_SLUG, "--check")
            run_path(
                CATALOG_SCRIPT, "--repository-root", str(repository),
                "--repository-slug", TEST_REPOSITORY_SLUG, "--check-package-links"
            )
            catalog = (repository / "catalog.yaml").read_text(encoding="utf-8")
            self.assertIn("SH0001", catalog)
            self.assertIn("packages/bgm100 - 测试作品 [v1.0.0].zip", catalog)
            self.assertIn("schema_version: 6", catalog)
            url_match = re.search(r'package_download_url: "([^"]+)"', catalog)
            self.assertIsNotNone(url_match)
            download_url = url_match.group(1)
            cdn_match = re.search(r'package_cdn_url: "([^"]+)"', catalog)
            self.assertIsNotNone(cdn_match)
            cdn_url = cdn_match.group(1)
            self.assertNotIn(" ", download_url)
            self.assertIn("%E6%B5%8B%E8%AF%95%E4%BD%9C%E5%93%81", download_url)
            self.assertIn("%5Bv1.0.0%5D.zip", download_url)
            self.assertEqual(
                unquote(urlparse(download_url).path.removeprefix("/example/repo/main/")),
                "packages/bgm100 - 测试作品 [v1.0.0].zip",
            )
            self.assertIn("cdn.jsdelivr.net/gh/example/repo@main/", cdn_url)
            markdown = (repository / "CATALOG.md").read_text(encoding="utf-8")
            self.assertIn("| 项目资料 | 字幕成品 |", markdown)
            self.assertIn(f"[原始下载]({download_url})", markdown)
            self.assertIn(f"[CDN 加速]({cdn_url})", markdown)
            self.assertNotIn("[压缩包](packages/", markdown)
            review = series / "SH0001--test-tv/review.md"
            review.write_text(
                review.read_text(encoding="utf-8").replace(
                    "status: planning", "status: final-review"
                ),
                encoding="utf-8",
            )
            run_path(
                CATALOG_SCRIPT, "--repository-root", str(repository),
                "--repository-slug", TEST_REPOSITORY_SLUG, "--check-package-links"
            )

    def test_local_package_builder_is_check_only_and_writes_no_zip(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            repository, series, _, _, args = initialize_project(root, video_name="custom-cut-name.mkv")
            run("init_project.py", *args)
            current = series / "SH0001--test-tv/subtitles/current"
            current.mkdir(parents=True)
            (current / "VERSION").write_text("1.0.0\n", encoding="utf-8")
            (current / "custom-cut-name.zh-Hans.ass").write_text(
                release_ass(100, "测试作品", "S01E01"), encoding="utf-8", newline="\n")
            mark_review_release_ready(series / "SH0001--test-tv")
            checked = run_path(PACKAGE_SCRIPT, "--repository-root", str(repository), "--check")
            self.assertIn("valid", checked.stdout)
            self.assertIn("bgm100 - 测试作品 [v1.0.0].zip", checked.stdout)
            refused = run_path(PACKAGE_SCRIPT, "--repository-root", str(repository), expect=1)
            self.assertIn("local package generation is disabled", refused.stderr)
            action_refused = run_path(
                PACKAGE_SCRIPT, "--repository-root", str(repository), "--action-build", expect=1
            )
            self.assertIn("local package generation is disabled", action_refused.stderr)
            self.assertEqual(list((repository / "packages").glob("*.zip")), [])

    def test_credit_filter_is_conservative_and_preserves_identified_attribution(self) -> None:
        valid = "诸神字幕组；台本整理:散仙 翻译:龟龟之蛋 校对:mam 时间轴:时末"
        self.assertEqual(validated_source_credit_parts(valid), valid.split("；"))
        self.assertTrue(is_high_confidence_credit_fragment("翻译 白楸兔引 Riho；".rstrip("；")))
        for ambiguous in (
            "欢迎访问 example.org", "本字幕仅供学习交流", "中文底稿：old.ass", "可能是某字幕组制作",
        ):
            self.assertFalse(is_high_confidence_credit_fragment(ambiguous))
            with self.assertRaises(PackageError):
                validated_source_credit_parts(ambiguous)

    def test_release_cleanup_harvests_credit_before_removing_all_comments(self) -> None:
        events = (
            "[Events]\n"
            "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
            "Comment: 0,0:00:00.00,0:00:00.01,CN-Main,Source-Metadata,0,0,0,,"
            "[源字幕信息] 本字幕由诸神字幕组（example.org）制作，仅供交流学习\n"
            "Comment: 0,0:00:00.00,0:00:00.01,CN-Main,,0,0,0,template,automation code\n"
            "Dialogue: 0,0:00:01.00,0:00:02.00,CN-Main,,0,0,0,,测试\n"
        )
        cleaned, credits, removed = normalize_source_metadata(events)
        self.assertEqual(credits, ["诸神字幕组"])
        self.assertEqual(removed, 2)
        self.assertNotIn("Comment:", cleaned)
        self.assertIn("Dialogue:", cleaned)

    def test_release_cleanup_drops_nonruntime_sections_and_rejects_duplicate_styles(self) -> None:
        source = (
            "[Script Info]\nScriptType: v4.00+\n[Aegisub Project Garbage]\nVideo File: local.mkv\n"
            "[V4+ Styles]\nFormat: Name, Fontname\nStyle: CN-Main,Noto Sans CJK SC\n"
            "[Fonts]\nfontname: unwanted\n[Events]\nFormat: Layer, Start, End, Style, Name, "
            "MarginL, MarginR, MarginV, Effect, Text\n"
        )
        styles = ass_section(source, "[V4+ Styles]")
        events = ass_section(source, "[Events]")
        self.assertNotIn("[Fonts]", styles)
        self.assertNotIn("local.mkv", styles + events)
        duplicate = (
            "[V4+ Styles]\nStyle: CN-Main,Noto Sans CJK SC\n"
            "Style: CN-Main,Noto Sans CJK SC\n"
        )
        with self.assertRaises(NormalizeError):
            normalize_styles(duplicate, {"CN-Main"}, {"CN-Main": SC_FONT})

    def test_global_font_replacement_preserves_special_style_and_event_properties(self) -> None:
        styles = (
            "[V4+ Styles]\n"
            "Format: Name, Fontname, Fontsize, PrimaryColour, Alignment, MarginL, MarginR, MarginV\n"
            "Style: CN-Main,Unavailable Dialogue Font,62,&H00FFFFFF,2,90,90,54\n"
            "Style: Sign-Top,Decorative Missing Font,41,&H00112233,8,17,23,31\n"
            "Style: JP-Note,Another Missing Font,33,&H00445566,7,5,6,7\n"
        )
        events = (
            "[Events]\n"
            "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
            "Dialogue: 3,0:00:01.00,0:00:02.00,Sign-Top,sign,11,12,13,fx,{\\pos(222,111)\\fnRare Sign Font}注释\n"
            "Dialogue: 4,0:00:03.00,0:00:04.00,JP-Note,note,21,22,23,karaoke,{\\fnRare JP Font}テスト\n"
            "Dialogue: 0,0:00:05.00,0:00:06.00,CN-Main,,0,0,0,,"
            "{\\fnRare CN Font}English and 中文\\N{\\fnRare Inline JP}テスト\n"
        )
        references = {"CN-Main", "Sign-Top", "JP-Note"}
        targets = font_targets_by_style(events, references)
        self.assertEqual(targets, {"CN-Main": SC_FONT, "Sign-Top": SC_FONT, "JP-Note": JP_FONT})

        normalized_styles, removed, changes = normalize_styles(styles, references, targets)
        self.assertEqual(removed, [])
        self.assertEqual(changes, 3)
        before_style_lines = [line for line in styles.splitlines() if line.startswith("Style:")]
        after_style_lines = [line for line in normalized_styles.splitlines() if line.startswith("Style:")]
        for before, after, target in zip(before_style_lines, after_style_lines, (SC_FONT, SC_FONT, JP_FONT)):
            before_fields = before.split(",")
            after_fields = after.split(",")
            self.assertEqual(after_fields[1], target)
            self.assertEqual(after_fields[:1] + after_fields[2:], before_fields[:1] + before_fields[2:])

        normalized_events, inline_changes = normalize_inline_fonts(events, targets)
        self.assertEqual(inline_changes, 4)
        expected = events.replace("\\fnRare Sign Font", f"\\fn{SC_FONT}")
        expected = expected.replace("\\fnRare JP Font", f"\\fn{JP_FONT}")
        expected = expected.replace("\\fnRare CN Font", f"\\fn{SC_FONT}")
        expected = expected.replace("\\fnRare Inline JP", f"\\fn{JP_FONT}")
        self.assertEqual(normalized_events, expected)
        self.assertIn(r"\pos(222,111)", normalized_events)
        self.assertIn(",Sign-Top,sign,11,12,13,fx,", normalized_events)


class CandidateContractTests(unittest.TestCase):
    def test_rendered_regression_rejects_non_font_style_or_event_changes(self) -> None:
        styles = (
            "[V4+ Styles]\n"
            "Style: CN-Main,Noto Sans CJK SC,62,&H00FFFFFF,2,90,90,54\n"
        )
        events = (
            "[Events]\n"
            "Dialogue: 0,0:00:01.00,0:00:02.00,CN-Main,,0,0,0,,测试\n"
        )
        with self.assertRaises(NormalizeError):
            assert_rendered_regression(
                styles,
                styles.replace(",62,", ",60,"),
                events,
                events,
                {"CN-Main"},
            )
        with self.assertRaises(NormalizeError):
            assert_rendered_regression(
                styles,
                styles,
                events,
                events.replace("0:00:02.00", "0:00:03.00"),
                {"CN-Main"},
            )

    def test_release_coverage_is_invalidated_by_master_change(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _, series, _, _, args = initialize_project(root, video_name="coverage.S01E01.mkv")
            run("init_project.py", *args)
            project = series / "SH0001--test-tv"
            current = project / "subtitles/current"
            current.mkdir(parents=True)
            (current / "VERSION").write_text("1.0.0\n", encoding="utf-8")
            (current / "coverage.S01E01.zh-Hans.ass").write_text(release_ass(100, "测试作品", "S01E01"), encoding="utf-8")
            mark_review_release_ready(project)
            master = project / "project/workspace/episodes/S01E01/master.ass"
            master.write_text(master.read_text(encoding="utf-8") + "; changed\n", encoding="utf-8")
            result = run("validate_project.py", str(project), "--release", expect=1)
            self.assertIn("coverage for S01E01 is stale", result.stdout)

    def test_noto_master_builds_candidate_without_font_transition(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _, series, _, _, args = initialize_project(root, video_name="candidate-cut.S01E01.mkv")
            run("init_project.py", *args)
            project = series / "SH0001--test-tv"
            run_path(NORMALIZE_SCRIPT, str(project), "--version", "1.0.0")
            candidate = project / "project/workspace/build/current-candidate/candidate-cut.S01E01.zh-Hans.ass"
            text = candidate.read_text(encoding="utf-8")
            self.assertIn("Noto Sans CJK SC", text)
            self.assertNotIn("Microsoft YaHei UI", text)

    def test_candidate_builder_rejects_non_noto_schema9_master(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _, series, _, _, args = initialize_project(root, video_name="candidate-cut.S01E01.mkv")
            run("init_project.py", *args)
            project = series / "SH0001--test-tv"
            master = project / "project/workspace/episodes/S01E01/master.ass"
            master.write_text(master.read_text(encoding="utf-8").replace("Noto Sans CJK SC", "Arial"), encoding="utf-8")
            result = run_path(NORMALIZE_SCRIPT, str(project), "--version", "1.0.0", expect=1)
            self.assertIn("master has non-Noto fonts", result.stderr)

    def test_candidate_builder_requires_current_project_contract(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _, series, _, _, args = initialize_project(root, video_name="old-contract-cut.S01E01.mkv")
            run("init_project.py", *args)
            project = series / "SH0001--test-tv"
            metadata = project / "project.yaml"
            text = metadata.read_text(encoding="utf-8")
            text = text.replace("schema_version: 9", "schema_version: 7", 1)
            metadata.write_text(text, encoding="utf-8")
            result = run_path(NORMALIZE_SCRIPT, str(project), "--version", "1.0.0", expect=1)
            self.assertIn("upgrade project to the Skill 1.4.0 contract", result.stderr)
            self.assertFalse((project / "project/workspace/build/current-candidate").exists())


class TermAuditTests(unittest.TestCase):
    def test_audit_counts_declared_forms_and_blocks_short_old_translation(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            subtitle = root / "episode.ass"
            subtitle.write_bytes(baseline_ass_bytes("乌尔苏拉来了"))
            with subtitle.open("a", encoding="utf-8") as stream:
                stream.write(
                    "Dialogue: 0,0:00:03.00,0:00:04.00,CN-Main,,0,0,0,,乌苏拉也来了\n"
                    "Dialogue: 0,0:00:05.00,0:00:06.00,CN-Main,,0,0,0,,Úrsula llegó\n"
                    "Comment: 0,0:00:07.00,0:00:08.00,CN-Main,,0,0,0,,乌苏拉\n"
                )
            manifest = root / "terms.json"
            manifest.write_text(
                json.dumps({
                    "schema_version": 1,
                    "terms": [{
                        "term_id": "character.ursula",
                        "approved_forms": ["乌尔苏拉"],
                        "forbidden_forms": ["乌苏拉"],
                        "source_forms": ["Úrsula"],
                    }],
                }, ensure_ascii=False),
                encoding="utf-8",
            )
            before = subtitle.read_bytes()
            result = run("audit_terms.py", "--terms", str(manifest), str(subtitle), expect=2)
            report = json.loads(result.stdout)
            forms = report["files"][0]["terms"][0]
            self.assertEqual(forms["approved_forms"][0]["count"], 1)
            self.assertEqual(forms["forbidden_forms"][0]["count"], 1)
            self.assertEqual(forms["source_forms"][0]["count"], 1)
            self.assertEqual(report["summary"], {"forbidden_hits": 1, "passed": False})
            self.assertEqual(subtitle.read_bytes(), before)
            clean = root / "clean.ass"
            clean.write_bytes(before.replace("乌苏拉".encode(), "乌尔苏拉".encode()))
            passed = json.loads(run("audit_terms.py", "--terms", str(manifest), str(clean)).stdout)
            self.assertEqual(passed["summary"], {"forbidden_hits": 0, "passed": True})

    def test_audit_rejects_ambiguous_or_conflicting_form_assignment(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            subtitle = root / "episode.ass"
            subtitle.write_bytes(baseline_ass_bytes())
            manifest = root / "terms.json"
            manifest.write_text(
                json.dumps({
                    "schema_version": 1,
                    "terms": [
                        {"term_id": "a", "approved_forms": ["雷梅黛丝"], "forbidden_forms": []},
                        {"term_id": "b", "approved_forms": ["蕾梅黛丝"], "forbidden_forms": ["雷梅黛丝"]},
                    ],
                }, ensure_ascii=False),
                encoding="utf-8",
            )
            result = run("audit_terms.py", "--terms", str(manifest), str(subtitle), expect=1)
            self.assertIn("assigned more than once", result.stderr)


class StaticAuditTests(unittest.TestCase):
    def test_audit_reports_full_counts_and_code_proven_layout_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "audit.ass"
            path.write_text(
                "[Script Info]\nScriptType: v4.00+\nWrapStyle: 0\nScaledBorderAndShadow: yes\nPlayResX: 1920\nPlayResY: 1080\nYCbCr Matrix: TV.709\n\n"
                "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
                "Style: CN-Main,Noto Sans CJK SC,62,&H00FFFFFF,&H000000FF,&H00101010,&H00000000,0,0,0,0,100,100,0,0,1,3,0,2,96,96,70,1\n\n"
                "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
                "Dialogue: 0,0:00:01.00,0:00:00.90,CN-Main,,0,0,0,,测试\n"
                "Dialogue: 0,0:00:02.00,0:00:04.00,CN-Main,,0,0,0,,第一行\\N第二行\\N第三行\n"
                "Dialogue: 0,0:00:05.00,0:00:07.00,CN-Main,,0,0,0,,{\\pos(2500,120)}越界\n",
                encoding="utf-8",
            )
            data = json.loads(run("audit_subtitle.py", str(path)).stdout)["files"][0]
            self.assertEqual(data["events"], 3)
            self.assertEqual(data["chinese_in_scope"], 3)
            self.assertEqual(data["static_layout_checked"], 3)
            categories = {item["category"] for item in data["findings"]}
            self.assertIn("invalid-duration", categories)
            self.assertIn("explicit-lines", categories)
            self.assertIn("off-screen", categories)


if __name__ == "__main__":
    unittest.main()
