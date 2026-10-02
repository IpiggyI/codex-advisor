# Recovery and handoff

Read this after a failed acceptance, before issuing rework or reassigning work.
A reassignment is a new dispatch: also follow [operations.md](operations.md).

## Count a complete attempt

A complete worker attempt includes implementation, ordinary debugging, and verification,
then failed acceptance or a concrete inability to finish the objective. Intermediate
failing tests and individual tool errors are not complete failed attempts.

## Diagnose before acting

Diagnose environment problems, missing facts, contract gaps, reasoning failures,
and executor suitability before choosing repair, clarification, or a ladder step.
Repair environment problems first. A contract gap (unclear expected behavior,
conflicting requirements, a reserved interface) is a corrected contract on the
same thread, not a ladder step and not a capability failure. Environment problems
and contract gaps do not move work along the path below. Primary takeover is
available in ordinary work; Architect mode keeps edits delegated.

## Climb the escalation ladder

After a failed acceptance, issue R1: a rework ticket in the same thread at the
same dial. Rework names the violated requirement, reproducible failure, expected
behavior, and verification; it contains no fix, and structural preference alone
does not justify it. When rework also fails and the diagnosis attributes the cause
to capability, the attempt and rework together count as one capability failure.

After a capability failure, move the work to the next tier in a fresh thread with
the handoff below. Do not switch to another model in the same tier unless no other
choice exists. The next dial's model segment in the
[routing profile](routing-profile.md#model-segments) cannot be lower than the failed dial's
unless no other choice exists; if the model stays the same, use a higher effort.
Above that floor, choose by the difficulty the failure exposed.

The path is `mainstay` -> `crux` -> `rescue` -> the user. `rescue` is reached only
through `crux` or a user declaration; work that starts in `crux` reaches `rescue`
after one `crux` capability failure. R3 remains a guard: raise the same model at
most once. Under R4, a major execution problem such as repeated tool failures,
runaway execution, or touching a reserved item may skip rework and counts as one
capability failure.

## Keep or replace the thread

Same-model, same-effort worker rework may continue its thread through native
follow-up, which keeps the thread's `task_name`. Every delegated effort change,
upward or downward, requires a new native thread with explicit settings; model
changes and role reassignments also require new matching entries. A resumed thread
with a different requested effort does not satisfy this policy, and a resume with
a changed prompt is never reported as a new session. This is an explicit lifecycle
policy, not a universal claim about cache behavior or savings.

## Hand off actual state

Before replacing a writer, finish or stop its conflicting activity and obtain
available evidence. Inspect actual scoped changes and preserve useful partial
results and unrelated edits. Give the successor this compact handoff alongside
its role packet:

~~~text
OBJECTIVE AND BINDING DECISIONS
<Original task, authorized scope, ownership, retained interfaces, and constraints.>

CURRENT STATE
<Actual changed/new files, useful partial changes, relevant task/source references,
and confirmation that the predecessor no longer writes this scope.>

ATTEMPT AND DIAGNOSIS
<Previous role/model/effort/thread, completed checks, failed acceptance or inability,
reproducible evidence, diagnosed cause, and any unresolved contract gap.>

REMAINING WORK
<Corrections and verification still needed without lowering acceptance conditions.>
~~~

Record predecessor/successor IDs, observed efforts, and new-spawn versus follow-up
events. Compare real IDs and settings, not labels or prose. Missing or contradictory
transition evidence leaves the transition unverified.
