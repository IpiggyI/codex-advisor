# 05: Direct Sol Implementation for Complex and Higher-Risk Work

Status: resolved

Blocked by: 04 - Independent Astra Review with a Primary-Effort Floor.

**What to build:** The Astra architect selects Sol directly when implementation requires substantial judgment or context, or carries higher risk. Sol's result passes the architect's acceptance checks and, when required, independent Astra review before completion.

- [x] The fork offers a native Sol Implementer under its own identity and includes it in installation, selective checks, runtime inspection, and supported invocation instructions.
- [x] Judgment-heavy, context-heavy, or higher-risk implementation can be assigned directly to `gpt-5.6-sol`; the workflow does not require a failed or corrected Luna attempt first.
- [x] Sol defaults to `high` for Astra's Architect-mode delegated calls and honors explicit supported user adjustments, with actual runtime evidence confirming the selected effort.
- [x] The Sol default is not imposed on a directly used Sol primary session, and the existing Luna delegated `max` constraint is preserved.
- [x] Sol receives the same complete implementation specification, ownership requirements, evidence contract, and prohibition on further implementation delegation as Luna.
- [x] Material ambiguity and scope conflicts are surfaced to the architect rather than used to justify unapproved architecture changes or silent expansion of ownership.
- [x] The architect inspects all actual Sol-produced changes and reruns key verification; higher-risk work then completes the independent Astra review workflow from ticket 04.
- [x] An invalid or unavailable delegated model or effort is reported explicitly and is not silently replaced or accepted as a valid Sol execution.
- [x] Luna remains the choice for bounded, fully specified work. The final active fork contracts cover the Advisor, Luna Implementer, Sol Implementer, and Independent reviewer without an additional selectable Terra implementation lane.
- [x] Installed-plugin scenarios show direct Sol selection, the default and an adjusted effort, primary-session effort freedom, ownership and verification evidence, and completion of a higher-risk task through independent review.
- [x] The verification entry point and structured role checks describe the actual active contracts and no longer require obsolete upstream role inventory or route wording.

## Verification

Use a disposable task with an existing meaningful verification check and enough implementation judgment to select Sol directly. Observe the selected role, model and effort, owned diff, architect verification, and independent Astra review for the higher-risk case. Distinguish parser-fixture success from live execution evidence.

## Acceptance

Completed on 2026-09-06. Native Sol installation and runtime checks pass. Installed
scenarios confirm direct Sol high and explicit medium execution, primary Sol low
freedom, actual owned edits, architect checks, fresh Astra review for higher-risk
work, and refusal when the Sol role is unavailable. Other recognized efforts have
fixture coverage only. See [the acceptance record](../acceptance-05-06.md).
