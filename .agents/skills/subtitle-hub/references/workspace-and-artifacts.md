# Workspace, temporary artifacts, and archives

## SH-WS-002 — Standard separation

```text
project/
├─ sources/                         immutable inputs
├─ workspace/
│  ├─ episodes/<episode>/master.ass durable working masters
│  ├─ temp/
│  │  ├─ tools/                     project-only scripts
│  │  ├─ intermediate/              extracts, mappings, conversions
│  │  ├─ review/                    disposable candidates/diffs/evidence
│  │  └─ logs/                      reproducible output/logs
│  └─ build/                        checked, complete release candidates
└─ archive/                         frozen historical engineering archives
```

Official outputs live outside `project/` under `subtitles/current/` and `subtitles/previous/`. Durable control facts live only in `project.yaml`, `docs/project-guide.md`, `docs/review.md`, and `docs/ledger.tsv`.

## SH-WS-003 — Lifecycles

- `episodes/`: next-release working authority, tracked. A tool writes a candidate, compares it, and only then replaces the master; no temporary result silently becomes the baseline.
- `temp/`: disposable, untracked, and never a runtime dependency or unique durable evidence. Put screenshots under the active review attachments directory.
- `build/`: reproducible complete candidates that have passed the current round's specified checks; never the published version.
- `archive/`: stopped but traceable engineering history. Require stable name/date, original-path manifest, sizes, per-file SHA-256, and archive SHA-256. Extract only into `temp/intermediate/` for an explicit trace; never run archived scripts as current tooling.

## SH-WS-004 — One-off automation

Place project-specific scripts in `temp/tools/`, define explicit input/output/scope, read immutable sources, write to intermediate/review, compare against the master, register approved substantive edits, then update the master. Promote a tool to repository scope only after demonstrated multi-project reuse, stable contracts, tests, and a separate decision; do not prebuild a universal subtitle pipeline.

## SH-WS-005 — Safe cleanup

Before recursive cleanup, resolve and verify that every target is inside the current work's `project/workspace/temp/` or `project/workspace/build/`. Do not use broad roots, unresolved variables, or unsafe globs. Before deleting temp, migrate all durable conclusions and confirm that no master, unregistered change, or unique evidence remains.

Never include `workspace/episodes/`, `sources/`, the work `docs/`, `archive/`, or `subtitles/` in temporary cleanup.
