# 01：宿主探测与咨询机制决定

**要构建的内容：** 记录在 `acceptance.md` §01 中的证据，它解决本规格其余部分所依赖的每一项宿主事实，加上写入规格 §Mechanism decision 的咨询机制决定。本工单不变更任何插件、文档、脚本或测试文件。

**Blocked by:** None（可以立即开始）。

**Status:** resolved

## 开始前必读

- `.scratch/tiers-and-advisor-consult/spec.md`：§Materials、§Authority and conflicts、TR-2、TR-3、AC-3、AC-4、AC-8、AC-9、AC-10、AC-11、AC-12、EN-5（最后一条）、X-1、X-2、§Mechanism decision、§Open Decisions（O4）、§Stop and Return（S1–S6、S9）、§Testing Decisions 第 6 项、§Further Notes（各项假设）。
- `.scratch/tiers-and-advisor-consult/sources.md` §2.4 行 D17、D20、D29、D31、D33、D34、D41、D42、D43、D44、D45。
- `plugins/codex-advisor/skills/orchestration/references/operations.md` §Install and discover（临时 `CODEX_HOME` 规程）以及 §Invoke and validate（派发形态、检查器用法）。
- `.scratch/tier-role-pool/acceptance.md` §Live route check（要复用的方法与记录形态）。
- `docs/adr/0004-tier-named-entries-first-round-pool.md` 第 29 行与第 47 行（优先级事实及其重新检查触发条件）。
- Codex 文档，现在重新阅读并记录阅读日期：Hooks <https://learn.chatgpt.com/docs/hooks>、App Server <https://learn.chatgpt.com/docs/app-server>、Subagents <https://learn.chatgpt.com/docs/agent-configuration/subagents>。
- 处于提交 `d74b1c99830a565f3df3f37e0a36616d17ffc574` 的 rpiv-advisor：`advisor/execute.ts` 与 `advisor/context.ts`，用于 "current effective context" 的含义（压缩之后的视图、进行中的调用已被去掉、用户角色的尾部）。

## 拥有

- `acceptance.md` §01（在那里创建这些表）。
- `spec.md` 的 §Mechanism decision 块：填写决定并设置它的状态行。不改变规格中的其他任何东西。如果一项发现与另一行规格矛盾，就停止（S8）。
- 一次性探测材料位于仓库之外的一个临时目录中，并在之后删除。

## 探测

按 X-2 在一个临时 `CODEX_HOME` 中运行每一次探测，父代理处于最便宜的设置，除非 X-2 另有说明。对每一次派发，记录命令形态、线程标识、来自 `inspect-agent-runtime.sh` 的观察到的模型与推理等级（对探测入口，通用模式即可），以及 Codex 版本。

1. **P1 宿主版本。** 记录 `codex --version` 与日期。
2. **P2 拨档可用性（TR-3、S1）。** 把 TR-3 中每一个不同的（模型、推理等级）各运行一次，并记录观察到的模型与推理等级：
   - `gpt-6-luna`：`high`、`xhigh`、`max`
   - `gpt-6-sol`：`medium`、`high`、`xhigh`、`max`
   - `gpt-6-astra`：`low`、`medium`、`high`、`xhigh`

   使用把 `fork_turns` 设为 `"none"` 的每次派发覆盖，或临时主目录中的临时探测模板。
3. **P3 本版本上的优先级（S2）。** 记录三种情形：
   - 一份固定 `model` 与 `model_reasoning_effort` 的探测模板，以相互冲突的每次派发值来派发。
   - 一份只固定 `model` 的模板，以每次派发的推理等级来派发。
   - 一次完整历史分叉（`fork_turns` 被省略或为 `"all"`）带有每次派发覆盖，以查看它继承什么。
