# Proofreading, approval, and project records

## SH-CTRL-003 — Two durable control files

An active work keeps exactly `project.yaml` and root-level `review.md` as control files.

`project.yaml` records durable identity, scope, languages, sources/roles, video map and timing authority, ordinary-style profile, limitations, initialization approval, and confirmed overrides. Fixed paths, release mechanics, and Action configuration belong to this Skill, not each project. An override cites a stable rule ID, scope, rationale/evidence, confirmer, and date; a terminology deviation also cites the series `term_id`.

`review.md` schema 3 keeps one `status` (`planning`, `awaiting-approval`, `implementing`, `final-review`, `released`, or `blocked`), current scope, releases, episodes, and coverage. Coverage records evidence tier, timing authority, the selected alignment source, master/source fingerprints, Chinese/source denominators, static-layout coverage, applicable human reviews, and unresolved P0/P1. Media questions live in proposal rows, not duplicate counters. Git preserves closed rounds; replace closed detail when a new round begins instead of accumulating an archive.

## SH-CTRL-007 — Proposal and approval gate

Analyze without modifying masters. In `review.md`, use categorized tables with `item_id`, episode/time or bounded scope, category, before, proposed result, evidence/rationale, severity/risk, decision, status, actual result, and verification. Initial proposal rows use pending/awaiting approval; update the same rows after feedback, implementation, verification, final review, and release.

List every retranslation, dialogue deletion/addition, meaning correction, and context-sensitive terminology change separately. Batch only deterministic same-category work such as confirmed surface forms of one entity, punctuation rule, or ordinary-dialogue style mapping; state every matched form, its count, episodes, exclusions, and examples. A full name does not authorize substring replacement: a short name, surname, nickname, or name-plus-title joins the batch only after its entity and canonical form are confirmed. Never hide semantic edits in a batch.

Ask once for the complete, categorized proposal. Record the user's decisions on the corresponding rows before moving to `implementing`. If the full review produces no proposed edits, record the zero-edit result and enter `implementing` only for any requested derived assembly or candidate build. `align_bilingual.py apply` and the candidate builder require `implementing`. Defer unapproved work. If new work is essential for release, finish unaffected work and request a decision for the changed items only. Documentation or tooling edits explicitly requested by the user can proceed under that authorization.

## SH-TRANS-008 — Full-text coverage contract

Count every visible Chinese Dialogue event in the release scope, excluding only documented non-content automation/templates or exact duplicates that will not render. Record `chinese_in_scope = chinese_reviewed + chinese_excluded`; every exclusion needs a bounded rule and count. A changed master fingerprint invalidates prior coverage.

For A/B evidence, also account for every source-text unit in both directions. Record `source_in_scope = source_aligned + source_excluded + source_unresolved`; source exclusions are bounded special text, never ordinary dialogue. Chinese-to-source review catches unsupported additions and meaning changes; source-to-Chinese review catches omissions and excessive compression. One-to-many, many-to-one, and cross-event alignment are valid when meaning, order, timing, and layout remain complete. Time alignment raises candidates but never proves semantic resolution. Record unresolved units explicitly; zero issue rows never substitutes for coverage counts.

Use `scripts/align_bilingual.py plan` for A/B ordinary-dialogue coverage. It creates a disposable system-temp manifest and bounded packets; every ordinary Chinese and source unit must belong to exactly one monotonic reviewed group. Candidate groups start pending and may be split or joined inside the reviewed packets when time overlap grouped unrelated speakers or special text; unit uniqueness and order remain mandatory. Confirm each group only after checking speaker, action, object, reference, polarity, number, causality, information gain/loss, register, terms, and necessary context. A source-only special item may use `excluded-special` with a reason; ordinary Chinese without source or ordinary source without Chinese remains unresolved. A 1:N, N:1, or N:N confirmation needs a short split/merge rationale.

