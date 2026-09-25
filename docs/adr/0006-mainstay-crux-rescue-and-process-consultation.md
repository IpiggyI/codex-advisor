---
status: accepted
---

# Mainstay, crux, rescue, and process consultation

## Decision

The capability tiers are `mainstay`, `crux`, and `rescue`. New work starts in
`mainstay`, may start in `crux` for an identified key difficulty or interacting
constraints, and reaches `rescue` only through a `crux` capability failure or a
user declaration. The narrower first-round `crux` admission remains recorded but
disabled. There is no usage quota or observation log.

The routing profile remains the sole source for model, effort, default, candidate,
consultation, and acceptance dials. It uses `gpt-6-luna`, `gpt-6-sol`, and
`gpt-6-astra` across thirteen role-and-tier native entries. The eleven 0.2.0
entries join the eight 0.1.0 entries in the retire set. An entry still pins its
model and pins effort only for a single-effort cell.

One capability failure consists of a complete attempt that fails acceptance and
a same-thread, same-dial rework that also fails for a diagnosed capability cause.
The next attempt moves to the next tier without a same-tier model switch unless
no other choice exists. Its model level cannot be lower unless no other choice
exists, and the effort must rise when the model stays the same. The path is
`mainstay` -> `crux` -> `rescue` -> the user. R3 still limits one model to one
raise, and a major execution problem may skip rework and count as one failure.

Process consultation replaces decision advice packets. The primary, workers, and
Explorers call it with zero arguments. The assigned advisor receives the caller's
current effective context automatically, has no tools, and returns exactly one
plan, correction, or stop signal with its actual model and effort. Unsupported
reconstruction and execution failure return explicit failure rather than advice.
Exact caller/advisor model identity selects the full or reduced posture; an unknown
model follows the same identity comparison, without a model-family list. Advice is
adopted by default under the canonical adoption rules.

`SessionStart` injects the primary's posture; native entries carry each delegate's
posture. `PostToolUse` verifies native dispatch model and effort. Neither a primary
`Stop` nor a worker `SubagentStop` hook blocks completion. On 2026-09-26 the user
cancelled the previously proposed worker finish enforcement while retaining
posture, consultation, and dispatch verification. The scope decision and its
acceptance boundary are recorded in the task's decision ledger and acceptance file.

Independent acceptance remains a read-only, packet-based review of the actual
deliverable in a fresh thread after primary checks. It remains required for high-risk
work and explicit review requests, and consultation never substitutes for it. The
acceptance dial follows the accepted work's tier; work from several tiers uses the
highest tier involved. Primary-authored work uses the lowest advisor dial not weaker
than the primary, or the strongest advisor dial when none qualifies or the primary's
exact model id is absent from the profile. A low-confidence verdict stays pending
and goes to the user without an automatic higher-dial review. ADR-0005's acceptance
ownership, evidence reuse, verification batching, and scenario-selection rules stand.

The release is `0.3.0`. The previously planned grok lane moves to `0.4.0`.

## Consultation mechanism and host facts

The selected mechanism is B-prime: a zero-argument MCP call binds host-supplied
`_meta` thread, turn, and item identity to one caller rollout snapshot. It replays
ordered `response_item` records and replaces accumulated history at each
`compacted.replacement_history`, stopping before the in-flight consultation. It
uses no bounded turn window and accepts no caller-written summary.

A fresh ephemeral App Server thread starts through `thread/start`, receives the
structured effective history through `thread/inject_items`, and runs with source
base instructions plus consultant instructions that preserve caller constraints.
The replay preserves roles, supported content, tool calls and results, images,
truncated caller-visible output, and opaque reasoning. The advisor process starts
with a custom empty-tool model catalog and the qualified tool-disable settings.
The host inference trace must show the actual empty request tool set and the assigned
model and effort. Trace and catalog files are temporary, and the component never
handles credentials.

These facts were established on 2026-09-26 with Codex CLI `0.157.0`:

