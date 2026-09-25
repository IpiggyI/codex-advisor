# 01: Host probes and the consultation mechanism decision

**What to build:** Evidence, recorded in `acceptance.md` §01, that settles every host fact the rest of the spec depends on, plus the consultation mechanism decision written into spec §Mechanism decision. No plugin, documentation, script, or test file changes in this ticket.

**Blocked by:** None (can start immediately).

**Status:** resolved

## Required reading before starting

- `.scratch/tiers-and-advisor-consult/spec.md`: §Materials, §Authority and conflicts, TR-2, TR-3, AC-3, AC-4, AC-8, AC-9, AC-10, AC-11, AC-12, EN-5 (last bullet), X-1, X-2, §Mechanism decision, §Open Decisions (O4), §Stop and Return (S1–S6, S9), §Testing Decisions item 6, §Further Notes (assumptions).
- `.scratch/tiers-and-advisor-consult/sources.md` §2.4 rows D17, D20, D29, D31, D33, D34, D41, D42, D43, D44, D45.
- `plugins/codex-advisor/skills/orchestration/references/operations.md` §Install and discover (the temporary `CODEX_HOME` procedure) and §Invoke and validate (spawn shape, inspector usage).
- `.scratch/tier-role-pool/acceptance.md` §Live route check (method and record shape to reuse).
- `docs/adr/0004-tier-named-entries-first-round-pool.md` lines 29 and 47 (the precedence facts and their recheck trigger).
- Codex documentation, re-read now and record the read date: Hooks <https://learn.chatgpt.com/docs/hooks>, App Server <https://learn.chatgpt.com/docs/app-server>, Subagents <https://learn.chatgpt.com/docs/agent-configuration/subagents>.
- rpiv-advisor at commit `d74b1c99830a565f3df3f37e0a36616d17ffc574`: `advisor/execute.ts` and `advisor/context.ts`, for what "current effective context" means (post-compaction view, in-flight call stripped, user-role tail).

## Owns

- `acceptance.md` §01 (create the tables there).
- The §Mechanism decision block of `spec.md`: fill the decision and set its status line. Change nothing else in the spec. If a finding contradicts another spec line, stop (S8).
- Throwaway probe material lives in a temporary directory outside the repository and is deleted afterwards.

## Probes

Run every probe in a temporary `CODEX_HOME` per X-2, with parents at the cheapest setting except where X-2 says otherwise. For every spawn, record the command shape, the thread IDs, the observed model and effort from `inspect-agent-runtime.sh` (generic mode is fine for probe entries), and the Codex version.

1. **P1 Host version.** Record `codex --version` and the date.
2. **P2 Dial availability (TR-3, S1).** Run each distinct (model, effort) in TR-3 once and record the observed model and effort:
   - `gpt-6-luna`: `high`, `xhigh`, `max`
   - `gpt-6-sol`: `medium`, `high`, `xhigh`, `max`
   - `gpt-6-astra`: `low`, `medium`, `high`, `xhigh`

   Use per-spawn overrides with `fork_turns` set to `"none"`, or temporary probe templates in the temporary home.
3. **P3 Precedence on this version (S2).** Record three cases:
   - A probe template that pins `model` and `model_reasoning_effort`, spawned with conflicting per-spawn values.
   - A template that pins only `model`, spawned with a per-spawn effort.
   - A full-history fork (`fork_turns` omitted or `"all"`) with per-spawn overrides, to see what it inherits.
