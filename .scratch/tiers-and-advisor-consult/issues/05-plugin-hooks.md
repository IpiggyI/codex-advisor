# 05: Plugin hooks: posture injection and per-dispatch verification

**What to build:** Hooks shipped with the plugin, doing two things:
- inject the primary's posture variant at every session start;
- verify every native dispatch's actual model and effort automatically, surfacing a mismatch to the primary.

No hook runs on the primary's `Stop` or a worker's `SubagentStop`, and no hook keeps any record beyond one session. The user cancelled AC-9 on 2026-09-26 and authorized continuation to ticket 06 with this retained scope. Workers still follow the canonical consultation posture.

**Blocked by:** 01 (hook capabilities on this Codex version, including the P5 rows that need trusted running hooks), 02 (canonical posture text), 03 (routing profile and entries, for the AC-5 comparison and the AC-10 expectations), 04 (consultation result validation).

**Status:** resolved

## Required reading before starting

- `spec.md`: AC-5, AC-8, AC-9, AC-10, AC-11, AC-12, EN-5 (last bullet), DR-5 (ticket 05 section), DR-9 (the hooks field), X-2, X-3, §Decision Boundaries, §Open Decisions (O3, O4), §Stop and Return (S5, S6, S9), §Testing Decisions items 3 and 6, §Goal-Drift Checks.
- `sources.md` §2.4 rows D8, D20, D27, D29, D30, D31, D33, D42. The originals behind these rows (Part 1 U5, U6, U10) are traceability only and are not required reading.
- `acceptance.md` §01 P5 (hook capabilities on this Codex version) and §04 (consultation observability).
- `plugins/codex-advisor/skills/orchestration/references/consult-posture.md` (the injected text, unmodified).
- `plugins/codex-advisor/skills/orchestration/references/routing-profile.md` (advisor model per caller, for the AC-5 comparison; expected dials for AC-10).
- `references/operations.md` §Process consultation (from ticket 04).
- Codex Hooks documentation <https://learn.chatgpt.com/docs/hooks>, re-read and date-stamped.

## Owns

- The plugin's hook files and scripts under `plugins/codex-advisor/`.
- The `plugin.json` `hooks` field, if the default location is not used.
- A `verify.sh` hooks group, included in the unqualified run.
- The new §Hooks in `references/operations.md`, the hooks group in §Verify changes, and their twins.

## Acceptance

- [x] **`SessionStart`.**
  - It selects the variant by comparing the session's model id with the advisor model id AC-4 assigns to the primary, and injects exactly that `consult-posture.md` block plus the adoption rules, byte-equal.
  - Tests: `gpt-6-astra` gets reduced; `gpt-6-sol` gets full; `gpt-5.6-terra` gets full; the resumed-session case is covered.
  - If ticket 01 found that it fires in subagent sessions, subagents receive nothing from it.
- [x] **No primary `Stop` or worker `SubagentStop` hook** exists (D30 and the AC-9 cancellation).
- [x] **AC-10 route.**
  - A dispatch whose actual model and effort match the expected ones is silent.
  - A mismatched model, a mismatched effort, and a caller-effort entry spawned without an effort are each surfaced to the primary in the same session without a manual inspector run.
- [x] **AC-11.**
  - The only state written lives in a per-session temporary location and is deleted at session end, or cannot be read by any later session.
  - Nothing is written to the repository or `CODEX_HOME`, and nothing is aggregated.
  - Record each file-write site in the hook code and where it writes.
- [x] The hooks group in `verify.sh` covers every case above at the hook command-line boundary, with pinned JSON fixtures. Each blocking or surfacing case also has a negative proof: the hook disabled or its condition inverted makes the test fail.
- [x] **AC-12.** Nothing in the plugin, installer, or docs marks hooks trusted, edits trust state, or passes `--dangerously-bypass-hook-trust`. The §Hooks section of `operations.md` states the `/hooks` review for first install and for updates that change hooks.
- [x] Live check (`acceptance.md` §05), in a temporary `CODEX_HOME` with the plugin and entries installed. Every row records its trust state: trusted through `/hooks`, bypassed (only if O4 allows it), or untrusted.
  - [x] untrusted after install: the hooks are skipped and the host's `/hooks` warning appears;
  - [x] at least one run with hooks the user trusted through `/hooks`, showing the injection works without any bypass;
  - [x] the primary sees its injected variant in a new and in a resumed session;
  - [x] a caller-effort entry spawned without an effort is surfaced;
  - [x] after the sessions end, no per-session state remains.

## Verification

- `sh plugins/codex-advisor/scripts/verify.sh` (all groups)
- `python3 tests/test_zh_mirror.py`
- `git diff --check`
- The live table in `acceptance.md` §05

## Stop conditions

S5, S6, S8, S9. Do not replace a missing hook capability with a primary `Stop` hook or with skill-only text.

## Not in this ticket

README, the manual, the version bump, and any logging or statistics.

## Comments

Resolved on 2026-09-26 after primary verification and fresh independent senior
acceptance. See `../acceptance.md` section 05 and Final acceptance for
evidence and limitations. D47 cancels finish blocking, D48 permits only a local
commit, and D49 waives only repetition of the final-definition manual trust test.
No push or real installation update was performed.