Never use time overlap, nearest time, the prior translation, or an auxiliary translation to auto-confirm or fill Chinese. `align_bilingual.py apply` may project only source text from a fully reviewed mapping and must leave every Chinese event unchanged. For bilingual output, each confirmed group produces one secondary event per Chinese event on its exact start/end. Resolve any overlap between ordinary Chinese cues on the reviewed shared timeline first (SH-LAYOUT-002); apply preflights every episode and fails before writing masters, rather than copying the overlap into the second language or silently trimming it. A single Chinese event joins the source units in order. Multiple Chinese events require reviewed `secondary_cuts`: ascending, zero-based Python Unicode character offsets into the source-unit texts joined by one ASCII space, one cut per Chinese boundary. The tool slices the original locally and trims edge whitespace; no source words need to be rewritten by the model. For example, two Chinese cues use `secondary_cuts: [12]` only if offset 12 was actually reviewed as their semantic boundary. Existing `secondary_texts` remains readable for reviewed records; do not generate new full-text lists, and never specify both fields. The combined visible text must preserve the source character sequence except whitespace; it may not add, omit, duplicate, reorder or paraphrase source words. Review every cut semantically, including word boundaries; character preservation alone never proves meaning. Source coverage counts original source units, not output events. After approved Chinese or timing corrections, regenerate the mapping before apply/verify. Run `verify` against the final master; write its selected `alignment_source_id`, `alignment_verified: verified`, denominators, exclusions, unresolved count, master/source fingerprints, and material findings to `review.md`, then remove the disposable session after candidate verification. A changed master or selected source fingerprint invalidates the claim.

For C/D evidence, the Agent still reviews every Chinese event for grammar, wording, consistency, punctuation, segmentation, timing code, and static layout, but cannot mark source fidelity complete. A source-language-capable human must perform full-meaning review before that claim or release gate can pass.

Review ordinary names, brands, and cultural references in their subtitle context under the same coverage denominators. Apply the terminology inventory to core terms admitted by SH-TRANS-007. For A/B evidence, account for every source mention of each admitted term and its aligned Chinese rendering. In every tier, account for all observed forms of the admitted term. In the relevant `review.md` row record the surface forms, counts, scope, exclusions, and unresolved hits. Claim terminology completion when forbidden and unclassified hits for the admitted terms are both zero.

## SH-TRANS-009 — Executable Chinese quality standard

- **Faithfulness:** no mistranslation, omission, unsupported addition, polarity/number/person/object/causality error, term drift, censorship or unjustified compression.
- **Clarity:** grammatical, unambiguous, natural modern Simplified Chinese that can be understood in one viewing; repair typos, collocation, reference, logic, punctuation and segmentation.
- **Voice:** preserve register, relationship, attitude, rhythm, humor and reveal order after faithfulness and clarity are secure; elegance never licenses invention.
- **Continuity:** keep names, terms, honorifics, quantities, time references and recurring phrasing consistent across the complete scope.

An auxiliary translation is a disambiguation witness only. Use it when source wording remains ambiguous, record material conflicts, and never decide by majority vote.

## SH-TRANS-011 — Bounded full-scope batches

For a large scope, partition the complete chronological range into non-overlapping coverage batches before review; do not batch only discovered problems. `plan` defaults to at most 16 groups and 6000 visible Chinese/source characters per packet (`--batch-size`, `--batch-chars`); one oversized group remains intact, is marked `requires_paging`, and must be read in pages. Neighbor context is limited to one group per side and is loaded only when needed. Do not dump complete packets, masters, long review tables, or auxiliary translations into tool output. Load a matching auxiliary window only for a concrete unresolved ambiguity.

Use the existing tool instead of disposable readers/decision scripts:

```text
align_bilingual.py status PROJECT --session SESSION
align_bilingual.py read PROJECT --session SESSION --group-id G000001 --side source --offset 0 --max-chars 2400
align_bilingual.py read PROJECT --session SESSION --group-id G000001 --side chinese --offset 0 --max-chars 2400
align_bilingual.py decide PROJECT --session SESSION --batch-id B0001 --decisions DECISIONS_JSON
```

`status` returns counts and the next unfinished batch IDs without subtitle text; it checks live input identity and requires valid bilingual segmentation before marking a batch complete. `read` returns at most 4000 text characters and 20 intersecting unit metadata records, with absolute character spans, speaker/style/time fields, and `next_offset`. Read both sides through `next_offset: null` before confirming; pagination is not permission to sample. The source side uses the exact character coordinate system of `secondary_cuts`. Context groups can be read by ID as needed from the neighboring packet.

