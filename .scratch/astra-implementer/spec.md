# Codex Advisor: Astra Implementer and Default Implementation Routing

Status: ready-for-agent

## Problem Statement

Architect mode currently assigns bounded implementation to Luna and judgment-heavy, context-heavy, or higher-risk implementation to Sol. Users who prioritize completion quality while managing Codex subscription allowance cannot select a dedicated Astra Implementer through the plugin's supported installation, invocation, and runtime-verification contracts.

Sol's place in the default routing policy no longer matches the intended trade-off. Users want Luna for clearly specified work with little implementation judgment, Astra for work requiring more judgment or carrying higher risk, and Sol when explicitly requested. They also need a predictable Astra implementation effort that does not automatically inherit the stronger reasoning allocation of the primary architect.

Adding a role alone would leave conflicting selection guidance, incomplete installation and evidence checks, and uncertainty about failure handling and independent review. The complete workflow must express the same responsibility and model-selection rules.

## Solution

Add a dedicated Astra Implementer and make Luna and Astra the default implementation choices within authorized Architect mode. Luna uses `max` for bounded tasks with complete specifications, little implementation judgment, and clear acceptance checks. Astra defaults to `medium` for tasks requiring substantial implementation judgment or cross-module understanding, or carrying higher risk. The architect can select Astra directly without first attempting Luna.

Keep the existing Sol Implementer, with its Sol model identity and default `high` effort, available only when explicitly selected by the user. Explicit supported user adjustments remain available for Astra and Sol. All implementers receive complete specifications; model selection does not transfer architecture or final acceptance to an implementer.

The architect diagnoses failed acceptance before deciding whether to clarify a specification, request a Luna correction, or reassign to Astra. No fixed failure count or automatic Sol fallback is introduced. The architect inspects all changes and reruns key verification. High-risk work and explicit review requests receive a fresh Astra Independent reviewer after those checks; choosing Astra for implementation alone does not require additional review.

## User Stories

1. As an Architect-mode user, I want a dedicated Astra Implementer, so that I can delegate demanding implementation through a supported native role.
2. As an Architect-mode user, I want bounded work with little implementation judgment assigned to Luna, so that routine implementation can conserve my Codex subscription allowance.
3. As an Architect-mode user, I want work requiring substantial judgment or cross-module understanding assigned to Astra, so that the default executor matches the work's demands.
4. As an Architect-mode user, I want higher-risk implementation assigned directly to Astra, so that risk influences model selection before implementation begins.
5. As an Architect-mode user, I want direct Astra selection without an unsuccessful Luna attempt, so that unnecessary attempts do not consume time or allowance.
6. As a user, I want Sol used only when I explicitly select it, so that the default routing policy has two clear choices.
7. As a user explicitly selecting Sol, I want the existing Sol role to continue using Sol, so that its name and runtime identity remain reliable.
8. As an Architect-mode user, I want Astra implementation to default to `medium`, so that delegated implementation has a predictable reasoning allocation.
9. As a user, I want to explicitly choose another supported Astra implementation effort, so that I can adjust the allocation when needed.
10. As an Architect-mode user, I want Luna implementation to remain at `max`, so that the established Luna configuration is preserved.
11. As a user explicitly selecting Sol, I want `high` by default and supported explicit effort adjustments, so that the retained role remains controllable.
12. As a user, I want implementation defaults to leave my primary model and effort under my control, so that delegated settings do not restrict my own session.
13. As an Astra user, I want Architect mode to continue requiring explicit authorization, so that installing an Astra Implementer does not change ordinary solo work.
14. As an Implementer, I want a complete objective, ownership boundary, interfaces, constraints, and verification requirements, so that my assigned work is actionable.
15. As an Implementer, I want material specification gaps resolved by the architect before dependent edits, so that I do not invent requirements.
16. As an Architect-mode user, I want implementation and corrections performed by implementers, so that the architect remains responsible for design and acceptance.
17. As a user, I want implementers to preserve concurrent and unrelated changes, so that delegated work respects shared ownership.
18. As an Architect-mode user, I want scheduling to remain with the architect, so that implementers do not create additional implementation delegations.
19. As an Architect-mode user, I want failed Luna acceptance diagnosed before reassignment, so that a tool failure or missing requirement is not mistaken for insufficient model capability.
20. As an Architect-mode user, I want the architect to choose clarification, Luna correction, or Astra reassignment without a fixed retry count, so that the response follows the cause of failure.
21. As an Architect-mode user, I want a replacement implementer to receive the actual current state and remaining gaps, so that reassignment preserves useful work and avoids conflicting edits.
22. As a user, I want unavailability, budget pressure, waiting time, and implementation failure to avoid automatic Sol substitution, so that my explicit model-selection boundary remains effective.
23. As a user, I want actual role, model, effort, and permission evidence checked for every delegated call, so that requested settings are not mistaken for observed behavior.
24. As a user, I want missing, invalid, or conflicting evidence to keep affected acceptance pending, so that incomplete verification does not become a success claim.
25. As an Architect-mode user, I want the architect to inspect every actual change and rerun key checks, so that a worker report alone cannot establish completion.
26. As an Architect-mode user, I want ordinary Astra implementation to finish after the architect's checks when no review trigger applies, so that selecting Astra does not automatically add another model call.
27. As an Architect-mode user, I want high-risk implementation to receive a fresh Astra Independent reviewer after the architect's checks, so that required review examines the actual deliverable.
28. As a user, I want an explicit independent-review request honored even for ordinary work, so that I can request additional scrutiny.
29. As an Architect-mode user, I want review effort determined from the primary architect's effort, so that the implementer's `medium` default does not lower the review floor.
30. As an Architect-mode user, I want corrections after required review to receive fresh review, so that acceptance applies to the revised deliverable.
31. As a user, I want the companion installer to install and check the Astra role, so that the role can be discovered in a fresh Codex task.
32. As a user, I want selective Astra checks through the existing installer interface, so that I can verify that role without unrelated role conflicts blocking the check.
33. As a user, I want repeated installation and checks to preserve identical files, so that routine maintenance is predictable.
34. As a user, I want modified or unsafe destinations refused without partial mutation, so that an upgrade cannot overwrite my local changes.
35. As a user, I want unrelated agents, existing Sol identities, and primary-session configuration preserved, so that adding Astra does not repurpose my environment.
36. As a user, I want installer success distinguished from discovery and actual runtime routing, so that each availability claim has the appropriate evidence.
37. As a user, I want runtime diagnostics to expose only the routing evidence needed for verification, so that prompts and unrelated sensitive content do not leak into reports.
38. As a user, I want installation instructions, role descriptions, routing guidance, and verification tools to agree, so that the new default behavior is discoverable and consistent.
39. As a user, I want any claimed quality or allowance improvement supported by representative accepted work, so that an `Astra-high` benchmark is not presented as proof of `Astra-medium` behavior.

