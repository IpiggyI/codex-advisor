---
name: orchestration
description: "Use for authorized Astra Architect work with delegated implementation, or primary implementation with Astra advice at design decisions, persistent failures, and multi-step completion."
---

# Codex Advisor orchestration

## Delegate exploration

When this skill applies, use `codex_advisor_luna_explorer` by default for exploration
you decide to delegate. This applies to every primary model, including all non-Astra
models, and does not require Architect mode. Preserve existing rules and user
authorization for whether to delegate. The installed role is also callable without
this skill; outside the skill, the primary chooses from available role descriptions.

Before invoking the Explorer, read the investigation packet in
[role-contracts.md](references/role-contracts.md) and the Explorer installation,
invocation, effort selection, and validation procedure in
[operations.md](references/operations.md). Explicitly choose a supported reasoning
effort for each call. Exploration has no `max` minimum; the Luna Implementer's
fixed `max` requirement remains unchanged.

Check the returned source evidence and actual call settings. The Explorer supplies
read-only findings; the primary owns decisions. If the role is unavailable or its
findings are insufficient, report the gap and investigate directly as needed.
A more expensive delegated substitute requires explicit user authorization.

## Establish the work mode

Use the primary model identity exposed by the host. Preserve the user's primary
model and reasoning effort; this plugin imposes no primary-session effort floor.
If identity is unknown, resolve it from host evidence before selecting a mode.
Do not infer it from the installed plugin or a model's self-description.

- Non-Astra primary sessions, including Sol and Luna, use Advisor mode. The primary
  agent implements and verifies the work, consulting Astra at the boundaries below.
- An Astra primary session without an explicit user request or accepted proposal for
  Architect mode continues ordinary solo work. A suggestion alone and a generic
  request to implement do not authorize delegation-only Architect mode.
- Architect mode requires both Astra and an explicit user request or accepted
  proposal. Record the authorizing request and its scope in task context. By default
  it covers the current task, its follow-up turns, and implementation subtasks;
  expire it for an unrelated new task. Only explicit session-wide authorization
  carries into subsequent tasks, and Astra remains a prerequisite. Recheck scope
  at task boundaries and identity when the host model changes.
- If a non-Astra primary receives an Architect-mode request, explain the unmet
  prerequisite without claiming activation or changing the primary model. A
  dedicated mode-switch command is not required.

## Carry out authorized Architect-mode work

The architect owns design, task specifications, scheduling, and acceptance. Every
implementation edit belongs to an Implementer, including one-line changes and
corrections. The architect may write design and task-specification artifacts.

Before implementation, read the shared implementation packet in
[role-contracts.md](references/role-contracts.md) and the installation, invocation,
and evidence checks in [operations.md](references/operations.md). Select the native
Luna Implementer at `max` for bounded, fully specified work with little implementation
judgment and clear acceptance checks. Select the native Astra Implementer directly
for substantial implementation judgment, cross-module understanding, or higher risk;
a failed Luna attempt is not a prerequisite. Astra defaults to `medium`; explicitly
pass that effort or the user's supported adjustment. Keep implementation effort
independent of the primary effort and do not automatically raise it after failure.
Select the native Sol Implementer only when the user explicitly requests Sol, passing
`high` or the user's supported adjustment. Luna and Astra are the default choices;
Sol is not an automatic fallback for failures, unavailability, cost, or waiting time.

Validate the observed role, model, requested effort, and permissions for every call.
An invalid or unavailable model or effort, or missing or conflicting evidence,
leaves affected acceptance pending. Report the reason without silently substituting
a role or setting. Delegated settings never restrict a directly used primary session.

When Luna fails acceptance, diagnose the cause before choosing specification
clarification, a Luna correction, or Astra reassignment. There is no fixed retry
count; environment failures and specification gaps alone do not establish insufficient
model capability. Resolve material specification gaps before dependent edits. For
reassignment, follow the actual-state handoff in [operations.md](references/operations.md).

