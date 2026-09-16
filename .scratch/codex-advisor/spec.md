# Codex Advisor: Native Architect and Advisor Modes

Status: ready-for-agent

## Problem Statement

Users need to choose how much work their primary model performs without losing access to Astra's judgment. The current plugin requires a Sol primary session at high reasoning and organizes work through four selective routes. It cannot express an Astra architect that delegates all implementation, or a Sol or Luna primary session that implements work while consulting Astra at important decisions.

Users also need predictable delegated model settings without having the plugin restrict the reasoning effort of models they use directly. Selecting Astra must not automatically turn an ordinary coding session into a delegation-only workflow.

## Solution

Create a Codex-only fork named `codex-advisor`, using the project's existing native custom-agent foundation. Replace the old four-route protocol with Architect mode and Advisor mode while preserving ordinary solo work outside authorized Architect mode.

An Astra primary session enters Architect mode only when the user requests it or agrees to a proposal. Authorization defaults to the current task, including its follow-up turns and implementation subtasks. It does not carry into a new task unless the user explicitly authorized Architect mode for the whole session. Without authorization, Astra continues ordinary solo work.

Other primary models, including Sol and Luna, use Advisor mode: the primary agent performs the work and consults Astra at the agreed decision boundaries. The primary agent remains accountable for decisions and must explain disagreements with its Advisor.

Architect mode keeps design, specifications, and acceptance in the primary session and delegates every implementation change to Luna or Sol. Independent Astra review is added for high-risk work or at the user's request. Required delegated calls use verified models and reasoning settings; unavailable or unobservable required consultation and review pause the affected step instead of silently changing the workflow.

## User Stories

1. As a Codex user, I want to install the fork as `codex-advisor`, so that I can identify and invoke the intended workflow.
2. As a Codex user, I want native custom agents, so that the workflow fits the host I already use.
3. As an Astra user, I want ordinary solo work without automatic Architect mode, so that choosing a model does not change my preferred workflow.
4. As an Astra user, I want an explicit request to activate Architect mode, so that I control when implementation is delegated.
5. As an Astra user, I want the assistant to obtain my agreement before activating a proposed Architect mode, so that a suggestion alone does not authorize it.
6. As a user, I want Architect-mode authorization to cover the current task's follow-up turns and subtasks, so that I do not have to approve the same workflow repeatedly.
7. As a user, I want a new task to start without inherited task-scoped authorization, so that a previous choice does not silently govern unrelated work.
8. As a user, I want to explicitly authorize Architect mode for a whole session, so that I can choose a consistent workflow for several tasks.
9. As a user, I want Architect mode to require an Astra primary session, so that the designated architect model actually owns the work.
10. As a user, I want the plugin to preserve my primary model and reasoning effort, so that my host settings remain under my control.
11. As a Sol or Luna user, I want my primary agent to implement work in Advisor mode, so that consulting a stronger model does not transfer the whole task to it.
12. As an Advisor-mode user, I want Astra consulted before architecture decisions, data migrations, API designs, and refactors touching at least three files, so that judgment arrives before consequential implementation choices.
13. As an Advisor-mode user, I want Astra consulted after two distinct unsuccessful attempts at the same problem, so that the primary agent can obtain an independent assessment before continuing.
14. As an Advisor-mode user, I want consultation before a multi-step deliverable is declared complete, so that completion receives an additional judgment check.
15. As an Advisor-mode user, I want additional consultations when useful, so that the fixed triggers do not prevent justified requests for help.
16. As an Advisor-mode user, I want the primary agent to explain how it handled the Advisor's recommendation, so that I can inspect disagreements rather than discover that advice was silently ignored.
17. As a user, I want my authorization boundaries and project approval requirements preserved, so that an Advisor's opinion does not substitute for my permission.
18. As an Architect-mode user, I want the architect to own design, task specifications, and acceptance, so that architectural responsibility remains clear.
19. As an Architect-mode user, I want every implementation change delegated, including one-line changes and corrections, so that the responsibility boundary does not depend on patch size.
20. As an Architect-mode user, I want bounded, fully specified implementation assigned to Luna, so that the selected executor matches the task requirements.
21. As an Architect-mode user, I want judgment-heavy, context-heavy, or higher-risk implementation assigned directly to Sol, so that the workflow does not require an unsuitable Luna attempt first.
22. As an Architect-mode user, I want delegated Luna calls to use `max`, so that the intended implementation configuration is stable.
23. As an Architect-mode user, I want delegated Sol calls to default to `high` while allowing explicit adjustments, so that I can change the reasoning allocation when necessary.
24. As an Advisor-mode user, I want Astra consultations to default to `high` while allowing explicit adjustments, so that consultation settings are predictable and controllable.
25. As a user directly running Luna, Sol, or Astra, I want no plugin-imposed reasoning-effort restriction, so that delegated-call policies do not constrain the primary session.
26. As an Implementer, I want a complete specification containing the objective, ownership, interfaces, constraints, and verification requirements, so that I can work within a settled scope.
27. As a user, I want concurrent edits preserved and implementation ownership respected, so that delegated work does not overwrite unrelated changes.
28. As an Architect-mode user, I want independent tasks with nonconflicting ownership dispatched in parallel, so that useful concurrency is available within the host limit.
29. As an Architect-mode user, I want implementation scheduling to remain with the primary agent, so that Implementers do not create further implementation delegations.
30. As an Architect-mode user, I want the primary agent to inspect all actual changes and rerun key verification, so that a worker's completion claim alone is insufficient for acceptance.
31. As an Architect-mode user, I want a fresh Astra reviewer for high-risk work or when I request independent review, so that those changes receive scrutiny outside the architect's accumulated context.
32. As an Architect-mode user, I want ordinary work to finish after the architect's acceptance checks without a mandatory additional reviewer, so that independent review is added for the agreed reasons.
33. As an Architect-mode user, I want an Independent reviewer's default effort to be the higher of `high` and the primary session's effort, so that review does not default to a lower reasoning tier than the architect.
34. As an Architect-mode user, I want explicit reviewer-effort adjustments to remain at or above the primary session's effort, so that a manual override preserves the review floor.
35. As a user, I want Advisors and Independent reviewers to provide judgment without implementing their own changes, so that judgment and implementation responsibilities remain separate.
36. As a user, I want a required consultation or review to pause when Astra is unavailable or its actual model or effort cannot be confirmed, so that the workflow does not falsely report that the required step occurred.
37. As a user, I want configuration intentions distinguished from observed runtime settings, so that an installed role definition is not presented as proof of the model that actually ran.
38. As a user, I want the actual permission boundary reported for judgment agents, so that a behavioral read-only instruction is not mistaken for enforced isolation.
39. As a user, I want installation and checking to preserve modified, unsafe, and unrelated local files, so that changing the plugin does not silently damage my environment.
40. As a user, I want runtime inspection to expose only the routing evidence it needs, so that prompts, credentials, and unrelated session content do not appear in diagnostics.
41. As a user, I want the new workflow without the old `SELECTIVE ROUTE` declaration requirement, so that I do not have to reason about two overlapping routing protocols.
42. As a user, I want decision consultation distinguished from final review of actual changes, so that an ordinary consultation is not reported as satisfying a different review obligation.

