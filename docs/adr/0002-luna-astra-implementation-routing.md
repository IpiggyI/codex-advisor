---
status: accepted
---

# Luna and Astra implementation routing

The implementation selection and failure policy in this record are superseded by [Autonomous primary and tiered role pool](0003-autonomous-primary-and-tiered-role-pool.md). The original decision and evidence below remain historical.

Architect mode will use Luna and Astra as its default implementation choices, with Sol available when explicitly selected by the user. This decision supersedes the implementation routing and implementation-effort decisions in [ADR-0001](0001-codex-native-dual-mode-orchestration.md). It records the target design; implementation and installation require separate work.

## Roles and selection

| Native role | Model | Selection | Reasoning effort |
|---|---|---|---|
| `codex_advisor_luna_implementer` | `gpt-5.6-luna` | Bounded work with a complete specification, little implementation judgment, and clear acceptance checks | Always `max` |
| `codex_advisor_astra_implementer` | `gpt-6-astra` | Work requiring substantial implementation judgment or cross-module understanding, or carrying higher risk | Default `medium`; explicit supported user adjustments allowed |
| `codex_advisor_sol_implementer` | `gpt-5.6-sol` | Work for which the user explicitly selects Sol | Default `high`; explicit supported user adjustments allowed |

The architect may select Astra directly; a failed Luna attempt is not required. Astra implementation effort does not automatically follow the primary agent's effort or increase after a failed attempt.

Every implementer receives a complete specification, defined ownership, and verification requirements. The architect resolves material specification gaps before dependent implementation. The Astra implementer owns the assigned implementation and corrections; design, scheduling, and final acceptance belong to the architect.

Astra receives a separate native role with a fixed model identity. The existing Sol role continues to identify Sol. Native roles are installed into user environments and checked against their expected models; repurposing the Sol identity would create an installation and verification migration without improving responsibility boundaries.

## Failure handling and acceptance

When Luna's implementation fails acceptance, the architect diagnoses the cause and decides whether to clarify the specification, request a Luna correction, or reassign the work to Astra. There is no fixed retry count. Environment failures and specification gaps do not by themselves establish that Luna lacks the required capability. Reassignment follows the existing ownership and actual-state handoff requirements.

Sol is not an automatic fallback for unavailability, implementation failure, budget pressure, or waiting time. It requires an explicit user selection. Invalid or unavailable roles or efforts, and missing or conflicting routing evidence, leave affected acceptance pending until resolved.

The architect inspects every actual change and reruns key verification. High-risk work and explicit user requests require a fresh Astra independent review after those checks. Selecting Astra as the implementer does not by itself trigger that additional review. Once required, review remains pending through corrections until the revised deliverable passes a fresh review. Review effort follows ADR-0001's rule based on the primary agent's effort, independently of the implementer's `medium` default.

## Decision basis and validation limits

As of 2026-09-08, the user prioritizes completion quality while considering actual Codex subscription allowance consumption. The intended trade-off is to retain Luna for work that benefits from its lower resource cost and use Astra where implementation requires more judgment, while keeping Sol available for an explicit cost or model preference.

The user supplied these DeepSWE results for the same evaluation workload:

| Model and effort | Reported completion | Reported cost |
|---|---|---|
| Luna at `max` | 67% ± 4% | $0.61 |
| Sol at `high` | 69% ± 1% | $2.66 |
| Astra at `high` | 73% ± 3% | $5.72 |

The evaluation setup, uncertainty definition, and results have not been independently verified. These observations motivate the routing choice but do not establish statistical significance, actual subscription savings, or the performance of Astra at `medium`.

The `medium` default rests on the expectation that an Astra architect's completed design and specification reduce the implementer's reasoning burden. The [official Astra model documentation](https://developers.openai.com/api/docs/models/gpt-6-astra), checked on 2026-09-08, lists `medium` as supported. Support does not establish adequacy for this workflow. Representative delegated tasks must check acceptance quality, correction work, and actual allowance consumption before claiming a quality or cost improvement. Repeated failures attributable to insufficient implementation reasoning would warrant revisiting the default.

The [official Codex pricing documentation](https://learn.chatgpt.com/docs/pricing), checked on 2026-09-08, states that allowance consumption depends on model choice, context, reasoning, tool use, retrieval, and caching. Evaluation costs in dollars are not a direct measurement of the user's subscription allowance. Model and allowance guidance should be checked again when validating the implementation or when host support or billing rules change.
