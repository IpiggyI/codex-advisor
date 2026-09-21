---
name: orchestration
description: "Use when a primary agent implements or delegates work, selects a role and capability tier from the routing profile, recovers failed attempts through the escalation ladder, or needs Advisor decision advice and independent acceptance."
---

# Codex Advisor orchestration

## Own the task

Any primary model may implement directly, delegate bounded work, or combine both.
Preserve the user's primary model and reasoning effort. A midrange primary is a
preference, not a plugin requirement. Choose decomposition, order, and division
of work within the user's authorized goals, scope, reserved decisions, acceptance
conditions, and resource limits. Do not change those boundaries to make the task
easier. Investigate mismatches with current code, seek resolution for user-owned
changes, and continue independent unaffected work.

Explicit Architect-mode authorization makes every implementation edit and correction
delegated for its scope, for any primary model. The primary owns design, contracts,
scheduling, and acceptance and may write design and task artifacts. Model identity,
a ticket, a specification, or an unaccepted proposal does not activate this mode.
Record the authorizing request. It lasts for this task and follow-ups; unrelated
tasks need new authorization unless the user explicitly granted session-wide scope.

## Allocate by role and capability tier

Before a delegated call, read the relevant packet in
[role-contracts.md](references/role-contracts.md), the installation, invocation,
evidence, and permission procedures in [operations.md](references/operations.md),
and the dial table in [routing-profile.md](references/routing-profile.md). Every
model name, effort option, default, and candidate order lives in the routing
profile, not here. Respect host capacity and explicit user exclusions and resource
limits. Select a dial explicitly without asking permission for each routine allocation.

Choose the role by the output you need: evidence is an Explorer, a change is a
worker, judgment or acceptance is an Advisor. Choose the tier inside the first-round
pool, light or standard, by how much the outcome depends on judgment the packet
cannot capture. There is no precondition between light and standard; light to
standard is not an escalation. Take the cheapest adequate dial at its default.
Eligibility does not force escalation.

Senior is reached only through the senior gate: two capability-attributed complete
failed attempts inside the pool on the same work, or a user declaration. For the
Advisor the gate is only a verdict that reports low confidence or a user declaration;
worker failures do not open it. The Advisor's decision packet defaults to the
standard tier and its acceptance packet to the light tier.

## Delegate outcomes and retain scheduling

Give every worker an objective, owned scope, retained interfaces, reserved constraints,
and meaningful verification. Include the original task and source references so
the worker can inspect them. Unspecified local implementation choices belong to
the worker. Expected-behavior ambiguity, conflicting requirements, or required
changes to reserved interfaces are contract gaps to resolve before dependent edits.

Workers do their own debugging and implementation without further implementation
delegation. They preserve concurrent and unrelated edits and report actual changes,
checks, judgment calls, and gaps. A worker runs the verification its packet
specifies and whatever its own debugging needs; acceptance checks that span
other work packages or the whole delivery stay in your plan. Rework identifies
the violated requirement, reproducible failure, expected behavior, and
verification; structural preference alone is insufficient.

Check dependencies, ownership (including generated files and check side effects),
and actual available slots before dispatch. Decide ticket boundaries, dispatch
count, and verification batches separately: combine checks that share costly
setup while the scope stays understandable and a failure stays locatable, and
keep a real check where dependent work rests on its result. Independent delegated
tasks may run concurrently; sequence dependencies, conflicting ownership, and
excess capacity. Do not split a shared file into nominally independent owners or
nest workers to evade capacity. Collect each report and inspect the combined
result. A successful sibling does not complete failed or missing work.

## Recover from evidence

A complete worker attempt includes implementation, ordinary debugging, and verification,
then failed acceptance or a concrete inability to finish the objective. Intermediate
failing tests and individual tool errors are not complete failed attempts.

Diagnose environment problems, missing facts, contract gaps, reasoning failures,
and executor suitability. Repair environment problems first. A contract gap
(unclear expected behavior, conflicting requirements, a reserved interface) is
a corrected contract on the same thread, not a ladder step and not a capability
failure. Primary takeover is available in ordinary work; Architect mode keeps
edits delegated.

After a failed acceptance, follow the escalation ladder:

- R1: a rework ticket in the same thread at the same dial. Rework names the violated
  requirement, reproducible failure, expected behavior, and verification; it
  contains no fix.
- R2: when rework also fails and the cause is capability, a raise in a fresh thread
  carrying the current-state handoff: either a higher effort of the same model or
  another model.
- R3: the same model is raised at most once.
- R4: a major execution problem (tools failing repeatedly, runaway, touching reserved
  items) may skip the rework ticket and change model directly; it counts as one failure.

Whether the second complete failure inside the pool warrants senior is a key decision
requiring advice, so the senior gate coincides with that consultation and the
Advisor's verdict also settles whether senior is warranted. Stop the previous
conflicting writer, inspect actual state, and preserve useful changes before
reassignment. Follow the current-state handoff in the operations reference.

Every delegated effort change, upward or downward, requires a new native thread.
Model changes and role reassignments also require new matching entries.
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
intermediate tool errors, and worker failure alone do not open the Advisor's senior
gate. Diagnose a relevant advisory failure and choose fact gathering, clarification,
or another dial for that question. A dial change starts a new thread.

## Accept the actual deliverable

Inspect all actual changes yourself, including new files, corrections, and
worker-authored acceptance tests. Check that tests can fail for the intended
requirement and that the evidence describes the current deliverable. A report,
false completion claim, skipped required check, or missing runtime evidence
cannot establish success.

Primary checks are the checks you own and confirm. Run them yourself or assign
them to an executor that receives the complete batch requirements and reports
executor, scope, command, exit status, output location, and unverified items;
a delegated run never moves the acceptance decision. Reuse a result while the
relevant code, artifacts, checks, inputs, and environment still support it. A
changed executor or a new session is not by itself a reason to run a check again;
a changed dependency, an evidence gap, an unexplained failure, or an identified
risk is, and rework covers the failed scenario and the scope it affects.

Ordinary direct, delegated, and mixed multi-step work may complete after primary
checks. Step count, file count, primary identity, or a senior implementation alone
does not require delivery advice or independent acceptance.

High-risk delivery and explicit independent-review requests each require independent
acceptance after primary checks, for any primary model: the Advisor's acceptance
packet on an Advisor entry in a fresh thread. Assess risk by failure consequences,
reversibility, and difficulty establishing correctness. Decision advice and independent
acceptance are the two request shapes of one Advisor role and its entries. Earlier
advice, a worker's self-review, and a delegated check run do not satisfy
independent final acceptance.

Choose the acceptance dial independently of primary effort; a primary at a high
effort may receive acceptance at the light tier. Only a low-confidence verdict or
a user declaration opens the Advisor's senior gate. Check routing, fresh invocation,
tool activity, and scoped before/after state. Resolve material findings, reverify
corrections, and obtain a fresh review of the revised deliverable even at an
unchanged dial.

Unavailable required execution, unsupported settings, absent or conflicting evidence,
or unresolved material findings leave affected acceptance explicitly pending.
Report the gap without silent substitution; independent unaffected work can continue.