## Implementation Decisions

- Keep the implementation Codex-native. Adapt the plugin manifest and marketplace registration, orchestration skill, native agent definitions, role contracts, installation and checking tools, runtime inspector, verification entry point, and user-facing instructions already present in the project.
- Use `codex-advisor` as the active fork identity and a corresponding distinct namespace for its installed roles. Remove active dependency on the old four-route protocol and its compatibility layer. Historical attribution is not an active workflow identifier.
- Separate eligibility from authorization. Astra is required for Architect mode, but Astra identity alone is insufficient. An explicit user request or accepted proposal provides authorization; a suggestion, generic request to implement, or unrelated task does not supply it.
- Preserve task-scoped authorization through follow-up turns and implementation subtasks. A new task requires new authorization unless the user explicitly selected session-wide authorization. Continue to require an Astra primary session while Architect mode is active.
- Provide activation through the user's request and consent in the normal conversation. Do not require a dedicated mode-switch command or change the host's primary model automatically.
- Preserve ordinary Astra solo work. Advisor mode applies to other primary models, including Sol and Luna. The two plugin work modes do not redefine every ordinary host operation as a plugin-controlled route.
- Do not impose a primary-session reasoning floor or rewrite the user's primary model settings. This includes Astra used directly as the architect and Luna used directly in Advisor mode.
- Define separate native contracts for the Advisor, Luna Implementer, Sol Implementer, and Independent reviewer. The Advisor and Independent reviewer have different inputs and purposes even though both use Astra for judgment.
- Apply reasoning rules by call context: Luna delegated by Astra in Architect mode always uses `max`; Sol delegated in that mode defaults to `high` and permits explicit adjustments; Astra consultation in Advisor mode defaults to `high` and permits explicit adjustments.
- For an Independent Astra reviewer in Architect mode, choose the higher of `high` and the primary session's resolved reasoning effort by default. An explicit adjustment must not fall below the primary session's effort. Use the host's supported reasoning settings and actual runtime evidence rather than comparing display labels or strings lexicographically.
- Ensure native role configuration and invocation precedence permit the allowed adjustments while preserving the required model identity and Luna constraint. An immutable default in a role definition must not silently defeat an allowed user adjustment. The exact supported native configuration mechanism must be verified during implementation.
- Keep model and effort resolution, input validation, evidence parsing, and error reporting deterministic where executable tooling owns them. Keep task interpretation, risk assessment, specification writing, and review judgment with the model. Extend existing interfaces before introducing new orchestration infrastructure.
- Retain the five-part implementation contract: objective, files and ownership, interfaces, constraints, and verification. Require a structured return containing completion status, actual changes, verification evidence, judgment calls, and unresolved gaps. Do not treat that report as independent proof of acceptance.
- Keep every implementation edit with an Implementer during Architect mode, including corrections to earlier delegated work. The architect continues to own design and task-specification artifacts as part of its assigned responsibility.
- Select Luna for bounded, fully specified implementation. Select Sol directly for work that requires substantial judgment or context, or carries higher risk. An unsuccessful Luna attempt is not a prerequisite for Sol selection.
- Permit parallel implementation only for independent tasks with nonconflicting ownership, within host concurrency limits. Keep implementation delegation one level deep and scheduling under primary-agent control.
- In Advisor mode, require consultation at the agreed design boundaries, after two distinct failed attempts at one problem, and before declaring a multi-step deliverable complete. Permit additional useful consultation. Require the primary agent to explain its treatment of the Advisor's recommendation, including any disagreement.
- In Architect mode, require the architect to inspect all actual changes and rerun key verification. Add a fresh Independent reviewer after those checks for high-risk work or an explicit user review request. Do not add mandatory independent review to every implementation task.
- Preserve the distinction between consultation and independent final review. Coverage of the old responsibility combinations does not preserve every old route-specific gate, verdict format, or declaration rule.
- Use observed role, model, effort, and permission evidence when accepting delegated results. Prefer exposed runtime metadata and use the existing narrow runtime-inspection interface for fields the public evidence omits. Missing or conflicting evidence is not permission to infer a successful call.
- Pause an affected required consultation or independent review if Astra is unavailable or its actual model or reasoning effort cannot be confirmed. Report the reason and do not silently substitute another model or skip the required step. Failure handling must not weaken Architect-mode Luna's `max` requirement.
- Request read-only behavior and supported isolation for judgment agents, and report the actual observed boundary. Preserve the existing distinction between an enforced read-only sandbox and a behavioral instruction under broader host permissions.
- Retain the installer's non-destructive checking and refusal behavior. Do not overwrite modified or unsafe destinations, change global primary-session configuration, or treat a successful installation as proof of a successful model invocation.

