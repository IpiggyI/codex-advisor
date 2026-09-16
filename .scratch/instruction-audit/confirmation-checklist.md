# Instruction Audit: Confirmation Checklist

Status: needs-triage

Recorded: 2026-09-13.
Reviewed repository revision: `7eca26d41f51c8d63ec4f62c2783fa9cc60c3146`.

This record preserves the twelve findings from the instruction audit for individual user review. No recommendation below is approved for implementation. Recording this checklist does not authorize changes to runtime rules, role defaults, installed copies, permissions, commits, or deployments. This is an audit record, not a combined implementation ticket.

## How to record decisions

Leave an item unchecked until the user has reviewed it. Then check it and replace its decision field with `keep`, `simplify`, `remove`, `update`, `defer`, or `reject`, followed by the agreed scope. A checked item means its decision is recorded; it does not mean implementation or verification is complete.

The suggestions to reduce verification in R07, change logging coverage in R10, and introduce a unique Sol worker default in R08 need explicit behavioral decisions. The remaining recommendations also remain pending until the user confirms their scope.

## Evidence and scope

- The audit began with the [OpenAI article on rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra), read on 2026-09-13. It supports accurate triggers, progressive disclosure, and proportionate verification; it does not itself authorize removing project safeguards or changing model preferences.
- Current project policy is [ADR-0003](../../docs/adr/0003-autonomous-primary-and-tiered-role-pool.md). Earlier ADRs and acceptance records provide historical context only where superseded or not rerun.
- Scope covered the plugin skill, descriptions, references, eight role configurations, presentation metadata, repository instructions, README, domain guidance, relevant architecture records, and three Chinese mirrors. Deployment scope is the repository's existing README, AGENTS.md, and operations reference; there is no additional deployment guide identified for this audit.
- External inspection covered the loaded [global instructions](/home/hyy/.codex/AGENTS.md), relevant WSL and Windows configuration, and corresponding role, marketplace, and plugin-cache copies. No other plugin's posture, routing, or acceptance strategy is adopted.
- Observations below were made during the 2026-09-13 audit. Recheck host-dependent claims after host, configuration, installation, marketplace, or template changes. Recheck file locations against the reviewed revision after edits.
- Expected savings are reasoned estimates of avoided work. No latency, token, cost, or quality improvement was measured.

## Pending findings

### R01: Deployment line endings and exact-template checks

- [ ] Review R01 and record the decision.

**Decision:** Pending.

**Classification:** Further verification required.

**Location and original instruction:** [Operations, lines 27–33](../../plugins/codex-advisor/skills/orchestration/references/operations.md): “Exact files remain unchanged”; modified or conflicting destinations are refused. [The installer, line 82](../../plugins/codex-advisor/scripts/install-agents.sh) compares templates with `cmp -s`.

**Verified observation:** Windows marketplace and plugin-cache text files use CRLF, while the eight installed role files use LF. Their contents match after line-ending normalization, but their original bytes differ. WSL repository, marketplace, cache, and installed role comparisons passed.

**Proposal:** Document the managed-file line-ending convention, installer source, and target directory. Consider repository attributes that preserve LF in distributed files after checking the actual Windows path. Keep strict drift detection rather than immediately weakening comparison.

**Impact:** May avoid manual reconciliation caused solely by line endings. Exact-template refusal remains intact.

**Unverified and next check:** Windows-native execution of cached scripts was not run. Do not label installation as broken from the byte comparison alone. A later authorized check should exercise the documented Windows shell and selective installer check, without overwriting customized roles.

### R02: Chinese mirror changes the failure-reassessment rule

- [ ] Review R02 and record the decision.

**Decision:** Pending.

**Classification:** Correct and simplify.

**Location and original instruction:** [English skill, lines 103–105](../../plugins/codex-advisor/skills/orchestration/SKILL.md): “rather than an unconditional counter-driven call.” [Chinese mirror, line 57](../../docs/zh/skills/orchestration/SKILL.md), verbatim: “而不是无条件地按反对意见再调一次”.

