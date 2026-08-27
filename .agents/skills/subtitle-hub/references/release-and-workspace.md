# Workspace and release

## SH-WS-001 — Create paths on demand

Durable masters are `project/workspace/episodes/<episode>/master.ass`. Initialization creates only paths needed for `project.yaml`, root-level `review.md`, immutable copied sources, local video mapping, and these masters.

- `project/workspace/temp/tools/`: project-only scripts, created with the first tool.
- `project/workspace/temp/notes/`: temporary supplemental instructions or small handoff notes, created with the first note. It is not a control plane or evidence archive.
- `project/workspace/build/`: complete checked candidate, created when building.
- `subtitles/current/` and `subtitles/previous/`: releases, created only by release rotation.

Do not create `archive/`, screenshot/evidence trees, `intermediate/`, or `logs/`. Prefer system temporary storage for disposable generated data. Delete obsolete temporary files after durable conclusions are in `review.md` or `project.yaml`.

## SH-REL-002 — Release layout and versioning

`subtitles/current/VERSION + *.ass` is published authority. After the first replacement keep one complete `previous/`; first `1.0.0` needs none. PATCH fixes the same contract, MINOR expands compatible scope/languages, and MAJOR changes an incompatible contract. Skill/tool/directory-only migration does not change subtitle version.

Release files are `<target-video-stem>.zh-Hans.ass`. Each has matching version/language header fields and at most one canonical `Subtitle-Hub-Source-Credit`. Any high-confidence source credit found while building must be retained there; absence is allowed only when no qualifying credit was identified.

## SH-REL-003 — Conservative source-credit contract

Treat attribution as high-confidence only when it is an unambiguous subtitle-group name or a complete role-to-person credit line. Preserve the original names and roles, deduplicate exact repetitions, and consolidate qualifying fragments into `Subtitle-Hub-Source-Credit`. A prior canonical credit is still evidence and must survive subsequent builds.

Prefer omission to invention: do not infer a credit from filenames, websites, release-group tags, dialogue, translation provenance, or an unclear free-form sentence. Strip URLs, promotional text, disclaimers, legal notices, source lists, local workflow notes, and engineering provenance rather than presenting them as attribution. Harvest qualifying credits before removing non-rendering metadata. Never turn credits into Events; never silently drop an already identified qualifying credit.

## SH-REL-004 — ASS release boundary

Preserve valid Script Info geometry/matrix and rendered special styles/effects. A release contains only runtime subtitle content and canonical metadata: remove editor/project sections, embedded attachments, local paths, empty or duplicate metadata, automation/template code, disabled/comment-only events, disclaimers, websites, workflow notes, and rendered provenance. Harvest `SH-REL-003` credits first.

After non-rendering Events are removed, delete every style not referenced by a remaining rendered Event, `\rStyle`, or implicit `Default`; fail on undefined references. Preserve referenced special styles without merging or standardizing them. Ordinary dialogue normalization follows `SH-LAYOUT-005`. Do not delete a visible Event merely because it resembles a credit or note; content deletion still follows the approval gate.

## SH-REL-006 — Transaction and rollback

Build a complete candidate, set version markers and VERSION, validate, then rename old `current` to `previous` and candidate to `current`. If promotion fails, restore the rotated directory. Every changed release must receive a new version. Local work must not create, update, delete, inspect by extraction, or commit distribution ZIPs under `packages/`.

## SH-REL-007 — Package and catalog

Locally run only `.github/scripts/build_subtitle_packages.py --check`; it validates releases and planned package identities without writing ZIPs. Never run its Action-only build mode locally. GitHub Actions is the sole producer, remover, verifier, and committer of `packages/*.zip`.

The deterministic package is `packages/bgm<subject-id> - <name_cn> [v<version>].zip` and contains current ASS files, VERSION, and CHECKSUMS only. `catalog.yaml` and `CATALOG.md` are also Action-owned derived outputs: do not edit, generate, or validate them locally. After a release push, the packaging Action builds packages; only when `packages/` changed does it regenerate both indexes and commit the package/index set together. Project metadata and `review.md` remain their inputs and durable truths.
