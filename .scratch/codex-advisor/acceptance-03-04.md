# Tickets 03 and 04 acceptance

Date: 2026-09-06. Implementation base: `d313560e5efaf27895f1573450869adf0c573c44`.
Scope: authorized Astra Architect work with Luna, and independent Astra review.
Direct Sol and parallel implementation remain outside this delivery.

## Ticket 03 verification

Focused installation and runtime checks passed. New checks first failed for the
absent Luna template and then for the absent `--luna` interface before their
implementations passed. Installation checks cover all shipped roles, exact bytes,
selective checks, unrelated configuration preservation, and refusal before any
partial installation. Runtime fixtures reject wrong roles/models, Luna effort
below max, missing permissions, and conflicting evidence without emitting payloads.

Live runs used Codex CLI `0.153.4` in a disposable home and workspaces at
`/tmp/codex-advisor-03-04.5e8rordh`. The plugin and native roles were installed there;
the active user installation was unchanged. Each scenario has a named prompt,
JSONL event log, and final response. Native rollouts live in that home's `sessions`.
These paths are temporary local evidence, not release assets.

| Scenario | Observation | Evidence |
|---|---|---|
| No authorization and an unaccepted proposal | Astra / low performed the one-line fix itself and verified `PASS: double`; no delegation. | `solo.jsonl`; parent `01a074ca-e572-7242-8564-20b0f18d6aa9` |
| Task authorization, bounded one-line change | Astra / low delegated to native Luna / max, inspected complete before/after contents, and reran the meaningful check. No extra reviewer was added. | `authorized.jsonl`; parent `01a074ca-da5e-7141-b26d-55f05ba5d67b`; child `01a074cb-c760-7b30-b646-21a1b674d707` |
| Same-task correction and inadequate evidence | The harness changed the result to multiplication by 3 and supplied a false pass report without command evidence. The parent observed a failing check, resumed the Luna Implementer for correction, and reran the check successfully. | `correction.jsonl`; same parent and child; child patch and parent check output |
| Unrelated task after task authorization | The parent explicitly expired the authorization, created `label.txt` itself, checked exact bytes, and preserved existing hashes. No delegation. | `task-new.jsonl`; same task-authorized parent |
| Session-wide authorization | The initial task and an unrelated later task each used Luna / max; the parent checked actual changes and reran verification. | `sessionwide.jsonl`, `session-new.jsonl`; parent `01a074cc-62d7-7f72-9b00-1bce7e7785f3`; children `01a074cd-5c53-7582-9b88-3dbb0c1dde06`, `01a074cf-6ef2-7210-9333-840d7ab7428e` |
| Non-Astra prerequisite and direct Luna freedom | Luna primary remained at low and declined to claim active Architect mode. No file edit, model switch, or delegation occurred. | `nonastra.jsonl`; parent `01a074cc-7ffa-78d2-9436-66e87e8fb333` |

The delegated patches and parent reruns were inspected independently of final
reports. Parent turn contexts establish the direct low efforts; child turn contexts
and `--luna` output establish the native model and max effort. Implementers made
the observed implementation edits and no further implementation delegations.

## Ticket 04 verification

The full `sh plugins/codex-advisor/scripts/verify.sh` entry point passed after
implementation. Focused runtime checks passed after test cleanup. JSON, TOML,
YAML, skill frontmatter parsing, local skill links, and `git diff --check` passed.
These are the applicable static checks; this repository has no typed application.
New tests first failed for the missing reviewer template and then for the missing
effort selector. Fixtures cover all five specified primary defaults, every pair
of primary and explicit reviewer efforts, unestablished ordering, role/model
mismatches, missing and conflicting settings/permissions, and payload filtering.

Successful live review runs used a second disposable installation at
`/tmp/codex-advisor-03-04.2j5aqxnj` on the same Codex version. All review spawns used
`fork_turns: none`. The parent inspected actual changes and reran the meaningful
check before review. Reviewer activity independently shows actual file inspection
and check execution. The parent compared scoped state and verified runtime settings
before acceptance; the implementation agent and reviewer were distinct threads.

