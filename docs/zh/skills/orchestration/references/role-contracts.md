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

每个档位一个 Advisor 入口，用于回答验收数据包。它在新线程中只读运行。按被验收的工作选择 dial：单一档位产出的工作使用该档位；多个档位共同产出的工作使用其中最高档位；primary 自行产出的工作使用不弱于 primary dial 的最低 Advisor dial。没有合格的 Advisor dial，或 routing profile 中没有 primary 的精确模型标识时，使用最强 Advisor dial。低置信度裁定会使验收保持待定并交给用户，不会自动触发另一个 dial 的复审。

过程咨询不使用数据包。它是一个单独的无参数调用，受 routing profile 和 [consult-posture.md](consult-posture.md) 约束，绝不能代替 independent acceptance。

### Independent acceptance

在 primary 亲自检查交付物、并完成自己负责的检查之后，把验收数据包发给全新的 Advisor 线程。先前的咨询、worker 报告或委派的检查执行都不能满足它。

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
the accepted work's tier or the primary-derived dial rule; requested isolation,
and scoped state captured before review.>
Remain read-only. Do not write, format, implement, or delegate implementation.
Use checks that preserve scoped state; disclose unavailable checks.

RETURN
READINESS: <ready, changes required, or unverified, with reason>
FINDINGS: <severity, exact source references, evidence, and impact>
VERIFICATION: <checks inspected or run, commands, status, and relevant output>
GAPS: <missing evidence, unchecked conditions, and residual risks>
~~~

primary 核验全新调用、路由、引用的发现、工具活动，以及前后状态。缺失证据、低置信度裁定或实质性发现会使必要验收保持待定。在修正并由 primary 再核验之后，即使入口和 effort 未变，也要在新线程中评审修订后的交付物。
