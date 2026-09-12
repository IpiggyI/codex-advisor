# 02: Tiered Read-Only Exploration

**What to build:** Any primary can select an appropriate read-only Explorer, obtain source-backed findings, and verify which model and effort actually ran. Light exploration uses Luna at high; standard and senior exploration usually use Luna at max, while direct Sol or Astra exploration is available when the task warrants it. Selection, native discovery, invocation, evidence, and a small route check are delivered together, without depending on worker orchestration.

**Blocked by:** None (can start immediately).

**Status:** resolved

- [x] Explorer remains a read-only evidence role available to any primary, without requiring Architect mode or a particular primary model. The plugin preserves the primary's selected model and effort.
- [x] Light exploration uses Luna at high. Standard and senior exploration usually prefer Luna at max, with Sol at medium or high and Astra at medium or high also available.
- [x] Luna is a preference, not a prerequisite. The primary may directly choose an authorized Sol or Astra Explorer based on complexity, judgment needs, or existing evidence without first attempting Luna or asking the user to approve each routine route.
- [x] The primary respects explicit model exclusions, resource limits, and scope. It selects effort explicitly; focused questions with sufficient evidence can use medium where allowed, while alternatives or conflicting evidence can justify high.
- [x] Retain the model-pinned Luna Explorer and add distinct model-pinned Sol and Astra Explorers with the same evidence contract. Adjustable Explorer templates honor the caller's effort; installation names are not separate capability tiers.
- [x] Every Explorer receives a scoped question, source boundary, and expected evidence. It returns precise source locations, examined scope, supporting observations, explanations labeled where inferred, and unresolved gaps. A negative search result does not imply absence outside the examined scope.
- [x] Explorers do not write, format, implement, or delegate. The primary retains design decisions and acceptance and may inspect the original source; exploration does not count as implementation or independent final review.
- [x] Explorer calls start with fresh context and explicit settings. Any effort increase or decrease, model change, or role reassignment uses a new native thread; an effort-changing resume cannot satisfy this requirement.
- [x] Full and selective installation checks discover the new entries while preserving existing identities. Repeated installation is idempotent; modified, conflicting, or unsafe destinations are refused before partial mutation. Unrelated agents and primary settings are preserved.
- [x] Runtime checking recognizes every allowed Explorer allocation, distinguishes Explorers from workers using the same model, and rejects unlisted default allocations such as Explorer xhigh. It validates observed role, model, effort, thread, parent association, working directory, and permissions without exposing prompts or credentials.
- [x] A missing role, unsupported setting, or absent, ambiguous, or conflicting evidence is reported explicitly. The primary may continue independent investigation but cannot silently substitute a call or certify an unobserved route.
- [x] Requested read-only access is distinguished from actual host permissions. Check source evidence, tool activity, and scoped before/after state; broader permissions with no observed writes establish behavioral read-only operation, not enforced isolation.
- [x] Explorer selection instructions, native descriptions, installation and invocation guidance, glossary, applicable architecture decisions, and public descriptions agree on the delivered routes. This slice works with the existing primary workflow even if ticket 01 has not been implemented.
- [x] Reuse one tiny source lookup to check each advertised Explorer route, including direct Sol and Astra selection without a Luna attempt. Native metadata establishes actual dispatch; existing fixtures cover allocation validation, installation refusal, malformed evidence, and bounded diagnostics. Record any unexercised route.
- [x] Keep a compact record of expected and observed routing, source citations, thread identity where relevant, permission limits, tested revision and host, and gaps. Integrate with completed sibling changes and rerun affected checks without deferring documentation or verification to another ticket.
- [x] Verification remains a simple route check, not a model-quality, cost, or stability evaluation. Reuse calls and fixtures rather than testing every primary and transport combination, and keep the active user installation unchanged.

## Acceptance

Completed on 2026-09-12. All six advertised Explorer allocations ran natively,
including Sol before any Luna call. Each returned correct per-file evidence for
the same source lookup. Installation, allocation refusal, actual metadata, and
unchanged source checks passed. See [acceptance evidence](../acceptance.md), which
distinguishes observed read-only behavior from unavailable hard isolation.
