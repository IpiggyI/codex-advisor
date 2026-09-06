---
name: orchestration
description: "Use for Codex delivery with Astra advice at design decisions, persistent failures, and multi-step completion, while preserving ordinary Astra solo work."
---

# Codex Advisor orchestration

## Establish the work mode

Use the primary model identity exposed by the host. Preserve the user's primary
model and reasoning effort; this plugin imposes no primary-session effort floor.
If identity is unknown, resolve it from host evidence before selecting a mode.
Do not infer it from the installed plugin or a model's self-description.

- Non-Astra primary sessions, including Sol and Luna, use Advisor mode. The primary
  agent implements and verifies the work, consulting Astra at the boundaries below.
- An Astra primary session without an explicit user request or accepted proposal for
  Architect mode continues ordinary solo work. A suggestion alone and a generic
  request to implement do not authorize delegation-only Architect mode.
- Architect mode requires Astra and user authorization. This release does not yet
  deliver Architect-mode implementation. If requested, explain that limitation and
  pause mode-dependent work without claiming activation. A dedicated mode-switch
  command is not required; model selection remains a host operation.

## Carry out Advisor-mode work

Consult an independent Astra Advisor:

- Before committing to an architecture decision, data migration, API design, or
  refactor touching at least three files.
- After two distinct unsuccessful attempts at the same problem, before another
  attempt. State both attempted approaches and their observed failures.
- Before declaring a multi-step deliverable complete, after inspecting actual
  changes and running the relevant verification.

Additional useful consultations are allowed. Each consultation addresses its current
boundary; an earlier design discussion does not satisfy a later readiness check.

Before a consultation, read [role-contracts.md](references/role-contracts.md) for
the decision packet and [operations.md](references/operations.md) for selective
installation checks, exact native invocation, runtime validation, and permissions.
Use a fresh context and supply only the relevant evidence and constraints.
The Advisor provides judgment and does not implement changes.

The consultation defaults to `high`; explicitly pass that effort on the native
call unless the user requested another supported setting. The native role pins
`gpt-6-astra` while leaving effort open to the call. Verify the actual role, model,
effort, and permission evidence before relying on the recommendation.

If Astra is unavailable, invocation fails, or required actual model or effort
evidence is missing or conflicting, pause the affected decision or completion
step. Report the reason and the evidence gap. Do not silently substitute a model,
skip a required consultation, or claim it occurred. Independent unaffected work
may continue while the affected step remains explicitly pending.

## Own the decision and delivery

Check the Advisor's cited evidence against the scoped sources. Explain the
recommendation, your resulting decision, and the reasons for any disagreement.
Advice does not replace user authorization or project approval requirements.
Implement and verify any resulting change in the primary session.

Before reporting multi-step completion, inspect the final changes, report actual
verification and gaps, and obtain the readiness consultation required above.
Reassess readiness if subsequent changes invalidate its evidence.
An ordinary consultation, including readiness advice, is not proof of an independent
final review of the actual changes. Do not report it as that separate review.
