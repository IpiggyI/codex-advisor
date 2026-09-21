# Codex Advisor

Shared vocabulary for primary autonomy and delegated responsibilities.

## Language

**Primary agent**:
The agent that owns the user's task, decomposition, scheduling, technical decisions within authorization, and final acceptance. It can implement, delegate, or combine both in ordinary work.
_Avoid_: Treating autonomy as authority to change user goals, acceptance conditions, or resource limits.

**Architect mode**:
An explicitly user-authorized mode, available to any primary model, in which the primary owns design and acceptance and delegates every implementation edit and correction.
_Avoid_: Activating the mode from model identity or a task artifact.

**Advisor**:
A read-only delegated judgment role with two request shapes: decision advice before a commitment, and independent acceptance after a deliverable is complete. The primary checks its evidence, owns the decision, and explains material disagreement.
_Avoid_: Treating advice as authorization, an automatic veto, or a new binding requirement; a separate reviewer role.

**Worker**:
A delegated agent responsible for an outcome within assigned ownership, retained interfaces, constraints, and verification. It owns unspecified local implementation choices and debugging.
_Avoid_: Implementer; transferring scheduling or final acceptance to the worker.

**Native entry**:
A shipped Codex custom-agent TOML named by role and tier (`ca_explorer_light`, `ca_worker_standard_m`). It pins the model, and pins the reasoning effort only when its cell has a single effort. In a tier with several models, `-m` is the default candidate, `-h` a stronger alternative, `-l` a cheaper one.
_Avoid_: Naming an entry by model; treating an entry as a tier or role of its own.

**Routing profile**:
The table from (role, tier) to native entries and dials, shipped inside the skill's references and read by the primary before its first allocation. It is the only place where effort options, defaults, and candidate order are written.
_Avoid_: Repeating effort options, defaults, or candidate order in `SKILL.md` or in a TOML description (a pinned entry's description names only its own fixed effort); a hand-edited installed copy.

**Companion installer**:
The plugin script that writes the shipped native entries onto `$CODEX_HOME/agents`, overwriting this plugin's own files, deleting retired entry names, and touching nothing else.
_Avoid_: Hand-editing installed entries; expecting the installer to preserve a hand-edited copy.

**Capability tier**:
The light, standard, or senior allocation level of one delegated call, orthogonal to role. Light and standard form the first-round pool; senior is behind the senior gate.
_Avoid_: Treating model names as tiers; treating light to standard as an escalation that needs a prior failure.

**First-round pool**:
The light and standard tiers together. The primary chooses freely between them by the task's judgment dependence, with no precondition, and takes the cheapest adequate dial by default.
_Avoid_: Reaching senior from the pool without passing the senior gate.

**Senior gate**:
The precondition for a senior tier: two capability-attributed complete failed attempts inside the first-round pool, or a user declaration. For the Advisor, only a verdict that reports low confidence or a user declaration.
_Avoid_: Opening the gate on one failed attempt, on task size, or on the primary's own judgment of difficulty.

**Escalation ladder**:
The four rules after a failed acceptance. R1: a rework ticket in the same thread at the same dial. R2: when rework also fails and the cause is capability, a raise in a fresh thread with the takeover packet, either a higher effort of the same model or another model. R3: the same model is raised at most once. R4: a major execution problem may skip the rework ticket and change model directly, counted as one failure.
_Avoid_: Raising effort three times on one model; treating a contract gap as a capability failure.

**Dial**:
A model at one reasoning effort inside a (role, tier) cell, written `model[a*, b, c]`: every listed effort is a first-round option and `*` marks the default. The listed order of models in a cell is the candidate order.
_Avoid_: Comparing dials across tiers; writing a dial as a tier.

**Explorer**:
A read-only evidence role available to any primary that investigates scoped questions and returns precise sources, observations, examined scope, and gaps.
_Avoid_: Assigning implementation or counting exploration as independent final acceptance.

**Complete attempt**:
An executor's attempt through its assigned work and ordinary checks, ending in accepted completion, failed acceptance, or concrete inability. An advisory attempt must answer its specified question with a supportable conclusion.
_Avoid_: Counting intermediate test/tool failures, or mere disagreement with advice, as complete failed attempts.

**Primary checks**:
The checks the primary owns and confirms for acceptance. It runs them itself or assigns one executor that receives the complete batch requirements and reports executor, scope, command, exit status, output location, and unverified items. Inspecting the actual complete diff and confirming that a test can fail for the intended requirement stay with the primary.
_Avoid_: Treating a delegated run as the acceptance decision; repeating a valid result because the executor or the session changed.

**Verification batch**:
A group of acceptance checks with one named executor, formed separately from ticket and dispatch boundaries so that work sharing costly setup is checked together while the scope stays understandable and a failure stays locatable.
_Avoid_: Accumulating unverified premises that dependent work rests on in order to lower the number of runs; moving a worker's own debugging into the batch.

**Independent acceptance**:
The Advisor's acceptance request shape: a fresh thread examines the actual complete deliverable after primary checks, required for high-risk work or an explicit review request. It defaults to the light tier; decision advice defaults to standard.
_Avoid_: Reusing decision consultation, worker self-review, a delegated check run, or an earlier review thread after corrections; a dedicated reviewer entry.

**Current-state handoff**:
A transfer of the objective, binding decisions, ownership, actual changes, checks, failure evidence, and remaining work after conflicting predecessor activity stops.
_Avoid_: Replacing actual state with a copied full conversation or discarding useful partial changes.
