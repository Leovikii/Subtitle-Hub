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

`project.yaml` is the only project descriptor. It records identity, type/scope, languages, sources/roles, video map, initialization, and release configuration. Do not create a second source catalog, video manifest, `latest.yaml`, archive registry, per-version release YAML, or repository checksum file.

Schema 6 remains valid. New projects record `initialization.skill_version: 1.1.0`; existing 1.0 initialization values remain truthful history. Intake JSON, map TSV, and absolute local paths are disposable/not portable control files.

## SH-CTRL-004 — project-guide.md

Only this file may supplement/override Skill or series rules. Keep sections for scope/languages; evidence-source division; project risks; styles/special layout; rule table; workspace constraints; known limits/prohibited automation.

Rule table columns are `rule_id type global_ref scope rule rationale`. `type` is `supplement` or `override`; `global_ref` is a stable Skill rule ID such as `SH-TIME-004`, not a path/heading. A series terminology deviation additionally cites `term_id`, evidence, scope, and user confirmation. Do not store progress, issue rows, version history, or narrative migration history here.

## SH-CTRL-005 — review.md

`docs/review.md` combines the machine-readable current state and the user-facing active-round report. Keep YAML front matter with `schema_version work_id updated_at baseline_release target_release overall_status active_round stages episodes`. Stages are `source_inventory baseline_setup translation_review timing_review typography_review visual_review release_qc`.

Stage/episode status values are `not-started`, `in-progress`, `candidate-review`, `blocked`, `verified`, `not-applicable`, and `released` only where the existing episode/release state requires it. `overall_status` may also use `baseline-released` or `released`. `active_round.status` may use `completed` and `awaiting-review` for actual round state. Do not use derived readiness values `ready/limited/blocked` as stage values except the already-defined `blocked` stage state.

The body is the readable proofreading plan and result. It contains categorized proposal tables detailed under `SH-PLAN-001`, actual machine/human coverage, decisions, implemented results, verification, and remaining risk. Update at proposal, approval feedback, implementation completion, and final-review readiness—not after every internal step. Git history preserves prior rounds.

## SH-CTRL-006 — ledger.tsv

Columns:

```text
item_id round_id date episode start end category severity before proposed_after evidence rationale decision status actual_after actor reviewer resolution
```

Use one row per substantive item and update that row through proposal, decision, implementation, and verification. A round ID may group rows but does not replace them. Documentation/tooling/release metadata changes may use `episode=ALL`. Evidence cites media, source text, user feedback, or a stable Skill rule ID, never only a disposable attachment.

`decision` values are `pending`, `approved`, `rejected`, `deferred`, `waived`, `not-required`, and `not-recorded` only for honestly migrated history. `status` values are `candidate`, `confirmed`, `awaiting-approval`, `in-progress`, `blocked`, `applied`, `verified`, `closed`, `reverted`, and `released`. A rejected or waived item uses `status=closed` with authority, date, reason, and risk in `resolution`. Do not create a second issue or change ledger.

## SH-CTRL-007 — Proposal and approval gate

Analyze first without modifying masters. Record the complete detailed plan in review/ledger, set `awaiting-review`, and ask once for item or bounded-batch approval. A diagnose-only request never authorizes fixes.

After feedback, record approved/rejected/deferred/waived rows. Apply and verify approved scope continuously through a complete release candidate. Do not seek new approval for routine findings already inside that scope, ordinary dialogue font/size/margin normalization, or local spot checks. A newly discovered semantic change outside scope is added to the plan and deferred unless it is release-blocking.

Project-control, documentation, tooling, and other non-subtitle changes may proceed under the user's current explicit implementation request without a second approval round, but still require ledger and review updates when substantive.

## SH-CTRL-008 — Feedback, evidence, and closure

Write feedback into the affected rows and summarize it in `review.md`; do not create a separate feedback report. Temporary detector output is disposable. Create no screenshot by default; if one concrete visual question requires it, keep it outside the durable project structure and record the timestamp/conclusion.

When implementation is complete, update the proposal into an actual-results report and build the candidate. Pause for the single release-candidate final review. After user acceptance, publish, mark rows/review released, and clean disposable artifacts.
