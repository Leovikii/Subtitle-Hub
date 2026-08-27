#!/usr/bin/env python3
"""Compatibility test entry point for the Skill 1.1 toolchain."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_ROOT = Path(__file__).resolve().parent


def run(script: str, *args: str, expect: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(SCRIPT_ROOT / script), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != expect:
        raise AssertionError(
            f"{script} exited {result.returncode}, expected {expect}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


@unittest.skip("superseded by test_skill_1_0.py")
class ScriptBehaviorTests(unittest.TestCase):
    def test_skill_local_markdown_links_resolve(self) -> None:
        skill_root = SCRIPT_ROOT.parent
        missing = []
        for markdown in skill_root.rglob("*.md"):
            text = markdown.read_text(encoding="utf-8")
            for raw in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                target = raw.split("#", 1)[0]
                if not target or "://" in target or target.startswith("#"):
                    continue
                if not (markdown.parent / target).resolve().exists():
                    missing.append(f"{markdown.relative_to(skill_root)} -> {raw}")
        self.assertEqual(missing, [])

    def test_rule_ids_are_unique_and_active_project_refs_resolve(self) -> None:
        skill_root = SCRIPT_ROOT.parent
        rule_sources: dict[str, str] = {}
        duplicates = []
        for markdown in [skill_root / "SKILL.md", *sorted((skill_root / "references").glob("*.md"))]:
            text = markdown.read_text(encoding="utf-8")
            for rule_id in re.findall(r"(?m)^#{2,4}\s+(SH-[A-Z]+-\d{3})\b", text):
                if rule_id in rule_sources:
                    duplicates.append(f"{rule_id}: {rule_sources[rule_id]} and {markdown.name}")
                rule_sources[rule_id] = markdown.name
        self.assertEqual(duplicates, [])
        repository_root = skill_root.parents[2]
        works_root = repository_root / "works"
        if works_root.exists():
            unresolved = []
            for metadata in works_root.glob("**/project.yaml"):
                for rule_id in re.findall(r"(?:global_ref:\s*|`)(SH-[A-Z]+-\d{3})", metadata.read_text(encoding="utf-8")):
                    if rule_id not in rule_sources:
                        unresolved.append(f"{metadata.relative_to(repository_root)}: {rule_id}")
            self.assertEqual(unresolved, [])

    def test_no_parallel_root_docs_standard_remains(self) -> None:
        repository_root = SCRIPT_ROOT.parent.parents[2]
        old_docs = repository_root / "docs"
        remaining = sorted(path for path in old_docs.rglob("*") if path.is_file()) if old_docs.exists() else []
        self.assertEqual(remaining, [])

    def test_active_repository_markdown_links_resolve(self) -> None:
        repository_root = SCRIPT_ROOT.parent.parents[2]
        markdown_files = [
            repository_root / "README.md",
            repository_root / "CATALOG.md",
            repository_root / "AGENTS.md",
            *sorted((repository_root / "works").glob("**/*.md")),
        ]
        missing = []
        for markdown in markdown_files:
            if "project/archive" in markdown.as_posix() or not markdown.is_file():
                continue
            text = markdown.read_text(encoding="utf-8")
            for raw in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                target = raw.split("#", 1)[0]
                if not target or "://" in target or target.startswith("#"):
                    continue
                if not (markdown.parent / target).resolve().exists():
                    missing.append(f"{markdown.relative_to(repository_root)} -> {raw}")
        self.assertEqual(missing, [])

    def make_inputs(self, root: Path, movie: bool = False) -> tuple[Path, Path, Path]:
        video = root / ("movie.mkv" if movie else "episode-01.mkv")
        subtitle = root / ("movie.zh-Hans.srt" if movie else "episode-01.zh-Hans.srt")
        video.write_bytes(b"test-video-placeholder")
        subtitle.write_text("1\n00:00:01,000 --> 00:00:02,000\n测试\n", encoding="utf-8")
        episode_map = root / "map.tsv"
        episode = "MOVIE" if movie else "S01E01"
        episode_map.write_text(f"episode\tvideo\tsubtitle\n{episode}\t{video}\t{subtitle}\n", encoding="utf-8")
        return video, subtitle, episode_map

    def test_inventory_reports_layered_readiness(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            video, subtitle, _ = self.make_inputs(root)
            result = run(
                "inventory_sources.py",
                "--source-language",
                "ja",
                "--target-video",
                str(video),
                "--subtitle",
                f"{subtitle}|zh-Hans|candidate-baseline,style-layout-reference",
            )
            data = json.loads(result.stdout)
            self.assertEqual(data["readiness"]["structure"], "ready")
            self.assertEqual(data["readiness"]["timing"], "ready")
            self.assertEqual(data["readiness"]["language"], "limited")
            self.assertEqual(data["readiness"]["visual"], "limited")
            self.assertEqual(data["readiness"]["release"], "blocked")

    def test_inventory_rejects_unresolved_language(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            video, subtitle, _ = self.make_inputs(root)
            result = run(
                "inventory_sources.py",
                "--source-language",
                "ja",
                "--target-video",
                str(video),
                "--subtitle",
                f"{subtitle}|und|timing-reference",
                expect=2,
            )
            self.assertIn("ask the user", result.stderr)

    def test_inventory_unlocks_full_local_review_capabilities(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            video, subtitle, _ = self.make_inputs(root)
            source_text = root / "episode-01.ja.srt"
            source_text.write_text("1\n00:00:01,000 --> 00:00:02,000\nテスト\n", encoding="utf-8")
            result = run(
                "inventory_sources.py",
                "--source-language",
                "ja",
                "--target-video",
                str(video),
                "--subtitle",
                f"{subtitle}|zh-Hans|candidate-baseline,style-layout-reference",
                "--subtitle",
                f"{source_text}|ja|source-text-reference,timing-reference",
                "--renderer-ready",
                "--fonts-ready",
            )
            readiness = json.loads(result.stdout)["readiness"]
            self.assertEqual(readiness["structure"], "ready")
            self.assertEqual(readiness["language"], "ready")
            self.assertEqual(readiness["timing"], "ready")
            self.assertEqual(readiness["visual"], "ready")
            self.assertEqual(readiness["release"], "blocked")

    def initialize(self, root: Path, movie: bool, secondary: str | None = "ja") -> Path:
        _, _, episode_map = self.make_inputs(root, movie=movie)
        snapshot = root / "bangumi.json"
        subject_id = "200" if movie else "100"
        snapshot.write_text(
            json.dumps({"id": int(subject_id), "name": "テスト", "name_cn": "测试作品"}, ensure_ascii=False),
            encoding="utf-8",
        )
        series = root / "series"
        series.mkdir()
        args = [
            "--series-dir",
            str(series),
            "--work-id",
            "SH9002" if movie else "SH9001",
            "--slug",
            "test-movie" if movie else "test-tv",
            "--type",
            "movie" if movie else "tv",
            "--bangumi-id",
            subject_id,
            "--bangumi-snapshot",
            str(snapshot),
            "--episode-map",
            str(episode_map),
            "--source-language",
            "ja",
        ]
        if secondary:
            args.extend(["--secondary-language", secondary])
        dry = run("init_project.py", *args, "--dry-run")
        self.assertFalse((series / ("SH9002--test-movie" if movie else "SH9001--test-tv")).exists())
        self.assertIn("videos_recorded_by_basename_only", dry.stdout)
        run("init_project.py", *args)
        return series / ("SH9002--test-movie" if movie else "SH9001--test-tv")

    def test_tv_initialization_and_validation(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            project = self.initialize(Path(raw), movie=False)
            result = run("validate_project.py", str(project), "--json")
            self.assertTrue(json.loads(result.stdout)["valid"])
            metadata = (project / "project.yaml").read_text(encoding="utf-8")
            self.assertNotIn(str(Path(raw)), metadata)
            self.assertIn('S01E01: "episode-01.mkv"', metadata)
            self.assertTrue((project / "review.md").is_file())
            self.assertFalse((project / "README.md").exists())
            self.assertFalse((project / "docs").exists())
            repeated = run(
                "init_project.py",
                "--series-dir",
                str(project.parent),
                "--work-id",
                "SH9001",
                "--slug",
                "test-tv",
                "--type",
                "tv",
                "--bangumi-id",
                "100",
                "--bangumi-snapshot",
                str(Path(raw) / "bangumi.json"),
                "--episode-map",
                str(Path(raw) / "map.tsv"),
                "--source-language",
                "ja",
                "--secondary-language",
                "ja",
                expect=2,
            )
            self.assertIn("target already exists", repeated.stderr)

    def test_movie_initialization_and_validation(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            project = self.initialize(Path(raw), movie=True)
            result = run("validate_project.py", str(project), "--json")
            self.assertTrue(json.loads(result.stdout)["valid"])
            self.assertIn('MOVIE: "movie.mkv"', (project / "project.yaml").read_text(encoding="utf-8"))

    def test_monolingual_chinese_initialization(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            project = self.initialize(Path(raw), movie=False, secondary=None)
            metadata = (project / "project.yaml").read_text(encoding="utf-8")
            self.assertIn("    secondary: null", metadata)
            result = run("validate_project.py", str(project), "--json")
            self.assertTrue(json.loads(result.stdout)["valid"])

    def test_initialization_rejects_missing_video(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _, _, episode_map = self.make_inputs(root)
            lines = episode_map.read_text(encoding="utf-8").splitlines()
            fields = lines[1].split("\t")
            fields[1] = str(root / "missing.mkv")
            episode_map.write_text(lines[0] + "\n" + "\t".join(fields) + "\n", encoding="utf-8")
            snapshot = root / "bangumi.json"
            snapshot.write_text('{"id": 100, "name": "x", "name_cn": "y"}', encoding="utf-8")
            result = run(
                "init_project.py",
                "--series-dir",
                str(root / "series"),
                "--work-id",
                "SH9001",
                "--slug",
                "missing-video",
                "--type",
                "tv",
                "--bangumi-id",
                "100",
                "--bangumi-snapshot",
                str(snapshot),
                "--episode-map",
                str(episode_map),
                "--source-language",
                "ja",
                "--secondary-language",
                "ja",
                expect=2,
            )
            self.assertIn("target video is not readable", result.stderr)

    def test_initialization_rejects_missing_bangumi_name_cn(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _, _, episode_map = self.make_inputs(root)
            snapshot = root / "bangumi.json"
            snapshot.write_text('{"id": 100, "name": "x", "name_cn": ""}', encoding="utf-8")
            result = run(
                "init_project.py",
                "--series-dir",
                str(root / "series"),
                "--work-id",
                "SH9001",
                "--slug",
                "missing-name-cn",
                "--type",
                "tv",
                "--bangumi-id",
                "100",
                "--bangumi-snapshot",
                str(snapshot),
                "--episode-map",
                str(episode_map),
                "--source-language",
                "ja",
                "--secondary-language",
                "ja",
                expect=2,
            )
            self.assertIn("lacks required values", result.stderr)


if __name__ == "__main__":
    raise SystemExit(subprocess.call([sys.executable, "-B", str(SCRIPT_ROOT / "test_skill_1_0.py")]))
