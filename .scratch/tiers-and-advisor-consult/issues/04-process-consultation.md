# 04: Process consultation

**What to build:** A zero-parameter consultation that the primary, any worker, and any explorer can call, through the mechanism ticket 01 selected:
- It carries the caller's current effective context automatically, including the unfinished turn and the post-compaction view.
- It runs the advisor at the AC-4 dial for that caller, with no tools.
- It returns exactly one of plan, correction, or stop, with the actual model and effort.
- It flags a model or effort mismatch to the caller.

In the same ticket, every explorer and worker entry gains its posture section (EN-5), so that no entry tells a delegate to call a consultation that does not exist yet.

**Blocked by:** 01 (mechanism decision), 02 (canonical posture text and consultation doctrine), 03 (routing profile and installed entries).

**Status:** resolved

## Required reading before starting

- `spec.md`: AC-3, AC-4, AC-5, AC-10 (the consultation part), AC-11, EN-1 (last bullet: extra entries, if the mechanism needs them), EN-5, EN-6, DR-5 (ticket 04 section), X-2, X-4, §Mechanism decision, §Decision Boundaries, §Open Decisions (O3), §Testing Decisions items 1 (posture checks), 4 and 6, §Goal-Drift Checks (the first three items and the posture-section item).
- `sources.md` §2.4 rows D17, D18, D19, D20, D28, D33, D34, D41, D43, D44.
- `plugins/codex-advisor/skills/orchestration/references/consult-posture.md` (from ticket 02; the only source of the posture sections, copied without rewording).
- Current explorer and worker templates, their `docs/zh/agents/` twins, and the `verify.sh` installation group (from ticket 03).
- `acceptance.md` §01 P4 (the selected configuration's evidence) and §03 (installed entries).
- `plugins/codex-advisor/skills/orchestration/references/routing-profile.md` (AC-4 mapping as shipped).
- rpiv-advisor at `d74b1c99`: `advisor/execute.ts`, `advisor/context.ts`, `advisor/inventory.ts`, `prompts/advisor-system.txt`, and the tests `advisor.execute.test.ts`, `advisor.strip.test.ts`, `advisor.errorresult.test.ts` (behaviour cases to mirror).

## Owns

- The consultation component, at the location the mechanism requires, under `plugins/codex-advisor/`.
- The `plugin.json` fields it needs, such as an MCP server entry. Not `version` and not descriptions.
- A new `verify.sh` group for it (the unqualified run includes it).
- The new §Process consultation in `references/operations.md` and its twin.
- Any extra native entries, per EN-1's last bullet, with their twins, routing-profile rows, retire and manifest handling, and checks.
- The posture section of every explorer and worker template (`plugins/codex-advisor/agents/ca-explorer-*.toml`, `ca-worker-*.toml`) and of their twins. Nothing else in those templates.
- In the `verify.sh` installation group: the posture checks, and narrowing the same-role identical-instructions check to the text outside the posture section.

## Establishes and consumes

- **Establishes** AC-3, AC-4, EN-5, and the consultation part of AC-10.
- **Consumes** the ticket 01 mechanism, the ticket 02 posture text, the ticket 03 routing profile and templates, and AC-11.

Ticket 05's before-done hook needs to know that a consultation happened. Document in the §Process consultation section how a consultation is observable within a session (for example, the tool call name in the session record, or per-session state). Ticket 05 relies on that description.

## Acceptance

- [x] The consultation takes zero parameters. A caller cannot pass a summary in place of the automatic context.
- [x] Context (D43): fixture tests show that these all reach the advisor call:
  - [x] an unfinished turn's tool call and result;
  - [x] a compaction summary with later messages;
  - [x] a constraint from the earliest uncompacted turn of a session longer than any window the mechanism uses.

  The live nonce, compaction, and earliest-context checks pass (`acceptance.md` §04).
- [x] The advisor call has no tools (D44). The tests assert the tool set the component sends is empty. The live evidence is the actual tool set of the advisor request, as sent or as recorded by the host, shown empty; a refused attempt or the advisor's own statement is not evidence.
- [x] Dial: for a `mainstay`, `crux`, and `rescue` caller, and for a primary on `gpt-6-astra[xhigh]`, `gpt-6-sol[high]`, and `gpt-5.6-terra` (fixture), the advisor dial equals AC-4. The result reports the actual model and effort; a mismatch between actual and expected is surfaced to the caller as a failure, not as advice.
- [x] Output: exactly one of plan, correction, or stop. An executor error, abort, or empty output returns an explicit failure. Whether to retry is the implementer's choice, but any retry is bounded to one; no retry loop.
- [x] No credential is read, copied, or sent by the component (D41). The only state kept is per-session, per AC-11.
- [x] Callable live from the primary, from a spawned worker, and from a spawned explorer, each recorded with thread IDs and the observed advisor model and effort (`acceptance.md` §04).
- [x] §Process consultation in `operations.md` (and its twin) says:
  - [x] how to call it, what it returns, and how dial and mismatch work;
  - [x] how, within one session, three outcomes are each observable and told apart: a consultation started, a consultation succeeded (a valid plan, correction, or stop at the expected dial), and a consultation failed (error, abort, empty, or mismatch);
  - [x] how a failure is shown to the caller.

  Ticket 05 relies on this. The distinction is required whichever way the user decides O3.
- [x] **Posture sections (EN-5).**
  - [x] Each explorer and worker template has one delimited posture section, byte-equal to the `consult-posture.md` variant AC-5 assigns: full for `gpt-6-luna` and `gpt-6-sol` entries, reduced for `gpt-6-astra` entries.
  - [x] Advisor templates have no posture section.
  - [x] Outside the section, same-role instructions stay byte-identical.
  - [x] The section states the rule's outcome and never asks the delegate to infer its own model.
  - [x] Twins translate the section and keep its delimiters character-exact.
- [x] **Posture checks in the `verify.sh` installation group.**
  - [x] Section equality. The variant is computed by comparing each entry's model id with its tier's advisor model id from the routing profile, never by a family-name list.
  - [x] No section in advisor templates.
  - [x] Same-role identity outside the section.
  - [x] Record a negative proof for each: a section edited by one character, a `gpt-6-luna` entry given the reduced variant, and an advisor template given a section each make the group fail.

## Verification

- `sh plugins/codex-advisor/scripts/verify.sh` (all groups)
- `python3 tests/test_zh_mirror.py`
- `git diff --check`
- The live table in `acceptance.md` §04

## Stop conditions

S3 and S4 (if the live behaviour contradicts ticket 01), S8, S9.

## Not in this ticket

Hooks, posture injection, the before-done enforcement, README, the manual, and the version bump.

## Comments

Resolved on 2026-09-26. The checked items record this ticket's acceptance
checkpoint; later tickets extend the intermediate state where specified.
See `../acceptance.md` section 04 for commands, evidence, authorized
exceptions and the current result. Final delivery review is recorded separately.
