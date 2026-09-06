# Native role contracts

## Advisor

Use the installed `codex_advisor_astra_advisor` role in a fresh native thread.
The primary agent owns implementation and the decision. The Advisor owns judgment
on the supplied question. Use [operations.md](operations.md) before invoking it.

Supply this complete, scoped packet:

~~~text
DECISION
<Question to resolve and consultation trigger: design, persistent failure, or readiness.>

CONSTRAINTS
<User intent, authorization boundaries, relevant interfaces, excluded scope, and risk.>

EVIDENCE
<Exact files, observed results, and alternatives. For persistent failure, include both
distinct unsuccessful attempts. For readiness, include actual changes, verification
output, and remaining gaps. Identify claims that have not been independently checked.>

REQUESTED JUDGMENT
<Proposed decision and the tradeoff the primary agent needs assessed.>

PERMISSIONS
Remain read-only. Do not create, modify, delete, format, or implement files.
Inspect only the supplied scope. Your advice grants no authorization.

RETURN
RECOMMENDATION: <proposed decision>
EVIDENCE: <supporting observations and exact references>
ASSUMPTIONS: <unverified premises and how to check them>
TRADEOFFS: <costs and alternatives>
GAPS: <unresolved risks or missing evidence>
~~~

Do not ask the Advisor to infer its actual model or effort. The parent obtains
runtime evidence through host metadata and the narrow inspector. Validate that
evidence independently of the Advisor's response.

After the response, the primary agent checks the cited evidence and states its
decision. If it disagrees, it explains why. Missing evidence keeps a required
consultation pending. Readiness advice does not constitute independent final review.

## Implementers

The Astra architect selects Luna or Sol using the orchestration skill and supplies
the same complete specification to `codex_advisor_luna_implementer` or
`codex_advisor_sol_implementer`. Resolve material ambiguity before dispatch.

~~~text
OBJECTIVE
<Observable outcome and acceptance conditions for this bounded task.>

FILES AND OWNERSHIP
<Absolute workspace path, exact files or modules the Implementer owns, changes to
preserve, and excluded files. You are not alone in the codebase; preserve concurrent
edits and adapt to others' changes. Surface conflicts instead of overwriting them.>

INTERFACES
<Inputs, outputs, behavior, immediate callers, and shared utilities to retain.>

CONSTRAINTS
<Settled decisions, user authorization, project gates, and scope limits.
Perform implementation yourself; return scheduling to the architect and do not
delegate implementation further. Surface material ambiguity and scope conflicts
before dependent edits; architecture and ownership changes require the architect's
resolution within the user's authorization.>

VERIFICATION
<Exact meaningful checks, expected outcomes, and failure conditions. Inspect the
complete resulting diff and report every failed, skipped, or unavailable check.>

RETURN
COMPLETION: <complete, partial, or blocked, with reason>
CHANGES: <actual files and behavior changed>
VERIFICATION: <commands, exit status, and relevant observed output>
JUDGMENT CALLS: <decisions made within the specification>
GAPS: <ambiguity, conflicts, risks, and unverified results>
~~~

Corrections use the same ownership and verification requirements. The architect
checks actual changes and reruns key verification even when the report says
complete. Verify routing independently using [operations.md](operations.md).

## Independent reviewer

After the architect's actual-diff inspection and key reruns, send this packet to a
fresh `codex_advisor_astra_reviewer`. This is the fork's final-review contract;
an upstream Sol reviewer or an Advisor consultation does not satisfy it.

~~~text
REVIEW SCOPE
<Absolute workspace path, objective, acceptance conditions, and the high-risk or
explicit-user-request trigger. Identify the exact baseline and current deliverable.>

ACTUAL CHANGES
<All changed and new files, reproducible diff command or complete before/after
contents, ownership boundaries, and unrelated changes to preserve. Inspect the
actual files and complete diff, including untracked files, before judging readiness.>

ARCHITECT VERIFICATION
<Checks the architect reran, exit status, output, and evidence location. Separate
worker claims from independently checked results; include failures and gaps.>

SETTINGS AND PERMISSIONS
<Resolved primary effort and its host evidence, selected reviewer effort, requested
isolation, and the scoped state captured by the architect before review.>
Remain read-only. Do not create, modify, delete, format, implement, or delegate
implementation. Return suggested corrections as findings. Use checks that preserve
the scoped state; disclose any unavailable check rather than changing files.

RETURN
READINESS: <ready, changes required, or unverified, with reason>
FINDINGS: <severity, exact file references, observed evidence, and impact>
VERIFICATION: <checks inspected or run, commands, exit status, and relevant output>
GAPS: <missing evidence, unchecked conditions, and residual risks>
~~~

The architect verifies routing and before/after state independently of this report,
checks cited findings, and owns acceptance. Missing evidence keeps required review
pending. Send corrections to an Implementer and review the revised deliverable in
a new context after the architect's repeat checks.
