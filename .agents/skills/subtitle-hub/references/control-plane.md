# Project control plane and schemas

## SH-CTRL-003 — Durable files

An active work keeps these durable control files:

```text
project.yaml
docs/project-guide.md
docs/review.md
docs/ledger.tsv
```

Do not add per-round reports, separate progress/issue/change files, or a project `docs/README.md`. A short work-root README may introduce the work and link the Skill/control files, but cannot duplicate rules, progress, item counts, or release version.

`project.yaml` is the only project descriptor. It records identity, type/scope, languages, source entries and roles, target-video episode map, workspace/release configuration, actual review coverage, and archives. Do not create a second source catalog, video manifest, `latest.yaml`, per-version release YAML, or repository checksum file.

Skill 1.0 projects use `schema_version: 6`. They record the short `project_name`; a `naming` approval block; API-verified Bangumi date/platform/episode count and user-confirmed scope; explicit source classifications; `video_sources.target-video.files`; and an `initialization` block with `skill_version: 1.0.0`, state, intake/map approvers, approval date, and initialization date. An ordinary new project uses `initialization.state: proofreading-ready`; migrated released projects may use `released-existing` with honest historical limitations. Intake JSON, approved map TSV, and local absolute video paths are not additional durable project descriptors.

## SH-CTRL-004 — project-guide.md

Only this file may supplement/override Skill or series rules. Keep sections for scope/languages; evidence-source division; project risks; styles/special layout; rule table; workspace constraints; known limits/prohibited automation.

Rule table columns are `rule_id type global_ref scope rule rationale`. `type` is `supplement` or `override`; `global_ref` is a stable Skill rule ID such as `SH-TIME-004`, not a path/heading. A series terminology deviation additionally cites `term_id`, evidence, scope, and user confirmation. Do not store progress, issue rows, version history, or narrative migration history here.

## SH-CTRL-005 — review.md

`docs/review.md` combines the machine-readable current state and the user-facing active-round report. Keep YAML front matter with `schema_version work_id updated_at baseline_release target_release overall_status active_round stages episodes`. Stages are `source_inventory baseline_setup translation_review timing_review typography_review visual_review release_qc`.

Stage/episode status values are `not-started`, `in-progress`, `candidate-review`, `blocked`, `verified`, `not-applicable`, and `released` only where the existing episode/release state requires it. `overall_status` may also use `baseline-released` or `released`. `active_round.status` may use `completed` and `awaiting-review` for actual round state. Do not use derived readiness values `ready/limited/blocked` as stage values except the already-defined `blocked` stage state.

The body keeps only the current round's goal/scope, actual machine/human coverage, candidate summary, user decisions, implementation result, verification, and remaining risk. Refer to ledger IDs instead of duplicating detailed evidence. Update on start, pause, approval request, feedback, completion, or scope change. Git history preserves older completed reports; do not create one report file per round. `subtitles/current/VERSION`, not review metadata, is the published-version authority.

## SH-CTRL-006 — ledger.tsv

Columns:

```text
item_id round_id date episode start end category severity before proposed_after evidence rationale decision status actual_after actor reviewer resolution
```

Use one row per substantive item and update that row through proposal, decision, implementation, and verification. A round ID may group rows but does not replace them. Documentation/tooling/release metadata changes may use `episode=ALL`. Evidence cites media, source text, user feedback, or a stable Skill rule ID, never only a disposable attachment.

`decision` values are `pending`, `approved`, `rejected`, `deferred`, `waived`, `not-required`, and `not-recorded` only for honestly migrated history. `status` values are `candidate`, `confirmed`, `awaiting-approval`, `in-progress`, `blocked`, `applied`, `verified`, `closed`, `reverted`, and `released`. A rejected or waived item uses `status=closed` with authority, date, reason, and risk in `resolution`. Do not create a second issue or change ledger.

## SH-CTRL-007 — Proposal and approval gate

For substantive subtitle meaning, timing, segmentation, style, or layout changes, analyze first without modifying `workspace/episodes/*/master.ass`. Record candidates in the ledger, summarize the proposed scope in `review.md`, set the round to `awaiting-review`, and ask the user or project owner to approve item IDs, a category, or an explicit batch scope. A diagnose-only request never authorizes fixes.

Approval may be item-specific or a clearly bounded batch authorization. Do not infer approval from silence or from a request to inspect/report. After feedback, set approved rows to `decision=approved`, rejected rows to `decision=rejected`, deferred rows to `decision=deferred`, and explicit requirement exceptions to `decision=waived`. Apply only approved scope, record `actual_after`, then verify neighbors and affected layout before setting `status=verified`.

Project-control, documentation, tooling, and other non-subtitle changes may proceed under the user's current explicit implementation request without a second approval round, but still require ledger and review updates when substantive.

## SH-CTRL-008 — Feedback, evidence, and closure

Write feedback directly into the affected ledger rows and summarize it in `review.md`; do not create a separate feedback report. Save optional screenshots, diffs, detector output, or logs under the active work's `project/workspace/temp/review/`, with screenshots under `attachments/`. These files are disposable evidence, not status or approval authority.

Close a round only after approved changes are applied and verified, rejected/deferred/waived dispositions are recorded, remaining risks are stated, and `review.md` is current. Before cleaning temporary evidence, confirm every durable decision and conclusion is represented in `review.md`, `ledger.tsv`, `project-guide.md`, or `project.yaml` as appropriate.
