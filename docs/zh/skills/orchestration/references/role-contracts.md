# Native 角色契约

## Explorer

任一 primary 都可以使用 Explorer 入口，配合新线程，并在入口未钉死 effort 时给出显式 effort。
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

## Worker

所有 Worker 入口使用同一份五部结果契约。角色职责与档位无关。primary 保留拆解、调度和验收；未规定的局部实现选择归 worker。

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
<The checks this contract requires, expected results, and failure conditions.
Run them, plus whatever your own debugging needs; checks that span other work
packages or the whole delivery belong to the primary's schedule. Inspect the
full resulting diff and report failed, skipped, or unavailable checks.>

RETURN
COMPLETION: <complete, partial, or blocked, with reason>
CHANGES: <actual files and behavior changed>
VERIFICATION: <commands, exit status, and relevant observed output>
JUDGMENT CALLS: <local decisions within the contract>
GAPS: <ambiguity, conflicts, risks, and unverified results>
~~~

返工须指出被违反的要求、可复现失败、期望行为和核验。仅有结构偏好不能构成返工理由。
worker 负责常规调试。改派使用 operations 中的 handoff；任何修正之后，primary 检查实际变更，并核验失败场景及其影响范围，复用该修正未触及的有效证据。

## Advisor

每个档位一个 Advisor 入口（`ca_advisor_light`、`ca_advisor_standard`、`ca_advisor_senior`），回答两种请求形态：决策数据包和验收数据包。两者都在新线程中只读运行。routing profile 指定每种形态的默认入口；senior 入口只能经报告低置信度的裁定或用户声明到达。

### 决策建议

用全新的 Advisor 线程提出有界判断请求。在前提仍成立时可以复用适用建议；它不是一次新的最终评审。

~~~text
DECISION
<Specific question and trigger: proactive advice, uncovered key decision,
invalidated premise, unclear failure cause after initial diagnosis, or the
senior gate after two complete failures.>

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

primary 核验路由，不要让 Advisor 推断自己的设置；核对引用的证据，并解释实质性分歧。一次 complete advisory attempt 在未回答其问题或结论被实质性推翻时失败；仅有分歧或 worker 失败两者都不算，也不能把 Advisor 推到其 senior 入口。

### Independent acceptance

在 primary 亲自检查交付物、并完成自己负责的检查之后，把验收数据包发给全新的 Advisor 线程。它是同一组入口的第二种请求形态，不是单独的评审人；先前的咨询、决策建议、worker 报告或委派的检查执行，都不能满足它。

~~~text
REVIEW SCOPE
<Absolute workspace, binding task contract, acceptance conditions, and high-risk
or explicit-review trigger. Identify the exact baseline and current deliverable.>

ACTUAL CHANGES
<All changed and new files, reproducible diff command or before/after contents,
ownership boundaries, and unrelated changes to preserve. Inspect the actual
complete diff, including untracked files, before judging readiness.>

PRIMARY VERIFICATION
<Checks the primary owns for this acceptance: executor, scope, command, exit
status, relevant output, evidence location, and unverified items. Separate worker
claims from results the primary organized and confirmed.>

SETTINGS AND PERMISSIONS
<Selected Advisor entry and, where the entry leaves it open, the explicit effort;
the low-confidence verdict or user declaration if selecting the senior entry;
requested isolation, and scoped state captured before review.>
Remain read-only. Do not write, format, implement, or delegate implementation.
Use checks that preserve scoped state; disclose unavailable checks.

RETURN
READINESS: <ready, changes required, or unverified, with reason>
FINDINGS: <severity, exact source references, evidence, and impact>
VERIFICATION: <checks inspected or run, commands, status, and relevant output>
GAPS: <missing evidence, unchecked conditions, and residual risks>
~~~

验收 dial 与 primary effort 无关。primary 核验全新调用、路由、引用的发现、工具活动，以及前后状态。
缺失证据或实质性发现会使必要验收保持待定。
在修正并由 primary 再核验之后，即使入口和 effort 未变，也要在新线程中评审修订后的交付物。
