---
status: accepted
---

# Autonomous primary and tiered role pool

The no-fixed-ladder rule, the distinct native entry for independent acceptance, and the routing table in this record are superseded by [Tier-named native entries, first-round pool with a gated senior tier, and a self-updating installer](0004-tier-named-entries-first-round-pool.md). The complete-attempt definition, the fresh-thread policy, Architect mode, the required-advice triggers, and the acceptance rules stand.

## Decision

Any primary model may implement, delegate, or combine both within user authorization.
The plugin preserves primary model and effort. Explicit Architect mode delegates
all implementation edits and corrections for its task scope, for any primary.
A task artifact or model identity does not activate it. Scope lasts through task
follow-ups; unrelated tasks require renewed authorization unless session-wide
scope was explicitly granted.

This record supersedes ADR-0001's mode eligibility, consultation triggers,
Explorer selection, delegated effort and review-floor rules, and ADR-0002's implementation selection
and failure policy. Codex-only identity, native model pins, ownership, scheduling,
safe installation, evidence validation, and user authorization boundaries remain.

| Role | Tier | Allocation |
|---|---|---|
| Explorer | light | Luna high |
| Explorer | standard / senior | Usually Luna max; direct Sol or Astra medium/high allowed |
| worker (Implementer) | light | Luna max |
| worker (Implementer) | standard | Sol high/xhigh initially |
| worker (Implementer) | senior | Astra medium/high; xhigh after relevant complete worker failure |
| Advisor, including independent acceptance | senior | Astra medium/high; xhigh after relevant complete advisory failure |

Luna is a usual exploration preference, not an obligatory first attempt.
Native names distinguish model and responsibility. Worker contracts specify
outcome, ownership, retained interfaces, constraints, and verification while
leaving local implementation decisions to the worker. Scheduling and acceptance
stay with the primary; workers do not delegate implementation further.

## Failure and sessions

Complete worker failure follows implementation, ordinary debugging, and verification,
ending in failed acceptance or concrete inability. Intermediate failures do not
qualify. Diagnose environment, facts, contracts, reasoning, and executor suitability
before choosing repair, clarification, rework, effort change, or takeover; no
fixed ladder is imposed. Preserve useful changes and stop conflicting writers.

Every delegated effort change in either direction, model change, or role reassignment
starts a new native thread with the current task state. Same-model, same-effort
worker correction may reuse a thread. Independent acceptance always starts fresh,
including after corrections. This is the user's lifecycle policy, not a universal
statement about host cache invalidation or savings.

## Judgment and delivery

Advice is available proactively and required for uncovered key decisions, invalidated
key plan assumptions, or failure causes still unclear after initial diagnosis.
Applicable advice remains reusable while its premises hold. The primary checks
sources and explains material disagreement without turning advice into authorization,
a veto, or changed user requirements.

Ordinary multi-step completion follows primary inspection and meaningful checks.
High-risk work or an explicit review request requires fresh independent acceptance
of the actual complete changes after those checks. Risk depends on consequences,
reversibility, and difficulty checking correctness. Counts and model identity
alone do not trigger it.

Decision advice and independent acceptance share the senior Advisor allocation
but retain distinct native entries and contracts. Review effort is independent
of primary effort. Only a relevant complete advisory failure to answer its question,
or a materially invalidated conclusion, makes advisory xhigh eligible; disagreement
or worker failure alone does not. The workflow establishes eligibility, while the
metadata inspector validates actual allocation. Required unavailable calls,
contradictory evidence, or unresolved material findings leave acceptance pending.

## Basis and verification

The user approved this policy on 2026-09-12 to give the primary more initiative
while making stronger and lighter delegates available within explicit boundaries.
The four tickets in `.scratch/autonomous-role-pool/issues/` govern implementation:
01 autonomous work, 02 exploration, 03 recovery (after 01), and 04 judgment (after 03).
The parent specification maps its verification cases to these four tickets.

The existing native roles and shell checks cover the platform boundary without
a new scheduler, bridge, profile schema, or budget service. New Sol/Astra Explorer
entries preserve existing native identities. Adjustable templates leave effort
to the caller; only Luna worker pins max.

Use disposable installation and small native route/lifecycle checks, reusing
evidence and controlled failures. Record tested host/revision and gaps in the
feature acceptance record. Recheck discovery, caller effort, and permission
handling after host/config changes. Read-only requests are distinct from observed
behavior and enforced isolation. These checks do not establish general quality,
stability, or savings; those require later real-task experience.
