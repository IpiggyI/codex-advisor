# Codex Advisor

Shared vocabulary for primary autonomy, delegated responsibilities, consultation,
and acceptance.

## Language

**Primary agent**:
The agent that owns the user's task, decomposition, scheduling, technical decisions within authorization, and final acceptance. It can implement, delegate, or combine both in ordinary work.
_Avoid_: Treating autonomy as authority to change user goals, acceptance conditions, or resource limits.

**Architect mode**:
An explicitly user-authorized mode, available to any primary model, in which the primary owns design and acceptance and delegates every implementation edit and correction.
_Avoid_: Activating the mode from model identity or a task artifact.

**Advisor**:
A read-only judgment role used for process consultation and independent acceptance. The primary checks its evidence, owns the decision, and explains material disagreement.
_Avoid_: Treating advice as authorization, an automatic veto, or a new binding requirement; a separate reviewer role.

**Worker**:
A delegated agent responsible for an outcome within assigned ownership, retained interfaces, constraints, and verification. It owns unspecified local implementation choices and debugging.
_Avoid_: Implementer; transferring scheduling or final acceptance to the worker.

**Native entry**:
A shipped Codex custom agent named by role and tier, such as `ca_explorer_mainstay_m` or `ca_worker_crux_m`. A native entry fixes its model and may fix its reasoning effort.
_Avoid_: Naming an entry by model; treating an entry as a tier or role of its own.

**Routing profile**:
The authoritative mapping from each role and capability tier to its native entries and dials, plus the mappings for process consultation and independent acceptance.
_Avoid_: Repeating model names, effort options, defaults, candidate order, or dial mappings in the orchestration doctrine; a hand-edited installed copy.

**Companion installer**:
The plugin script that writes the shipped native entries onto `$CODEX_HOME/agents`, overwriting this plugin's own files, deleting retired entry names, and touching nothing else.
_Avoid_: Hand-editing installed entries; expecting the installer to preserve a hand-edited copy.

**Capability tier**:
An ordered allocation level for one delegated call, set by its models, with effort as a finer grade inside it. The three tiers are `mainstay`, `crux`, and `rescue`.
_Avoid_: Treating effort as a tier; light, standard, or senior as current tier names.

**Mainstay**:
The default capability tier for new work and the tier intended to finish most tasks.
_Avoid_: First-round pool; requiring a prior failure before entering mainstay.

**Crux**:
The capability tier for work with an identified key difficulty or interacting constraints, and the next tier after a mainstay capability failure.
_Avoid_: A quota for first-round crux use; requiring the reserved narrow admission rule.

**Rescue**:
The standby capability tier reached through crux after a capability failure or by user declaration.
_Avoid_: Senior gate; selecting rescue at first round without a user declaration.

**Escalation ladder**:
The recovery sequence after failed acceptance: same-dial rework; one diagnosed capability failure moves work to the next tier without lowering model level or switching models inside the failed tier unless no other choice exists; rescue failure returns the work to the user. The same model is raised at most once, and a major execution problem may skip rework.
_Avoid_: Switching models inside one tier after capability failure when another choice exists; treating an environment problem or contract gap as a capability failure.

**Dial**:
A model at one reasoning effort inside a role-and-tier cell. The routing profile defines the allowed efforts, defaults, and candidate order.
_Avoid_: Writing a dial as a tier; reconstructing dial values from doctrine prose.

**Explorer**:
A read-only evidence role available to any primary that investigates scoped questions and returns precise sources, observations, examined scope, and gaps.
_Avoid_: Assigning implementation or counting exploration as independent acceptance.

**Complete attempt**:
An executor's attempt through its assigned work and ordinary checks, ending in accepted completion, failed acceptance, or concrete inability. An advisory attempt must answer its specified question with a supportable conclusion. A consultation attempt must return an allowed result that answers the decision in context with a supportable conclusion.
_Avoid_: Counting intermediate test or tool failures, or mere disagreement with advice, as complete failed attempts.

**Process consultation**:
A zero-argument judgment call that receives the caller's current effective context and returns a plan, correction, stop signal, or explicit failure. It uses no request packet and never replaces independent acceptance.
_Avoid_: Decision packet; a caller-written summary; fabricated advice after failed context reconstruction.

**Full posture**:
The consultation posture used when the caller's exact model id differs from its assigned advisor model id. It calls before substantive work, when stuck, before changing approach, and before declaring done.
_Avoid_: Selecting posture from a model family.

**Reduced posture**:
The consultation posture used when the caller's exact model id equals its assigned advisor model id. On multi-step work it calls before settling on an approach and before declaring done.
_Avoid_: Applying full-posture triggers to every same-model call.

**Reconcile call**:
One additional process consultation that states the evidence-advice conflict and asks which constraint breaks the tie.
_Avoid_: Silently changing direction; directly rejecting a different-model advisor for a reasoning flaw without reconciliation.

**Primary checks**:
The checks the primary owns and confirms for acceptance. It runs them itself or assigns one executor that receives the complete batch requirements and reports executor, scope, command, exit status, output location, and unverified items. Inspecting the actual complete diff and confirming that a test can fail for the intended requirement stay with the primary.
_Avoid_: Treating a delegated run as the acceptance decision; repeating a valid result only because the executor or session changed.

**Verification batch**:
A group of acceptance checks with one named executor, formed separately from ticket and dispatch boundaries so that work sharing costly setup is checked together while the scope stays understandable and a failure stays locatable.
_Avoid_: Accumulating unverified premises that dependent work rests on; moving a worker's ordinary debugging into the batch.

**Independent acceptance**:
A fresh-thread, packet-based review of the actual deliverable after primary checks, required for high-risk work or an explicit review request. Its advisor dial follows the accepted work's tier or, for primary-authored work, the lowest advisor dial not weaker than the primary.
_Avoid_: Reusing process consultation, worker self-review, a delegated check run, or an earlier review thread after corrections; an automatic higher-dial review after a low-confidence verdict.

**Current-state handoff**:
A transfer of the objective, binding decisions, ownership, actual changes, checks, failure evidence, and remaining work after conflicting predecessor activity stops.
_Avoid_: Replacing actual state with a copied full conversation or discarding useful partial changes.
