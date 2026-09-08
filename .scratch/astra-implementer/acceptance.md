# Astra Implementer acceptance

Date: 2026-09-08

Implementation baseline: `3fb02206b9a614d64e72c915978251242864fe0b`.
Scope: [the feature specification](spec.md) and [ADR-0002](../../docs/adr/0002-luna-astra-implementation-routing.md).

## Deterministic verification

The installation test first failed because full installation did not include an
Astra Implementer. The runtime test first failed because `--astra-effort` was an
unknown argument. Both passed after their corresponding implementation changes.

The following public checks passed:

~~~sh
sh plugins/codex-advisor/scripts/verify.sh --installation
sh plugins/codex-advisor/scripts/verify.sh --runtime
sh plugins/codex-advisor/scripts/verify.sh
git diff --check
~~~

Coverage includes full and selective installation checks, idempotence, refusal
without partial mutation, the previous valid Sol description during upgrade,
exact native role/model identity, adjustable Astra effort, wrong Astra judgment
roles, mismatched or missing settings, conflicting evidence, invalid arguments,
permission metadata, and payload filtering. JSON/TOML parsing and Shell syntax
checks are the applicable configuration checks; this project has no typecheck task.

These checks establish installer and parser behavior, not live model behavior.

## Live host observations

Host: `codex-cli 0.153.4`. The local marketplace, plugin, and all six role templates
were installed into a temporary `CODEX_HOME`. Four fresh fixture sessions used an
Astra primary at `high`, `workspace-write`, persistent runtime records, and explicit
task-scoped Architect-mode authorization. The user's active installation was not
updated. No implementation benchmark or subscription-allowance comparison was run.

Evidence root: `/tmp/codex-advisor-astra.isz2w1tr`. It contains fixture prompts,
source files, tests, event streams, final responses, selected check outputs, and
runtime sessions. Temporary connection settings and authentication were used for
these calls; authentication copies were removed after the sessions completed.

| Fixture | Observed result |
|---|---|
| Default Astra implementation | The parent explicitly passed `medium` without a user effort adjustment. The child implemented recursive dictionary merging; 8 meaningful tests went from failure to pass. The parent inspected the actual change, reran all 8 tests, and checked protected files. |
| Explicit Astra effort adjustment | The user selected `high`; the child observed `high` and completed the same 8-case contract. The parent inspected and reran the checks. |
| Default routing, explicit Sol, and required review | A bounded sum used Luna at `max`; user-selected stable deduplication used Sol at `high`; a designated high-risk balance validator used Astra at `medium` directly. All three owned files passed the combined suite. A fresh Astra reviewer at `high` then inspected the balance validator and returned no findings. |
| Missing Astra role | A separate temporary installation lacked only the Astra Implementer. Selective preflight failed; the primary left work and acceptance pending, made no edit, and did not invoke Sol or another substitute. |

Exact child evidence was checked independently with the repository runtime inspector:

| Native role | Effort | Child thread | Parent thread |
|---|---|---|---|
| `codex_advisor_astra_implementer` | `medium` | `01a07ee2-4b20-7932-8199-c37fcf0b4587` | `01a07ee0-bc9c-7e03-b91f-ab03891e32ff` |
| `codex_advisor_astra_implementer` | `high` | `01a07ee2-9b3f-76e2-93e5-221155860fd4` | `01a07ee0-fce3-7ae2-b6d8-3e1bd23f13b4` |
| `codex_advisor_luna_implementer` | `max` | `01a07ee6-88fe-77a1-b36b-8a50dbd58646` | `01a07ee5-6f1f-7f62-bdd6-27048292bb03` |
| `codex_advisor_sol_implementer` | `high` | `01a07ee6-f6df-7992-934c-87145b5f83dd` | `01a07ee5-6f1f-7f62-bdd6-27048292bb03` |
| `codex_advisor_astra_implementer` | `medium` | `01a07ee7-7254-74b2-9809-cf6feeff7146` | `01a07ee5-6f1f-7f62-bdd6-27048292bb03` |
| `codex_advisor_astra_reviewer` | `high` | `01a07ee9-ad4b-79b2-9506-144467f14ac8` | `01a07ee5-6f1f-7f62-bdd6-27048292bb03` |

Primary runtime records remained Astra at `high`; native spawn arguments selected
fresh contexts. The root verification reran both 8-case merge suites and the
3-case routing suite successfully, inspected the generated implementations, checked
protected files, and compared every observed parent association. The two ordinary
Astra sessions completed without an added Independent reviewer.

Initial WebSocket connections experienced transport retries; the host recovered
through HTTPS. Later fixture sessions disabled WebSocket support only in their
temporary connection configuration. This was transport handling, not a model
fallback. It does not establish terminal provider-failure handling.

The Independent reviewer was behaviorally read-only over the inspected fixture
files, with unchanged post-review state. Runtime permissions remained managed
`workspace-write`; this is not evidence of enforced read-only isolation.

## Review

Standards and Spec were reviewed independently against the staged changes from the
baseline. Standards found no documented-rule violation; the added per-role argument
branch follows the existing pattern, so its repeated validation did not warrant an
unrelated refactor. Spec found one missing named upgrade fixture for the old valid
Sol description. That fixture was added, the installation group passed, and the
Spec reviewer confirmed the finding was closed. No implementation defects or scope
creep were reported.

## Remaining validation limits

- Terminal invocation failure after discovery was not forced; transient recovered
  transport errors and the missing-role scenario do not cover that path.
- Missing/conflicting evidence rejection was tested at the inspector boundary;
  a live parent handling deliberately corrupted evidence was not exercised.
- Live specification-gap resolution, environment-caused Luna failure, cause-based
  Luna reassignment with partial edits, and rejection of a false worker completion
  report were not exercised. Their documented responsibilities were reviewed.
- The review fixture covered high risk plus an explicit review request. A separate
  low-risk review request, review-required corrections, and unavailable required
  review were not exercised in this run. Existing review-floor checks passed.
- Explicit Sol effort adjustment was covered by deterministic fixtures; this live
  run used Sol's default `high`.
- These fixtures do not establish broad `Astra-medium` quality, comparative latency,
  statistical significance, or savings in the user's Codex subscription allowance.

Temporary paths are evidence locations from this run and may be removed later.
Recheck current host discovery, model support, and allowance rules before extending
these observations to a different installation or performance claim.
