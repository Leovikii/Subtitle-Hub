---
name: subtitle-hub
description: Initialize, audit, proofread, build, validate, or release Subtitle Hub projects and Chinese-primary ASS subtitles. Use for any work in this repository that changes or assesses project identity, source roles, translation, timing, layout, control files, or release artifacts.
---

# Subtitle Hub

Use this Skill as the repository-level standard. Do not look for a parallel standard under root `docs/`, and do not consult external platform guides during routine work.

## Start here

Determine the task mode, then read only the listed references:

- New project or source intake: [project-initialization.md](references/project-initialization.md), [control-plane.md](references/control-plane.md), and [terminology.md](references/terminology.md).
- Subtitle proofreading or translation review: [workflow.md](references/workflow.md), [source-and-translation.md](references/source-and-translation.md), and [chinese-language.md](references/chinese-language.md).
- Timing, styles, fonts, or visual review: [timing-and-layout.md](references/timing-and-layout.md) and [quality-control.md](references/quality-control.md).
- Workspace, temporary evidence, or cleanup: [workspace-and-artifacts.md](references/workspace-and-artifacts.md).
- Build, release, rollback, or packaging: [release-and-packaging.md](references/release-and-packaging.md) and [quality-control.md](references/quality-control.md).
- Historical rule-path interpretation only: [legacy-rule-map.md](references/legacy-rule-map.md). Never use it as a second standard.
- External provenance or a deliberate baseline audit only: [external-basis.md](references/external-basis.md).

For any existing work, also read in order: the nearest series `series-guide.md` when present, the work `project.yaml`, `docs/project-guide.md`, `docs/progress.yaml`, `docs/issues.tsv`, and `docs/change-log.tsv`. Read a temporary review report only when `progress.yaml.active_round` says the work is awaiting human feedback, and only the matching round.

## Priority and authority

Apply, from highest to lowest: the user's current explicit instruction; confirmed project overrides in `docs/project-guide.md`; confirmed series terminology; this Skill; external references. Record any conflict and its resolution. Only `docs/project-guide.md` may supplement or override repository or series rules. A series-term override requires recorded user confirmation.

`project.yaml` records identity, scope, source facts, evidence roles, video mapping, and release configuration. `docs/progress.yaml` is the sole current-status record. Issues and changes belong in their TSV ledgers. Temporary review files are feedback artifacts, not authority.

## Non-negotiable boundaries

- Treat `project/sources/` as immutable. Never edit sources in place.
- Never edit `subtitles/current/` as a working copy. Work under `project/workspace/`; use the release transaction for promotion.
- Keep one current release and, after the first replacement release, one complete previous release. `subtitles/current/VERSION` is the release version authority.
- Name released subtitles `<video-stem>.<primary-language>.ass`; use `.zh-Hans.ass` for Simplified Chinese primary subtitles and never append the secondary language.
- Preserve identifiable original subtitle production credits in one `Subtitle-Hub-Source-Credit` header field. Do not put credits, disclaimers, websites, or engineering provenance in Events.
- Put project-only scripts in `project/workspace/temp/tools/`; do not invent a cross-project pipeline.
- Treat automated findings as candidates unless the data proves a structural violation. Never bulk-rewrite semantic, timing, or visual candidates without evidence.
- Record every substantive edit in `docs/change-log.tsv`, unresolved work in `docs/issues.tsv`, and update `docs/progress.yaml` before stopping.
- Never claim human review or full-playback coverage that was not performed and recorded.
- Perform visual checks locally. Do not attach batches of screenshots, continuous frames, contact sheets, or Base64 images to chat. Record timestamps, conclusions, and local evidence paths. Only when the user explicitly asks for one point may a message contain at most two compressed screenshots.

## Chinese-primary design

Maintain one visual system with Simplified Chinese as the primary subtitle. English or Japanese may appear below it as a secondary subtitle. Preserve the reviewed baseline's useful styles and effects, using target-video embedded subtitles as same-release timing/layout evidence when available. Do not create an independent secondary-language visual system or sacrifice Chinese meaning, readability, or stable layout.

Use `Noto Sans CJK SC` for Simplified Chinese and English and `Noto Sans CJK JP` for Japanese. Font replacement changes geometry even if ASS effect tags remain; recheck width, wrapping, positioned text, motion, karaoke, and other high-risk events.

## Stop conditions

Pause for the user when Bangumi identity is materially ambiguous, `name_cn` is empty, work scope differs between plausible entries, an embedded track's language/role cannot be established, a series-term decision has real alternatives, or a P1 release exception needs approval. Missing optional sources should reduce a readiness dimension, not automatically block project creation.