The disposable UTF-8 decision file contains only changed decisions, for example `{"groups":[{"group_id":"G000001","status":"confirmed","rationale":"reviewed semantic split","secondary_cuts":[12]}],"risks":[]}`. `decide` accepts only IDs, status, rationale, and cuts; it validates every supplied decision before atomically replacing that one packet, leaves source/unit data untouched, and reports counts/status without echoing text. Source-only exclusions and duplicate-risk dispositions use the same command. Split/join mapping groups locally when necessary, preserving the original unit dictionaries and uniqueness/order; then use `decide` for the decisions. Write only necessary Chinese corrections and brief evidence in `review.md`, not long original passages. Do not retype unchanged source passages into shell arguments, patches, JSON decisions, or chat; use IDs/offsets and local extraction. These measures reduce unnecessary transcription and output volume, not platform content checks, and cannot guarantee that a stream will never be blocked.

Finish a batch by writing its material proposal rows to `review.md` and marking only its input hash, denominator, completion, and row IDs in the disposable manifest. Do not reread a completed batch after context compaction or truncated output unless its input changed, a cross-boundary conflict appears, or verification fails. A truncated batch remains incomplete and resumes at its first unfinished unit.

After an interrupted or blocked stream, inspect saved files and run `status` before retrying; a disconnect does not roll back successful commands. Do not replay the same long output or assume reconnection will fix a content block. Resume at the first unconfirmed group/risk in the reported batch, retaining valid decisions; if a platform block persists on the necessary bounded work, record the limitation and stop that operation rather than repeatedly resubmitting or claiming completion. During a Skill upgrade preserve old disposable records until compatible decisions have been checked against the current inputs; do not relabel an old manifest as the new Skill version or discard prior reviewed work blindly.

After all batches, run one global denominator, ordering, duplicate-risk, and terminology-continuity check. For proposed edits, set `awaiting-approval` and give the user a categorized summary and the `review.md` path. Follow SH-CTRL-007 for implementation and SH-REL-006 for release-candidate approval.

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

## SH-TRANS-007 — Glossary before proofreading

**Scan subtitles first.** Run one local candidate pass across every mapped episode's available source text and visible Chinese dialogue and on-screen text. Start with original names, places, organizations, titles, and setting words, including source names omitted in Chinese. Deduplicate occurrences, collect observed Chinese renderings, and read only enough nearby cues to identify each plausible core candidate. Machine extraction supplies candidates. This pass leaves subtitle text and line-by-line coverage unchanged.

**Decide which terms need a canonical form before searching.** Admit an observed candidate only when its referent or meaning is identifiable and inconsistent rendering would affect identity, plot comprehension, or continuity. Typical entries are major or recurring characters, plot-relevant aliases and titles, distinctive places and organizations, and named setting concepts, items, or abilities. A one-off alias that matters to a reveal qualifies. Count occurrences to prioritize review. Capitalization and frequency alone do not establish a need for an index entry.

Exclude these classes by default: ordinary personal names and passing celebrity references, real-world locations, companies and brands, generic titles and everyday concepts, credits and incidental signage, and transient nicknames or jokes. Reinstate a candidate only when the subtitle context establishes a concrete admission reason. For example, an actual company central to a documentary or a real location that identifies a recurring scene can qualify. Resolve one-cue names and uncertain low-impact candidates during formal proofreading. Record one short reason per admitted term. The default exclusions apply as a class, so skip web lookup and per-name exclusion records for the rest.

**Build the canonical index.** When core terms qualify, reuse or create the single `series-guide.md` in the series directory. Use `term_id`, `原文`, `规范简体中文`, `变体`, `范围`, `入表理由`, `证据`, and `状态`. Retain stable IDs and scope work-only terms to that work. Use only Wikipedia's Mainland Simplified Chinese view at `https://zh.wikipedia.org/zh-cn/…` for the canonical index, including inherited terms used for this project, variants adopted as canonical, and project overrides. Verify that the rendered article is in the mainland variant and explicitly uses the selected form for the same entity, work continuity, and meaning. Use the mainland rendering in the article. A form that the article identifies as a different region's translation supplies context only. Cite the direct `/zh-cn/` link with `zh-Hans wikipedia`, the section, and the observed form. During an upgrade, reopen old references in `/zh-cn/` and check the wording before updating the glossary. Search snippets, other locale variants, and cited external pages cannot supply wording missing from the mainland article.