## Implementation Decisions

- Add the native role `codex_advisor_astra_implementer`, fixed to `gpt-6-astra`, with the existing Implementer responsibility and reporting contract. Keep `codex_advisor_sol_implementer` fixed to `gpt-5.6-sol`; do not rename it or repurpose it as an Astra alias.
- Pin the Astra model while leaving the role template's reasoning effort unset, following the existing adjustable-role pattern. The architect explicitly passes `medium` unless the user specifies another effort supported by the current host and model. Verify the actual setting. Do not automatically inherit the primary effort or increase effort after failure. Luna remains fixed at `max`; Sol defaults to explicitly requested `high` unless adjusted by the user.
- Update orchestration guidance and role descriptions together. Default selection is Luna for bounded, fully specified work with little implementation judgment and clear acceptance checks, or Astra for substantial judgment, cross-module understanding, or higher risk. Neither file count alone nor a prior Luna failure determines the selection. Sol selection requires an explicit user request.
- Preserve Architect-mode eligibility and authorization: an Astra primary session plus explicit authorization, with the existing task and session scope rules. New role availability does not authorize Architect mode. Advisor-mode consultation rules, Explorer selection, and directly used primary-session settings remain governed by their existing contracts.
- Apply the complete five-part implementation packet and structured completion report to Astra. Keep architecture, specification clarification, scheduling, and final acceptance with the architect. Implementers own their assigned edits and corrections and do not delegate implementation further.
- When Luna fails acceptance, require the architect to distinguish implementation reasoning problems from specification gaps, environment failures, and ownership conflicts. The architect chooses the appropriate clarification, Luna correction, or Astra reassignment. Do not import the Advisor-mode two-failure consultation trigger as an implementation retry threshold.
- For reassignment, use the existing scheduling and actual-state handoff process: end the previous conflicting work, obtain its report and actual changes, inspect the current state, and supply updated ownership and remaining verification to the next implementer. Do not discard partial changes automatically or treat an earlier report as proof that the current state passes.
- Do not add automatic Sol fallback, an automatic failure counter, a budget router, or a provider retry executor. If the required role or effort is unavailable, or observed evidence is invalid, missing, or conflicting, report the reason and keep affected acceptance pending. Explicit Sol selection must still satisfy the usual specification, evidence, and review requirements.
- Preserve actual-diff inspection and rerun verification by the architect for every implementer, including corrections and combined parallel results. Missing reports, skipped checks, unresolved conflicts, or incomplete work cannot be concealed by another worker's success.
- Preserve independent-review triggers: high-risk work or an explicit user request. Ordinary Astra implementation alone is not a new trigger. Required review uses fresh context after the architect's own checks and continues through corrections until a fresh review covers the revised deliverable. Resolve the review default and floor from the primary architect's effort using the existing deterministic selector, independently of the implementer's effort.
- Extend the existing companion installer, role-to-template mapping, and integrity checks with the Astra Implementer. Full installation and full checking include the new role alongside the five existing roles. Add `astra` to the existing repeatable `--check-role` interface; this option performs a non-mutating selective check. Retain preflight refusal, idempotence, and preservation of unrelated files and primary configuration.
- Maintain the installer's existing refusal behavior when updated role text differs from an installed copy, including a Sol description updated to explain explicit selection. Document the required inspection and explicit reconciliation rather than promising automatic replacement or deleting installed roles.
- Extend the existing runtime-inspection interface with `--astra-effort EFFORT`, mapped to `codex_advisor_astra_implementer` and `gpt-6-astra`. The caller supplies the resolved expected effort, normally `medium`. Validate the actual model, native role, effort, and applicable evidence. Successful inspection returns the existing metadata JSON fields; invalid input or evidence exits nonzero with a bounded diagnostic. Preserve selector exclusivity and existing output fields. Do not accept Advisor or Independent reviewer evidence as implementation evidence merely because those roles also use Astra.
- Keep runtime inspection limited to routing metadata. The caller checks the expected parent-thread association and the user's explicit Sol selection; the inspector must not read prompt content to infer authorization. Parser acceptance of an effort string does not establish that the current host and model support it.
- Keep role mapping, argument validation, runtime parsing, and verification statuses deterministic in the existing scripts. Task interpretation, risk assessment, and failure diagnosis remain model judgments in the orchestration instructions. Extend the current mechanisms without adding dependencies or a second orchestration engine.
- Update the plugin's user-facing descriptions, installation and invocation guidance, role contracts, and operations guidance to describe the added role and the new defaults. Keep the accepted architecture decision and the implementation documentation consistent when implementation ships.

