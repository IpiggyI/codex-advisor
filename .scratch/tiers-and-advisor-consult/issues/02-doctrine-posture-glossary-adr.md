# 02：原则、规范姿态文本、术语表以及 ADR-0006

**要构建的内容：** 加载该技能的主代理读到新的档位机制（准入、升级、失败计数）、咨询姿态与采纳规则，以及验收拨档规则。规范姿态文本只存在一次，位于一份新的参考中，后续工单逐字节复制它。术语表与 ADR-0006 与之匹配。每一份被触碰的 Markdown 文件的中文对照在同一次变更中更新。

**Blocked by:** 01（咨询措辞以及 ADR-0006 的机制小节需要它的机制决定；ADR-0006 的宿主事实来自它的探测）。

**Status:** resolved

## 开始前必读

- `spec.md`：§Authority and conflicts、TR-1、TR-4 到 TR-8、AC-1 到 AC-7、DR-1、DR-3、DR-4、DR-5（工单 02 的各小节）、DR-6、DR-7、AC-12（供 ADR-0006）、X-4、X-5（阶段范围说明）、§Decision Boundaries、§Goal-Drift Checks、§Mechanism decision（由 01 填写）。
- `sources.md` §2.4（全部行：被拒绝的行不得再次出现；被取代的行展示要避免的措辞）。
- `acceptance.md` §01（供 ADR-0006 的宿主事实）。
- 当前文件：`plugins/codex-advisor/skills/orchestration/SKILL.md`、`references/role-contracts.md`、`references/operations.md`（§Recover and hand off actual state、§Advice and independent acceptance）、`CONTEXT.md`、`docs/adr/0003-*.md`、`0004-*.md`、`0005-*.md`、`plugins/codex-advisor/skills/orchestration/agents/openai.yaml`。
- 处于 `d74b1c99` 的 rpiv-advisor：`advisor/register.ts`（`DEFAULT_PROMPT_GUIDELINES`，AC-7 所改写的文本）以及 `prompts/advisor-system.txt`（plan / correction / stop 契约）。
- `AGENTS.md` 一节 §Chinese mirror of runtime docs。

## 拥有

- `plugins/codex-advisor/skills/orchestration/SKILL.md`
- `plugins/codex-advisor/skills/orchestration/references/consult-posture.md`（新）
- `plugins/codex-advisor/skills/orchestration/references/role-contracts.md`
- `references/operations.md`，仅 §Recover and hand off actual state 与 §Advice and independent acceptance
- `plugins/codex-advisor/skills/orchestration/agents/openai.yaml`，仅当它的文本点名一个已退役概念时
- `CONTEXT.md`
- `docs/adr/0006-*.md`（新）
- 上面每一份 Markdown 文件的 `docs/zh/` 对照

不是路由配置：工单 03 拥有它，以便验证器的配置到模板检查保持一致。

## 所确立与所消费

- **所确立** DR-3：规范姿态文本。工单 04（EN-5）、05（AC-8）与 06 复制或阅读它，并且不得改写它。
- **所确立** TR-1、TR-4 到 TR-8、AC-1 到 AC-6、DR-1、DR-4、DR-6、DR-7 的原则文本。
- **所消费** 工单 01 的机制决定。

## 验收

- [x] `SKILL.md` 覆盖：
  - [x] 准入：默认 `mainstay`；当识别出一项关键困难或相互影响的约束时，第一轮使用 `crux`；没有配额；没有用户声明时，`rescue` 从不在第一轮使用。
  - [x] 升级：下一档位，没有同一档位内的模型切换，有一个模型级下限，并且当模型保持不变时使用更高的推理等级。
  - [x] 失败计数以及通向用户的路径，R3 保留，按 TR-8。
  - [x] 按 AC-3 的咨询，姿态与采纳规则指向 `consult-posture.md`。
  - [x] 按 AC-1 与 AC-2 的验收，包括低置信度规则。
  - [x] 没有 first-round pool、senior gate、decision packet、"Proactive advice is allowed"、模型名称或推理等级值。
  - [x] 完整尝试、新线程、Architect 模式以及验收所有权的文本在含义上未改变。
- [x] `consult-posture.md` 有三个带定界的块：完整变体、精简变体以及采纳规则。文本遵循 AC-5 到 AC-7，带有祈使触发条件，没有 "commit" 步骤，有调用之前必须持久化的规则、在下一次回复中重述的规则，以及调和调用；AC-6 是完整的。它陈述 AC-5 身份规则以及 `gpt-5.6-terra` 示例，而不把一份家族列表写死。
- [x] `role-contracts.md` 保留 explorer 与 worker 数据包，保留带有 AC-2 拨档规则与低置信度规则的验收数据包，移除决策数据包，并说明咨询不使用数据包。
- [x] `operations.md` 的 §Recover and hand off actual state 与 §Advice and independent acceptance 描述 TR-7/TR-8 与 AC-1/AC-2；这些小节中不再留下 senior 门禁或决策数据包。
- [x] `CONTEXT.md` 按 DR-6 变更。
- [x] ADR-0006 记录本规格的决定，通过引用列出 ADR-0003、ADR-0004 与 ADR-0005 每一句被取代的句子，记录工单 01 的机制决定与宿主事实并附有失效检查，把 AC-12 的 `/hooks` 评审记录为 ADR-0004 只允许安装这条规则所不能去掉的那一个用户步骤，并把 grok 通道移到 `0.4.0`。
- [x] 对照被重新翻译。标识符、入口名称、拨档记法以及姿态块定界符保持逐字符精确。

## 验证

- `python3 tests/test_zh_mirror.py` 通过。
- `sh plugins/codex-advisor/scripts/verify.sh` 通过。它在这些文档之中只读取路由配置，而本工单不触碰路由配置，因此这里的失败意味着一处意外的耦合。报告它，而不是绕过它。
- 文本搜索，限于本工单所拥有的文件（D45）：`SKILL.md`、`consult-posture.md`、`role-contracts.md`、`operations.md` 中所拥有的两个小节、被触碰时的 `openai.yaml`，以及它们的对照，外加 `CONTEXT.md`，但其 `_Avoid_` 行除外，DR-6 要求那些行点名已退役术语。ADR-0006 被排除，因为它引用被取代的文本。路由配置、`operations.md` 的其余部分、模板、脚本、README 以及 `plugin.json` 仍然持有旧术语，由工单 03 与 06 变更；这里不搜索它们。
  - 该范围内没有这些：`first-round pool`、`senior gate`、`decision packet`、`DECISION packet`、`Proactive advice is allowed`，或作为档位名称使用的 `light`/`standard`/`senior`。
  - 不在 `SKILL.md` 或其对照中：任何 `gpt-` 字符串，或形式为 `name[effort…]` 的任何拨档记法。

  记录这些命令及其输出。
- `git diff --check`。

## 停止条件

S8。如果工单 01 的决定仍然待定，也要停止。

## 不在本工单内

路由配置、模板、安装器、检查器、咨询组件、钩子、README 以及版本说明书。

## 评论

于 2026-09-26 解决。已勾选的条目记录本工单的验收
检查点；后续工单在有规定的地方延伸中间状态。
见 `../acceptance.md` 第 02 节，其中有命令、证据、已授权的
例外以及当前结果。最终交付评审另行记录。
