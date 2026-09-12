---
name: orchestration
description: "Use when a primary agent implements or delegates work, selects tiered exploration, recovers failed attempts, or needs Astra decision advice and independent acceptance."
---

# Codex Advisor orchestration

## Own the task

Any primary model may implement directly, delegate bounded work, or combine both.
Preserve the user's primary model and reasoning effort. A midrange primary such
as Sol is a preference, not a plugin requirement. Choose decomposition, order,
and division of work within the user's authorized goals, scope, reserved decisions,
acceptance conditions, and resource limits. Do not change those boundaries to
make the task easier. Investigate mismatches with current code, seek resolution
for user-owned changes, and continue independent unaffected work.

Explicit Architect-mode authorization makes every implementation edit and correction
delegated for its scope, for any primary model. The primary owns design, contracts,
scheduling, and acceptance and may write design and task artifacts. Model identity,
a ticket, a specification, or an unaccepted proposal does not activate this mode.
Record the authorizing request. It lasts for this task and follow-ups; unrelated
tasks need new authorization unless the user explicitly granted session-wide scope.

## Allocate by responsibility and capability

Before a delegated call, read the relevant packet in
[role-contracts.md](references/role-contracts.md) and the installation, invocation,
evidence, and permission procedures in [operations.md](references/operations.md).
Respect host capacity and explicit user exclusions and resource limits. Select an
allowed effort explicitly without asking permission for each routine allocation.

| Responsibility | Tier | Model and effort |
|---|---|---|
| Explorer | light | Luna `high` |
| Explorer | standard / senior | Usually Luna `max`; direct Sol or Astra `medium` / `high` allowed |
| worker (Implementer) | light | Luna `max` |
| worker (Implementer) | standard | Sol `high` / `xhigh`, including the first attempt |
| worker (Implementer) | senior | Astra `medium` / `high`; `xhigh` after a relevant complete failed worker attempt |
| Advisor, including independent acceptance | senior | Astra `medium` / `high`; `xhigh` after a relevant complete failed advisory attempt |

Luna is the usual exploration preference, not a prerequisite. Complexity, judgment
needs, or existing evidence can justify direct Sol or Astra exploration. Model-specific
native names are entry points, not extra capability tiers. Where allowed, use
`medium` for a focused question with sufficient evidence; alternatives, conflicting
evidence, or cross-module constraints can justify `high` initially. Eligibility
does not force escalation. No Explorer `xhigh` route exists.

## Delegate outcomes and retain scheduling

Give every worker an objective, owned scope, retained interfaces, reserved constraints,
and meaningful verification. Include the original task and source references so
the worker can inspect them. Unspecified local implementation choices belong to
the worker. Expected-behavior ambiguity, conflicting requirements, or required
changes to reserved interfaces are contract gaps to resolve before dependent edits.

Workers do their own debugging and implementation without further implementation
delegation. They preserve concurrent and unrelated edits and report actual changes,
checks, judgment calls, and gaps. Rework identifies the violated requirement,
reproducible failure, expected behavior, and verification; structural preference
alone is insufficient.

Check dependencies, ownership (including generated files and check side effects),
and actual available slots before dispatch. Independent delegated tasks may run
concurrently; sequence dependencies, conflicting ownership, and excess capacity.
Do not split a shared file into nominally independent owners or nest workers to
evade capacity. Collect each report and inspect the combined result. A successful
sibling does not complete failed or missing work.

## Recover from evidence

A complete worker attempt includes implementation, ordinary debugging, and verification,
then failed acceptance or a concrete inability to finish the objective. Intermediate
failing tests and individual tool errors are not complete failed attempts.

Diagnose environment problems, missing facts, contract gaps, reasoning failures,
and executor suitability. Repair environment problems and clarify contracts first.
Choose unchanged-allocation rework, a different effort, a more suitable worker, or
primary takeover from the observed cause; there is no mandatory ladder. Primary
takeover is available in ordinary work; Architect mode keeps edits delegated.

Relevant complete worker failure makes Astra worker `xhigh` eligible for the same
work, including takeover carrying that evidence. Unrelated task or role failures
do not qualify. Sol worker `xhigh` needs no prior failure. Stop the previous
conflicting writer, inspect actual state, and preserve useful changes before
reassignment. Follow the current-state handoff in the operations reference.

Every delegated effort change, upward or downward, requires a new native thread.
Model changes and role reassignments also require new matching entry points.
Same-model, same-effort worker rework may reuse its thread. Independent acceptance
always starts fresh, including review after corrections. Never report a resume
with a changed prompt as a new session. Compare actual IDs and settings; this is
an explicit lifecycle policy, not a universal claim about cache behavior or savings.

## Seek judgment when it changes a decision

Proactive advice is allowed. Advice is required for:

- Key decisions not covered by an applicable plan.
- New evidence invalidating a key plan assumption.
- Failure causes still unclear after initial diagnosis.

Reuse applicable advice while its relevant premises hold. Material new evidence
requires renewed judgment; repeated failures require reassessment rather than an
unconditional counter-driven call. Check cited evidence and explain material
disagreement. Advice grants no authorization, veto, new requirement, or ownership
of user goals.

A complete advisory attempt fails when it does not answer the specified question
or source/verification evidence invalidates its material conclusion. Mere disagreement,
intermediate tool errors, and worker failure alone do not unlock Advisor `xhigh`.
Diagnose a relevant advisory failure and choose fact gathering, clarification, or
adjusted effort for that question. An effort change starts a new thread.

## Accept the actual deliverable

Inspect all actual changes, including new files, corrections, and worker-authored
acceptance tests. Check that tests can fail for the intended requirement and rerun
key verification yourself. A report, false completion claim, skipped required
check, or missing runtime evidence cannot establish success.

Ordinary direct, delegated, and mixed multi-step work may complete after primary
checks. Step count, file count, primary identity, or Astra implementation alone
does not require delivery advice or independent acceptance.

High-risk delivery and explicit independent-review requests each require a fresh
Astra Independent reviewer after primary checks, for any primary model. Assess
risk by failure consequences, reversibility, and difficulty establishing correctness.
Decision advice and independent acceptance are both the semantic Advisor role,
but use distinct native entries and contracts. Earlier advice or worker self-review
does not satisfy independent final acceptance.

Choose reviewer `medium` or `high` initially, independently of primary effort;
a primary at `max` may receive either. Only a relevant complete advisory failure
makes reviewer `xhigh` eligible. Check routing, fresh invocation, tool activity,
and scoped before/after state. Resolve material findings, reverify corrections,
and obtain a fresh review of the revised deliverable even at unchanged effort.

Unavailable required execution, unsupported settings, absent or conflicting evidence,
or unresolved material findings leave affected acceptance explicitly pending.
Report the gap without silent substitution; independent unaffected work can continue.
