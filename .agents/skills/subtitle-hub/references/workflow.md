# Workflow and rule routing

This reference defines the normal lifecycle. Rule IDs are stable; project overrides cite IDs rather than Markdown headings.

## SH-CTRL-001 — Open the control plane

Before modifying an existing work, read the series guide when present, then `project.yaml`, `docs/project-guide.md`, `docs/review.md`, and `docs/ledger.tsv`. A diagnose-only request authorizes findings and records, not fixes.

## SH-ID-001 — Verify identity before a formal project

Use the Bangumi API identity gate in `project-initialization.md`. Do not create a formal work directory from filenames, search snippets, another database, or model memory.

## SH-INIT-001 — Inventory sources and readiness

Register the exact target videos, candidate Chinese subtitle, per-episode mapping, task languages, and source roles. Optional evidence unlocks stronger capabilities but is not cosmetic. Compute readiness per dimension; never summarize it as a misleading single pass/fail.

## SH-WS-001 — Establish a writable baseline

Copy or transform an immutable source/current release into `project/workspace/episodes/<episode>/master.ass`. Place experiments under `workspace/temp/` and release candidates under `workspace/build/`. Do not link the working master back to an immutable source.

## SH-SRC-001 — Separate evidence dimensions

Choose timing, source-text, translation, and forced-sign evidence independently. The same embedded track may fill multiple roles only when each role is supported. A Chinese baseline or translated subtitle is never source-language evidence.

## SH-TRANS-001 — Review meaning before polish

Establish actual speech, then use matching source-language text, context, image evidence, series terminology, and confirmed user decisions. Review mishearing, subject/object, negation, quantities, causality, omissions, additions, register, terminology, and continuity before stylistic polish.

## SH-TIME-001 — Align to the target video

Use same-release embedded timing when reliable, but return to actual audio, waveform, shots, and visible information for errors. Numeric limits create candidates; the correction floor in `timing-and-layout.md` creates mandatory review/fix items.

## SH-LAYOUT-001 — Preserve a Chinese-primary visual system

Prefer proven baseline styles and effects. Use embedded subtitles as layout, split, effect, and timing evidence, but do not copy coordinates blindly across different PlayRes/resolution systems. Reflow or split when Chinese cannot remain complete and readable.

## SH-QC-001 — Validate in layers

Run structure/encoding/style checks, bilingual pairing checks, language/terminology checks, timing/readability candidate checks, local visual checks at risk points, and only the human viewing coverage actually requested or performed. Separate machine facts from human judgments.

## SH-CTRL-002 — Record and review

Use one ledger row for each substantive item from candidate through decision, implementation, and verification. Before changing subtitle masters, present the proposed scope in `review.md` and obtain item or batch approval under `SH-CTRL-007`. Update `review.md` on start, pause, scope change, approval request, feedback, and completion. Human feedback must be written to the ledger and review before the round closes.

## SH-REL-001 — Release transactionally

Build a complete candidate, pass the release gates, rotate directories atomically, and verify the package contract. Documentation-only or tooling-only migration does not increment subtitle content version.