4. **P4 Consultation candidates (AC-3, S3, S4).** Test each configuration you try, and record every configuration you did not try as untested.
   - **A:** native spawn with a positive-integer `fork_turns` (at least `"1"` and one larger value) and a pinned probe advisor template.
   - **A':** App Server `thread/fork` (with and without `lastTurnId`), then `thread/resume` with a model override.
   - **B:** an MCP tool that locates the calling session's record, rebuilds the context, and calls `codex exec` with the advisor dial and tools disabled.

   Stay within D41: no configuration may read or send credentials itself. For each configuration, record:
   - **(a) Nonce.** In one turn, a tool call prints a random value, then the consultation runs in the same turn; the advisor must repeat the value.
   - **(b) Model and effort.** The actual model and effort equal the AC-4 dial.
   - **(c) Compaction.** Force a compaction, add a message, and consult; the advisor must see both the summary and the later message.
   - **(d) Tools.** The advisor has no tools. Show the actual tool set of the advisor request, as sent or as recorded by the host, and show that it is empty (D44). A refused tool attempt, one unavailable tool, or the advisor saying it has no tools does not count; read-only tools fail this check. If the host exposes no record of the tool set for a configuration, that configuration is unproven and not eligible.
   - **(e) Callers.** The consultation can be called from the primary, from a spawned worker, and from a spawned explorer.
   - **(f) Earliest context.** State a constraint in the first turn of a session, then add more uncompacted turns than any window the configuration uses, and consult. The advisor must report the constraint (D43). For a configuration with a bounded window, also record the rule that makes the window cover the whole current effective context in every session state, not only in this test.
5. **P5 Hooks (AC-8, AC-9, AC-10, AC-11, AC-12, S5, S6).** Use a temporary plugin install that ships hooks, through the `plugin.json` `hooks` field or `hooks/hooks.json`, installed only by the X-2 route (a throwaway copy of the checkout is allowed for probe hooks, so that no repository file changes). Record:
   - The trust state of every run: trusted by the user through `/hooks` in the temporary home, bypassed (only if the user decided O4 to allow it), or untrusted. A run without a recorded trust state is not evidence.
   - Untrusted plugin hooks: with the plugin freshly installed and nothing trusted, the hooks are skipped and the host prints its `/hooks` warning. Record both.
   - Plugin hooks load once trusted.
   - `SessionStart` input fields; its `additionalContext` reaches the model in a new session and in a resumed session.
   - Whether `SessionStart` also fires in subagent sessions (EN-5).
   - `SubagentStart` input fields, and whether the child's model and effort are present.
   - `SubagentStop` input fields; whether `{"decision": "block", "reason": …}` or exit code 2 makes the worker continue, and whether a loop-prevention signal exists.
   - `PostToolUse` input for the spawn tool, and whether it sees `agent_type`, `reasoning_effort`, and the child thread ID.
   - Whether `SessionEnd` exists for cleaning up per-session state.

   Rows that need trusted running hooks wait until the user decides O4 or trusts the hooks through `/hooks` in the temporary home. Such waiting rows do not block ticket 02, but they must be filled before ticket 05 starts. Never count an untrusted skip as S5 (spec AC-12).
6. **Cleanup.** Delete the temporary home, the credential copies, workspaces, probe templates, and logs. Record that you did.

## Acceptance

- [x] `acceptance.md` §01 has P1–P5 tables. Every row has observed values and thread IDs, or is marked untested with a reason.
- [x] Every S1–S6 and S9 condition is marked "not triggered" with the probe that shows it, or "triggered" with the evidence and a stop.
- [x] If no stop triggered, the spec's §Mechanism decision names the selected configuration and its five-check and caller evidence, gives the reasons for choosing it among the eligible ones, and has its status line changed from "pending ticket 01" to the date and the word "decided".
- [x] The documentation read dates are recorded next to the facts taken from each page.
- [x] Compared with the state recorded at ticket start (`git status --short` output plus the SHA-256 of every file in the task directory), the only files this ticket changed are `acceptance.md` and `spec.md`, and `git diff --stat` for tracked files is empty. Files that were already untracked at the start stay as they were: do not commit, move, or delete them to satisfy this check (D45).
- [x] The temporary home and credential copies are gone.

## Stop conditions

S1–S6 and S9 (spec §Stop and Return). On a stop, finish recording, leave §Mechanism decision as pending with the reason, and report to the user. Do not start ticket 02.

## Not in this ticket

Writing any runtime file, template, script, test, ADR, or README; the thirteen-entry route check (ticket 03).

## Comments

Resolved on 2026-09-26. The checked items record this ticket's acceptance
checkpoint; later tickets extend the intermediate state where specified.
See `../acceptance.md` section 01 for commands, evidence, authorized
exceptions and the current result. Final delivery review is recorded separately.
