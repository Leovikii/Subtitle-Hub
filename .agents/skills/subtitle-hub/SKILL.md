---
name: subtitle-hub
description: Initialize, audit, proofread, build, validate, or release Subtitle Hub projects and Chinese-primary ASS subtitles. Use for repository work involving identity, sources, translation, timing, layout, control files, or releases.
metadata:
  version: "1.5.0-beta.2"
---

# Subtitle Hub

This Skill is the repository standard. Do not reconstruct rules from history or re-query external platform guides during routine work.

## Route by task

- Intake or initialization: [project-initialization.md](references/project-initialization.md).
- Translation, Chinese, terminology, plans, approval, or records: [proofreading-and-approval.md](references/proofreading-and-approval.md).
- Timing, styles, fonts, static audit, or visual review: [timing-style-and-qc.md](references/timing-style-and-qc.md).
- Workspace, candidate, promotion, package, or release: [release-and-workspace.md](references/release-and-workspace.md).

For an existing work read the nearest `series-guide.md` if present, then `project.yaml` and root `review.md`.

## Lifecycle

Before step 0, locate a compatible base Python from the Codex workspace runtime or the host, then run `scripts/setup_runtime.py --check`. If the shared runtime is absent or outdated, run `scripts/setup_runtime.py` with existing authorization or obtain only the permission required for the download and installation. Continue with the returned environment Python. Do not install into or modify system Python. If no base Python can run the initializer, report that single prerequisite and stop.

0. For an existing project, require project schema 9, review schema 3, and `initialization.skill_version: "1.5.0-beta.2"`. If any differ, upgrade that project to the current templates before audit, editing, build, validation, or release; never execute an older contract in place. Do not upgrade dormant projects proactively.
1. Inventory the Chinese baseline and available text. Probe tracks only for supplied video. Run the initializer's read-only dry run before proposing any developer-facing names. Present its checked series directory, project name, verified identity, scope, materials, episode map, timing authority, and release languages in one initialization confirmation.
2. Recheck the approved dry-run digest and run the transactional initializer with that digest. Scan the full subtitle scope for term candidates, admit only forms that need a consistent rendering, and index their canonical names in `series-guide.md` using only Wikipedia's Mainland Simplified Chinese view (`/zh-cn/`). Pass `--ready-for-proofreading` before line-by-line proofreading. Follow [SH-TRANS-007](references/proofreading-and-approval.md#sh-trans-007--glossary-before-proofreading) for admission rules, search limits, and late discoveries.
3. Audit the complete scope without editing masters. For A/B evidence use the reviewed mapping contract in `proofreading-and-approval.md`. Time overlap never closes meaning. Process large scopes in bounded internal batches, put the complete categorized proposal in `review.md`, and list every semantic edit separately. Obtain approval for proposed edits before implementation.
   Use the alignment tool's `status`, paged `read`, and ID/character-cut `decide` commands; extract unchanged original text locally instead of regenerating it in tool arguments. After interruption inspect saved progress before retrying. See `SH-TRANS-011` for limits and recovery.
4. Record the user's proposal decisions and set `review.md` to `implementing` before writing approved master edits, applying bilingual projection, or building the release candidate. Update the same rows, verify the complete Noto master (including non-overlapping ordinary cues within each language), and proceed without routine interruptions. Follow SH-CTRL-007 for a completed review with zero proposed edits.
5. Present one complete, verified release candidate for final review when release is in scope. Promote only after the user approves that candidate.

## User decisions and continuation

Within the requested scope, keep working through discovery, tool calls, recoverable failures, and internal batches until the next required user decision or the requested deliverable is complete. Use progress updates while continuing. Dry-run, material and glossary readiness, successful batches, routine validation, and candidate preparation are internal checks. Reuse approval already given for the same concrete decision.

The routine user decisions are initialization (SH-INIT-005), the complete edit proposal (SH-CTRL-007), and release-candidate final review (SH-REL-006). Wait only for one of these decisions or when an essential fact, authorization, first-use SSH trust or credential interaction, material scope change, unresolved core terminology choice, or required P1 waiver cannot be resolved with the available evidence and permissions. Keep each wait to the dependent work. Complete other authorized work first and collect related decisions in one request. General authorization to work autonomously permits routine work within scope. Approval of specific edits and the release candidate requires review of their concrete details.

On failure, inspect saved state and the exact error, recover with authorized inputs, and continue from the first unfinished step. Apply an in-scope fallback when it preserves the approved scope and evidence claims. If a current prerequisite genuinely prevents further progress, report what finished, the exact blocker, and the single next action that would unblock it. Record this in `review.md` when the project exists. Keep unverified coverage pending.

## Authority and boundaries

Priority: current user instruction; confirmed `project.yaml` overrides; confirmed series terminology; this Skill; the single style basis in `timing-style-and-qc.md`.

- The initializer, readiness check, proposal decision, and final review are required at their respective stages. Use the Skill's checked entry points for initialization, alignment, and candidate builds. An informal hand-built project, a passed structural check, or an agent-written status cannot substitute for the required checks or user decisions.
- `project.yaml` is durable project truth. `review.md` is the sole current state, proposal, decision, result, and verification surface; Git preserves closed history.
- Keep `project/sources/` immutable. Edit only workspace masters, never `subtitles/current/`.
- Review every visible Chinese event. Evidence shortage lowers the tier; sampling never proves completion. Automated findings remain candidates unless structure proves the defect.
- Use text first and media only for a concrete unresolved timing, special-subtitle, local-layout, or scene-context point. Never imply unperformed listening, viewing, or human review.
- Use only the shared `~/.codex/subtitle-hub/` runtime and state root; never create per-project environments or dependency copies.
- For user-declared SSH video, use only `scripts/remote_media.py` with its pinned ED25519 host key and dedicated identity. During SSH initialization accept the password once through its local graphical prompt, use it only in that Python process to enroll the public key, and never request it during later media actions. Never put it in chat, arguments, environment variables, files, or project records. Never install remote tools, upload media, write remote outputs, or broaden approved paths.
- Create paths with their first file. `temp/` permits only on-demand `tools/` and `notes/`; never create archives, logs, intermediates, screenshot trees, audit sidecars, copied shared tools, or project reports.
- Keep only `project.yaml` and root `review.md` as project control files. Intake, mappings, raw audits, frames, waveforms, and renders are disposable system-temp data.
- Keep visual evidence local. Only at explicit user request show at most two compressed screenshots for one point.

## Chinese-primary invariant

Every master and release uses `Noto Sans CJK SC/JP` globally across retained styles and nonempty inline fonts. Normalize other properties only for declared ordinary dialogue. Preserve the position, size, color, motion, karaoke, and effects of notes, signs, songs, titles, credits, broadcasts, and other special subtitles unless a concrete defect is confirmed.

Ordinary bilingual output uses one primary and one secondary event per cue with identical start/end times. Review semantic split/merge mappings separately from output pairs; special subtitles keep their independent timing. See `SH-LAYOUT-002` for the full contract.
