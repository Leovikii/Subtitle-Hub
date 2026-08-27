---
name: subtitle-hub
description: Initialize, audit, proofread, build, validate, or release Subtitle Hub projects and Chinese-primary ASS subtitles. Use for any work in this repository that changes or assesses project identity, source roles, translation, timing, layout, control files, or release artifacts.
metadata:
  version: "1.0.0"
---

# Subtitle Hub

Use this Skill 1.0 as the repository-level standard. Do not look for a parallel standard under root `docs/`, and do not consult external platform guides during routine work.

## Start here

Determine the task mode, then read only the listed references:

- New project or source intake: [project-initialization.md](references/project-initialization.md), [control-plane.md](references/control-plane.md), and [terminology.md](references/terminology.md).
- Subtitle proofreading or translation review: [workflow.md](references/workflow.md), [source-and-translation.md](references/source-and-translation.md), and [chinese-language.md](references/chinese-language.md).
- Timing, styles, fonts, or visual review: [timing-and-layout.md](references/timing-and-layout.md) and [quality-control.md](references/quality-control.md).
- Workspace, temporary evidence, or cleanup: [workspace-and-artifacts.md](references/workspace-and-artifacts.md).
- Build, release, rollback, or packaging: [release-and-packaging.md](references/release-and-packaging.md) and [quality-control.md](references/quality-control.md).
- Historical rule-path interpretation only: [legacy-rule-map.md](references/legacy-rule-map.md). Never use it as a second standard.
- External provenance or a deliberate baseline audit only: [external-basis.md](references/external-basis.md).

For any existing work, also read in order: the nearest series `series-guide.md` when present, the work `project.yaml`, `docs/project-guide.md`, `docs/review.md`, and `docs/ledger.tsv`. The review file is the sole current-status and active-round report; the ledger is the sole item history.

## New-project gate

For a new proofreading project, follow this contract before creating a work directory:

1. Verify Bangumi identity and scope.
2. Run `scripts/inventory_sources.py` against the exact target video(s) and Chinese baseline. Let it probe audio/subtitle tracks and propose material roles and episode relationships.
3. Resolve every blocking language/audio question, then obtain approval for the episode map, evidence roles, release languages, and a short developer-facing project name such as `yamato-2199-tv`.
4. Run `scripts/init_project.py --dry-run`; create the project only after the manifest is reviewed.
5. Require `scripts/validate_project.py --ready-for-proofreading` to pass before subtitle analysis begins.

The intake JSON and approved mapping TSV are disposable handoff artifacts, not additional durable control files. Keep absolute video paths only in ignored `project/local.paths.yaml`. The initialized work directory is `<SHxxxx>--<approved-project-name>`; do not derive or create it before approval.

## Priority and authority

Apply, from highest to lowest: the user's current explicit instruction; confirmed project overrides in `docs/project-guide.md`; confirmed series terminology; this Skill; external references. Record any conflict and its resolution. Only `docs/project-guide.md` may supplement or override repository or series rules. A series-term override requires recorded user confirmation.

`project.yaml` records identity, scope, source facts, evidence roles, video mapping, and release configuration. `docs/review.md` records current state and the user-facing active-round report. `docs/ledger.tsv` records each candidate, decision, applied change, and verification once. Temporary review files are evidence artifacts, not authority.

## Non-negotiable boundaries

- Treat `project/sources/` as immutable. Never edit sources in place.
- Never edit `subtitles/current/` as a working copy. Work under `project/workspace/`; use the release transaction for promotion.
- Keep one current release and, after the first replacement release, one complete previous release. `subtitles/current/VERSION` is the release version authority.
- Name released subtitles `<video-stem>.<primary-language>.ass`; use `.zh-Hans.ass` for Simplified Chinese primary subtitles and never append the secondary language.
- Preserve identifiable original subtitle production credits in one `Subtitle-Hub-Source-Credit` header field. Do not put credits, disclaimers, websites, or engineering provenance in Events.
- Put project-only scripts in `project/workspace/temp/tools/`; do not invent a cross-project pipeline.
- Treat automated findings as candidates unless the data proves a structural violation. Never bulk-rewrite semantic, timing, or visual candidates without evidence.
- Before changing a subtitle master, record substantive candidates in `docs/ledger.tsv`, summarize the proposed scope in `docs/review.md`, and obtain user approval for the item IDs or an explicit batch scope. Apply and verify only the approved scope, then update the same rows and review file before stopping.
- Never claim human review or full-playback coverage that was not performed and recorded.
- Perform visual checks locally. Do not attach batches of screenshots, continuous frames, contact sheets, or Base64 images to chat. Record timestamps, conclusions, and local evidence paths. Only when the user explicitly asks for one point may a message contain at most two compressed screenshots.

## Chinese-primary design

Maintain one visual system with Simplified Chinese as the primary subtitle. English or Japanese may appear below it as a secondary subtitle. Preserve the reviewed baseline's useful styles and effects, using target-video embedded subtitles as same-release timing/layout evidence when available. Do not create an independent secondary-language visual system or sacrifice Chinese meaning, readability, or stable layout.

Use `Noto Sans CJK SC` for Simplified Chinese and English and `Noto Sans CJK JP` for Japanese. Font replacement changes geometry even if ASS effect tags remain; recheck width, wrapping, positioned text, motion, karaoke, and other high-risk events.

## Stop conditions

Pause for the user when Bangumi identity is materially ambiguous, `name_cn` is empty, work scope differs between plausible entries, an embedded track's language/role cannot be established, a series-term decision has real alternatives, or a P1 release exception needs approval. Missing optional sources should reduce a readiness dimension, not automatically block project creation.
