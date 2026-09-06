# 02: Advisor Mode and Ordinary Astra Solo Work

Status: resolved

Blocked by: 01 - Independent Installation and Safe Verification.

**What to build:** Sol and Luna primary sessions perform their own work and consult an independent Astra Advisor at the agreed boundaries. Astra primary sessions remain able to work solo without unsolicited Architect-mode activation. The new workflow replaces the old selective-route protocol.

- [x] Non-Astra primary sessions, including Sol and Luna, use Advisor mode without a plugin-imposed requirement on their primary reasoning effort.
- [x] An Astra primary session without an explicit Architect-mode request or consent remains in ordinary solo work; an assistant's unaccepted proposal does not authorize delegation-only Architect mode.
- [x] The plugin does not automatically change the primary model or require a dedicated mode-switch command.
- [x] A native Astra Advisor contract is installable, selectively checkable, and callable under the fork identity. It provides judgment and does not implement changes.
- [x] Advisor-mode consultations use `gpt-6-astra`, default to `high`, and permit explicit supported reasoning adjustments. Live invocation confirms that native configuration precedence honors an allowed adjustment.
- [x] Consultation occurs before architecture decisions, data migrations, API designs, and refactors touching at least three files.
- [x] Consultation is required after two distinct unsuccessful attempts at the same problem and before declaring a multi-step deliverable complete; additional useful consultations remain allowed.
- [x] The primary agent supplies the decision and relevant constraints, checks the Advisor's evidence, and explains its resulting decision, including any disagreement. The Advisor's recommendation does not replace user authorization or project approval requirements.
- [x] A required consultation pauses the affected step when Astra is unavailable or actual model or effort evidence is missing or conflicting. The workflow neither silently substitutes a model nor claims consultation occurred.
- [x] Judgment-agent permissions are observed and reported accurately; a behavioral read-only instruction under broader host permissions is not reported as enforced isolation.
- [x] Ordinary consultation is not reported as proof of independent final review of actual changes.
- [x] The old `SELECTIVE ROUTE` declaration, four-route dispatch contract, Sol-primary reasoning prerequisite, and old-route compatibility requirement no longer govern the fork's workflow.
- [x] The installed-plugin acceptance scenarios demonstrate primary-session effort freedom, ordinary Astra solo work, consultation triggers, an explicit Advisor-effort adjustment, disagreement handling, and unavailable or unobservable required consultation.
- [x] Runtime fixtures cover the new Advisor evidence and refusal cases without exposing unrelated session content. Obsolete exact-word old-route assertions are updated and are not presented as behavioral proof.

## Verification

Exercise Advisor mode and ordinary Astra solo work through the installed plugin in a disposable workspace. Inspect the actual consultation record, model and effort metadata, permission evidence, and primary-agent response. Use deterministic fixtures for parser and failure cases, and state separately which model-dependent scenarios were run. Delegated Architect-mode implementation is delivered by ticket 03.

## Acceptance

Completed on 2026-09-06. Installed-host runs observed Sol and Luna at low primary
effort, Astra consultations at default high and explicit medium, ordinary Astra solo
work, required consultation boundaries, explicit disagreement handling, and pausing
when native consultation was unavailable. Runtime fixtures cover missing and
conflicting evidence. Permissions were broader than enforced read-only isolation.
See [the acceptance record](../acceptance-01-02.md) for exact evidence and limits.