The maintenance sources are the [mechanism decision](../../.scratch/tiers-and-advisor-consult/spec.md#mechanism-decision-filled-by-ticket-01),
the [decision ledger](../../.scratch/tiers-and-advisor-consult/sources.md#24-decision-ledger),
and the [P6 probe record](../../.scratch/tiers-and-advisor-consult/acceptance.md#p6-authorized-continuation-and-selected-mechanism).

| Host fact | Evidence boundary | Invalidation check |
|---|---|---|
| Host MCP `_meta` supplies caller thread, session, turn, item, model, and effort identity to a zero-property tool call. | One primary route and the qualified worker and Explorer routes in the ticket 01 probes. | Requalify after MCP metadata or tool-call schema changes. |
| Ordered single-snapshot replay with replacement at `compacted.replacement_history` preserved the earliest effective context, unfinished-turn nonces, forced and automatic compaction, images, truncated output, and encrypted reasoning in the exercised shapes. | The actual source/advisor request comparisons recorded in ticket 01 acceptance P6; audio, video, rollback, parallel tool races, and other shapes were not certified. | Requalify after host version, rollout schema, compaction record, or supported item-shape changes; fail explicitly for an unqualified shape. |
| `thread/start` plus `thread/inject_items` made the structured history model-visible in a fresh ephemeral thread. | The qualified B-prime probes. A fork-plus-current-turn splice failed intra-turn compaction and is rejected. | Requalify after App Server protocol or injection semantics change. |
| The custom startup catalog plus the qualified disable settings produced an actual empty request tool set at the assigned dial. | The host inference-request trace, not an advisor statement or refused tool attempt. | Requalify after model catalog, configuration, tool registry, or request-trace format changes; missing trace evidence is failure. |
| A relative MCP script path with `cwd="."` resolved to the installed plugin root, and caller-home discovery worked for the versioned cache layout. | The temporary installed-plugin probe. | Requalify after plugin path resolution or cache-layout changes; unsupported layouts fail explicitly. |
| Shipped custom-agent model and pinned-effort precedence held in the tested pinned cases; caller effort held where the template left effort open. | Ticket 01 P3. Full-history routing evidence remained conflicting and is not generalized. | Re-run precedence checks after host, template schema, or spawn semantics change. |

Production must validate identity binding, the consultation boundary, supported item
shapes, tool pairing, truncation, context overflow, cancellation, result shape, and
temporary-state cleanup. It must reject missing or contradictory trace evidence,
absent replacement history, rollback, incomplete reconstruction, and unsupported
content instead of shortening context or fabricating advice. The qualification
artifacts and copied credentials used by temporary probes were deleted; no raw
evidence or persistent telemetry is part of the product.

Plugin hooks are a host security gate. Installing or updating the plugin does not
trust them; the user owns the review after the first install and after any update
that changes a hook definition, and product instructions retain the `/hooks` review.
Trust is keyed to the current hook hash, and an untrusted hook is skipped. This is
the one user step that the installation-only delivery rule from ADR-0004 cannot
remove. Temporary automated checks may use the user-approved trust bypass.

The user-trust and untrusted-skip paths were exercised on 2026-09-26 in the correct
temporary `CODEX_HOME`. At the host startup dialog titled "Hooks need review", the
user selected "Trust all and continue"; the subsequent no-bypass exec, thread
`01a0d9e1-e5d5-7fa0-9f66-56fbd8cc2b9b`, returned `HOOK_USER_TRUST_30941`, wrote the
matching `SessionStart` receipt, and exited 0. After the fixture hook hash changed
and the plugin was removed and added again, the primary selected "Continue without
trusting" in the startup review dialog. Thread
`01a0d9e3-0490-7a80-9788-0e3802b681aa` returned `MISSING`, wrote no new receipt,
and the `/hooks` overview showed `SessionStart` as Installed 1, Active 0, Review 1
with "1 hook needs review before it can run". The user made the trust choice and
the primary made the skip choice in startup review dialogs; this probe does not
claim that the user entered `/hooks`.
Revalidate this boundary if the host's hook discovery, startup review, hash trust,
overview, warning, or event semantics change.
The detailed sequence belongs in the
[P7 trust record](../../.scratch/tiers-and-advisor-consult/acceptance.md#p7-user-trusted-execution-and-untrusted-skip).

## What this supersedes

The quotations below are every complete sentence in ADR-0003, ADR-0004, and
ADR-0005 whose rule this decision replaces. Unquoted acceptance ownership,
fresh-thread, Architect-mode, installer safety, evidence reuse, batching, and
scenario-selection rules remain in force.

From ADR-0003:

> The complete-attempt definition, the fresh-thread policy, Architect mode, the required-advice triggers, and the acceptance rules stand.

Only the required-advice triggers in that mixed sentence are replaced; the other
listed rules stand.

> Complete worker failure follows implementation, ordinary debugging, and verification, ending in failed acceptance or concrete inability. Intermediate failures do not qualify. Diagnose environment, facts, contracts, reasoning, and executor suitability before choosing repair, clarification, rework, effort change, or takeover; no fixed ladder is imposed. Preserve useful changes and stop conflicting writers.

The first, second, third, and fourth sentences are quoted together because the
new failure count retains the first two and fourth but replaces the third sentence's
no-ladder rule.

> Advice is available proactively and required for uncovered key decisions, invalidated key plan assumptions, or failure causes still unclear after initial diagnosis.

> Applicable advice remains reusable while its premises hold. The primary checks sources and explains material disagreement without turning advice into authorization, a veto, or changed user requirements.

> Decision advice and independent acceptance share the senior Advisor allocation but retain distinct native entries and contracts.

> Review effort is independent of primary effort.

> Only a relevant complete advisory failure to answer its question, or a materially invalidated conclusion, makes advisory xhigh eligible; disagreement or worker failure alone does not.

> The workflow establishes eligibility, while the metadata inspector validates actual allocation.

From ADR-0004:

> Native entries are named by role and capability tier, not by model: `ca_explorer_light`, `ca_explorer_standard_m`, `ca_explorer_standard_h`, `ca_explorer_senior`, `ca_worker_light`, `ca_worker_standard_m`, `ca_worker_standard_h`, `ca_worker_senior`, `ca_advisor_light`, `ca_advisor_standard`, `ca_advisor_senior`.

> The skill text carries mechanism only: light and standard form the first-round pool, chosen by judgment dependence with no precondition between them and the cheapest adequate dial at its default; senior is reached only through the senior gate (two capability-attributed complete failed attempts inside the pool, or a user declaration; for the Advisor, a low-confidence verdict or a user declaration); after a failed acceptance the escalation ladder applies: R1 rework ticket in the same thread at the same dial; R2 raise in a fresh thread with the current-state handoff when rework fails and the cause is capability, either a higher effort of the same model or another model; R3 the same model is raised at most once; R4 a major execution problem may skip the rework ticket and change model, counted as one failure.

> Independent acceptance is the Advisor's second request shape and runs on the Advisor entries in a fresh thread; the separate reviewer entry is retired.

Only the second-request-shape clause is replaced. Independent acceptance still
runs through Advisor entries in a fresh thread, and there is still no separate
reviewer entry.

> Decision advice defaults to the standard tier, acceptance to the light tier.

> The companion installer owns this plugin's installed files: it overwrites the eleven shipped entries when they differ, deletes the eight retired filenames when present, touches nothing else, and fails its check mode on drift or residue.

Only the entry counts and retire set in that sentence are replaced; its ownership,
overwrite, isolation, and drift rules stand.

> Version `0.2.0`, with a version manual.

> ADR-0003: the sentence that no fixed ladder is imposed is replaced by the escalation ladder and the senior gate; the wording that decision advice and independent acceptance retain distinct native entries is replaced by one Advisor entry per tier with two request shapes; the routing table in the skill is replaced by the routing profile reference. The complete-attempt definition, the fresh-thread policy for every effort or model change, Architect mode, the required-advice triggers, and the acceptance rules stand.

Both sentences are quoted together because the new decision replaces the old
ladder, consultation, entry, and required-advice parts while retaining the named
lifecycle, mode, and acceptance rules.

> `gpt-6-sol` or another generation ships: change the model identifier in the affected TOML and the routing profile only; no new ADR.

> The grok lane (0.3.0) is designed: mechanism recorded here as a Node runner wrapping the `grok` CLI with a spec and receipt flow through the shell, ported from the sibling plugin's runner; naming, tests, and doctrine wording get their own spec and decision record.

From ADR-0005:

> A delegated check run uses a Worker entry, because the Explorer and Advisor entries pin `sandbox_mode = "read-only"` and a check that writes fails there; the tier follows the existing cheapest-adequate rule and the routing profile.

Only the tier-selection clause is replaced: delegated check execution now follows
the `mainstay` default, first-round `crux` admission, and normal escalation rules.