**Verified observation:** The English instruction concerns automatic consultation driven by a failure count. The Chinese sentence instead refers to opposing opinions. The mirror-existence check cannot detect this semantic difference.

**Proposal:** Restore the failure-count meaning. Correct unclear translations such as the rendering of judgment calls, using natural Chinese for explanatory prose and preserving exact commands, parameters, and role identifiers.

**Impact:** Removes a conflicting interpretation without changing the English policy. Preserve mirror synchronization and inspect the meaning of changed clauses.

**Verification:** Run the existing mirror-existence check and compare edited clauses against their English sources. Model execution is not needed to validate this translation change.

### R03: Separate requested settings, host records, and server execution

- [ ] Review R03 and record the decision.

**Decision:** Pending.

**Classification:** Clarify and update against official documentation.

**Location and original instruction:** [Operations, lines 77–99](../../plugins/codex-advisor/skills/orchestration/references/operations.md): “Public spawn/details metadata is authoritative” and requirements to validate actual routing.

**Verified observation:** [The inspector, lines 168–185](../../plugins/codex-advisor/scripts/inspect-agent-runtime.sh), extracts `session_meta` and `turn_context` fields. These are host records, not independent evidence of server-side execution. The [official subagent documentation](https://developers.openai.com/codex/subagents), read on 2026-09-13, describes explicit settings, custom-agent overrides, and parent permission overrides.

**Proposal:** Name four distinct layers: invocation request, configuration after role overrides, host-observed metadata, and server-side execution. Scope each conclusion to the fields and entrance actually observed. Retain contradiction handling and avoid inventing a metadata tool when the current host does not expose it.

**Impact:** Prevents overclaiming and unnecessary searches for evidence outside an entrance's contract. Do not replace routing checks with role self-reports or silently substitute settings.

**Unverified:** Server-side model or effort selection was not investigated. Do not require new server-side investigation for every routine call merely to clarify documentation.

### R04: Make the root skill a smaller phase router

- [ ] Review R04 and record the decision.

**Decision:** Pending.

**Classification:** Simplify.

**Location and original instruction:** [Root skill, lines 27–29](../../plugins/codex-advisor/skills/orchestration/SKILL.md), requires the role packet and installation, invocation, evidence, and permission procedures before delegation. The root also repeats recovery and acceptance procedures.

**Verified observation:** The root contains 142 lines; the role-contract and operations references contain 146 and 235 lines respectively at the reviewed revision. Several responsibilities appear in multiple locations. Line count is context here, not a deletion threshold.

**Proposal:** Retain authorization, allocation, required-advice triggers, and completion boundaries in the root. Route to invocation material for calls, recovery material after failures, and maintainer verification only when changing the plugin. Explicitly allow reuse of already-loaded guidance while its premises remain valid.

**Impact:** Reduces irrelevant reading without removing the underlying procedures. Preserve accurate skill triggers; the description is already relatively short.

**Verification:** Check that each workflow still has a reachable authoritative entry and that relocated runtime Markdown retains its Chinese twin. No empirical performance claim follows from fewer lines.

### R05: Keep caller scheduling duties out of delegate instructions

- [ ] Review R05 and record the decision.

**Decision:** Pending.

**Classification:** Simplify.

**Location and original instruction:** [Advisor configuration, lines 10–11](../../plugins/codex-advisor/agents/codex-advisor-astra-advisor.toml), repeats mandatory consultation triggers. [Sol worker configuration, lines 24–29](../../plugins/codex-advisor/agents/codex-advisor-sol-implementer.toml), repeats thread replacement, predecessor handling, and primary metadata checks.

**Verified observation:** These caller duties also appear in the root skill and operations reference. Delegates cannot independently perform all of them.

**Proposal:** Keep delegate objectives, ownership, local decision authority, boundaries, meaningful verification, and actual-result reporting in role instructions. Keep dispatch, consultation triggers, lifecycle transitions, and metadata collection with the primary. Preserve information the caller needs to select a standalone role in its discoverable description.

**Impact:** Reduces redundant context and responsibility confusion. Roles may be called without the skill, so their essential read-only or ownership boundaries must remain self-contained. A new configuration-generation system is not proposed.

**Verification:** Inspect both skill-assisted and standalone role contracts for retained selection information and boundaries; do not apply worker change contracts to read-only evidence roles.

### R06: Concentrate installation and update instructions in README

- [ ] Review R06 and record the decision.

**Decision:** Pending.

**Classification:** Simplify and update against official documentation.

**Location and original instruction:** [README, lines 78–117](../../README.md), repeats failure, lifecycle, advice, and acceptance procedures. Its update instruction says to “repeat plugin installation and the companion installer.”

**Verified observation:** On WSL, `codex plugin list --json` reports a marketplace snapshot in `.source.path`, while this session loads the skill from the plugin cache. Their bytes currently match. Both WSL and Windows marketplace configurations point at GitHub. CLI `0.154.0` still exposes the documented plugin commands.

**Proposal:** Keep purpose, prerequisites, installation, examples, a concise role table, and update entry points in README. Link to internal procedures. Distinguish Git-backed marketplace updates from local-checkout development and identify the editable source, marketplace snapshot, loaded cache, and installed role target.

**Impact:** Makes installation conditions and update operations easier to find. Preserve the companion installer, source/target paths, conflict handling, and fresh-task discovery step.

**Verification:** Check commands against the target host and the selected marketplace type. Keep maintainer dependencies separate from end-user installation requirements.

### R07: Remove duplicate checks without dropping final verification

- [ ] Review R07 and record the decision.

**Decision:** Pending; explicit approval required for the reduced verification schedule.

**Classification:** Simplify; safeguard-related change.

**Location and original instruction:** [Operations, lines 212–233](../../plugins/codex-advisor/skills/orchestration/references/operations.md), says to use focused checks and then the full suite, showing `--installation`, `--runtime`, and the unqualified verifier in sequence, followed by the full native scenario list.

**Verified observation:** The unqualified [verifier](../../plugins/codex-advisor/scripts/verify.sh) contains both groups. Executing all three listed commands repeats each group.

**Proposal:** Select checks by changed behavior. Documentation and mirrors need applicable structure, links, and semantic checks. Configuration changes need parsing and affected contracts. Routing and lifecycle changes need relevant native scenarios. Run the full suite once when required. After corrections, rerun affected checks.

**Retained acceptance responsibility:** Workers verify their own changes. The primary inspects the complete actual deliverable, including new files and worker-authored tests, and runs key verification on the final combined state. High-risk or explicitly requested independent acceptance still requires a fresh second reader after primary checks.

**Impact and lost coverage:** Removes repeated execution on unchanged state and native scenarios unrelated to the change. It must not remove the distinct final integration check or substitute a worker report for primary acceptance.

**Unverified:** Real-task savings and the adequacy of any concrete reduced check set remain to be established for the affected change.

### R08: Distinguish defaults, allowed efforts, and escalation eligibility

- [ ] Review R08 and record the decision.

**Decision:** Pending; introducing a unique Sol worker default is a behavioral choice.

**Classification:** Clarify; any new default is a behavior change.

**Location and original instruction:** [Root role table, lines 33–47](../../plugins/codex-advisor/skills/orchestration/SKILL.md), mixes “Usually,” allowed ranges, and failure eligibility. It also says “No Explorer `xhigh` route exists.”

**Proposal:** Describe that exclusion as a restriction of this plugin's default pool, not a universal host limitation. Mark defaults with `*`, keep initial choices separate from conditional later eligibility, and retain explicit user choices.

| Role | Existing initial policy to preserve | Additional condition or pending choice |
|---|---|---|
| Luna light Explorer | `[high*]` | Preserve the current light allocation. |
| Luna standard/senior Explorer | `[max*]` | A usual preference, not a mandatory predecessor to Sol or Astra. |
| Sol or Astra direct Explorer | `[medium* / high]` | Here `medium*` is only the existing preference for focused questions with sufficient evidence, not an unconditional default. |
| Luna worker | `[max*]` | Fixed by the role configuration. |
| Sol worker | `[high / xhigh]` | Both are initially allowed. Choosing `[high* / xhigh]` as a unique default needs confirmation. |
| Astra worker | `[medium* / high]` | The same conditional medium preference applies. Relevant complete worker failure makes `xhigh` eligible. |
| Astra Advisor or Independent reviewer | `[medium* / high]` | The same conditional medium preference applies. Relevant complete advisory failure makes `xhigh` eligible. |

**Verified observation:** Only the Luna worker pins `model_reasoning_effort`; other role templates omit it. Role-file values can override explicit invocation settings under the official custom-agent contract.

**Impact:** Reduces routine allocation questions and mistaken inheritance. Do not transfer worker failure eligibility to Explorers or Advisors, derive reviewer effort from the primary, or claim a configured choice executed without corresponding evidence. Astra remains ineligible for first-attempt `xhigh` under the current policy. No additional model or route is proposed.

### R09: Replace metric-triggered refactoring actions with scoped judgment

- [ ] Review R09 and record the decision.

**Decision:** Pending.

**Classification:** Simplify; remove mechanical action triggers.

**Location and original instruction:** [Global instructions, lines 57–64](/home/hyy/.codex/AGENTS.md), associate function length, duplication count, and parameter count with splitting, extraction, or object wrapping.

**Verified observation:** The section already labels these as rules of thumb. It is not a universal mandatory-refactor rule, but its action table can pull work beyond the requested change.

**Proposal:** Keep metrics as investigation clues. Require an actual comprehension, correctness, or maintenance problem within the task before proposing or performing a refactor.

**Impact:** May reduce unrelated proposals and abstractions. No specific runtime safeguard is removed. This concerns the global instruction source, not a new rule to copy into the plugin.

**Verification:** Check consistency with surgical changes, local ownership, and the ban on speculative abstractions.

### R10: Narrow default logging coverage while retaining explicit failure

- [ ] Review R10 and record the decision.

**Decision:** Pending; explicit approval required for the logging-coverage change.

**Classification:** Simplify; error-handling and logging change.

**Location and original instruction:** [Global instructions, line 70](/home/hyy/.codex/AGENTS.md), require logging catch blocks and external calls when no project convention exists.

**Proposal:** Preserve recovery, rethrowing, or explicit failure returns; prohibit fabricated success and hidden failure. Record sufficient diagnostic context at the boundary responsible for handling the failure. Log successful external calls when auditing, diagnosis, or project policy requires it rather than universally. Avoid duplicate logs as the same exception passes through layers.

**Impact and lost coverage:** Reduces duplicate logging and unnecessary instrumentation, but removes universal default coverage for successful external calls and every catch point. This is not merely wording deduplication.

**Replacement safeguard:** Retain the operation, failure cause, and necessary correlation context without secrets; follow stronger project auditing requirements.

**Unverified:** No business code was reviewed, so dependencies on success-call logs or particular catch-point logs are unknown. Confirm those requirements when applying the rule to a concrete system.

### R11: Consolidate disclosures and clarify when uncertainty blocks work

- [ ] Review R11 and record the decision.

**Decision:** Pending.

**Classification:** Simplify.

**Location and original instruction:** [Global instructions](/home/hyy/.codex/AGENTS.md), lines 3, 33, and 81 require scope disclosure, checkpoints, and a stepwise verification plan. Line 29 says: “If you don't understand why existing code is shaped a certain way, ask first.”

**Proposal:** Give one proportionate scope and verification disclosure, then update at material findings, scope changes, or handoff. Investigate unknown implementation reasons using reachable evidence before asking. Pause dependent work for unresolved matters that would change the outcome. Record sources and invalidation conditions for load-bearing assumptions without creating records for ordinary local choices.

**Impact:** Reduces repeated planning and questions answerable by available tools. User-owned choices, authorizations, explicit gates, irreversible actions, and primary-session reserved operations remain unchanged.

**Verification:** Check that the consolidated wording preserves those stop conditions and continues unaffected work where appropriate.

### R12: Remove inapplicable domain-document templates

- [ ] Review R12 and record the decision.

**Decision:** Pending.

**Classification:** Simplify; some referenced skill entrances need verification.

**Location and original instruction:** [Domain guidance, lines 5–39](../../docs/agents/domain.md), requires preliminary domain reading, describes multi-context layouts, and names entrances such as `/grill-with-docs`. Repository instructions select a single-context layout.

**Proposal:** Retain `CONTEXT.md`, relevant ADRs, and explicit conflict disclosure. Remove unused multi-context examples and make reading conditional on the terminology or architecture question. Refer to maintained skill names. The [triage table](../../docs/agents/triage-labels.md) can drop duplicate identity-mapping columns while retaining every state meaning.

**Impact:** Reduces template reading and obsolete-name searches. This is lower priority than factual and responsibility issues.

**Evidence boundary:** Some named skill entrances were not exposed in the audited session. That does not establish absence from every host or installation; verify the intended integration before replacing them.

## Safeguards and policies recommended for retention

These are recommendations to preserve existing policy, not new requirements or already approved audit decisions.

- Any primary may implement or delegate. Architect mode requires explicit authorization and delegates every implementation edit within that scope.
- Intermediate test or tool failures are distinct from complete worker failures. Recovery follows diagnosis rather than a mandatory escalation counter.
- The primary inspects actual complete changes and performs meaningful key verification. Worker reports or self-review do not substitute for a second reader where independent acceptance is required.
- High-risk delivery and explicit independent-review requests retain fresh independent acceptance. File count, step count, primary identity, or primary effort alone do not trigger it.
- Effort changes and independent acceptance follow the accepted fresh-thread policy. The current documents already identify this as a user policy, not a general law about host caches or guaranteed savings.
- Exact-template checks, refusal to overwrite modified or unsafe destinations, preservation of unrelated configuration, and honest permission/isolation evidence remain.
- The [official plugin packaging documentation](https://developers.openai.com/plugins/build/plugins), read on 2026-09-13, still supports `.codex-plugin/plugin.json` as a compatibility layout. A portable-manifest migration is not necessary solely because a newer format exists.
- The [upstream README at revision 37b75cad535abdd46531f0227483a8842d045ab8](https://github.com/DannyMac180/sol-advisor/blob/37b75cad535abdd46531f0227483a8842d045ab8/README.md) uses a fixed Sol primary and a different route policy. No direct policy import was recommended.

## Separate safeguard-change register

| Finding | Proposed change | Retained or replacement safeguard | Remaining uncertainty |
|---|---|---|---|
| R07 | Reduce duplicate suites and unrelated native scenarios. | Worker verification, primary complete-result inspection and final key checks, and required fresh independent review. | Concrete check-set adequacy and measured savings. |
| R10 | Remove universal logging at every catch point and every successful external call. | Explicit failure handling, responsible-boundary diagnostics, and applicable audit requirements. | System-specific diagnostic and audit dependencies. |

No recommendation authorizes broader permissions, removal of mandatory independent review, weaker drift refusal, weaker concurrent-write isolation, deletion of recovery backups, or broader release staging. R01 proposes consistent deployment files while retaining strict comparison.

## Completed checks and remaining verification

The audit completed read-only role-template comparisons, JSON/TOML parsing, local-link checks for current documents, three Chinese-mirror existence checks, and `git diff --check`. These establish structure and file consistency only, except for the explicit semantic observations recorded above.

The audit did not run the full fixture suite, native model route/lifecycle scenarios, Windows installation, server-side configuration investigation, or business-code review. Historical native acceptance remains a reported prior result, not a newly executed test. Translation accuracy beyond the inspected clauses and task-level efficiency gains are not established by the structural checks.

At audit completion, the existing untracked `.scratch/codex-advisor/spec.md` was preserved. This follow-up adds only this checklist. Implementation status remains unchanged for all twelve findings.