When a task has multiple implementation parts, read the scheduling procedure in
[operations.md](references/operations.md). Dispatch independent parts with disjoint
ownership concurrently when host capacity permits. Sequence dependencies, conflicting
ownership, and work exceeding available capacity. Scheduling stays with the primary;
Implementers perform their assigned work without further implementation delegation.

Inspect every actual change, including new files and corrections, against the
ownership boundary and specification. Rerun key verification yourself. Check the
worker's report against those observations; missing, false, failed, or skipped
evidence cannot establish acceptance. Send any correction to an Implementer and
repeat the affected checks. Obtain every required worker report and rerun key checks
against the combined deliverable before acceptance. A failed, blocked, or incomplete
worker leaves its affected work pending; another worker's success cannot complete
the whole task. A report alone never completes this step.

After these checks, ordinary work may complete without adding a reviewer, including
work implemented by Astra. The implementation model alone is not a review trigger.
High-risk work and explicit user requests for independent review require a fresh
Astra Independent reviewer after the architect's checks. Read the review packet in
[role-contracts.md](references/role-contracts.md) and the floor selection, invocation,
and permission safeguards in [operations.md](references/operations.md).
Apply these obligations to the combined deliverable, including parallel work.

Resolve the current Astra primary effort from actual host evidence. Select the
default review effort as the higher of `high` and that effort using the inspector's
deterministic selector. Explicit supported adjustments may be below `high` only
when they remain at or above the primary effort. This rule never restricts the
primary session. Unknown ordering or unavailable primary evidence leaves the
review floor unestablished and the required review pending.

Validate the actual reviewer role, Astra model, selected effort, fresh context,
permissions, and unchanged scoped state before accepting its judgment. If the
required call is unavailable, fails, or has missing or conflicting evidence, pause
the affected review/completion step with the reason. No substitute or successful
review claim is permitted. Advisor consultation does not satisfy this contract.
The Independent reviewer supplies findings, while the architect owns acceptance.
Assign corrections to an Implementer, inspect them, rerun affected checks, and
obtain a fresh review of the revised deliverable before required-review completion.

## Carry out Advisor-mode work

Consult an independent Astra Advisor:

- Before committing to an architecture decision, data migration, API design, or
  refactor touching at least three files.
- After two distinct unsuccessful attempts at the same problem, before another
  attempt. State both attempted approaches and their observed failures.
- Before declaring a multi-step deliverable complete, after inspecting actual
  changes and running the relevant verification.

Additional useful consultations are allowed. Each consultation addresses its current
boundary; an earlier design discussion does not satisfy a later readiness check.

Before a consultation, read [role-contracts.md](references/role-contracts.md) for
the decision packet and [operations.md](references/operations.md) for selective
installation checks, exact native invocation, runtime validation, and permissions.
Use a fresh context and supply only the relevant evidence and constraints.
The Advisor provides judgment and does not implement changes.

The consultation defaults to `high`; explicitly pass that effort on the native
call unless the user requested another supported setting. The native role pins
`gpt-6-astra` while leaving effort open to the call. Verify the actual role, model,
effort, and permission evidence before relying on the recommendation.

If Astra is unavailable, invocation fails, or required actual model or effort
evidence is missing or conflicting, pause the affected decision or completion
step. Report the reason and the evidence gap. Do not silently substitute a model,
skip a required consultation, or claim it occurred. Independent unaffected work
may continue while the affected step remains explicitly pending.

## Own the Advisor-mode decision and delivery

Check the Advisor's cited evidence against the scoped sources. Explain the
recommendation, your resulting decision, and the reasons for any disagreement.
Advice does not replace user authorization or project approval requirements.
Implement and verify any resulting change in the primary session.

Before reporting multi-step completion, inspect the final changes, report actual
verification and gaps, and obtain the readiness consultation required above.
Reassess readiness if subsequent changes invalidate its evidence.
An ordinary consultation, including readiness advice, is not proof of an independent
final review of the actual changes. Do not report it as that separate review.
