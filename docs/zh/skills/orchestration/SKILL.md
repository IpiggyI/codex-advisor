---
name: orchestration
description: "主代理自行实现或委派工作、按 routing profile 选择角色与 capability tier、经 escalation ladder 从失败尝试中恢复，或需要 Advisor 决策建议与 independent acceptance 时使用。"
---

# Codex Advisor 编排

## 负责任务

任一 primary 模型都可以直接实现、委派有界工作，或两者并用。
保留用户的 primary 模型与 reasoning effort。中档 primary 是偏好，不是插件要求。在用户已授权的目标、范围、保留决定、验收条件和资源限额内，选择拆解、顺序和分工。不要为了让任务更容易而改动这些边界。调查与当前代码的不符之处，为用户拥有的变更寻求决议，并继续处理不受影响的独立工作。

明确的 Architect mode 授权会使其范围内的每一处实现编辑与修正都改为委派，对任一 primary 模型都成立。primary 拥有设计、契约、调度和验收，可以写设计和任务件。模型身份、工单、规格或未被接受的提议，都不会激活该模式。记录授权请求。它覆盖本任务及其后续；无关任务需要新的授权，除非用户明确授予会话级范围。

## 按角色与 capability tier 分配

委派调用前，阅读 [role-contracts.md](references/role-contracts.md) 中的对应数据包、[operations.md](references/operations.md) 中的安装、调用、证据和权限程序，以及 [routing-profile.md](references/routing-profile.md) 中的 dial 表。每一个模型名、effort 选项、默认值和候选顺序都写在 routing profile 里，不写在这里。尊重宿主容量，以及用户明确排除项和资源限额。显式选择 dial，不要为每次例行分配再问一次许可。

按你需要的产出选择角色：要证据用 Explorer，要变更用 worker，要判断或验收用 Advisor。在 first-round pool（light 与 standard）内选择档位，依据是结果对数据包无法承载的判断依赖多深。light 与 standard 之间没有前置条件；从 light 到 standard 不是升级。取最便宜且够用的 dial，用其默认值。具备资格并不强制升级。

senior 只能经 senior gate 到达：同一工作在 pool 内两次归因于能力的 complete failed attempt，或用户声明。对 Advisor，gate 只有报告低置信度的裁定或用户声明两种；worker 失败不能打开它。Advisor 的决策数据包默认 standard 档，验收数据包默认 light 档。

## 委派结果并保留调度

给每个 worker 目标、拥有范围、须保留的接口、保留约束和有意义的核验。附上原任务与来源引用，以便 worker 自行查阅。未规定的局部实现选择归 worker。预期行为不明、要求冲突，或必须改动保留接口，属于契约缺口，须在依赖编辑之前解决。

worker 自行调试与实现，不再向下委派实现。它们保留并发和无关编辑，并报告实际变更、检查、判断调用和缺口。返工须指出被违反的要求、可复现失败、期望行为和核验；仅有结构偏好不够。

派发前检查依赖、所有权（含生成文件和检查副作用）以及实际可用槽位。独立的委派任务可以并发；有依赖、所有权冲突或超出容量的工作须串行。不要把共享文件拆成名义上独立的所有者，也不要嵌套 worker 来规避容量。收集每份报告并检查合并结果。成功的兄弟任务不能补上失败或缺失的工作。

## 依据证据恢复

一次 complete worker attempt 包含实现、常规调试和核验，然后以验收失败或确实无法完成目标结束。中间失败的测试和单次工具错误不算 complete failed attempt。

诊断环境问题、缺失事实、契约缺口、推理失败和执行者是否合适。先修复环境问题。契约缺口（预期行为不明、要求冲突、涉及保留接口）在同一线程上以修正后的契约解决；它不是 ladder 的一步，也不是能力失败。普通工作允许 primary 接管；Architect mode 仍把编辑委派出去。

验收失败之后，遵循 escalation ladder：

- R1：在同一线程、同一 dial 上发一张返工工单。返工指出被违反的要求、可复现失败、期望行为和核验；工单里不含修法。
- R2：返工也失败且原因是能力时，在新线程中提档，并携带 current-state handoff：同一模型的更高 effort，或另一个模型。
- R3：同一模型最多提档一次。
- R4：重大执行问题（工具反复失败、失控、触碰保留项）可以跳过返工工单直接换模型，计为一次失败。

pool 内的第二次 complete failure 是否值得上 senior，是一项必须征求建议的关键决定，因此 senior gate 与这次咨询重合，Advisor 的裁定同时决定 senior 是否成立。在改派之前，停止先前冲突的写入者，检查实际状态，并保留有用变更。遵循 operations 参考中的 current-state handoff。

每一次委派 effort 变更，无论升高或降低，都需要新的 native 线程。模型变更和角色改派也需要新的匹配入口。同模型、同 effort 的 worker 返工可以复用其线程。independent acceptance 一律重新开始，含修正之后的评审。不要把改了提示词的 resume 报告成新会话。比较实际标识和设置；这是明确的生命周期策略，不是对缓存行为或节省的普遍主张。

## 会改变决定时再寻求判断

允许主动征求建议。在以下情况必须征求建议：

- 适用计划未覆盖的关键决定。
- 新证据使计划的关键假设失效。
- 初步诊断之后，失败原因仍不清楚。

在相关前提仍成立时，可以复用适用建议。实质性新证据需要重新判断；反复失败需要重新评估，而不是按失败次数无条件触发的调用。核对其引用的证据，并解释实质性分歧。建议不授予授权、否决权、新要求，也不接管用户目标。

一次 complete advisory attempt 在未回答指定问题，或来源/核验证据推翻其实质性结论时失败。仅有分歧、中间工具错误，以及仅有 worker 失败，都不能打开 Advisor 的 senior gate。诊断相关的 advisory 失败，并为该问题选择收集事实、澄清或另一个 dial。dial 变更会开启新线程。

## 验收实际交付物

检查全部实际变更，含新文件、修正和 worker 撰写的验收测试。确认测试会在意图要求被破坏时失败，并亲自重跑关键核验。报告、虚假的完成主张、跳过的必要检查或缺失的运行时证据，都不能确立成功。

普通的直接、委派或混合多步工作，可在 primary 检查之后完成。步数、文件数、primary 身份或由 senior 档实现本身，都不要求交付建议或 independent acceptance。

高风险交付和明确的独立评审请求，都要求在 primary 检查之后做 independent acceptance，对任一 primary 模型都成立：在新线程中把 Advisor 的验收数据包发给一个 Advisor 入口。按失败后果、可逆性和确立正确性的难度评估风险。决策建议与 independent acceptance 是同一 Advisor 角色及其入口的两种请求形态。先前的建议或 worker 自评，不能满足独立最终验收。

验收 dial 的选择与 primary effort 无关；高 effort 的 primary 也可以接受 light 档的验收。只有低置信度裁定或用户声明才能打开 Advisor 的 senior gate。检查路由、全新调用、工具活动，以及范围内的前后状态。处理实质性发现，再核验修正，即使 dial 未变，也要对修订后的交付物做一次新的评审。

必要执行不可用、设置不受支持、证据缺失或冲突，或实质性发现未解决时，受影响的验收明确保持待定。报告缺口，不要静默替换；不受影响的独立工作可以继续。
