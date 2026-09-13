---
name: orchestration
description: "主代理自行实现或委派工作、按档位选择探索、从失败尝试中恢复，或需要 Astra 决策建议与 independent acceptance 时使用。"
---

# Codex Advisor 编排

## 负责任务

任一 primary 模型都可以直接实现、委派有界工作，或两者并用。
保留用户的 primary 模型与 reasoning effort。中档 primary（例如 Sol）是偏好，不是插件要求。在用户已授权的目标、范围、保留决定、验收条件和资源限额内，选择拆解、顺序和分工。不要为了让任务更容易而改动这些边界。调查与当前代码的不符之处，为用户拥有的变更寻求决议，并继续处理不受影响的独立工作。

明确的 Architect mode 授权会使其范围内的每一处实现编辑与修正都改为委派，对任一 primary 模型都成立。primary 拥有设计、契约、调度和验收，可以写设计和任务件。模型身份、工单、规格或未被接受的提议，都不会激活该模式。记录授权请求。它覆盖本任务及其后续；无关任务需要新的授权，除非用户明确授予会话级范围。

## 按职责与能力分配

委派调用前，阅读 [role-contracts.md](references/role-contracts.md) 中的对应数据包，以及 [operations.md](references/operations.md) 中的安装、调用、证据和权限程序。
尊重宿主容量，以及用户明确排除项和资源限额。在允许的 effort 中显式选择，不要为每次例行分配再问一次许可。

| 职责 | 档位 | 模型与 effort |
|---|---|---|
| Explorer | light | Luna `high` |
| Explorer | standard / senior | 通常 Luna `max`；允许直接使用 Sol 或 Astra 的 `medium` / `high` |
| worker（Implementer） | light | Luna `max` |
| worker（Implementer） | standard | Sol `high` / `xhigh`，含首次尝试 |
| worker（Implementer） | senior | Astra `medium` / `high`；在一次相关的 complete worker attempt 失败之后可用 `xhigh` |
| Advisor，含 independent acceptance | senior | Astra `medium` / `high`；在一次相关的 complete advisory attempt 失败之后可用 `xhigh` |

Luna 是通常的探索偏好，不是前置条件。复杂度、判断需要或已有证据，都可以直接选择 Sol 或 Astra 探索。按模型区分的 native 名称是入口，不是额外的 capability tier。在允许的范围内，证据充足的聚焦问题使用 `medium`；备选方案、冲突证据或跨模块约束可以一开始就用 `high`。具备资格并不强制升级。不存在 Explorer `xhigh` 路径。

## 委派结果并保留调度

给每个 worker 目标、拥有范围、须保留的接口、保留约束和有意义的核验。附上原任务与来源引用，以便 worker 自行查阅。未规定的局部实现选择归 worker。预期行为不明、要求冲突，或必须改动保留接口，属于契约缺口，须在依赖编辑之前解决。

worker 自行调试与实现，不再向下委派实现。它们保留并发和无关编辑，并报告实际变更、检查、判断调用和缺口。返工须指出被违反的要求、可复现失败、期望行为和核验；仅有结构偏好不够。

派发前检查依赖、所有权（含生成文件和检查副作用）以及实际可用槽位。独立的委派任务可以并发；有依赖、所有权冲突或超出容量的工作须串行。不要把共享文件拆成名义上独立的所有者，也不要嵌套 worker 来规避容量。收集每份报告并检查合并结果。成功的兄弟任务不能补上失败或缺失的工作。

## 依据证据恢复

一次 complete worker attempt 包含实现、常规调试和核验，然后以验收失败或确实无法完成目标结束。中间失败的测试和单次工具错误不算 complete failed attempt。

先诊断环境问题、缺失事实、契约缺口、推理失败和执行者是否合适。先修复环境问题并澄清契约。再按观察到的原因选择：原分配不变的返工、不同 effort、更合适的 worker，或 primary 接管；没有强制阶梯。普通工作允许 primary 接管；Architect mode 仍把编辑委派出去。

相关的 complete worker failure 使同一工作的 Astra worker `xhigh` 具备资格，含携带该证据的接管。无关任务或角色的失败不算。Sol worker `xhigh` 不需要先前失败。在改派之前，停止先前冲突的写入者，检查实际状态，并保留有用变更。遵循 operations 参考中的 current-state handoff。

每一次委派 effort 变更，无论升高或降低，都需要新的 native 线程。模型变更和角色改派也需要新的匹配入口。同模型、同 effort 的 worker 返工可以复用其线程。independent acceptance 一律重新开始，含修正之后的评审。不要把改了提示词的 resume 报告成新会话。比较实际标识和设置；这是明确的生命周期策略，不是对缓存行为或节省的普遍主张。

## 会改变决定时再寻求判断

允许主动征求建议。在以下情况必须征求建议：

- 适用计划未覆盖的关键决定。
- 新证据使计划的关键假设失效。
- 初步诊断之后，失败原因仍不清楚。

在相关前提仍成立时，可以复用适用建议。实质性新证据需要重新判断；反复失败需要再评估，而不是无条件地按反对意见再调一次。核对其引用的证据，并解释实质性分歧。建议不授予授权、否决权、新要求，也不接管用户目标。

一次 complete advisory attempt 在未回答指定问题，或来源/核验证据推翻其实质性结论时失败。仅有分歧、中间工具错误，以及仅有 worker 失败，都不能解锁 Advisor `xhigh`。诊断相关的 advisory 失败，并为该问题选择收集事实、澄清或调整 effort。effort 变更会开启新线程。

## 验收实际交付物

检查全部实际变更，含新文件、修正和 worker 撰写的验收测试。确认测试会在意图要求被破坏时失败，并亲自重跑关键核验。报告、虚假的完成主张、跳过的必要检查或缺失的运行时证据，都不能确立成功。

普通的直接、委派或混合多步工作，可在 primary 检查之后完成。步数、文件数、primary 身份或 Astra 实现本身，都不要求交付建议或 independent acceptance。

高风险交付和明确的独立评审请求，都要求在 primary 检查之后使用全新的 Astra Independent reviewer，对任一 primary 模型都成立。按失败后果、可逆性和确立正确性的难度评估风险。决策建议与 independent acceptance 同属语义上的 Advisor 角色，但使用不同的 native 入口和契约。先前的建议或 worker 自评，不能满足独立最终验收。

评审人最初在 `medium` 或 `high` 中选择，与 primary effort 无关；primary 为 `max` 时两者都可用。只有相关的 complete advisory failure 才使评审人 `xhigh` 具备资格。检查路由、全新调用、工具活动，以及范围内的前后状态。处理实质性发现，再核验修正，即使 effort 未变，也要对修订后的交付物做一次新的评审。

必要执行不可用、设置不受支持、证据缺失或冲突，或实质性发现未解决时，受影响的验收明确保持待定。报告缺口，不要静默替换；不受影响的独立工作可以继续。
