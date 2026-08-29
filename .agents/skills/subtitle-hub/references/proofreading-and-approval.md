# Proofreading, approval, and project records

## SH-CTRL-003 — Two durable control files

An active work keeps exactly `project.yaml` and root-level `review.md` as control files.

`project.yaml` records durable identity, scope, languages, sources/roles, video map and timing authority, ordinary-style profile, limitations, initialization approval, and confirmed overrides. Fixed paths, release mechanics, and Action configuration belong to this Skill, not each project. An override cites a stable rule ID, scope, rationale/evidence, confirmer, and date; a terminology deviation also cites the series `term_id`.

`review.md` schema 3 keeps one `status` (`planning`, `awaiting-approval`, `implementing`, `final-review`, `released`, or `blocked`), current scope, releases, episodes, and coverage. Coverage records evidence tier, timing authority, master fingerprints, Chinese/source denominators, static-layout coverage, applicable human reviews, and unresolved P0/P1. Media questions live in proposal rows, not duplicate counters. Git preserves closed rounds; replace closed detail when a new round begins instead of accumulating an archive.

## SH-CTRL-007 — Proposal and approval gate

Analyze without modifying masters. In `review.md`, use categorized tables with `item_id`, episode/time or bounded scope, category, before, proposed result, evidence/rationale, severity/risk, decision, status, actual result, and verification. Initial proposal rows use pending/awaiting approval; update the same rows after feedback, implementation, verification, final review, and release.

List every retranslation, dialogue deletion/addition, meaning correction, and context-sensitive terminology change separately. Batch only deterministic same-category work such as confirmed surface forms of one entity, punctuation rule, or ordinary-dialogue style mapping; state every matched form, its count, episodes, exclusions, and examples. A full name does not authorize substring replacement: a short name, surname, nickname, or name-plus-title joins the batch only after its entity and canonical form are confirmed. Never hide semantic edits in a batch.

After approval, implement and verify the approved scope continuously through a complete release candidate. New semantic work outside scope is added as pending and deferred unless release-blocking. Documentation/tooling changes explicitly requested by the user need no second approval round. Never create a separate feedback or completion report.

## SH-TRANS-008 — Full-text coverage contract

Count every visible Chinese Dialogue event in the release scope, excluding only documented non-content automation/templates or exact duplicates that will not render. Record `chinese_in_scope = chinese_reviewed + chinese_excluded`; every exclusion needs a bounded rule and count. A changed master fingerprint invalidates prior coverage.

For A/B evidence, also account for every source-text unit in both directions. Chinese-to-source review catches unsupported additions and meaning changes; source-to-Chinese review catches omissions and excessive compression. One-to-many, many-to-one, and cross-event alignment are valid when meaning, order, timing, and layout remain complete. Time alignment raises candidates but never proves semantic resolution. Record unresolved units explicitly; zero issue rows never substitutes for coverage counts.

For C/D evidence, the Agent still reviews every Chinese event for grammar, wording, consistency, punctuation, segmentation, timing code, and static layout, but cannot mark source fidelity complete. A source-language-capable human must perform full-meaning review before that claim or release gate can pass.

Terminology coverage is part of these same denominators, not a separate report. For A/B evidence, account for every source mention of a confirmed entity and its aligned Chinese rendering; for every tier, assign each observed Chinese proper-name form to a confirmed `term_id`, a documented exclusion, or an unresolved proposal. Replacing and scanning only the full name never closes the term. In the relevant `review.md` row record the checked surface-form set, per-form counts, scope, ambiguous exclusions, and remaining forbidden or unclassified hits. Claim terminology completion only when forbidden and unclassified hits are both zero within the declared scope.

## SH-TRANS-009 — Executable Chinese quality standard

- **Faithfulness:** no mistranslation, omission, unsupported addition, polarity/number/person/object/causality error, term drift, censorship or unjustified compression.
- **Clarity:** grammatical, unambiguous, natural modern Simplified Chinese that can be understood in one viewing; repair typos, collocation, reference, logic, punctuation and segmentation.
- **Voice:** preserve register, relationship, attitude, rhythm, humor and reveal order after faithfulness and clarity are secure; elegance never licenses invention.
- **Continuity:** keep names, terms, honorifics, quantities, time references and recurring phrasing consistent across the complete scope.

An auxiliary translation is a disambiguation witness only. Use it when source wording remains ambiguous, record material conflicts, and never decide by majority vote.

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

When a series has cross-project terms, keep one `series-guide.md` with stable `term_id`, source form, canonical Simplified Chinese, variants, scope, evidence, and status. Do not create an empty guide. Research only unresolved additions/conflicts. A project deviation is a confirmed `project.yaml` override citing the term, exact scope, evidence, confirmer, and date.

For a person or other entity, `variants` is a form-to-entity inventory rather than a loose synonym list. Scan the complete available source and Chinese scope and record each form that actually occurs: full name, given name, family name, nickname, and title/honorific combination when applicable. Distinguish approved Chinese forms from forbidden or unresolved forms. Do not invent unused variants or derive a short form by blindly truncating a full name; use aligned source text, dialogue context, or other confirmed identity evidence where a form could name more than one entity. Keep temporary occurrence lists outside the project and write only the durable mappings to `series-guide.md` and the current decision/counts to `review.md`.

## SH-TRANS-010 — Entity surface-form closure

Before proposing or verifying a terminology batch, search both directions: known source aliases to their Chinese renderings, and every known approved/forbidden Chinese form across all visible Chinese events. Expand the inventory when this search exposes an unlisted partial name, surname-only use, nickname, title combination, spelling variant, or typo. Confirm its entity before changing it; ambiguous hits remain separate proposal rows.

After implementation, repeat the same full-scope searches against the changed master. Verification must show the per-form before/after counts, zero forbidden forms, and zero unclassified entity forms or list each unresolved hit explicitly. “Full name replaced”, “exact old string absent”, and a clean scan limited to previously listed forms are insufficient evidence of terminology completion.

Use `scripts/audit_terms.py --terms <temporary-manifest.json> <masters...>` for the reproducible part of both scans. The disposable schema-1 manifest contains a nonempty `terms` array; each item has a unique `term_id`, a nonempty `approved_forms` array, a `forbidden_forms` array, and optionally a `source_forms` array. Declare only evidence-confirmed literal forms. The command counts visible Dialogue occurrences and exits 2 while any forbidden Chinese form remains. Keep the manifest and raw JSON outside the project; summarize the form set, counts, scope, exclusions, and command result in the existing `review.md` row.

The audit proves coverage only for declared literal forms. It cannot discover an unknown alias, resolve a shared surname, align meaning, or prove translation quality. Inspect source-to-Chinese alignment and Chinese proper-name candidates across the full scope, expand the manifest when a new form is found, and keep ambiguous forms unresolved rather than forcing them into a deterministic batch.
