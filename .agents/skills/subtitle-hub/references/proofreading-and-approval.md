# Proofreading, approval, and project records

## SH-CTRL-003 — Two durable control files

An active work keeps exactly `project.yaml` and root-level `review.md` as control files.

`project.yaml` records durable identity, scope, languages, sources/roles, video map, initialization, release configuration, ordinary-style profile, limitations, and confirmed project overrides. An override cites a stable Skill rule ID, scope, rationale/evidence, confirmer, and date; a terminology deviation also cites the series `term_id`. Do not add a second source catalog, project guide, ledger, progress file, issue file, per-round report, or project README.

`review.md` combines machine-readable current state with the readable active plan and result. Keep YAML front matter with `schema_version work_id updated_at baseline_release target_release overall_status active_round stages episodes`. Git history preserves closed rounds; replace completed current-round detail when a new round begins instead of accumulating an archive.

## SH-CTRL-007 — Proposal and approval gate

Analyze without modifying masters. In `review.md`, use categorized tables with `item_id`, episode/time or bounded scope, category, before, proposed result, evidence/rationale, severity/risk, decision, status, actual result, and verification. Initial proposal rows use pending/awaiting approval; update the same rows after feedback, implementation, verification, final review, and release.

List every retranslation, dialogue deletion/addition, meaning correction, and context-sensitive terminology change separately. Batch only deterministic same-category work such as one exact confirmed term replacement, punctuation rule, or ordinary-dialogue style mapping; state the match rule, count, episodes, exclusions, and examples. Never hide semantic edits in a batch.

After approval, implement and verify the approved scope continuously through a complete release candidate. New semantic work outside scope is added as pending and deferred unless release-blocking. Documentation/tooling changes explicitly requested by the user need no second approval round. Never create a separate feedback or completion report.

## SH-TRANS-001 — Review meaning before polish

Establish actual speech, then use matching source text, context, image evidence, series terminology, and confirmed decisions. Check speaker/object/action, negation, number, causality, omissions, additions, register, terminology, continuity, grammar, punctuation, segmentation, and timing. A Chinese or translated subtitle is never source-language evidence.

## SH-SRC-003 — Evidence by dimension

- Timing: sampled same-video embedded timing; actual audio/waveform/shots; exact-cut external subtitles; other releases only for comparison.
- Source text: matching official subtitle/script; listening-confirmed transcription; multiple independent transcriptions; translations only as aids.
- Chinese: every existing version is a candidate translation. Resolve conflict against actual source meaning, not majority vote.

Embedded source-language subtitles may provide source text and timing. Embedded non-source-language subtitles provide timing/layout and auxiliary translation/disambiguation only.

## SH-SRC-004 — Source-text conflicts

Prefer matching official same-language subtitles/scripts, then listening-confirmed text and independent transcriptions. Official captions may be condensed, censored, hearing-impaired, or from another cut; resolve conflicts against actual target audio and record the decision.

## SH-TRANS-002 — Translation objective

Preserve information and attitude first, make modern Simplified Chinese understandable in one viewing second, then preserve voice/rhythm/humor. For high-risk changes record timestamp, audio, available source text, context/image, and Chinese decision. If evidence is insufficient, use the most neutral defensible wording and state the limitation.

Compress only for a genuine reading/layout need and never remove negation, qualification, names, quantities, direction/order/causality, plot terms, register, jokes, or reveal order.

## SH-ZH-002 — Chinese punctuation

- Ordinary dialogue omits commas and final full stops; use one ASCII space for a natural internal pause.
- Use `？` for questions and `！` only for necessary force; never stack them.
- Use `……` for hesitation/trailing meaning and `——` for interruption.
- Use `：` only for a clear label, quotation, or explanation. Use `“”` and nested `‘’`.
- `、` is allowed only where a list would otherwise be ambiguous. Formal documents, code, signs, or reproduced on-screen text may preserve source punctuation.

## SH-ZH-003 — Spacing, characters, and notes

Use one ASCII space at a semantic boundary between Chinese and Latin/Greek letters or Arabic numerals; do not split codes such as `EX178` or `α-1`. Do not pad line edges or spaces around Chinese punctuation. Prefer Chinese numerals for ordinary small approximations and ASCII numerals for exact measurements, dates, models, and coordinates. Use confirmed series forms and `·` where a foreign personal name needs separation.

Notes are exceptional: only for plot-relevant comprehension loss that natural translation cannot solve, and they must be brief, non-editorial, non-obstructive, and project-defined.

## SH-TRANS-007 — Series terminology

Each series has one `series-guide.md` with stable `term_id`, source form, canonical Simplified Chinese, variants, scope, evidence, and status. Research only unresolved additions/conflicts. A project deviation is a confirmed `project.yaml` override citing the term, exact scope, evidence, confirmer, and date.
