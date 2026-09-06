# 03: Authorized Architect Mode with Luna Implementation

Status: resolved

Blocked by: 02 - Advisor Mode and Ordinary Astra Solo Work.

**What to build:** After explicit user authorization, an Astra primary session completes a bounded implementation task by specifying work, delegating all implementation to Luna at `max`, inspecting the actual result, and rerunning key verification before acceptance.

- [x] Architect mode requires both an Astra primary session and an explicit user request or accepted proposal. Model identity, a generic implementation request, or an unaccepted suggestion alone is insufficient.
- [x] Task-scoped authorization survives follow-up turns and implementation subtasks within the same task but does not carry into an unrelated new task.
- [x] Explicit session-wide authorization applies to subsequent tasks in that session while the Astra prerequisite holds.
- [x] A non-Astra primary model is not reported as an active architect, and the plugin does not switch the primary model automatically.
- [x] The Astra architect's directly selected reasoning effort remains unrestricted by the plugin.
- [x] The architect owns design, task specifications, scheduling, and acceptance. Every implementation edit, including a one-line change and a correction to delegated work, is performed by an Implementer.
- [x] Bounded, fully specified implementation is delegated to native `gpt-5.6-luna` at observed `max` effort. Incorrect or unobservable routing is not accepted as satisfying the contract.
- [x] The Luna constraint applies to Astra's delegated calls in Architect mode and does not leak into the reasoning settings of a directly used Luna primary session.
- [x] Each implementation specification supplies objective, files and ownership, interfaces, constraints, and verification. It requires preservation of concurrent edits and a structured evidence report.
- [x] The Implementer stays within ownership, surfaces material ambiguity and failed verification, and does not create further implementation delegations.
- [x] The architect inspects all actual changes and reruns the key verification checks. A worker report with missing or incorrect evidence cannot by itself establish acceptance.
- [x] A bounded task that does not require independent review completes after the architect's checks without automatically adding another reviewer.
- [x] The native role contract, installation checks, runtime evidence handling, and user instructions agree on the supported behavior and model constraint.
- [x] Installed-plugin scenarios cover authorization present and absent, unaccepted proposals, task and session lifetimes, one-line changes, correction ownership, Luna's actual effort, and rejection of inadequate worker evidence.

## Verification

Use a disposable repository with a small behavior change and an existing meaningful check. Observe who edited the files, the delegated model and effort, the complete resulting diff, and the architect's rerun evidence. Include authorization scenarios across follow-up turns and a new task. Independent-review completion is delivered by ticket 04, and direct Sol implementation by ticket 05.

## Acceptance

Completed on 2026-09-06. Installed-host scenarios confirmed task and session
authorization lifetimes, ordinary solo work, the non-Astra prerequisite refusal,
Luna implementation and corrections at observed max effort, and rejection of an
inadequate worker report through actual-diff inspection and rerun verification.
See [the acceptance record](../acceptance-03-04.md) for evidence and limits.
