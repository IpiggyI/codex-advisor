---
name: orchestration
description: "Use when a primary agent implements or delegates work, selects a role and capability tier from the routing profile, recovers failed attempts through the escalation ladder, uses process consultation, or needs independent acceptance."
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
model name, effort option, default, candidate order, consultation mapping, and
acceptance mapping lives in the routing profile. Respect host capacity, explicit
user exclusions, and resource limits. Select a dial explicitly without asking
permission for each routine allocation.

Choose the role by the output you need: evidence is an Explorer, a change is a
worker, and independent acceptance is an Advisor. New work starts in `mainstay`.
It may start in `crux` when a key difficulty is already identified or interacting
constraints must be handled. There is no usage quota. `rescue` is never a first-round
choice unless the user declares it. The narrower admission rule recorded for possible
future use is not enabled.

Inside a role-and-tier cell, take the first candidate at its default. Take a later
candidate when the outcome depends more on judgment the packet cannot capture.
A capability tier is set by its models; effort is a finer grade inside the tier.

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

After a failed acceptance, issue R1: a rework ticket in the same thread at the
same dial. Rework names the violated requirement, reproducible failure, expected
behavior, and verification; it contains no fix. When rework also fails and the
diagnosis attributes the cause to capability, the attempt and rework together
count as one capability failure.

After a capability failure, move the work to the next tier in a fresh thread with
the current-state handoff. Do not switch to another model in the same tier unless
no other choice exists. The next dial's model level cannot be lower than the failed
dial's unless no other choice exists; if the model stays the same, use a higher
effort. Above that floor, choose by the difficulty the failure exposed.

The path is `mainstay` -> `crux` -> `rescue` -> the user. `rescue` is reached only
through `crux` or a user declaration; work that starts in `crux` reaches `rescue`
after one `crux` capability failure. R3 remains a guard: raise the same model at
most once. Under R4, a major execution problem such as repeated tool failures,
runaway execution, or touching a reserved item may skip rework and counts as one
capability failure.

Stop the previous conflicting writer, inspect actual state, and preserve useful
changes before reassignment. Follow the current-state handoff in the operations
reference. Environment problems and contract gaps do not move work along the path.

Every delegated effort change, upward or downward, requires a new native thread.
Model changes and role reassignments also require new matching entries.
Same-model, same-effort worker rework may reuse its thread. Independent acceptance
always starts fresh, including review after corrections. Never report a resume
with a changed prompt as a new session. Compare actual IDs and settings; this is
an explicit lifecycle policy, not a universal claim about cache behavior or savings.

## Consult at decision points

Process consultation takes no packet and is callable with zero arguments by the
primary, any worker, and any Explorer. It carries the caller's current effective
context automatically, including the unfinished turn and the effective history
after compaction. The advisor runs without tools and returns exactly one plan,
correction, or stop signal with its actual model and effort. An unsupported
reconstruction or failed consultation returns an explicit failure, never fabricated
advice.

A complete consultation attempt returns one allowed result that answers the decision
in context with a supportable conclusion. It fails when it returns no allowed result
or source and verification evidence materially invalidate its conclusion. Mere
disagreement, an intermediate tool error, or worker failure is not such a failure.

Before using consultation, read the consultation mapping in the routing profile
and [consult-posture.md](references/consult-posture.md). Compare the caller's exact
model identity with the assigned advisor model to select the full or reduced posture.
Follow the selected posture block and the adoption block exactly. The advisor has
no escalation path of its own. Consultation does not grant authorization and does
not replace fact checking or independent acceptance.

## Accept the actual deliverable

A complete advisory attempt fails when it does not answer its specified question
or source and verification evidence materially invalidate its conclusion. Mere
disagreement, intermediate tool errors, and worker failure alone are not complete
advisory failures.

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
checks. Step count, file count, primary identity, or use of a particular tier alone
does not require independent acceptance.

High-risk delivery and explicit independent-review requests each require independent
acceptance after primary checks, for any primary model: send the Advisor acceptance
packet to a matching Advisor entry in a fresh thread. A consultation, a worker's
self-review, and a delegated check run cannot satisfy independent acceptance.

Choose the acceptance dial from the routing profile. Work produced in one tier
uses that tier's Advisor entry; work produced by several tiers uses the highest
tier involved. For primary-authored work, use the lowest advisor dial that is not
weaker than the primary's dial; if none qualifies, use the strongest advisor dial.
A primary whose exact model identity is absent from the routing profile also uses
the strongest advisor dial. A low-confidence verdict leaves acceptance pending
and goes to the user; it does not trigger an automatic review at another dial.

Check routing, fresh invocation, tool activity, and scoped before/after state.
Resolve material findings, reverify corrections, and obtain a fresh review of the
revised deliverable even at an unchanged dial. Unavailable required execution,
unsupported settings, absent or conflicting evidence, or unresolved material
findings leave affected acceptance explicitly pending. Report the gap without
silent substitution; independent unaffected work can continue.
