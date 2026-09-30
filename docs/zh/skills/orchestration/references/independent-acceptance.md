# Independent acceptance

用户要求独立评审，或交付可能是高风险时，阅读本文件。通过 [operations.md](operations.md) 派发 Advisor。

## 判断是否需要

高风险交付和明确的独立评审请求，都要求在 primary checks 之后做 independent acceptance，对任一 primary 模型都成立。风险跟随后果、可逆性和检查正确性的难度，而不是步数、文件数或模型。咨询、探索、worker 自评和委派的检查执行，都不能满足 independent acceptance。

## 选择 Advisor

按 [routing profile](routing-profile.md#验收映射) 中的验收映射，选择 Advisor 入口及其 dial。一个 Advisor 入口在新线程中只读回答验收数据包。

## 发送验收数据包

检查交付物并完成你负责的检查之后，捕获范围内状态，并把以下数据包发给全新的 Advisor 线程：

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
the acceptance-mapping case that selected it; requested isolation, and scoped
state captured before review.>
Remain read-only. Do not write, format, implement, or delegate implementation.
Use checks that preserve scoped state; disclose unavailable checks.

RETURN
READINESS: <ready, changes required, or unverified, with reason>
FINDINGS: <severity, exact source references, evidence, and impact>
VERIFICATION: <checks inspected or run, commands, status, and relevant output>
GAPS: <missing evidence, unchecked conditions, and residual risks>
~~~

## 检查评审

核验 Advisor 的路由、全新调用和工具活动。检查它对完整 diff 的查看、它引用的发现，以及范围内的前后状态。

## 修正并重新评审

处理实质性发现，然后检查并再核验修正。普通模式允许 primary 修正；Architect mode 把修正委派出去。即使入口和 effort 未变，也要在新线程中对修订后的交付物取得一次新的评审。

缺失必要评审、必要执行不可用、设置不受支持、证据缺失或冲突、低置信度裁定，或未解决的实质性发现，都会使受影响的验收明确保持待定并交给用户。报告缺口，不要静默替换；不受影响的独立工作可以继续。