## Testing Decisions

- The primary acceptance boundary is the installed plugin's complete workflow in a disposable Codex workspace. Tests should observe authorization, actual delegated calls, model and effort evidence, owned changes, verification output, and completion behavior.
- Reuse the existing repository verification entry point for deterministic installer and runtime-inspection checks. Existing prior art includes disposable installation targets, idempotence checks, selective role checks, refusal without partial mutation, structured TOML validation, synthetic runtime records, invalid thread identifiers, missing records, and payload-leak checks.
- Treat exact-word and keyword assertions over Markdown as documentation consistency checks only. They cannot prove that a model respected authorization, used the intended effort, or performed an independent review. New workflow acceptance must not cite such assertions as behavioral evidence.
- Test externally visible behavior rather than internal helper names, prompt wording, or implementation structure. A meaningful negative test must fail when a required boundary is violated, such as an unauthorized architect delegation, a lower-effort Luna call, or acceptance without required review evidence.
- Prefer extending the current installation and runtime-inspection interfaces to creating additional low-level test interfaces. Use one workflow scenario matrix to organize live acceptance; use deterministic fixtures where they can establish the same boundary without a paid model call.

The workflow acceptance matrix must cover:

| Scenario | Required observation |
|---|---|
| Astra primary session, no Architect-mode request or consent | Ordinary solo work remains available; model identity alone does not activate Architect mode |
| Astra primary session, assistant proposes Architect mode but user has not agreed | The proposed mode is not treated as authorized |
| Astra primary session, explicit task-scoped authorization | Architect mode covers the current task and its follow-ups and subtasks |
| New task after task-scoped authorization | The earlier authorization does not carry over |
| Explicit session-wide authorization | Architect mode remains authorized for subsequent tasks in that session while its model prerequisite holds |
| Sol or Luna primary session at a user-selected effort | Advisor-mode work proceeds without imposing the delegated-call effort policy on the primary session |
| Architect mode requested with a non-Astra primary model | The plugin does not claim that Architect mode is active or silently change the primary model |
| Bounded implementation delegated to Luna | The observed model is Luna and its observed effort is `max` |
| Complex or higher-risk implementation delegated to Sol | Sol can be selected directly; its default effort is `high` and supported explicit adjustments take effect |
| Advisor-mode consultation with Astra | The observed model is Astra; its default effort is `high` and supported explicit adjustments take effect |
| Architecture, migration, API, or qualifying refactor decision | Consultation occurs before committing to the consequential implementation decision |
| Two distinct failed attempts at one problem | Required consultation occurs before further progress is accepted as following the workflow |
| Multi-step Advisor-mode deliverable | Required pre-completion consultation is evidenced before completion is declared |
| Primary agent disagrees with the Advisor | The decision and reasons for disagreement are visible; advice is not silently ignored |
| One-line implementation or correction in Architect mode | An Implementer performs the edit rather than the architect |
| Independent implementation tasks | Parallel dispatch respects ownership and host limits; Implementers do not delegate implementation further |
| Tasks with dependencies or conflicting ownership | Their implementation is not dispatched as independent concurrent work |
| Worker claims completion with missing or false evidence | The architect's acceptance checks expose the gap rather than accepting the claim alone |
| Architect-mode work requiring no extra reviewer | Completion follows actual-diff inspection and rerun verification without an automatically added Independent reviewer |
| High-risk Architect-mode work or an explicit review request | A fresh Independent Astra reviewer examines actual changes after the architect's checks |
| Astra architect at `low`, `medium`, or `high` | The Independent reviewer's default is `high` |
| Astra architect at `xhigh` or `max` | The Independent reviewer's default matches that effort |
| Explicit reviewer effort below the primary session | The lower setting is not accepted as satisfying the review floor |
| Required Astra call unavailable or model/effort evidence missing or conflicting | The affected step pauses with an explicit reason; no substitute or completed-step claim is silently introduced |
| Ordinary decision consultation | It is not reported as proof that independent final review of the actual changes occurred |
| New workflow invocation | The old `SELECTIVE ROUTE` declaration protocol is not required |

