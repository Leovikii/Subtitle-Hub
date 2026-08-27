---
name: subtitle-hub
description: Initialize, audit, proofread, build, validate, or release Subtitle Hub projects and Chinese-primary ASS subtitles. Use for repository work involving identity, sources, translation, timing, layout, control files, or releases.
metadata:
  version: "1.1.1"
---

# Subtitle Hub

This Skill is the repository standard. Do not reconstruct rules from history or re-query external platform guides during routine work.

## Route by task

- New project or material intake: [project-initialization.md](references/project-initialization.md).
- Proofreading plan, translation, Chinese, terminology, approval, or records: [proofreading-and-approval.md](references/proofreading-and-approval.md).
- Timing, dialogue styles, fonts, QC, or visual review: [timing-style-and-qc.md](references/timing-style-and-qc.md).
- Workspace, build, package, or release: [release-and-workspace.md](references/release-and-workspace.md).

For an existing work read, in order, the nearest `series-guide.md` if present, then `project.yaml` and root-level `review.md`.

## Lifecycle and approval gates

1. Probe the exact video and Chinese baseline. Resolve facts blocking identity, episode mapping, source roles, release languages, or a short project name; confirm those together once.
2. Run the initializer dry-run internally, create transactionally, and pass `--ready-for-proofreading`. Ask again only if the manifest materially differs from the confirmed plan.
3. Analyze without editing masters. Put a detailed categorized plan in `review.md`, then pause for approval. List each dialogue retranslation, deletion, addition, and meaning correction separately. Batch only deterministic same-rule mechanical changes with bounded scope and counts.
4. Implement and verify the approved scope continuously. Update the same plan rows with decisions, actual results, and verification; do not interrupt for routine detector findings, approved ordinary-dialogue normalization, or local spot checks.
5. Build the complete candidate and request one release-candidate final review. Publish only after it passes.

Stop elsewhere only for a blocking identity/source-language ambiguity, material scope expansion, unresolved series term, or P1 waiver.

## Authority and boundaries

Priority: current user instruction; confirmed project overrides in `project.yaml`; confirmed series terminology; this Skill; the single external style basis identified in `timing-style-and-qc.md`.

- `project.yaml` is the durable project truth: identity, sources, mappings, release contract, style profile, limitations, and confirmed overrides. `review.md` is the sole current plan, approval, result, and status surface. Git history preserves closed rounds. Create no parallel guide, ledger, progress, issue, or round report.
- `project/sources/` is immutable. Never edit `subtitles/current/` as a working copy; work in `project/workspace/` and promote transactionally.
- Automated findings are candidates unless structure proves the defect. Never claim unperformed listening, viewing, or human review.
- Create directories only with their first file. `temp/` may contain only on-demand `tools/` and `notes/`. Do not create `archive/`, screenshot trees, `intermediate/`, or `logs/`.
- Perform visual checks locally and record timestamps, conclusions, and optional local paths. Generate screenshots only for a concrete unresolved question. Never batch-send images; when explicitly requested, show at most two compressed screenshots for one point.

## Chinese-primary design

Normalize ordinary dialogue to the repository mono or bilingual profile. Optional source material does not make a release bilingual. Preserve special notes, signs, songs, titles, positioned text, motion, karaoke, and effects unless a concrete defect is confirmed. Font, size, ordinary-dialogue margins, and bilingual separation are covered by plan approval and final review; they do not need a separate screenshot gate.
