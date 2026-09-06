# 04: Independent Astra Review with a Primary-Effort Floor

Status: resolved

Blocked by: 03 - Authorized Architect Mode with Luna Implementation.

**What to build:** Architect-mode work that requires independent review is inspected by a fresh Astra reviewer after the architect's own checks. Review uses the agreed effort floor and cannot be reported complete when the required call or its evidence is unavailable.

- [x] A distinct native Independent reviewer contract uses Astra, starts with a fresh context, inspects the actual changes and verification evidence, and does not implement its own corrections.
- [x] High-risk work and explicit user review requests require independent review after the architect has inspected the complete diff and rerun key verification.
- [x] Work without either review trigger does not acquire mandatory independent review merely because Architect mode is active.
- [x] The default reviewer effort is the higher of `high` and the Astra primary session's resolved reasoning effort: `high` for primary `low`, `medium`, or `high`; `xhigh` for primary `xhigh`; and `max` for primary `max`.
- [x] Explicit reviewer-effort adjustments are honored only when supported and not below the primary session's effort. These checks do not restrict the user's directly selected primary effort.
- [x] Selection uses supported reasoning settings and observed evidence rather than lexical ordering or an assumed interpretation of a display label. An unestablished floor is not reported as satisfied.
- [x] Native configuration precedence does not silently replace the selected reviewer effort with a fixed lower setting, and actual runtime evidence confirms the effective model and effort.
- [x] If required Astra review is unavailable or actual model or effort evidence is missing or conflicting, the affected step pauses with a reason. No silent substitute or successful-review claim is introduced.
- [x] Actual reviewer permissions are reported accurately. Behavioral read-only instructions are distinguished from enforced isolation, with the existing state-comparison safeguards retained when broader permissions apply.
- [x] The fork's active independent-review contract replaces the upstream Sol reviewer role; Advisor consultation remains a separate contract and does not automatically satisfy final review.
- [x] The architect remains accountable for acceptance. A review report does not remove the architect's verification responsibility or authorize a reviewer to implement fixes.
- [x] Installed-plugin scenarios include a user-requested review of a bounded Luna-produced change, a high-risk review requirement, ordinary completion without extra review, the effort-floor cases, a rejected lower override, and required-review failure.
- [x] Deterministic fixtures validate role and effort evidence and refusal behavior. Live scenarios establish actual invocation and isolation results separately from fixture coverage.

## Verification

Build on the bounded implementation workflow from ticket 03 and explicitly request independent review to exercise the complete path. Use the same Astra model on both sides when checking the effort floor. Observe the fresh reviewer context, actual diff inspection, effective settings, and completion behavior; record unavailable live settings or permission probes as unverified.

## Acceptance

Completed on 2026-09-06. Installed-host runs confirmed fresh Astra review after
Luna implementation and architect checks, a high-risk review trigger, actual high,
xhigh, and max defaults, a supported medium adjustment, rejection of a lower
override, and pending acceptance when the required native role is unavailable.
Fixtures cover the complete specified effort matrix and missing/conflicting
evidence. Observed review was behaviorally read-only under workspace-write
permissions; enforced read-only isolation remains unverified.
See [the acceptance record](../acceptance-03-04.md) for evidence and limits.