1. Start with the work's article when available. Use its names to identify already observed candidates. Open related articles only for admitted terms whose evidence is missing, ambiguous, or conflicting.
2. Across the initial project preflight, open at most five distinct related articles beyond the work's article. Reuse those pages across terms. For each term, examine at most three of the additional articles and make at most one targeted search restricted to `zh.wikipedia.org`. Search with the observed original name and the work or franchise name. Directly related works, the shared setting, and the entity's own article are eligible.
3. Stop when the correct entity and form are supported and any material conflict is resolved, or when the limit is reached. Skip recursive link-following, category browsing, and harvesting franchise-wide entity lists. Cross-check only the candidate and omit names absent from the approved subtitle scope.

Record unresolved core terms and checked articles in `review.md`. On resume, count prior checks toward the same limits. Finish the other terms before asking once for a specific `/zh-cn/` Wikipedia article or a decision between forms attested in that variant for any remaining core conflicts that block the requested step.

Settle evidence-backed decisions automatically. A deviation from confirmed series usage requires user confirmation, a scoped `project.yaml` override, and Mainland Simplified Chinese Wikipedia evidence for its adopted form. Proceed directly after saving the completed, sourced table.

**Pass the gate and begin formal proofreading.** In the existing `review.md`, record the episodes scanned in `terminology_preflight.episodes`, the selected core IDs in `term_ids`, and the scanned texts, selection rationale, and evidence limits in `evidence`. List every admitted initial term. An empty list requires evidence of the full scan and a finding that no core term qualifies. Run `validate_project.py PROJECT --ready-for-proofreading` before creating or starting any formal review session. The gate checks full project scope, the scan record, admission reasons, confirmed forms, and allowed Wikipedia links for the selected IDs. Unresolved admitted terms block the initial gate. Ordinary names are handled during line-by-line proofreading. The reviewer verifies referents, wording, and actual scan coverage.

For a person or other entity, `variants` is a form-to-entity inventory rather than a loose synonym list. Scan the complete available source and Chinese scope and record each form that actually occurs: full name, given name, family name, nickname, and title/honorific combination when applicable. Distinguish approved Chinese forms from forbidden or unresolved forms. Do not invent unused variants or derive a short form by blindly truncating a full name; use aligned source text, dialogue context, or other confirmed identity evidence where a form could name more than one entity. Keep temporary occurrence lists outside the project and write only the durable mappings to `series-guide.md` and the current decision/counts to `review.md`.

If line-by-line review reveals a new candidate, apply the same admission test. Record a qualifying unresolved issue in `review.md` with its affected cues. Keep affected groups pending when the ambiguity prevents a reliable review, and continue elsewhere. Once resolved, update the glossary and add the confirmed ID to the review record. Recheck affected occurrences before completing coverage. Retain the initial preflight evidence for resume.

## SH-TRANS-010 — Entity surface-form closure

Before proposing or verifying a terminology batch, search both directions: known source aliases to their Chinese renderings, and every known approved/forbidden Chinese form across all visible Chinese events. Expand the inventory when this search exposes an unlisted partial name, surname-only use, nickname, title combination, spelling variant, or typo. Confirm its entity before changing it; ambiguous hits remain separate proposal rows.

After implementation, repeat the same full-scope searches against the changed master. Verification must show the per-form before/after counts, zero forbidden forms, and zero unclassified entity forms or list each unresolved hit explicitly. “Full name replaced”, “exact old string absent”, and a clean scan limited to previously listed forms are insufficient evidence of terminology completion.

Use `scripts/audit_terms.py --terms <temporary-manifest.json> <masters...>` for the reproducible part of both scans. The disposable schema-1 manifest contains a nonempty `terms` array; each item has a unique `term_id`, a nonempty `approved_forms` array, a `forbidden_forms` array, and optionally a `source_forms` array. Declare only evidence-confirmed literal forms. The command counts visible Dialogue occurrences and exits 2 while any forbidden Chinese form remains. Keep the manifest and raw JSON outside the project; summarize the form set, counts, scope, exclusions, and command result in the existing `review.md` row.

The audit proves coverage for declared literal forms. Inspect source-to-Chinese alignment for the admitted terms across the full scope. Expand the manifest when their observed forms change. Keep ambiguous forms unresolved until their contexts establish the entity.
