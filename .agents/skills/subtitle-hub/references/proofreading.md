# Proofreading and Chinese standard

## SH-TRANS-001 — Review meaning before polish

Establish actual speech, then use matching source text, context, image evidence, series terminology, and confirmed decisions. Check speaker/object/action, negation, number, causality, omissions, additions, register, terminology, continuity, grammar, punctuation, segmentation, and timing. A Chinese or translated subtitle is never source-language evidence.

## SH-SRC-003 — Evidence by dimension

- Timing: sampled same-video embedded timing; actual audio/waveform/shots; exact-cut external subtitles; other releases only for comparison.
- Source text: matching official subtitle/script; listening-confirmed transcription; multiple independent transcriptions; translations only as aids.
- Chinese: every existing version is a candidate translation. Resolve conflict against actual source meaning, not majority vote.

Embedded source-language subtitles can provide source text and timing. Embedded non-source-language subtitles provide timing/layout and auxiliary translation/disambiguation only.

## SH-SRC-004 — Source-text conflicts

Prefer matching official same-language subtitles/scripts, then listening-confirmed text and independent transcriptions. Official captions may be condensed, censored, hearing-impaired, or from another cut; resolve conflicts against actual target audio and record the decision.

## SH-TRANS-002 — Translation objective

Preserve information and attitude first, make modern Simplified Chinese understandable in one viewing second, then preserve voice/rhythm/humor. For high-risk changes record timestamp → audio → source text when available → context/image → Chinese decision. If evidence is insufficient, use the most neutral defensible wording and state the limitation.

Do not mechanically keep or delete reactions such as “啊/嗯/哎/哦”; check the audio and function. Compress only for a genuine reading/layout need and never remove negation, qualification, names, quantities, direction/order/causality, plot terms, register, jokes, or reveal order.

## SH-ZH-002 — Chinese punctuation

- Ordinary dialogue omits commas and final full stops; use one ASCII space for a natural internal pause.
- Use `？` for questions and `！` only for necessary force; never stack them.
- Use `……` for hesitation/trailing meaning and `——` for interruption.
- Use `：` only for a clear label, quotation, or explanation. Use `“”` and nested `‘’`.
- `、` is allowed only where a list would otherwise be ambiguous. Formal documents, code, signs, or reproduced on-screen text may preserve source punctuation.

## SH-ZH-003 — Spacing, characters, and terms

Use one ASCII space at a semantic boundary between Chinese and Latin/Greek letters or Arabic numerals; do not split codes such as `EX178` or `α-1`. Do not pad line edges or spaces around Chinese punctuation. Prefer Chinese numerals for ordinary small approximations and ASCII numerals for exact measurements, dates, models, and coordinates. Use confirmed series forms and `·` where a foreign personal name needs separation.

Notes are exceptional: only for plot-relevant comprehension loss that natural translation cannot solve, and they must be brief, non-editorial, non-obstructive, and project-defined.

## SH-ZH-005 — Language quality and notes

Check grammatical roles, modifier scope, negation, rhetorical questions, conditionals, causality, reference continuity, command hierarchy, collocation, ambiguity, and offensive-force equivalence. Do not sanitize or intensify without evidence. Any permitted note follows the exception above.

## SH-TRANS-007 — Series terminology

Each series has one `series-guide.md` with stable `term_id`, source form, canonical Simplified Chinese, variants, scope, evidence, and status. Research only unresolved additions/conflicts. A project deviation requires a `project-guide.md` override citing the term, exact scope, evidence, and user confirmation.

## SH-PLAN-001 — Detailed proofreading plan

Before master edits, `review.md` must show categorized tables with item/batch ID, episode/time or exact bounded scope, category, before, proposed result, evidence/rationale, severity, and risk. Put the complete row history in `ledger.tsv`.

List every retranslation, dialogue deletion/addition, meaning correction, and context-sensitive terminology change separately. Batch only deterministic same-category work such as one exact confirmed term replacement, one punctuation rule, or one ordinary-dialogue style mapping; state match rule, count, episodes, exclusions, and examples. Never hide semantic edits in a batch. After implementation replace proposals with actual results and verification/remaining risk in the same report.
