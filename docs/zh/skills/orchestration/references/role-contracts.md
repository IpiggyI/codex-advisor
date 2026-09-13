# Native 角色契约

## Explorer

任一 primary 都可以使用钉死模型的 Explorer，配合新线程和显式 effort。
用 [operations.md](operations.md) 安装、调用并核验所选路径。

~~~text
QUESTION
<Specific source question, definitions, callers, or behavior to trace.>

SCOPE
<Absolute workspace path, source boundary, exclusions, and known constraints.>

PERMISSIONS
Inspect read-only. Do not write, format, implement, or delegate.
The primary owns design decisions and acceptance.

RETURN
FINDINGS: <observations, precise per-file source locations, and examined scope>
EXPLANATION: <evidence-based reasoning; label inferences>
GAPS: <unavailable sources, failed checks, and unresolved questions>
~~~

独立核对其引用与实际路由。否定性搜索只在已检查范围内确立缺失。发现不足时，可以转为 primary 直接调查，或改用另一项已授权分配；披露任何未核验的调用。
探索既不是实现，也不是独立最终验收。

## Worker（Implementer）

所有 worker 模型使用同一份五部结果契约。角色职责与档位无关。primary 保留拆解、调度和验收；未规定的局部实现选择归 worker。

~~~text
OBJECTIVE
<Observable outcome, acceptance conditions, original task reference, and sources.>

FILES AND OWNERSHIP
<Absolute workspace path, exact owned files/modules, excluded scope, and current
changes. You are not alone in the codebase; preserve concurrent and unrelated
edits and adapt to others' work. Surface conflicts instead of overwriting them.>

INTERFACES
<Inputs, outputs, behavior, callers, and shared interfaces that must be retained.>

CONSTRAINTS
<Binding decisions, user boundaries, resources, and reserved choices. Inspect the
original task and relevant sources. Perform implementation yourself; do not delegate
implementation further. Resolve unclear expected behavior, conflicting requirements,
and changes to reserved interfaces with the primary before dependent edits.>

VERIFICATION
<Meaningful checks, expected results, and failure conditions. Inspect the full
resulting diff and report failed, skipped, or unavailable checks.>

RETURN
COMPLETION: <complete, partial, or blocked, with reason>
CHANGES: <actual files and behavior changed>
VERIFICATION: <commands, exit status, and relevant observed output>
JUDGMENT CALLS: <local decisions within the contract>
GAPS: <ambiguity, conflicts, risks, and unverified results>
~~~

返工须指出被违反的要求、可复现失败、期望行为和核验。仅有结构偏好不能构成返工理由。
worker 负责常规调试。改派使用 operations 中的 handoff；任何修正之后，primary 检查实际变更并重跑关键核验。

## 决策建议

使用全新的 `codex_advisor_astra_advisor` 提出有界判断请求。在前提仍成立时可以复用适用建议；它不是一次新的最终评审。

~~~text
DECISION
<Specific question and trigger: proactive advice, uncovered key decision,
invalidated premise, or unclear failure cause after initial diagnosis.>

CONSTRAINTS
<User intent, authorization, retained interfaces, excluded scope, and resources.>

EVIDENCE
<Exact sources, observations, options, and uncertainties. For failure, include
the completed attempt, checks, diagnosis, and remaining question.>

REQUESTED JUDGMENT
<Proposed decision and the tradeoff or uncertainty to resolve.>

PERMISSIONS
Remain read-only. Do not write, format, implement, or delegate implementation.
Advice grants no authorization and adds no binding requirement.

RETURN
RECOMMENDATION: <proposed decision answering the question>
EVIDENCE: <supporting observations and exact source references>
ASSUMPTIONS: <premises, unverified claims, and how to check them>
TRADEOFFS: <costs and alternatives>
GAPS: <missing evidence and unresolved risks>
~~~

primary 核验路由，不要让 Advisor 推断自己的设置；核对引用的证据，并解释实质性分歧。未回答问题的相关 complete failure，或被实质性推翻的结论，可以使 `xhigh` 具备资格。仅有分歧或 worker 失败不能。

## Independent acceptance

在 primary 检查和关键核验之后，使用全新的
`codex_advisor_astra_reviewer`。它是语义 Advisor 角色的独立 native 入口；先前的咨询或 worker 报告不能满足它。

~~~text
REVIEW SCOPE
<Absolute workspace, binding task contract, acceptance conditions, and high-risk
or explicit-review trigger. Identify the exact baseline and current deliverable.>

ACTUAL CHANGES
<All changed and new files, reproducible diff command or before/after contents,
ownership boundaries, and unrelated changes to preserve. Inspect the actual
complete diff, including untracked files, before judging readiness.>

PRIMARY VERIFICATION
<Checks rerun by the primary, exit status, relevant output, evidence location,
and unresolved gaps. Separate worker claims from independently checked results.>

SETTINGS AND PERMISSIONS
<Explicit reviewer effort, relevant failed advisory evidence if selecting xhigh,
requested isolation, and scoped state captured before review.>
Remain read-only. Do not write, format, implement, or delegate implementation.
Use checks that preserve scoped state; disclose unavailable checks.

RETURN
READINESS: <ready, changes required, or unverified, with reason>
FINDINGS: <severity, exact source references, evidence, and impact>
VERIFICATION: <checks inspected or run, commands, status, and relevant output>
GAPS: <missing evidence, unchecked conditions, and residual risks>
~~~

评审人 effort 与 primary effort 无关。primary 核验全新调用、路由、引用的发现、工具活动，以及前后状态。
缺失证据或实质性发现会使必要验收保持待定。
在修正并由 primary 再核验之后，即使模型和 effort 未变，也要在新线程中评审修订后的交付物。
