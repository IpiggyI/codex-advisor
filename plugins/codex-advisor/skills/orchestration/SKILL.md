---
name: orchestration
description: "Use when a primary agent is asked to delegate or is about to delegate work or to accept, rework, or escalate a delegated result, when the user authorizes Architect mode, or when a delivery needs independent acceptance. Also use when a primary, worker, or Explorer lacks applicable selected posture or adoption instructions."
---

# Codex Advisor orchestration

## Own the task

Any primary model may implement directly, delegate bounded work, or combine both.
Preserve the user's primary model and reasoning effort. Choose decomposition, order,
and division of work within the user's authorized goals, scope, reserved decisions,
acceptance conditions, and resource limits. Do not change those boundaries to make
the task easier. Investigate mismatches with current code, seek resolution for
user-owned changes, and continue independent unaffected work.

Explicit Architect-mode authorization makes every implementation edit and correction
delegated for its scope, for any primary model. The primary owns design, contracts,
scheduling, and acceptance and may write design and task artifacts. Model identity,
a ticket, a specification, or an unaccepted proposal does not activate this mode.
Record the authorizing request. It lasts for this task and follow-ups; unrelated
tasks need new authorization unless the user explicitly granted session-wide scope.

## Read references by event

Read only the references the current event names. The rule after each pointer
holds even before its reference is read.

- Before a new native spawn, including a reassignment and the Advisor dispatch for
  independent acceptance: read [operations.md](references/operations.md) and the
  dial table in [routing-profile.md](references/routing-profile.md). An Explorer
  or Worker spawn also reads its packet in
  [role-contracts.md](references/role-contracts.md); an Advisor spawn uses the
  packet in the independent-acceptance reference below instead. Spawn with
  `fork_turns: none`; a dispatch counts as checked only when the hook's
  confirmation line or the inspector shows its model and effort.
- Accepting a delegated result, or working under Architect mode: this file suffices.
- After a failed acceptance, before rework or escalation: read
  [recovery.md](references/recovery.md). Rework first in the same thread at the
  same dial; any change of effort, model, or role uses a new thread with the
  current-state handoff.
- When the user asks for independent review or a delivery may be high-risk: read
  [independent-acceptance.md](references/independent-acceptance.md) and the
  acceptance mapping in the routing profile. Independent acceptance runs in a
  fresh Advisor thread after your own checks; consultation, self-review, and a
  delegated check run never substitute for it.
- When a posture or adoption block is missing or inapplicable: read
  [consult-posture.md](references/consult-posture.md) and the consultation mapping
  in the routing profile, as described under consultation below.

## Allocate by role and capability tier

Every model segment, model name, effort option, default, candidate order, consultation mapping,
and acceptance mapping lives in the routing profile. Respect host capacity, explicit
user exclusions, and resource limits. Select a dial explicitly without asking
permission for each routine allocation.

Choose the role by the output you need: evidence is an Explorer, a change is a
worker, and independent acceptance is an Advisor. New work starts in `mainstay`.
It may start in `crux` when a key difficulty is already identified or interacting
constraints must be handled. There is no usage quota. `rescue` is never a first-round
choice unless the user declares it.

Inside a role-and-tier cell, take the first candidate at its default. Take a later
candidate when the task needs its higher model segment or depends more on judgment
the packet cannot capture. Compare model segments through the routing profile's
[segment table](references/routing-profile.md#model-segments).
A capability tier is set by its models; effort is a finer grade inside the tier.

## Delegate outcomes and retain scheduling

Give every worker an objective, owned scope, retained interfaces, reserved constraints,
and meaningful verification. Include the original task and source references so
the worker can inspect them. Unspecified local implementation choices belong to
the worker. Expected-behavior ambiguity, conflicting requirements, or required
changes to reserved interfaces are contract gaps to resolve before dependent edits.
Workers own implementation and ordinary debugging and do not delegate it further;
their packet carries the rest of the contract. Checks that span other work packages
or the whole delivery stay in your plan.

Check dependencies, ownership (including generated files and check side effects),
and actual available slots before dispatch. Decide ticket boundaries, dispatch
count, and verification batches separately: combine checks that share costly
setup while the scope stays understandable and a failure stays locatable, and
keep a real check where dependent work rests on its result. Independent delegated
tasks may run concurrently; sequence dependencies, conflicting ownership, and
excess capacity, and update each sequenced packet with the actual state its
predecessor left. Do not split a shared file into nominally independent owners or
nest workers to evade capacity. Collect each report and inspect the combined
result. Failed, blocked, missing, or incomplete work and its dependents stay
pending; a successful sibling does not complete them.

## Accept the actual deliverable

Inspect all actual changes yourself, including new files, corrections, and
worker-authored acceptance tests. Check that tests can fail for the intended
requirement and that the evidence describes the current deliverable. A report,
false completion claim, skipped required check, or missing runtime evidence
cannot establish success.

Primary checks are the checks you own and confirm. Name one executor per
verification batch: yourself, or a delegate that receives the complete batch
requirements, the merged changes, and the evidence already collected, and reports
executor, scope, command, exit status, output location, and unverified items;
a delegated run never moves the acceptance decision. Run each batch once, then
reconcile coverage, actual output, and the current combined state. Reuse a result
while the relevant code, artifacts, checks, inputs, and environment still support
it. A changed executor or a new session is not by itself a reason to run a check
again; a changed dependency, an evidence gap, an unexplained failure, or an
identified risk is, and rework covers the failed scenario and the scope it affects.

Ordinary direct, delegated, and mixed multi-step work may complete after primary
checks. Step count, file count, primary identity, or use of a particular tier alone
does not require independent acceptance.

## Consult at decision points

Process consultation is the `codex_advisor` MCP server's `process_consultation`
tool. The primary, any worker, and any Explorer call it with `{}`; it takes no
packet, summary, prompt, path, or dial. It carries the caller's current effective context
automatically, including the unfinished turn and the effective history after
compaction. The advisor runs without tools and returns exactly one plan,
correction, or stop signal with its host-recorded model and effort. A `stop` is a
successful result: halt and escalate as advised. Only a successful terminal result
counts as consultation. An unsupported reconstruction or failed consultation returns
an explicit failure, never fabricated advice; the work stays pending, and the caller
states the failure in its next visible reply without presenting it as advice or
declaring consultation complete.

A complete consultation attempt returns one allowed result that answers the decision
in context with a supportable conclusion. It fails when it returns no allowed result
or source and verification evidence materially invalidate its conclusion. Mere
disagreement, an intermediate tool error, or worker failure is not such a failure.

Use the selected consultation posture and adoption blocks already in context.
The server selects the advisor dial. If either block is missing or inapplicable,
read the consultation mapping in the routing profile and
[consult-posture.md](references/consult-posture.md), compare exact caller/advisor
model identities, and select the full or reduced posture. Follow both blocks
exactly; no hook blocks completion automatically. The advisor has no escalation
path of its own. Consultation does not grant authorization and does not replace
fact checking or independent acceptance.
