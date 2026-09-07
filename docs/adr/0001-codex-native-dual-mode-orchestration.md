---
status: accepted
---

# Codex-native dual-mode orchestration

The fork will be named `codex-advisor` and support Codex only. It will use the existing native-agent foundation and adopt two session work modes: architect mode and advisor mode. These responsibility rules replace the upstream task routes `solo`, `delegate`, `audit`, and `full`, including the `SELECTIVE ROUTE` declaration protocol. No compatibility layer for that protocol is retained. Worker specifications, risk-based review, and runtime verification remain part of the new workflow.

The new rules cover the main responsibility combinations of the old routes:

| Upstream route | Corresponding responsibility combination |
|---|---|
| `solo` | Ordinary solo work, including an Astra primary session without architect-mode authorization |
| `delegate` | Architect mode with an implementer and primary-agent acceptance, without an additional reviewer |
| `audit` | Advisor mode with primary-agent implementation and an independent Astra consultation before delivery; consultation alone is not equivalent to the old final-review gate |
| `full` | Architect mode with an implementer, primary-agent acceptance, and an independent Astra reviewer |

This is a replacement of the workflow policy, not a preservation of every old route guarantee. A decision consultation and a final review of actual changes are distinct activities; requesting a consultation does not establish that an independent final review occurred. The new rules determine when consultation and review are required.

Architect mode assigns design, task specifications, and acceptance to the primary agent. All implementation is delegated, including one-line changes and corrections to an implementer's work. This keeps responsibility explicit at the cost of an extra delegation round trip for small changes. Advisor mode lets the primary agent carry out the work and obtain judgment from an advisor.

Architect mode requires both an Astra primary session and an explicit user request or user consent. An Astra primary session without that authorization continues ordinary solo work; selecting Astra alone does not activate architect mode. Other primary models, including Sol and Luna, use advisor mode. The plugin does not require a dedicated mode-switch command. Changing the primary model is a host operation, not a plugin operation.

Architect-mode authorization defaults to the current task and remains valid across follow-up turns and implementation subtasks belonging to that task. A new task does not inherit that authorization. The user may explicitly authorize architect mode for the whole session instead.

Astra is the designated architect and advisor model. Reasoning requirements apply to these delegated calls:

| Caller and context | Delegated model | Reasoning requirement |
|---|---|---|
| Astra in architect mode delegating implementation | `gpt-5.6-luna` | Always `max` |
| Astra in architect mode | `gpt-5.6-sol` | Default `high`; explicit user adjustments allowed |
| A primary agent consulting its advisor in advisor mode | `gpt-6-astra` | Default `high`; explicit user adjustments allowed |
| Astra in architect mode requesting independent review | `gpt-6-astra` | Default to the higher of `high` and the primary session's reasoning effort; explicit adjustments must not fall below the primary session's effort |
| Any primary agent delegating exploration to the Luna Explorer | `gpt-5.6-luna` | Explicitly selected by the primary agent for each call from efforts supported by the current host and model |

The plugin imposes no reasoning-effort requirement on a model used directly as the primary session, including Astra in architect mode. These call-specific requirements are not global model restrictions.

In advisor mode, consultation is required before architecture decisions, data migrations, API designs, or refactors touching at least three files; after two distinct unsuccessful attempts at the same problem; and before declaring a multi-step deliverable complete. The primary agent may also request additional consultations. It owns the decision and must disclose disagreements with the advisor and explain its reasoning. User authorization and existing project approval requirements still apply.

Architect mode selects between Luna and Sol implementers. Bounded, fully specified work goes to Luna at `max`; work requiring substantial judgment or context, or carrying higher risk, goes directly to Sol. A Luna attempt is not required before selecting Sol.

The primary agent may dispatch independent tasks in parallel when file ownership does not conflict, within the host's concurrency limit. It owns implementation scheduling; implementers do not delegate implementation further.

The architect inspects all actual changes and reruns the key verification checks before acceptance. Worker reports alone are insufficient evidence.

After the architect's acceptance checks, a separate Astra reviewer with a fresh context reviews high-risk work or work for which the user requests independent review. Other work does not require an additional reviewer.

The independent reviewer's default reasoning effort is `high` when the primary session uses `high` or a lower effort, `xhigh` when the primary uses `xhigh`, and `max` when the primary uses `max`. This avoids reducing reasoning effort during independent review, at the cost of potentially higher latency and token usage. Matching or increasing effort does not guarantee a stronger review; fresh context and inspection of actual changes remain necessary.

When required consultation or independent review cannot run because Astra is unavailable, or its actual model or reasoning effort cannot be confirmed, the affected step pauses and reports the reason. It does not silently substitute another model or bypass the required consultation or review. Failure handling preserves the architect-mode requirement that delegated Luna implementation calls use `max`.

The native role `codex_advisor_luna_explorer` fixes the exploration model to `gpt-5.6-luna` so delegated exploration does not inherit a more expensive primary model. Once installed and discovered by the host, it is available to any primary model, including all non-Astra models, without requiring architect mode or loading `codex-advisor:orchestration`. Outside that skill, the primary agent may select it from its role description. When the skill is applied to the current task, a primary agent that decides to delegate exploration selects the Luna Explorer by default. The skill's trigger scope and existing rules for whether to delegate remain unchanged; installing the role does not establish a global default exploration route.

The Explorer performs read-only fact finding and returns source locations, supporting evidence, explanations grounded in that evidence, and unresolved questions. It does not own design decisions, implement changes, or serve as an independent reviewer. Its role template leaves reasoning effort unset, and the primary agent explicitly selects a supported effort for every call without a `max` minimum. If Luna is unavailable or its findings are insufficient, the primary agent may investigate directly; switching to a more expensive delegated model requires explicit user authorization.

These are design decisions for the fork; this record does not change the installed plugin or establish runtime enforcement.
