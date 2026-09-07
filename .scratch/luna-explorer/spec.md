# Luna Explorer

Status: ready-for-agent

## Problem Statement

Delegated exploration can inherit the primary session's model when no model is selected. Users who choose an expensive primary model need a separate exploration role with predictable model routing, without forcing every investigation to use maximum reasoning effort. The role must also be available to every non-Astra primary model, not just one named alternative.

## Solution

Provide the native Explorer role `codex_advisor_luna_explorer`, fixed to `gpt-5.6-luna`, with reasoning effort explicitly selected by the primary agent for each call. Once installed and discovered, any primary agent may select it without loading the orchestration skill or entering Architect mode. When the existing orchestration skill is applied and the primary decides to delegate exploration, it uses the Luna Explorer by default.

The Explorer performs read-only fact finding and returns source locations, evidence-based explanations, and unresolved questions. The primary agent retains design decisions and may investigate directly when the role is unavailable or its findings are insufficient. Switching to a more expensive delegated model requires explicit user authorization.

## User Stories

1. As a Codex user, I want an exploration role fixed to Luna, so that delegated exploration does not inherit an expensive primary model.
2. As a user of any primary model, I want access to the Explorer, so that exploration is independent of my primary model choice.
3. As a non-Astra user, I want the same Explorer access, so that I do not need an Astra session.
4. As a user, I want no primary-model whitelist, so that support is not limited to Sol or other enumerated examples.
5. As a user outside Architect mode, I want to delegate exploration, so that fact finding does not require implementation delegation.
6. As a user who has not loaded the orchestration skill, I want the installed role to remain callable, so that skill activation does not control role availability.
7. As a primary agent, I want a clear role description, so that I can select the Explorer from the host's available roles.
8. As a user outside the skill, I want the primary agent to decide whether to select the Explorer, so that installation does not add a global routing requirement.
9. As a user applying the orchestration skill, I want delegated exploration to default to Luna, so that the workflow uses the intended exploration model.
10. As a user, I want the existing skill trigger scope preserved, so that pure exploration does not introduce a new activation rule.
11. As a user, I want existing delegation authorization respected, so that an available role does not itself authorize a new delegation.
12. As a primary agent, I want to select supported reasoning effort for each call, so that effort matches the investigation.
13. As a user, I want exploration to permit efforts below max, so that simple questions need not use maximum effort.
14. As a user, I want my primary model and effort preserved, so that child settings do not change my session.
15. As a user, I want the Luna Implementer to retain its max requirement, so that exploration does not alter implementation policy.
16. As an Explorer, I want a scoped question and source boundary, so that I can gather relevant evidence.
17. As a user, I want exploration to remain read-only, so that investigation does not change my files.
18. As a primary agent, I want precise source locations and supporting facts, so that I can check the findings.
19. As a primary agent, I want uncertainty and unresolved gaps reported, so that inference is not presented as fact.
20. As a user, I want design decisions to remain with the primary agent, so that investigation does not silently assume decision authority.
21. As a user, I want exploration distinguished from implementation and independent review, so that one role is not claimed to satisfy another.
22. As a user, I want missing or failed Explorer calls reported, so that unsuccessful investigation is not claimed as complete.
23. As a primary agent, I want to investigate directly when Luna is unavailable or findings are insufficient, so that independent work can continue.
24. As a user, I want explicit authorization before a more expensive delegated model is substituted, so that model escalation remains my choice.
25. As a user, I want the companion installer to install and selectively check the Explorer, so that role discovery follows the existing installation process.
26. As a user, I want repeat installation and checks to preserve modified and unrelated files, so that adding the role does not damage my environment.
27. As a primary agent, I want the actual role, model, requested effort, and permissions checked, so that configuration intent is distinguished from observed execution.
28. As a user, I want runtime diagnostics to omit prompts and credentials, so that validation reveals only necessary routing evidence.
29. As a user, I want observed read-only behavior distinguished from enforced isolation, so that permission guarantees match the host evidence.
30. As a maintainer, I want the existing verification entry points extended, so that the feature does not create a parallel test framework.

## Implementation Decisions

