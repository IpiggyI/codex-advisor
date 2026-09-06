# 01: Independent Installation and Safe Verification

Status: resolved

Blocked by: None (can start immediately).

**What to build:** A user can install, discover, and check the Codex-only fork under the `codex-advisor` identity and its own native-agent namespace, without overwriting another installation or changing primary-session settings. This ticket establishes the installable delivery surface used by the later workflow tickets.

- [x] The marketplace entry, plugin registration, invocation instructions, and native role namespace consistently identify the active fork as `codex-advisor`.
- [x] A clean installation into a disposable target produces the expected native role definitions, and a fresh Codex task can discover the installed fork's supported entry points.
- [x] Repeating installation is idempotent; a successful check reports the expected installed state without modifying it.
- [x] Selective checks validate only the requested roles; an unrelated role conflict does not invalidate a valid selected-role check.
- [x] Missing roles, unknown role requests, modified destinations, unsafe destinations, and conflicting files fail with a clear reason and no partial mutation.
- [x] Existing `sol-advisor` installation files, unrelated agents, and global primary-session configuration remain unchanged.
- [x] Active installation references use the fork identity; historical attribution is preserved where it is not an active workflow identifier.
- [x] The existing verification entry point exercises installation, repeat installation, selective checking, and refusal behavior against disposable targets, using observed files and outcomes rather than documentation keywords alone.
- [x] Installation instructions describe the actual discovery and checking process. The report distinguishes successful installation and discovery from live model routing, which later workflow tickets verify.

## Verification

Use the existing installer and checking interfaces with disposable targets and before/after state comparisons. Inspect structured plugin and role metadata. Run a fresh-host discovery check when available and explicitly identify any discovery result that could not be observed. This ticket does not install the fork into the user's active environment as a side effect of development.

## Acceptance

Completed on 2026-09-06. Deterministic installation checks and fresh-host discovery
passed in disposable targets. See [the acceptance record](../acceptance-01-02.md)
for actual commands, host evidence, preservation checks, and verification limits.
