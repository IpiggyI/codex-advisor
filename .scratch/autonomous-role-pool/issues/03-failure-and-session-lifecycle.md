# 03: Failure Recovery and Fresh Sessions

**What to build:** After a complete failed worker attempt, the primary diagnoses the cause and chooses repair, clarification, rework, higher effort, or a more suitable executor. Any delegated effort change starts a fresh native session with the actual current task state. Same-model, same-effort worker correction can reuse its session. This recovery path builds on the autonomous worker execution delivered by ticket 01.

**Blocked by:** 01 - Autonomous Implementation and Delegation.

**Status:** resolved

- [x] A complete worker attempt includes implementation, ordinary debugging, and verification followed by failed acceptance or a concrete inability to complete the assigned objective. Intermediate failing tests and individual tool errors do not count as complete failed attempts.
- [x] The primary distinguishes environment problems, missing facts, contract gaps, reasoning failures, and an unsuitable executor. Environment and contract failures first lead to repair or clarification rather than presumed model insufficiency.
- [x] The primary chooses the response from the observed cause: unchanged-allocation rework, more effort, or stronger-worker takeover are options rather than a mandatory ladder. Eligibility for xhigh does not force its use.
- [x] Relevant complete failure makes Astra worker xhigh eligible for that same work, including a takeover carrying its failure evidence. An unrelated task or role failure does not establish eligibility. Sol worker xhigh remains available initially, and Explorer does not gain an xhigh route.
- [x] The handoff retains the failed objective, attempted allocation, observed checks and failure, diagnosis, and remaining work. The workflow establishes eligibility; the metadata inspector checks actual allocation without claiming to have inferred failure or authorization from private prompts.
- [x] Every delegated effort change, upward or downward, starts a fresh native thread with explicit settings. This lifecycle rule applies to all roles; use the already available worker routes to verify it without requiring ticket 02's additional Explorers.
- [x] Same-model, same-effort worker rework may reuse its thread. Model or role reassignment uses a fresh matching entry point, and independent acceptance always starts fresh even when its effort is unchanged.
- [x] Compare actual predecessor and successor thread IDs and observed efforts. A follow-up or resume in the old thread cannot be reported as a fresh session, even if its prompt requests a different effort.
- [x] Before reassignment, stop the previous conflicting writer, inspect actual scoped state, and preserve useful partial changes. The primary can take over directly in ordinary work; explicit Architect mode keeps implementation delegated.
- [x] The new executor receives the objective, binding decisions, ownership, current changes, relevant task and source references, completed checks, failed-attempt evidence, and remaining verification. It need not reconstruct state from a copied full conversation.
- [x] Corrections remain within user-authorized goals and constraints. The primary does not lower acceptance standards to declare recovery successful and verifies the actual combined result after rework or takeover.
- [x] Unknown failure causes lead to a focused request for judgment before another unsupported attempt; ticket 04 supplies the complete revised advisory policy and advisory-failure eligibility. Independent unaffected work can continue.
- [x] Missing or contradictory transition metadata, unsupported settings, or unavailable required execution leaves the affected result pending. No role self-report or silent substitution can establish a successful transition.
- [x] Recovery contracts, native invocation guidance, affected role instructions, current architecture decisions, and public descriptions agree on the lifecycle. Fresh sessions are an explicit policy, not a claim about universal cache invalidation or guaranteed savings.
- [x] Controlled evidence distinguishes an intermediate test failure from a complete failed attempt and exercises environment repair, contract clarification, unchanged rework, and eligible escalation. Use tiny tasks, not difficult real projects, to trigger the branches.
- [x] Observe one unchanged-allocation worker correction and effort changes in both directions, with actual native thread IDs, selected settings, and a compact current-state handoff. Reuse these traces and existing metadata fixtures across checks rather than repeating calls.
- [x] Record branch outcomes, actual thread transitions, tested revision and host, and unverified gaps. Run the relevant existing checks against the combined state, complete documentation in this ticket, and defer quality, stability, and savings judgments to later real-task experience.

## Acceptance

Completed on 2026-09-12. A controlled complete missing-prerequisite failure led to
environment repair and same-thread medium correction. Medium-to-high and high-to-medium
changes used different native threads with actual-state handoffs; an eligible xhigh
call carried the relevant failure evidence. Short policy probes covered clarification,
cause-based choices, and invalid transitions. See [acceptance evidence](../acceptance.md).