## Testing Decisions

- Use the installed plugin's complete workflow in a disposable Codex workspace as the primary acceptance boundary. Observe native discovery, actual delegated calls, model and effort evidence, scoped file changes, the architect's independent checks, required review, and completion or pending status. Reuse this existing boundary rather than adding a new application or test framework.
- Use the existing repository verification entry point and public installation and runtime-inspection interfaces for deterministic checks that do not require model calls. Prior art includes disposable installation targets, clean and repeated installation, selective checks, refusal before partial mutation, TOML parsing, synthetic runtime records, effort mismatch, missing evidence, invalid thread identifiers, and payload-leak checks.
- Test external outcomes. Documentation-wording checks can establish consistency, but cannot establish routing, authorization, implementation quality, or independent review. A meaningful negative case must fail when the intended boundary is violated, such as a Sol role being accepted as Astra, `high` being observed when `medium` was requested, or completion being claimed without required review evidence.
- Extend installer behavior tests for full installation, selective Astra and full checks, exact model identity, unset adjustable Astra effort, preservation of the existing Luna constraint and Sol identity, idempotence, modified or unsafe destinations, and unrelated configuration. A missing Astra role must fail selective checking without writing files, while an unrelated role conflict must not prevent a valid selective Astra check. Include an existing Sol installation whose changed description causes the documented refusal instead of silent overwrite.
- Extend runtime fixtures for the Astra Implementer at requested `medium` and an explicit supported adjustment. Include wrong model, wrong role, requested-versus-observed effort mismatch, missing or conflicting evidence, and Astra Advisor or Independent reviewer records presented as implementation evidence. Missing effort arguments and conflicting role selectors must fail. Retain existing privacy and invalid-input coverage.
- Exercise the live workflow scenarios below in a fresh host task after disposable installation. Actual calls must establish host behavior; fixtures establish only parser behavior. Record role, model, effort, permissions, owned changes, verification, and the architect's response. Unrun or inaccessible scenarios remain explicitly unverified.

