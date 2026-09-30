# Independent acceptance

Read this when the user asks for independent review or a delivery may be high-risk.
Dispatch the Advisor through [operations.md](operations.md).

## Decide whether it is required

High-risk delivery and explicit independent-review requests each require independent
acceptance after primary checks, for any primary model. Risk follows consequences,
reversibility, and difficulty checking correctness, not step/file count or model.
A consultation, exploration, a worker's self-review, and a delegated check run
cannot satisfy independent acceptance.

## Select the Advisor

Choose the Advisor entry and its dial by the acceptance mapping in the
[routing profile](routing-profile.md#acceptance-mapping). One Advisor entry
answers the acceptance packet, read-only, in a fresh thread.

## Send the acceptance packet

After inspecting the deliverable and completing the checks you own, capture the
scoped state and send this packet to a fresh Advisor thread:

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
the acceptance-mapping case that selected it; requested isolation, and scoped
state captured before review.>
Remain read-only. Do not write, format, implement, or delegate implementation.
Use checks that preserve scoped state; disclose unavailable checks.

RETURN
READINESS: <ready, changes required, or unverified, with reason>
FINDINGS: <severity, exact source references, evidence, and impact>
VERIFICATION: <checks inspected or run, commands, status, and relevant output>
GAPS: <missing evidence, unchecked conditions, and residual risks>
~~~

## Check the review

Validate the Advisor's routing, fresh invocation, and tool activity. Check its
complete-diff inspection, its cited findings, and the scoped before/after state.

## Correct and review again

Resolve material findings, then inspect and reverify the corrections. Ordinary mode
allows primary corrections; Architect mode delegates them. Obtain a fresh review of
the revised deliverable in a new thread, even when entry and effort are unchanged.

Missing required review, unavailable required execution, unsupported settings,
absent or conflicting evidence, a low-confidence verdict, or unresolved material
findings leave the affected acceptance explicitly pending and go to the user.
Report the gap without silent substitution; independent unaffected work can continue.
