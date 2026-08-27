# Project control plane and schemas

## SH-CTRL-003 — Durable files

An active work keeps these durable control files:

```text
project.yaml
docs/project-guide.md
docs/progress.yaml
docs/change-log.tsv
docs/issues.tsv
```

Do not recreate a project `docs/README.md`. A short work-root README may introduce the work and link the Skill/control files, but cannot duplicate rules, progress, issue counts, or release version.

`project.yaml` is the only project descriptor. It records identity, type/scope, languages, source entries and roles, target-video episode map, workspace/release configuration, actual review coverage, and archives. Do not create a second source catalog, video manifest, `latest.yaml`, per-version release YAML, or repository checksum file.

## SH-CTRL-004 — project-guide.md

Only this file may supplement/override Skill or series rules. Keep sections for scope/languages; evidence-source division; project risks; styles/special layout; rule table; workspace constraints; known limits/prohibited automation.

Rule table columns are `rule_id type global_ref scope rule rationale`. `type` is `supplement` or `override`; `global_ref` is a stable Skill rule ID such as `SH-TIME-004`, not a path/heading. A series terminology deviation additionally cites `term_id`, evidence, scope, and user confirmation. Do not store progress, issue rows, version history, or narrative migration history here.

## SH-CTRL-005 — progress.yaml

Top-level fields are `schema_version work_id updated_at baseline_release target_release overall_status active_round stages episodes`. Stages are `source_inventory baseline_setup translation_review timing_review typography_review visual_review release_qc`.

Stage/episode status values are `not-started`, `in-progress`, `candidate-review`, `blocked`, `verified`, `not-applicable`, and `released` only where the existing episode/release state requires it. `overall_status` may also use `baseline-released` or `released`. `active_round.status` may use `completed` and `awaiting-review` for actual round state. Do not use derived readiness values `ready/limited/blocked` as stage values except the already-defined `blocked` stage state.

Update on start, pause, completion, feedback, or scope change. `subtitles/current/VERSION`, not progress, is the published-version authority.

## SH-CTRL-006 — change-log.tsv

Columns:

```text
change_id batch_id date episode start end category severity before after source_ref rationale status agent reviewer
```

Use one row per substantive subtitle event; a batch ID may group rows but does not replace them. Documentation/tooling/release metadata changes may use `episode=ALL`. `source_ref` cites evidence or a stable Skill rule ID, never only a disposable report. Active status values are `applied`, `verified`, `reverted`, and `released` where existing release audit rows use it. Historical rows are immutable even if older status vocabulary differs.

## SH-CTRL-007 — issues.tsv

Columns:

```text
issue_id date episode start end category severity description evidence proposed_action status owner resolution
```

Active status values are `candidate`, `confirmed`, `in-progress`, `blocked`, `fixed`, `verified`, `waived`, and `wont-fix`. `waived` means an otherwise applicable requirement was knowingly accepted by an identified authority; include authority, date, reason, risk, and what must not be claimed. `wont-fix` means no change is planned and also requires reason/approver. This explicit `waived` value preserves the existing projects' valid visual waivers instead of disguising them.

## SH-CTRL-008 — Temporary review reports

Use `project/workspace/temp/review/review-<round>-<scope>.md` plus optional `attachments/`. State report/work/round/scope/baseline/date, machine and human coverage, candidates/evidence/risks, decisions needed, suggested durable-file updates, and status `draft`, `awaiting-review`, `feedback-received`, or `closed`.

Feedback must be written back to project guide, progress, change log, or issues before closing/removing the report. Archive a report only by explicit user request and with a frozen manifest/checksum.
