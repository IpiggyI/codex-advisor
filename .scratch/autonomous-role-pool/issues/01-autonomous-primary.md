# 01: Autonomous Implementation and Delegation

**What to build:** Any primary model can complete ordinary work by implementing directly, delegating a bounded task to an appropriate worker, or combining both. The primary chooses the initial allocation, supplies an outcome-based contract, checks the actual result, and can finish ordinary multi-step work without a mandatory Advisor call. An explicit Architect-mode request makes implementation delegation-only for its authorized scope. This ticket delivers the initial worker execution path; ticket 03 adds failure recovery and reassignment.

**Blocked by:** None (can start immediately).

**Status:** resolved

- [x] Ordinary work allows direct implementation and delegation for any primary model. A midrange primary such as Sol is a user preference; the plugin neither selects it nor changes the primary's model or effort.
- [x] The primary can adjust decomposition, order, and division of work within the user's authorization. A task artifact or model identity alone does not activate Architect mode.
- [x] An explicit Architect-mode request works with any primary model and delegates every implementation edit and correction within its scope. Authorization lasts for the current task and its follow-ups unless the user explicitly grants session-wide scope; unrelated tasks and unaccepted proposals do not inherit it.
- [x] The primary interprets and executes the user's requirements without unilaterally changing goals, scope, reserved decisions, acceptance conditions, or resource limits. It investigates mismatches with current code, seeks resolution for user-owned changes, and continues unaffected work.
- [x] The worker role is the routing name for Implementer. Role responsibility is distinct from capability tier; the same ownership and reporting contract applies to all worker models.
- [x] Initial worker routing is light: Luna at max; standard: Sol at high or xhigh; senior: Astra at medium or high. Sol xhigh is available on the first attempt without separate user selection. Astra xhigh is not an initial route without relevant failed-attempt evidence; its recovery path belongs to ticket 03.
- [x] The primary explicitly selects an allowed effort within authorized resources without a permission question for each call. Focused work with sufficient evidence can use medium where allowed; conflicting evidence, alternatives, or cross-module constraints can justify high initially.
- [x] Existing native worker identities retain their intended model pins. Luna worker remains fixed at max; adjustable workers honor the explicitly selected effort rather than overriding it or inheriting an unintended primary setting.
- [x] Each worker receives an objective, owned scope, retained interfaces, reserved constraints, and meaningful verification. It can inspect the original task and relevant source rather than relying only on the primary's summary.
- [x] Unspecified local implementation choices belong to the worker. Unclear expected behavior, conflicting requirements, or necessary changes to reserved interfaces are reported as contract gaps before dependent edits.
- [x] Rework instructions identify the violated requirement, reproducible failure, expected behavior, and verification. Structural preference alone does not justify rework, and the worker owns its local debugging.
- [x] Workers preserve unrelated and concurrent edits, perform their own implementation without further implementation delegation, and report actual changes, checks, judgment calls, and gaps.
- [x] The primary retains scheduling: independent tasks may run within available capacity, while dependencies and conflicting ownership are sequenced. It checks the combined deliverable rather than treating one worker's success as completion of all work.
- [x] The primary inspects actual changes, including new files and worker-authored acceptance tests, and reruns key verification before acceptance. A report, false completion claim, or skipped required check cannot establish success.
- [x] Ordinary direct, delegated, and mixed multi-step work can complete after the primary's checks without mandatory delivery advice. High-risk work and explicit independent-review requests still require a fresh second reader after those checks; ticket 04 changes advisory routing and effort rules.
- [x] A missing worker, unsupported allocation, or missing or conflicting runtime evidence leaves the affected work visibly pending without silent substitution. Evidence distinguishes native role, model, effort, thread, parent association, working directory, and observed permissions.
- [x] Worker installation and selective checking remain idempotent. Modified or unsafe destinations are refused before partial mutation, with explicit reconciliation for changed installed templates. Unrelated agents and primary configuration remain intact, and diagnostics do not expose prompts or credentials.
- [x] Current workflow instructions, worker descriptions, contracts, invocation guidance, glossary, architecture decisions, and public descriptions agree on this delivered behavior. Superseded Astra-only eligibility and explicit-Sol-selection decisions are identified without rewriting historical acceptance evidence or advertising unfinished routes.
- [x] A small disposable scenario demonstrates direct work, autonomous worker selection, primary verification, and ordinary completion; a separate instruction demonstrates delegation-only Architect mode. Tiny native calls cover the initial worker allocations, including first-attempt Sol xhigh, with actual metadata and simple outcome checks.
- [x] Reuse existing installation, runtime-evidence, and scheduling checks, adding only cases affected by this ticket. Controlled missing-role or invalid-evidence inputs exercise visible failure; no complex project or exhaustive primary, effort, and transport cross-product is required.
- [x] Record each scoped route or branch with expected behavior, observed evidence, tested revision and host, and explicit gaps. Check the combined state with already completed sibling work, reuse valid evidence, and rerun only affected checks; documentation and validation are completed within this ticket.
- [x] These checks establish routing behavior only. Quality, stability, and savings remain for later real-task experience. Use disposable installations; do not change the active user installation, publish a release, or add a scheduler, provider bridge, budget service, or profile schema.

## Acceptance

Completed on 2026-09-12. Public installation/runtime checks passed. Disposable Sol-primary
work exercised direct edits, autonomous light-worker selection, both initial Sol
efforts, senior worker calls, combined primary checks, ordinary completion, and an
explicit delegation-only Architect phase. See [acceptance evidence](../acceptance.md)
for exact native settings, state checks, and the deliberately limited smoke scope.
