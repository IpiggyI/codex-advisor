# Tickets 01 and 02 acceptance

Date: 2026-09-06. Implementation base: `37b75cad535abdd46531f0227483a8842d045ab8`.
Scope: independent installation, Advisor mode, and ordinary Astra solo work.
Tickets 03-06 remain outside this delivery.

## Deterministic verification

- `sh plugins/codex-advisor/scripts/verify.sh --installation`: passed.
- `sh plugins/codex-advisor/scripts/verify.sh --runtime`: passed.
- `sh plugins/codex-advisor/scripts/verify.sh`: passed after implementation.
- Plugin schema validation and skill frontmatter validation: passed.
- `git diff --check`: passed.

The installer tests observe exact bytes and directory state across clean and repeat
installation, non-mutating all-role and selective checks, missing and unknown roles,
modified files, symlinks, unsafe ancestors, directories, FIFOs, relative targets,
CODEX_HOME targets, and root refusal. Existing upstream-role files, unrelated agents,
and primary configuration are preserved. The fork currently ships only the Advisor;
selective checks ignore unrelated conflicting files.

Runtime fixtures verify the exact Advisor role/model, adjustable effort, absent and
conflicting settings, missing permissions, broader permissions, invalid and ambiguous
records, and an output allowlist that excludes prompt and credential markers.
The tests first failed on the missing fork identity and missing Advisor role before
the corresponding implementation passed. JSON/TOML parsing and shell syntax are the
applicable static checks; this repository has no typed application build.

## Installed-host observations

Host: Codex CLI `0.153.4`. All installations and workflow runs used temporary
CODEX_HOME directories and disposable workspaces. No active-environment installation
was performed. Raw acceptance logs live under
`/tmp/codex-advisor-acceptance.dft5rp7s`; initial discovery logs live under
`/tmp/codex-advisor-live.pfb9shnp`. These are local, temporary evidence, not release
assets. Credential copies are removed after verification.

The role's model-only configuration follows the
[official custom-agent precedence documentation](https://developers.openai.com/codex/subagents#custom-agents),
fetched on the acceptance date: role-level effort overrides spawn effort, while a
model-only role preserves the resolved spawn effort. The calls below verify that
assumption on this host. Recheck it after a host upgrade or native-role format change.

| Scenario | Observed result | Evidence |
|---|---|---|
| Independent plugin installation and discovery | Marketplace/plugin registration succeeded; fresh tasks exposed `codex-advisor:orchestration` and the fork's native types. The final package exposes `codex_advisor_astra_advisor` and passes selective checking. | Initial thread `01a074b0-f58b-7691-8a42-04b81214b6de`; final `plugin-list.json`, `sol-api.jsonl` |
| Sol primary effort freedom and API boundary | Parent remained `gpt-5.6-sol` / `low`; fresh native consultation preceded the API decision and file creation. | Parent `01a074b6-35e1-7412-9585-51b841f8e9e7`; design Advisor `01a074b6-c4e1-7ba2-8cc1-854329c4324e` |
| Explicit Advisor effort adjustment | Role selected `gpt-6-astra`; explicit `medium` took effect despite role defaults. Both design and readiness calls were observed at that effort. | Design above; readiness `01a074b8-ab76-7911-a40c-241f0fa05b77` |
| Multi-step readiness | Parent implemented and verified the sum function, then obtained a distinct readiness consultation before completion. The final report distinguished consultation from independent review. | `sol-api.jsonl`; separate HTTP repeat in `sol-http.jsonl` |
| Luna primary effort freedom and persistent failure | Parent remained `gpt-5.6-luna` / `low`. It reproduced two distinct ValueErrors, consulted Astra before a third approach, verified conversion to integer 1234, then obtained readiness advice. | Parent `01a074b7-a7be-7e33-aeb6-8905210ec75b`; Advisors `01a074b8-3ab8-7451-8ef4-96ed6a3c6af2` and `01a074b9-4fd1-7b53-bf4f-fa8371e16504`; `luna-failures.jsonl` |
| Default Advisor effort | Both Luna consultations ran `gpt-6-astra` / `high`. | The two Advisor records above |
| Ordinary Astra solo, unaccepted proposal | Astra / low wrote and verified exact `hello` bytes itself, with no delegation or Architect activation. | Parent `01a074b6-9ffb-7593-968a-9eec63819e26`; `astra-solo.jsonl` |
| Unavailable required consultation | With native agents disabled, Luna paused before choosing architecture, designing a migration, or refactoring three files. All three input files retained exact original bytes. | Parent `01a074b9-2056-7f83-bcf6-cb20805c722e`; `unavailable.jsonl` |
| Actual judgment permissions | Every observed Advisor had `workspace-write` / `managed` despite the role's read-only request. Scoped before/after state and activity showed behavioral read-only operation. Reports did not claim enforced isolation. | Narrow runtime inspector output and per-consultation hashes in the live logs |
| Disagreement handling | A same-task user requirement admitted bool values. The parent explicitly explained why this superseded the previous Advisor's bool-rejection recommendation, implemented the change itself, verified 150 for the old example and 3 for the bool example, and requested new design and readiness advice. | `disagreement.jsonl`; design `01a074bc-e9f9-78e0-89ba-9be56f21fedf`; readiness `01a074be-4edc-7300-a2ce-0acb77c852ca` |

The first Sol run encountered WebSocket reconnects and eventually completed. A
separate HTTP transport repeat also completed; no model substitution was used.
Primary settings were independently checked in parent turn-context records. A
child's prose described Sol generically and Luna's final report could not itself
observe the parent effort; those claims were not used as routing evidence.

## Verification boundaries

- Live calls establish routing for the exercised default `high` and adjusted
  `medium` efforts, not all supported settings. Other accepted parser values are
  fixture coverage only.
- Missing or contradictory runtime records are covered deterministically. The live
  failure scenario disables native invocation; it does not corrupt host records or
  establish behavior during every possible provider outage.
- Successful API and persistent-failure triggers were exercised live. Architecture,
  migration, and three-file refactor triggers were exercised together on the
  unavailable-call branch, not as separate successful migrations or refactors.
- The host's broader permissions mean enforced read-only isolation was not verified.
  Unchanged scoped files do not prove prevention of writes elsewhere.
- No Architect implementation or independent final-review workflow is claimed.

## Review

The code-review skill ran independent Standards and Spec agents against the staged
diff from the implementation base. The pre-commit diff adapts its usual HEAD-based
comparison to the implement skill's review-before-commit sequence.
Standards found no required changes. Spec found one live-acceptance gap: the initial
consultations had no disagreement. A same-task follow-up exercises a new explicit
user constraint against the actual previous Advisor recommendation. Its observed
decision and reasoning close that gap; both new calls again used Astra / medium.
