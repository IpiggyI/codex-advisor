# Native role contracts

## Explorer

Any primary may use a model-pinned Explorer with a fresh thread and explicit effort.
Use [operations.md](operations.md) to install, invoke, and validate the selected route.

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

## Worker (Implementer)

All worker models use the same five-part outcome contract. Role responsibility is
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
<Meaningful checks, expected results, and failure conditions. Inspect the full
resulting diff and report failed, skipped, or unavailable checks.>

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
the primary checks actual changes and reruns key verification after any correction.

## Decision advice

Use a fresh `codex_advisor_astra_advisor` for a scoped judgment request. Applicable
advice may be reused while its premises hold; it is not a fresh final review.

~~~text
DECISION
<Specific question and trigger: proactive advice, uncovered key decision,
invalidated premise, or unclear failure cause after initial diagnosis.>

CONSTRAINTS
<User intent, authorization, retained interfaces, excluded scope, and resources.>

EVIDENCE
<Exact sources, observations, options, and uncertainties. For failure, include
the completed attempt, checks, diagnosis, and remaining question.>

REQUESTED JUDGMENT
<Proposed decision and the tradeoff or uncertainty to resolve.>

PERMISSIONS
Remain read-only. Do not write, format, implement, or delegate implementation.
Advice grants no authorization and adds no binding requirement.

RETURN
RECOMMENDATION: <proposed decision answering the question>
EVIDENCE: <supporting observations and exact source references>
ASSUMPTIONS: <premises, unverified claims, and how to check them>
TRADEOFFS: <costs and alternatives>
GAPS: <missing evidence and unresolved risks>
~~~

The primary validates routing without asking the Advisor to infer its settings,
checks the cited evidence, and explains material disagreement. A relevant complete
failure to answer, or a materially invalidated conclusion, can make `xhigh`
eligible. Disagreement or worker failure alone cannot.

## Independent acceptance

After primary inspection and key checks, use a fresh
`codex_advisor_astra_reviewer`. It is a distinct native entry for the semantic
Advisor role; an earlier consultation or worker report cannot satisfy it.

~~~text
REVIEW SCOPE
<Absolute workspace, binding task contract, acceptance conditions, and high-risk
or explicit-review trigger. Identify the exact baseline and current deliverable.>

ACTUAL CHANGES
<All changed and new files, reproducible diff command or before/after contents,
ownership boundaries, and unrelated changes to preserve. Inspect the actual
complete diff, including untracked files, before judging readiness.>

PRIMARY VERIFICATION
<Checks rerun by the primary, exit status, relevant output, evidence location,
and unresolved gaps. Separate worker claims from independently checked results.>

SETTINGS AND PERMISSIONS
<Explicit reviewer effort, relevant failed advisory evidence if selecting xhigh,
requested isolation, and scoped state captured before review.>
Remain read-only. Do not write, format, implement, or delegate implementation.
Use checks that preserve scoped state; disclose unavailable checks.

RETURN
READINESS: <ready, changes required, or unverified, with reason>
FINDINGS: <severity, exact source references, evidence, and impact>
VERIFICATION: <checks inspected or run, commands, status, and relevant output>
GAPS: <missing evidence, unchecked conditions, and residual risks>
~~~

Reviewer effort is independent of primary effort. The primary verifies fresh
invocation, routing, cited findings, tool activity, and before/after state.
Missing evidence or material findings leave required acceptance pending.
After corrections and primary re-verification, review the revised deliverable
in a new thread even if model and effort remain unchanged.