4. **P4 咨询候选（AC-3、S3、S4）。** 测试你所尝试的每一种配置，并把每一种你没有尝试的配置记录为未测试。
   - **A：** 带有正整数 `fork_turns`（至少 `"1"` 以及一个更大的值）的原生派发，以及一份被固定的探测 advisor 模板。
   - **A'：** App Server 的 `thread/fork`（有与没有 `lastTurnId`），然后是带有模型覆盖的 `thread/resume`。
   - **B：** 一个 MCP 工具，它定位调用会话的记录、重建上下文，并以该 advisor 拨档且工具被禁用的方式调用 `codex exec`。

   停留在 D41 之内：任何配置都不得自行读取或发送凭据。对每一种配置，记录：
   - **（a）随机数。** 在一轮之内，一次工具调用打印一个随机值，然后咨询在同一轮中运行；advisor 必须重复该值。
   - **（b）模型与推理等级。** 实际的模型与推理等级等于 AC-4 拨档。
   - **（c）压缩。** 强制一次压缩，增加一条消息，然后咨询；advisor 必须同时看到摘要与后面的消息。
   - **（d）工具。** advisor 没有工具。展示 advisor 请求的实际工具集，按发送时或按宿主所记录的那样，并展示它是空的（D44）。一次被拒绝的工具尝试、一个不可用的工具，或 advisor 说它没有工具，都不算数；只读工具使这项检查失败。如果宿主对一种配置不暴露工具集的记录，该配置未经证明，并且没有资格。
   - **（e）调用者。** 咨询可以从主代理、从被派发的 worker、从被派发的 explorer 调用。
   - **（f）最早的上下文。** 在会话的第一轮陈述一条约束，然后增加比该配置所使用的任何窗口都多的、未被压缩的轮次，再咨询。advisor 必须报告该约束（D43）。对带有有界窗口的配置，还要记录使该窗口在每一种会话状态下都覆盖整个当前有效上下文的规则，而不仅是在这次测试中。
5. **P5 钩子（AC-8、AC-9、AC-10、AC-11、AC-12、S5、S6）。** 使用一次交付钩子的临时插件安装，经由 `plugin.json` 的 `hooks` 字段或 `hooks/hooks.json`，只按 X-2 路线安装（允许用检出的一次性副本来做探测钩子，以便没有仓库文件改变）。记录：
   - 每一次运行的信任状态：用户通过临时主目录中的 `/hooks` 予以信任、被绕过（仅当用户决定 O4 允许它时），或未受信任。一次没有记录信任状态的运行不是证据。
   - 未受信任的插件钩子：插件刚安装且没有任何东西受信任时，钩子被跳过，宿主打印它的 `/hooks` 警告。两者都要记录。
   - 插件钩子一旦受信任就会加载。
   - `SessionStart` 的输入字段；它的 `additionalContext` 在新会话中以及在恢复的会话中到达模型。
   - `SessionStart` 是否也在子代理会话中触发（EN-5）。
   - `SubagentStart` 的输入字段，以及子代理的模型与推理等级是否在场。
   - `SubagentStop` 的输入字段；`{"decision": "block", "reason": …}` 或退出码 2 是否使 worker 继续，以及是否存在防止循环的信号。
   - 派发工具的 `PostToolUse` 输入，以及它是否看到 `agent_type`、`reasoning_effort` 与子线程标识。
   - `SessionEnd` 是否存在，以便清理按会话的状态。

   需要受信任且正在运行的钩子的那些行，等到用户决定 O4，或通过临时主目录中的 `/hooks` 信任这些钩子。这样的等待行不阻塞工单 02，但它们必须在工单 05 开始之前被填上。决不要把一次未受信任的跳过算作 S5（规格 AC-12）。
6. **清理。** 删除临时主目录、凭据副本、工作区、探测模板以及日志。记录你已经这样做。

## 验收

- [x] `acceptance.md` §01 有 P1–P5 表。每一行都有观察到的值与线程标识，或者被标为未测试并附有理由。
- [x] 每一个 S1–S6 与 S9 条件都被标为 "not triggered" 并附有表明它的探测，或者被标为 "triggered" 并附有证据与一次停止。
- [x] 如果没有停止被触发，规格的 §Mechanism decision 点名所选配置及其五项检查与调用者证据，给出在有资格者当中选择它的理由，并且它的状态行已从 "pending ticket 01" 改为该日期以及 "decided" 这个词。
- [x] 文档阅读日期被记录在从每一页取得的事实旁边。
- [x] 与工单开始时所记录的状态相比（`git status --short` 的输出，加上任务目录中每一个文件的 SHA-256），本工单改变的仅有文件是 `acceptance.md` 与 `spec.md`，并且对已跟踪文件的 `git diff --stat` 为空。开始时已经未跟踪的文件保持原样：不要为了满足这项检查而提交、移动或删除它们（D45）。
- [x] 临时主目录与凭据副本已经不在。

## 停止条件

S1–S6 与 S9（规格 §Stop and Return）。在一次停止上，完成记录，把 §Mechanism decision 留为待定并附上理由，并向用户报告。不要开始工单 02。

## 不在本工单内

书写任何运行时文件、模板、脚本、测试、ADR 或 README；十三入口的路由检查（工单 03）。

## 评论

于 2026-09-26 解决。已勾选的条目记录本工单的验收
检查点；后续工单在有规定的地方延伸中间状态。
见 `../acceptance.md` 第 01 节，其中有命令、证据、已授权的
例外以及当前结果。最终交付评审另行记录。