| Scenario | Observation | Evidence |
|---|---|---|
| User-requested review of a bounded Luna change | Primary Astra / xhigh delegated the one-line fix to Luna / max, reran `check.py`, and invoked fresh Astra review / xhigh. | `review-xhigh.jsonl`; parent `01a074da-2029-7db2-8191-3762d9c8a622`; Implementer `01a074db-cde3-7783-ac50-3885ed75a9f1`; reviewer `01a074df-2836-7ec3-88a7-3d4f61c0e692` |
| High-risk review without an explicit review request | Acceptance of an existing access-policy change triggered review after complete diff inspection and `PASS: access policy`. Primary and reviewer both ran Astra / max. | `risk-max.jsonl`; parent `01a074da-3104-70b0-9670-40911debfec9`; reviewer `01a074dd-6eda-7c22-8099-4dc9fdc4730d` |
| Default review for low primary effort | Primary Astra / low invoked reviewer Astra / high and verified the unchanged scoped state. | `unavailable.jsonl`; parent `01a074db-1d93-7151-a3d9-9ef29f274301`; reviewer `01a074dc-26a3-7ab3-a3aa-5ff036f9c82b` |
| Explicit supported adjustment | Same low-effort primary obtained a new Astra review / medium. Actual effort confirms that the model-only role does not override the allowed adjustment. | `adjusted.jsonl`; reviewer `01a074de-fefb-78b1-9f34-102edc693a77` |
| Rejected lower override | Astra / xhigh inspected and checked the change, but rejected requested high review, invoked no reviewer, and reported acceptance pending. | `lower.jsonl`; parent `01a074da-3d39-7eb2-8d6a-59cc5c2cfb77` |
| Ordinary completion without review | The bounded ticket 03 scenarios completed after the architect's own checks with no automatically added reviewer. | Ticket 03 records above |
| Required reviewer unavailable | A separate installed home withheld only its reviewer role. The parent inspected the diff and passed its check, then stopped on the failed selective installation check. It invoked no substitute and explicitly left acceptance pending. | `/tmp/codex-advisor-03-04.hcj_ja7y/missing-reviewer.jsonl`; parent `01a074e1-bcda-7f71-bf92-97e727bfaf3f` |

All observed reviewers received `workspace-write` / `managed` permissions despite
their role's read-only request. Exact scoped contents, file metadata, and inventory
were compared before/after review, and tool activity contained reads and checks,
not implementation. Protected directory timestamps changed during sandbox mounts;
this was disclosed separately from file state. The evidence establishes behavioral
read-only review within the inspected scope, not enforced isolation or prevention
of writes elsewhere.

The logs named `unavailable` and `required-unavailable` both produced successful
reviews: disabling `multi_agent`, and then both `multi_agent` and `multi_agent_v2`,
did not remove native calls on this host. Neither run counts as failure coverage.
The separate missing-role scenario establishes unavailable-role refusal, not a
provider outage. Temporary authentication copies in all three test homes were
removed after the runs; no active-environment credential file was changed.

## Code review

The code-review skill ran separate read-only Standards and Spec agents against
`git diff --cached d313560e5efaf27895f1573450869adf0c573c44`. This adapts the usual
HEAD comparison to implement's review-before-commit sequence. No implementation
findings were reported on either axis. Spec kept ticket 04 live acceptance pending
until this record was completed. Its final read-only follow-up independently
confirmed the four observed reviewer settings, fresh contexts, parent linkage,
pre-review checks, and missing-role refusal, closing that gap without new findings.
Reviewers did not edit files or invoke live models.

## Evidence limits

The official custom-agent documentation endpoint returned HTTP 403 during this run.
Native precedence is established by the exercised host calls, not a fresh docs
fetch. Recheck after host upgrades or role configuration changes. Fixture success
establishes parser and refusal behavior, not live model behavior. Authorization
is a conversational contract; these observations do not establish deterministic
enforcement for every possible prompt.

Live floor coverage establishes low -> high, xhigh -> xhigh, max -> max, and an
explicit low -> medium adjustment. Medium/high primary defaults and other allowed
override pairs are fixture coverage only. Missing/conflicting runtime records are
tested deterministically, not by corrupting real host rollouts. Provider outages
and enforced read-only isolation remain unverified. High-risk implementation routing
belongs to ticket 05; the high-risk scenario here only accepts an existing change.