- Extend deterministic installation tests to the fork identity and new role contracts, including clean install, repeat install, non-mutating checks, selective checks, modified files, unsafe destinations, and preservation of unrelated configuration.
- Extend runtime fixtures to the new roles and relevant effort settings, including missing or contradictory evidence. Assert parsed values and refusal behavior, and retain checks that unrelated prompt or credential material is not emitted.
- Validate live model and effort routing in a fresh host task after role discovery. A fixture verifies the parser; it does not prove that Codex honored a role definition. Record each live scenario's actual outcome and leave unrun or inaccessible scenarios explicitly unverified.
- Include a scenario that observes effective permission behavior for a judgment agent. Do not infer enforced read-only isolation from a configuration field alone.
- During implementation, update obsolete old-route text assertions instead of retaining tests that require the retired protocol. Do not add a new general-purpose test framework merely to express these scenarios.

## Out of Scope

- Claude Code, Cursor, or other host support.
- External model-provider lanes, nested CLI runners, or user-mediated handoff lanes.
- An additional Terra implementation lane in the first version.
- Compatibility with the old four-route declaration protocol.
- A dedicated mode-switch command or automatic primary-model switching.
- Global reasoning-effort restrictions on directly used primary models.
- Automatic Architect mode based solely on choosing Astra.
- Implementation delegation by Implementers to further implementation agents.
- Mandatory independent review for every ordinary implementation task.
- Claims that higher effort guarantees a better review, or that different OpenAI models provide cross-vendor review.
- Automatic changes to the user's global host configuration, deletion of an existing installation, or deployment of this fork as part of writing this specification.
- Benchmarks, broad framework refactoring, or unrelated repository cleanup.

## Further Notes

This specification uses the project's Architect mode, Advisor mode, Advisor, Implementer, and Independent reviewer vocabulary and implements the accepted dual-mode architecture decision. It describes the target fork; the implementation baseline uses the upstream workflow.

The new rules cover the main responsibility combinations of solo work, delegated implementation, primary implementation with independent judgment, and delegated implementation with independent final review. They do not make every Advisor consultation equivalent to the upstream final-review gate.

Implementation is divided into six independently verifiable tickets: installation, Advisor mode, authorized Architect mode with Luna, independent Astra review, Sol implementation, and parallel implementation. Each ticket owns its behavior and corresponding verification. A ticket can start only after its declared blockers are complete; the readiness label does not override those dependencies.

Runtime capabilities that have not been exercised must remain identified as unverified when implementation is accepted. Static configuration checks and synthetic runtime records do not establish live model routing or enforced isolation.
