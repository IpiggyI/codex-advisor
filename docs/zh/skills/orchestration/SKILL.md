---
name: orchestration
description: "主代理被要求委派、即将委派工作，或即将验收、返工或升级一个委派结果时使用；用户授权 Architect 模式，或交付需要 independent acceptance 时也使用。主代理、worker 或 Explorer 缺少适用的已选定姿态或 adoption 指令时同样使用。"
---

# Codex Advisor 编排

## 负责任务

任一 primary 模型都可以直接实现、委派有界工作，或两者并用。保留用户的 primary 模型与 reasoning effort。在用户已授权的目标、范围、保留决定、验收条件和资源限额内，选择拆解、顺序和分工。不要为了让任务更容易而改动这些边界。调查与当前代码的不符之处，为用户拥有的变更寻求决议，并继续处理不受影响的独立工作。

明确的 Architect mode 授权会使其范围内的每一处实现编辑与修正都改为委派，对任一 primary 模型都成立。primary 拥有设计、契约、调度和验收，可以写设计和任务件。模型身份、工单、规格或未被接受的提议，都不会激活该模式。记录授权请求。它覆盖本任务及其后续；无关任务需要新的授权，除非用户明确授予会话级范围。

## 按事件阅读参考文件

只阅读当前事件点名的参考文件。每个指针后面的规则，在其参考文件被阅读之前也成立。

- 每次新的 native spawn 之前，包括改派和为 independent acceptance 派发 Advisor：阅读 [operations.md](references/operations.md) 和 [routing-profile.md](references/routing-profile.md) 中的 dial 表。Explorer 或 Worker 的 spawn 还要阅读 [role-contracts.md](references/role-contracts.md) 中的对应数据包；Advisor 的 spawn 改用下文 independent acceptance 参考文件中的数据包。spawn 时使用 `fork_turns: none`；只有钩子的确认行或检查器显示了派发的模型和 effort，该派发才算已检查。
- 验收委派结果，或在 Architect mode 下工作：本文件已足够。
- 验收失败后、返工或升级之前：阅读 [recovery.md](references/recovery.md)。先在同一线程、同一 dial 上返工；effort、模型或角色的任何变更都使用新线程，并携带 current-state handoff。
- 用户要求独立评审，或交付可能是高风险时：阅读 [independent-acceptance.md](references/independent-acceptance.md) 和 routing profile 中的验收映射。independent acceptance 在你自己的检查之后，于全新的 Advisor 线程中运行；咨询、自评和委派的检查执行都不能代替它。
- 姿态块或 adoption 块缺失或不适用时：按下文咨询一节所述，阅读 [consult-posture.md](references/consult-posture.md) 和 routing profile 中的咨询映射。

## 按角色与 capability tier 分配

每一个模型名、effort 选项、默认值、候选顺序、咨询映射和验收映射都写在 routing profile 中。尊重宿主容量、用户明确排除项和资源限额。显式选择 dial，不要为每次例行分配再问一次许可。

按所需产出选择角色：证据使用 Explorer，变更使用 worker，independent acceptance 使用 Advisor。新工作从 `mainstay` 开始。已经识别出关键难点或必须处理相互作用的约束时，可以从 `crux` 开始。使用次数没有配额。除非用户声明，否则 `rescue` 不能作为首轮选择。

在一个角色与档位单元中，采用第一个候选及其默认值。结果更依赖数据包无法承载的判断时，采用后面的候选。capability tier 由模型决定，effort 是档位内部的细分等级。

## 委派结果并保留调度

给每个 worker 目标、拥有范围、须保留的接口、保留约束和有意义的核验。附上原任务与来源引用，以便 worker 自行查阅。未规定的局部实现选择归 worker。预期行为不明、要求冲突，或必须改动保留接口，属于契约缺口，须在依赖编辑之前解决。worker 负责实现和常规调试，不再向下委派；契约的其余部分由其数据包承载。跨其他工作包或覆盖整体交付的检查，留在你的方案里。

派发前检查依赖、所有权（含生成文件和检查副作用）以及实际可用槽位。工单边界、派发次数和核验批次分别确定：把共用高成本准备的检查合并，前提是范围仍可理解、失败仍可定位；在后续工作依赖其结果的地方保留一次真实检查。独立的委派任务可以并发；有依赖、所有权冲突或超出容量的工作须串行，并用前任留下的实际状态更新每份串行数据包。不要把共享文件拆成名义上独立的所有者，也不要嵌套 worker 来规避容量。收集每份报告并检查合并结果。失败、受阻、缺失或不完整的工作及其依赖保持待定；成功的兄弟任务不能使它们完成。

## 验收实际交付物

亲自检查全部实际变更，含新文件、修正和 worker 撰写的验收测试。确认测试会在意图要求被破坏时失败，并确认证据描述的是当前交付物。报告、虚假的完成主张、跳过的必要检查或缺失的运行时证据，都不能确立成功。

primary checks 指由你负责并确认的检查。为每个核验批次指定一个执行者：你本人，或者一个受派者；受派者获得完整批次需求、合并后的变更和已收集的证据，并报告执行者、范围、命令、退出状态、输出位置和未核实项；委派执行绝不转移验收决定。每个批次运行一次，然后核对覆盖范围、实际输出与当前合并状态。相关代码、产物、检查、输入和环境仍支持原结论时，复用该结果。换执行者或换会话本身不构成重跑检查的理由；依赖变化、证据缺口、未解释的失败或已识别的风险才构成，返工则覆盖失败场景及其影响范围。

普通的直接、委派或混合多步工作，可在 primary checks 之后完成。步数、文件数、primary 身份或使用某一特定档位本身，都不要求 independent acceptance。

## 在决策点咨询

过程咨询是 `codex_advisor` MCP 服务器的 `process_consultation` 工具。primary、任一 worker 和任一 Explorer 都用 `{}` 调用它；它不接受数据包、摘要、提示词、路径或 dial。它自动携带调用者当前有效的上下文，包括未完成的当前轮次和压缩后的有效历史。Advisor 不使用工具，并返回且只返回一个 plan、correction 或 stop signal，同时给出宿主记录的模型与 effort。`stop` 是成功结果：按建议停止并升级。只有成功的终态结果才算作咨询。不支持的重建或失败的咨询会返回明确失败，绝不编造建议；工作保持待定，调用者在下一条可见回复中说明失败，不把它呈现为建议，也不宣称咨询已完成。

一次 complete consultation attempt 会返回一种允许的结果，以可支持的结论回答上下文中的决定。没有返回允许的结果，或来源与核验证据实质性推翻其结论时，该尝试失败。仅有分歧、中间工具错误或 worker 失败，不构成这种失败。

使用上下文中已有的所选咨询姿态块和 adoption 块。服务端自行选择 Advisor dial。任一块缺失或不适用时，阅读 routing profile 中的咨询映射和 [consult-posture.md](references/consult-posture.md)，比较调用者与 Advisor 的精确模型标识，并选择 full 或 reduced 姿态。严格遵循这两个块；没有钩子会自动阻止完成。Advisor 没有自己的升级路径。咨询不授予授权，也不能代替事实核对或 independent acceptance。
