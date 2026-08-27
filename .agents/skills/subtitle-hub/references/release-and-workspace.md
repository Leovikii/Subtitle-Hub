# Workspace and release

## SH-WS-001 — Create paths on demand

Durable masters are `project/workspace/episodes/<episode>/master.ass`. Initialization creates only paths needed for control files, immutable copied sources, local video mapping, and these masters.

- `project/workspace/temp/tools/`: project-only scripts, created with the first tool.
- `project/workspace/temp/notes/`: temporary supplemental instructions or small handoff notes, created with the first note. It is not a control plane or evidence archive.
- `project/workspace/build/`: complete checked candidate, created when building.
- `subtitles/current/` and `subtitles/previous/`: releases, created only by release rotation.

Do not create `archive/`, screenshot/evidence trees, `intermediate/`, or `logs/`. Prefer system temporary storage for disposable generated data. Delete obsolete temporary files after durable conclusions are in review/ledger.

## SH-REL-002 — Release layout and versioning

`subtitles/current/VERSION + *.ass` is published authority. After the first replacement keep one complete `previous/`; first `1.0.0` needs none. PATCH fixes the same contract, MINOR expands compatible scope/languages, and MAJOR changes an incompatible contract. Skill/tool/directory-only migration does not change subtitle version.

Release files are `<target-video-stem>.zh-Hans.ass`. Each has matching version/language header fields and one optional `Subtitle-Hub-Source-Credit`; credits, disclaimers, websites, and engineering provenance never become Events.

## SH-REL-004 — ASS release boundary

Preserve valid Script Info geometry/matrix and special styles/effects. Remove editor garbage, local paths, empty metadata, and rendered provenance. Remove an unused style only after checking event styles, `\rStyle`, and implicit `Default`. Ordinary dialogue normalization follows `SH-LAYOUT-005`; do not merge or standardize special styles.

## SH-REL-006 — Transaction and rollback

Build a complete candidate, set version markers and VERSION, validate, then rename old `current` to `previous` and candidate to `current`. If promotion fails, restore the rotated directory. Do not commit local distribution ZIPs.

## SH-REL-007 — Package and catalog

The deterministic package is `packages/bgm<subject-id> - <name_cn> [v<version>].zip` and contains current ASS files, VERSION, and CHECKSUMS only. Use `.github/scripts/build_subtitle_packages.py`; after release identity/content changes run `scripts/sync_catalog.py` and `--check`.