- Add one native role named `codex_advisor_luna_explorer`, with model `gpt-5.6-luna` and a read-only sandbox request. Omit the role-level reasoning setting so the caller can choose effort. The description must express applicability to any primary model and availability without skill activation.
- Extend the companion installer's existing role selection with `explorer`, including default installation, whole-install checks, and selective checks. Preserve preflight, refusal, and repeat-install behavior.
- Extend the narrow runtime inspector with `--explorer-effort`. Reuse its exact-thread lookup, expected-role/model/effort checks, permission evidence validation, and restricted output. Recognized effort strings are not a claim of host or model support.
- Put the exploration default in the existing orchestration skill without changing its trigger description or requiring Architect mode. Role availability outside the skill comes from native host discovery; no global routing rule is installed.
- Document a fresh-context native call with explicit effort, a scoped investigation packet, and independent runtime validation. Fresh context allows call-specific settings and keeps the investigation bounded.
- Keep the Explorer's responsibility limited to facts and evidence-based explanations. It neither changes files nor delegates work further. The primary agent owns decisions and validation of findings.
- When role/model/effort or required evidence is unavailable, do not certify that call. Report the gap; the primary may gather evidence directly. A more expensive delegated substitute requires explicit user authorization.
- Preserve the Luna Implementer's fixed max requirement and every existing Advisor, Implementer, and Independent reviewer contract.
- Update installation and usage documentation to distinguish role availability, skill-driven selection, and observed runtime behavior. Keep primary-session configuration unchanged.

## Testing Decisions

- Test through the existing installer and runtime-inspector command interfaces. A useful test fails when installation omits the role, selective checks inspect the wrong role, requested effort is ignored, or a wrong/missing runtime setting is accepted. Do not use prompt-string assertions as proof of agent behavior.
- Extend existing disposable installer cases for clean and repeat installation, selective checks, missing or modified roles, unsafe destinations, refusal before partial writes, and preservation of unrelated files and primary configuration.
- Extend the existing runtime fixtures for the Explorer's expected model and requested effort, invalid arguments, wrong roles/models/efforts, missing or conflicting permission evidence, and restricted output. Retain existing Luna Implementer max tests.
- Use isolated installed Codex homes and disposable source workspaces for the main live acceptance boundary. Exercise native role discovery and calls from Astra and non-Astra primaries, including Sol and another available non-Astra model. Check role definitions for absence of a primary-model whitelist; finite live cases do not prove every model or prompt.
- Outside the skill, demonstrate that a primary can select and call the discovered role. Do not require every exploration prompt to select it. Within the existing skill scope, demonstrate default Luna selection after the primary decides to delegate exploration.
- Observe at least two supported non-max effort values on the same Luna role. Check actual child role, model, effort, parent linkage, and unchanged primary settings rather than agent self-description.
- Use source questions with known answers to check precise references and evidence quality. Inspect tool activity and before/after scoped file state for mutations. Report actual permission metadata separately; no-write behavior alone does not establish enforced isolation.
- Exercise unavailable-role handling in an isolated installation, including direct primary investigation and no unauthorized expensive substitute. A missing-role test does not establish provider-outage coverage.
- Reuse prior installed-host acceptance and adjustable-effort tests. Run the complete deterministic suite after focused checks, and record unrun or inaccessible live scenarios explicitly.

## Out of Scope

- A global default exploration route, replacing Codex's built-in Explorer, or changing Codex itself.
- A new exploration skill or broader orchestration trigger scope.
- Primary-model restrictions, automatic Architect mode, or automatic primary-model changes.
- A fixed Explorer effort, a max minimum, or relaxing the Luna Implementer's max requirement.
- Explorer implementation, architectural decision ownership, formal review, or recursive delegation.
- Automatic escalation to more expensive delegated models.
- New providers, dependencies, routing services, or test frameworks.
- Automatic reconciliation of conflicting installed roles or deployment to the user's active Codex home.
- Quantified quota or latency savings and guarantees that every host enforces the requested sandbox.

## Further Notes

This specification uses the project's Explorer, Architect mode, Advisor mode, Implementer, and Independent reviewer vocabulary and the accepted exploration decision. Availability to every primary model is a role contract, not a promise that every primary will select the role on every prompt. The host must discover the installed role, and its current model support, permission policy, concurrency limits, and authorization rules remain applicable.
