# Native role contracts

## Explorer

Any primary may use an Explorer entry with a fresh thread and, unless the entry
pins its effort, an explicit effort. Use [operations.md](operations.md) to install,
invoke, and validate the selected route.

~~~text
QUESTION
<Specific source question, definitions, callers, or behavior to trace.>

SCOPE
<Absolute workspace path, source boundary, exclusions, and known constraints.>

PERMISSIONS
Inspect read-only. Do not write, format, implement, or delegate.
The primary owns design decisions and acceptance.

RETURN
FINDINGS: <observations, precise per-file source locations, and examined scope>
EXPLANATION: <evidence-based reasoning; label inferences>
GAPS: <unavailable sources, failed checks, and unresolved questions>
~~~

Check citations and actual routing independently. A negative search establishes
absence only in the examined scope. Insufficient findings may lead to direct
primary investigation or another authorized allocation; disclose any unverified call.
Exploration is neither implementation nor independent final acceptance.

## Worker

All Worker entries use the same five-part outcome contract. Role responsibility is
independent of tier. The primary retains decomposition, scheduling, and acceptance;
unspecified local implementation choices belong to the worker.

~~~text
OBJECTIVE
<Observable outcome, acceptance conditions, original task reference, and sources.>

FILES AND OWNERSHIP
<Absolute workspace path, exact owned files/modules, excluded scope, and current
changes. You are not alone in the codebase; preserve concurrent and unrelated
edits and adapt to others' work. Surface conflicts instead of overwriting them.>

INTERFACES
<Inputs, outputs, behavior, callers, and shared interfaces that must be retained.>

CONSTRAINTS
<Binding decisions, user boundaries, resources, and reserved choices. Inspect the
original task and relevant sources. Perform implementation yourself; do not delegate
implementation further. Resolve unclear expected behavior, conflicting requirements,
and changes to reserved interfaces with the primary before dependent edits.>

VERIFICATION
<The checks this contract requires, expected results, and failure conditions.
Run them, plus whatever your own debugging needs; checks that span other work
packages or the whole delivery belong to the primary's schedule. Inspect the
full resulting diff and report failed, skipped, or unavailable checks.>

RETURN
COMPLETION: <complete, partial, or blocked, with reason>
CHANGES: <actual files and behavior changed>
VERIFICATION: <commands, exit status, and relevant observed output>
JUDGMENT CALLS: <local decisions within the contract>
GAPS: <ambiguity, conflicts, risks, and unverified results>
~~~

For rework, identify the violated requirement, reproducible failure, expected
behavior, and verification. Structural preference alone does not justify rework.
The worker owns ordinary debugging. Use the operations handoff for reassignment;
after any correction the primary inspects the actual changes and verifies the
failed scenario and the scope it affects, reusing evidence the correction leaves
valid.

## Advisor

One Advisor entry per tier answers the acceptance packet. It runs read-only in a
fresh thread. Select its dial by the accepted work: use the work's tier, the highest
tier involved for work built by several tiers, or the lowest advisor dial not weaker
than the primary's dial for primary-authored work. If no advisor dial qualifies,
or the primary's exact model id is absent from the routing profile, use the strongest
advisor dial. A low-confidence verdict leaves acceptance pending and goes to the
user; it does not trigger an automatic review at another dial.

Process consultation takes no packet. It is a separate zero-argument call governed
by the routing profile and [consult-posture.md](consult-posture.md), and it never
substitutes for independent acceptance.

### Independent acceptance

After inspecting the deliverable and completing the checks you own, send the
acceptance packet to a fresh Advisor thread. An earlier consultation, worker report,
or delegated check run cannot satisfy it.

~~~text
REVIEW SCOPE
<Absolute workspace, binding task contract, acceptance conditions, and high-risk
or explicit-review trigger. Identify the exact baseline and current deliverable.>

ACTUAL CHANGES
<All changed and new files, reproducible diff command or before/after contents,
ownership boundaries, and unrelated changes to preserve. Inspect the actual
complete diff, including untracked files, before judging readiness.>

PRIMARY VERIFICATION
<Checks the primary owns for this acceptance: executor, scope, command, exit
status, relevant output, evidence location, and unverified items. Separate worker
claims from results the primary organized and confirmed.>

SETTINGS AND PERMISSIONS
<Selected Advisor entry and, where the entry leaves it open, the explicit effort;
the accepted work's tier or the primary-derived dial rule; requested isolation,
and scoped state captured before review.>
Remain read-only. Do not write, format, implement, or delegate implementation.
Use checks that preserve scoped state; disclose unavailable checks.

RETURN
READINESS: <ready, changes required, or unverified, with reason>
FINDINGS: <severity, exact source references, evidence, and impact>
VERIFICATION: <checks inspected or run, commands, status, and relevant output>
GAPS: <missing evidence, unchecked conditions, and residual risks>
~~~

The primary verifies fresh invocation, routing, cited findings, tool activity, and
before/after state. Missing evidence, a low-confidence verdict, or material findings
leave required acceptance pending. After corrections and primary re-verification,
review the revised deliverable in a new thread even if entry and effort remain
unchanged.