| Scenario | Required observation |
|---|---|
| Fresh disposable install and host task | The Astra Implementer is discoverable alongside the existing roles; discovery is recorded separately from installer success |
| Bounded, fully specified work with little implementation judgment | Luna performs the scoped edit at observed `max`; the architect inspects the actual change and reruns key verification |
| Work requiring substantial implementation judgment, with no independent-review trigger | Astra is selected directly, performs the scoped edit at observed `medium`, and may complete after the architect's checks without an automatically added reviewer |
| Astra primary uses a higher effort than `medium` | The Astra Implementer still observes `medium` by default; primary settings remain unchanged |
| User explicitly requests a supported Astra implementation effort | The requested effort is observed and verified rather than defeated by the role template |
| User explicitly selects Sol | The native Sol role and model are observed, with default `high` or the user's supported adjustment; ordinary acceptance obligations still apply |
| Astra role unavailable and no explicit Sol selection | The affected work remains pending with a reason; no automatic Sol substitute or completion claim appears |
| Astra invocation fails after role discovery and no explicit Sol selection | The affected work remains pending with an explicit failure report and no automatic Sol substitute; a missing-role test does not count as evidence for this distinct failure path |
| Astra model or effort evidence is missing or conflicting | The architect rejects the evidence as insufficient and leaves affected acceptance pending |
| Luna reports a material specification gap before dependent edits | The architect resolves the specification before dependent work; changing model does not substitute for that clarification |
| Luna's failed check is caused by an environment fault | The architect addresses or reports the environment fault; the failure alone does not trigger a capability-based reassignment |
| Luna's implementation fails acceptance because the work needs more implementation judgment | The architect may reassign to Astra with current-state evidence and updated ownership, without waiting for a fixed count; a documented cause-based choice to correct with Luna is also valid |
| Worker reports completion while an intended acceptance condition still fails | The architect's independent check exposes the failure; the report alone cannot complete the work |
| High-risk work implemented by Astra at `medium` | A fresh Astra Independent reviewer examines the actual changes after the architect's checks; review effort follows the primary-based default and floor |
| User explicitly requests independent review of ordinary work | A fresh Independent reviewer is used after the architect's checks regardless of the implementation model |
| Required review requests corrections | An Implementer makes the corrections, the architect rechecks them, and fresh review covers the revised deliverable before completion |
| Required review fails or cannot be evidenced | The affected completion remains pending; prior consultation or a different implementation model does not satisfy the review requirement |

- Retain focused coverage of existing authorization, primary-effort freedom, role ownership, and scheduling safeguards through the current suite. Do not rerun unrelated model workflows merely to increase the number of passing checks.
- Separate functional acceptance from outcome claims. This feature does not require reproducing the supplied benchmark or proving that `medium` is optimal. Any later claim of better completion quality or lower subscription consumption must compare representative delegated work using actual acceptance results, correction work, and observable allowance consumption. If allowance attribution is unavailable, report that limitation rather than substituting API-dollar estimates.

## Out of Scope

- Implementing or installing the plugin as part of publishing this specification.
- Removing or renaming the Sol Implementer, or changing its model identity to Astra.
- A model-neutral implementer whose backend silently switches between Astra and Sol.
- Automatic Sol fallback for outages, failures, budget pressure, or latency.
- Fixed retry counts, automatic reasoning-effort escalation, quota-based routing, a new retry executor, or an automatic model-selection benchmark system.
- Lowering Luna implementation below `max`, automatically inheriting the primary's effort for Astra implementation, or changing the existing review-effort floor.
- Changing Architect-mode authorization, Advisor-mode consultation, Explorer routing, or primary-session model configuration.
- Making every Astra implementation require independent review, or treating Advisor consultation as independent final review.
- Allowing Implementers to own architecture, final acceptance, or further implementation delegation.
- Adding other hosts, provider routes, models, dependencies, or unrelated refactors.
- Automatically overwriting modified installed roles, deleting installations, changing global configuration, or committing, pushing, or deploying this work.
- A benchmark suite, a subscription-usage dashboard, or a guarantee of improved quality or lower allowance consumption.

## Further Notes

This feature implements [ADR-0002](../../docs/adr/0002-luna-astra-implementation-routing.md), which supersedes the implementation-routing and implementation-effort portions of [ADR-0001](../../docs/adr/0001-codex-native-dual-mode-orchestration.md). The project's existing Architect mode, Advisor mode, Implementer, and Independent reviewer definitions apply.

The user-supplied DeepSWE observations and their verification limits are recorded in ADR-0002. Astra was evaluated at `high`; the chosen implementation default is `medium`. A supported setting is not evidence that its quality or allowance use has already been validated in this workflow.

This specification defines the implementation target; it does not establish installed availability, live routing, or completed acceptance. Implementation work must preserve the distinction between deterministic checks, observed host behavior, and unverified outcome assumptions.
