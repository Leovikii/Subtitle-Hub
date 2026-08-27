---
name: subtitle-hub
description: Initialize, audit, proofread, build, validate, or release Subtitle Hub projects and Chinese-primary ASS subtitles. Use for repository work involving identity, sources, translation, timing, layout, control files, or releases.
metadata:
  version: "1.1.0"
---

# Subtitle Hub

This Skill is the repository standard. Do not reconstruct rules from history or query external platform guides during routine work.

## Read only what the task needs

- New project/material intake: [project-initialization.md](references/project-initialization.md).
- Proofreading plan, translation, Chinese, terminology, and records: [proofreading.md](references/proofreading.md) and [control-plane.md](references/control-plane.md).
- Timing, dialogue styles, fonts, or visual review: [timing-and-layout.md](references/timing-and-layout.md).
- QC, final review, or release: [quality-control.md](references/quality-control.md) and [release-and-workspace.md](references/release-and-workspace.md).

For an existing work also read, in order: nearest `series-guide.md`, `project.yaml`, `docs/project-guide.md`, `docs/review.md`, and `docs/ledger.tsv`.

## Skill 1.1 lifecycle

1. Probe exact video and Chinese baseline; resolve only facts that block a reliable mapping. Confirm the Bangumi work/scope, episode map, material roles, release languages, and short project name in one initialization decision.
2. Run the initializer dry-run as an internal safety check, create the project transactionally, and pass `--ready-for-proofreading`. Do not ask for a second dry-run approval unless its result differs materially from the confirmed plan.
3. Analyze without editing masters. Write one detailed, categorized proofreading plan in `docs/review.md` and its item rows in `docs/ledger.tsv`, then pause for approval. Dialogue retranslations, deletions, additions, and corrections are listed one by one with episode/time/before/proposed/evidence/rationale. Combine only same-category mechanical changes governed by one rule and bounded scope.
4. After approval, implement and verify the approved scope continuously. Update the same report and ledger rows with actual results; do not interrupt for routine detector findings, font/size/dialogue-margin normalization, or local spot checks.
5. Build the complete `1.0.0` candidate and request one release-candidate final review. Publish only after the user passes that review. Later versions use the same proposal → implementation → final-review pattern.

Stop outside these gates only for a genuinely blocking identity/source-language ambiguity, a material scope change, an unresolved series-term choice, or a P1 waiver.

## Authority and boundaries

Priority: current user instruction; confirmed `docs/project-guide.md` overrides; confirmed series terminology; this Skill; external references. Only `project-guide.md` may add project-specific rules.

- `project/sources/` is immutable. Never edit `subtitles/current/` as a working copy; work in `project/workspace/` and promote transactionally.
- `docs/review.md` is the sole current report and approval surface. `docs/ledger.tsv` is the sole item/change history. Do not create per-round reports or parallel issue/change files.
- Automated findings are candidates unless structure proves the defect. Never claim unperformed listening, viewing, or human review.
- Create directories only when writing their first file. `temp/` may contain only on-demand `tools/` and `notes/`; ordinary analysis output stays ephemeral. Create `build/`, `subtitles/current/`, and `subtitles/previous/` only when needed. Do not create `archive/`.
- Perform visual checks locally and normally record only timestamps and text conclusions. Do not generate screenshots without a concrete unresolved visual question. Never batch-send images; when explicitly requested, show at most two compressed screenshots for one point.

## Chinese-primary design

Ordinary Chinese dialogue uses the repository baseline in `timing-and-layout.md`: Noto Sans CJK SC, a consistent readable size, bottom-center placement, safe margins, white fill, and dark outline. Use distinct vertical baselines for Chinese-only and bilingual releases; optional source material does not make a release bilingual. Font, size, ordinary-dialogue margins, and bilingual separation are normalized as part of the approved plan and checked at final review; they do not require a separate screenshot approval.

Do not standardize notes, signs, songs, titles, positioned text, motion, karaoke, or effects. Preserve useful reference styling and adapt only when it is visibly defective or incompatible with the target video.
