# Native Advisor contract

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
