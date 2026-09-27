# 验收记录：mainstay/crux/rescue 档位与过程咨询（0.3.0）

每一项探测、实况检查、视觉比较，以及针对 [spec.md](spec.md) 的最终扫尾，都由拥有它的工单记录在这里。某一节在其工单填写它之前保持 `pending`。记录 Codex 版本、日期、命令、观察到的值、线程 ID，以及每一项结果所不能确立的内容。

## 01 宿主探测与机制裁定

Status: 于 2026-09-26 完成。B′ 通过下面的资格检查；S3 与 S4 已被清除。P7 完成用户信任的执行以及不受信任的警告/跳过证据，并且全部临时环境已被移除。下面最初被阻塞的结果作为特定配置的历史被保留，并在被说明的地方由 P6/P7 取代。产品实现与验收保持分开。

### P1 环境、来源与范围

主代理在 WSL 上使用 `codex-cli 0.157.0` 执行了这些探测，开始于 `2026-09-26T01:09:45+08:00`。仓库 HEAD 是 `main` 上的 `f812f9b64c0fb4aa4d45f9a6ae8102c451ab367b`。起始状态恰好是：

```text
?? .agent-discuss/
?? .scratch/tiers-and-advisor-consult/
```

任务目录的 SHA-256 基线是在任何任务文件编辑之前捕获的。本表中的路径相对于本任务目录：

| 文件 | SHA-256 |
|---|---|
| `acceptance.md` | `ad450c358a93c1f80b97845a8a49d91a1d6626e828458a3b024eb43818f67efa` |
| `handoff-review.md` | `46069f0ae81ee5a2c2ccac88bd7121cadd4b2c4ccdcac31fa72c30a915f55890` |
| `issues/01-host-probes-and-mechanism.md` | `b79a277d9815161387c3a13c33c142898bfbbf0ce364c8d5be0d3ef26befd89c` |
| `issues/02-doctrine-posture-glossary-adr.md` | `31d1cd12f04cb299618d529d2bac8c40691a776ad9e6901ca186faac96320156` |
| `issues/03-profile-entries-installer-inspector.md` | `829ee7c8249d3bfbaffb897c39c740b48eab83d2d74d9a683ccbce560f0f3c58` |
| `issues/04-process-consultation.md` | `bbd409ee8b3ce333372f9e0ce2cbbe8c14142413605892ca316658a6e83943d8` |
| `issues/05-plugin-hooks.md` | `c3c89336f9131f25d186c8e3e3ab4e35bd68153a2e4215f5276bb51952a66390` |
| `issues/06-readme-manual-release.md` | `612aa3e11bc9c21cdb9541cb5e96752fc6f6e204cf6bd5a186175d77f54961af` |
| `sources.md` | `51466c306f7666e973f14e4734ca97f0cdf130591fd069c0253f8e97f0802226` |
| `spec.md` | `35bad6333d963baffef313f5f7509cd974079bb2010091246c0386212cba5939` |

阅读了已安装的 0.2.0 编排技能、当前操作、路由配置与角色契约；ADR-0004；先前的路由检查方法；当前规格与工单 01；以及必需的裁定账本行。参考仓库仍位于 `d74b1c99830a565f3df3f37e0a36616d17ffc574`。其 `advisor/execute.ts:117` 在调用时重建当前分支，并且 `:153` 发送 `tools: []`；`advisor/context.ts` 移除进行中的咨询调用，并提供一个用户角色尾部。这些是参考语义，并不是 Codex 支持的证据。

官方来源已在 2026-09-26 成功获取并阅读：

| 来源 | 使用的事实 | 限度 |
|---|---|---|
| [钩子](https://learn.chatgpt.com/docs/hooks) | 插件钩子发现、基于哈希的 `/hooks` 信任、上下文注入、子代理事件，以及 `SessionEnd`。 | 文档并不是一次已信任钩子的执行结果。 |
| [App Server](https://learn.chatgpt.com/docs/app-server) | 进行中的 `lastTurnId` 会被拒绝；省略它会以一个中断标记进行分叉。 | 仅该标记并不能确立一个已完成的工具结果是否到达下一次模型请求。 |
| [子代理](https://learn.chatgpt.com/docs/agent-configuration/subagents) | 模板的模型/推理等级优先级；当模板只钉选其模型时的调用方推理等级。 | 账户可用性在 P2 中另行检查。 |
| [配置参考](https://learn.chatgpt.com/docs/config-file/config-reference) 与 [配置 schema](https://developers.openai.com/codex/config-schema.json) | 工具开关以及 `features.tool_registry.turn_metadata_includes_tool_info`。 | 获取到的配置 schema 是一份官方快照，并不能证明所有设置都会影响该宿主所暴露的工具。 |

确切的已安装 App Server 协议 schema 由 `codex app-server generate-json-schema --experimental --out <temporary>/schema` 生成。检查了它的 start/fork/resume/turn schema。没有从那些 schema 或检查过的运行时记录中取得实际的空模型请求工具清单。

### 临时安装与命令形态

全部模型探测都使用 `/tmp` 之外、`/home/hyy/ca-tier-probe-ou6tpics/` 之下的一次性主目录。只使用了必需的认证/配置副本。复制的配置保留了连接/提供方与插件设置；无关的 MCP 服务器、用户钩子、项目设置以及记忆使用被排除。父请求使用 `gpt-6-astra[low]`。没有任何探测更改用户的安装、信任状态、市场或仓库运行时文件。

工作区检出通过必需路线成功安装：

```sh
CODEX_HOME=<temporary-home> codex plugin marketplace add /home/hyy/develop/personal/GitHub/codex-advisor
CODEX_HOME=<temporary-home> codex plugin add codex-advisor@codex-advisor
sh <temporary-home>/plugins/cache/codex-advisor/codex-advisor/0.2.0/scripts/install-agents.sh --target-dir <temporary-home>/agents
```

三条命令全部以退出码 0 结束。已安装的插件根位于临时主目录之下；全部十一个现有模板与安装器清单匹配。额外的 `probe_pinned`、`probe_model` 与 `probe_consult` 入口是在该主目录中新建的一次性模板；随附的已安装入口没有被手工编辑。

P2/P3/原生 P4 的父命令是 `CODEX_HOME=<temporary-home> codex exec -C <temporary-workspace> --skip-git-repo-check --json -m gpt-6-astra -c 'model_reasoning_effort="low"' -`，有界探测提示位于 stdin。每个 P2 子项使用 `agent_type=default`、显式 `model`、显式 `reasoning_effort` 与 `fork_turns=none`，并在没有工具或进一步委派的情况下返回 `PROBE_OK`。子项按顺序运行。通用检查使用 `sh plugins/codex-advisor/scripts/inspect-agent-runtime.sh --sessions-dir <temporary-home>/sessions <child-UUID>`。

### P2 拨档可用性

下面请求的值与观察到的值一致。每一行都有已完成的子项响应，且检查器退出码为 0。观察到的全部子项工作目录都是临时工作区；观察到的沙箱/权限元数据是 `read-only` / `managed`。这并不能独立确立硬隔离、模型质量、成本或稳定性。

| 请求的模型 | 请求的推理等级 | 观察到的模型 | 观察到的推理等级 | 子线程 | 检查器 |
|---|---|---|---|---|---|
| `gpt-6-luna` | `high` | `gpt-6-luna` | `high` | `01a0d98d-31ac-7de3-9880-f640aee31e7e` | 0 |
| `gpt-6-luna` | `xhigh` | `gpt-6-luna` | `xhigh` | `01a0d98e-297b-7931-bf8a-a6be0bb3c1ae` | 0 |
| `gpt-6-luna` | `max` | `gpt-6-luna` | `max` | `01a0d98e-56f3-73e3-a7d5-ec00bfb843ce` | 0 |
| `gpt-6-sol` | `medium` | `gpt-6-sol` | `medium` | `01a0d98e-7f9a-7771-b8ca-691e992a6990` | 0 |
| `gpt-6-sol` | `high` | `gpt-6-sol` | `high` | `01a0d98e-adce-7842-8bbf-91fb586f10fa` | 0 |
| `gpt-6-sol` | `xhigh` | `gpt-6-sol` | `xhigh` | `01a0d98e-ccbd-7413-a6f9-3e026b55c581` | 0 |
| `gpt-6-sol` | `max` | `gpt-6-sol` | `max` | `01a0d98e-f3ca-7810-b67e-c8c4cf0f2ab9` | 0 |
| `gpt-6-astra` | `low` | `gpt-6-astra` | `low` | `01a0d98f-2350-72d0-a0e2-c95d0008fdff` | 0 |
| `gpt-6-astra` | `medium` | `gpt-6-astra` | `medium` | `01a0d98f-4c35-7350-810f-8221e99c80d2` | 0 |
| `gpt-6-astra` | `high` | `gpt-6-astra` | `high` | `01a0d98f-73d5-7f60-873e-9ea5fe9b4fe5` | 0 |
| `gpt-6-astra` | `xhigh` | `gpt-6-astra` | `xhigh` | `01a0d98f-9edc-7a31-bd92-7021aacdd049` | 0 |

第一行的父项是 `01a0d98d-19ab-7cf1-8b81-5eafdffd762e`；其余十个共享父项 `01a0d98e-09fe-7c51-b898-5d15a744afea`。对每一个子项都检查了父项关联。

### P3 优先级

父项：`01a0d990-b7d0-72e1-b579-0f8cc8818e6c`，运行 `gpt-6-astra[low]`。三个子项全部以 `PROBE_OK` 完成。

| 情形 | 模板 | 派发参数 | 观察到的元数据 | 子项 | 检查器 / 裁定 |
|---|---|---|---|---|---|
| 钉选冲突 | `probe_pinned`：`gpt-6-luna[high]` | `model=gpt-6-sol`，`reasoning_effort=medium`，`fork_turns=none` | `gpt-6-luna[high]` | `01a0d990-cf01-7763-870b-98e94738e6e8` | 退出码 0；两处模板钉选都胜出。 |
| 调用方推理等级 | `probe_model`：`gpt-6-sol`，推理等级被省略 | `reasoning_effort=xhigh`，`fork_turns=none` | `gpt-6-sol[xhigh]` | `01a0d990-ef04-75f2-8a7b-319126b95b55` | 退出码 0；模板模型与调用方推理等级均保持。 |
| 完整历史覆盖 | 内置 `default`，没有模板钉选 | `model=gpt-6-luna`，`reasoning_effort=high`，`fork_turns=all` | 继承的 `turn_context` 位于 `gpt-6-astra[low]`，随后子上下文位于 `gpt-6-luna[high]` | `01a0d991-1420-7c72-b96a-82abb5637b04` | 退出码 1：路由证据相互冲突。该调用已被接受，但当前检查器并不为这一混合历史情形出具认证。 |

完整历史观察不同于 ADR-0004 先前对覆盖的叙述。它并不能确立模板优先级的丧失：两个模板情形通过了，而完整历史情形没有钉选。S2 没有被已测试的钉选情形触发。工单 01 中没有做检查器更改。未来使用完整历史分叉的机制，在声称已认证路由之前，必须解决这一证据边界。

### P4 咨询配置

每一项配置都必须通过每一项资格检查以及全部三条调用方路线。一个失败或未经证明的单元格会使该配置不具备资格。前提已失败的测试没有被扩展，以避免在一项已经缺乏资格的配置上消耗配额。

| 配置 | 未完成回合 nonce | 实际拨档 | 压缩 | 实际的空请求工具集 | 最早有效上下文 | 主代理 / worker / explorer | 结果 |
|---|---|---|---|---|---|---|---|
| A1：钉选 `probe_consult`，`fork_turns=1` | 失败：子项报告 nonce 不存在；其会话记录中不存在 nonce。 | `gpt-6-astra[low]`，检查器 0。 | nonce 失败后未经测试。 | 未经证明；没有取得实际请求清单。 | 未经测试；没有规则证明一个固定的一轮窗口覆盖每一个有效上下文。 | 主代理已测试；worker/explorer 未经测试。 | 不具备资格。 |
| A8：同一模板，`fork_turns=8` | 失败：子项报告 nonce 不存在；其会话记录中不存在 nonce。 | `gpt-6-astra[low]`，检查器 0。 | nonce 失败后未经测试。 | 未经证明；没有取得实际请求清单。 | 未经测试；没有规则证明一个固定的八轮窗口覆盖每一个有效上下文。 | 主代理已测试；worker/explorer 未经测试。 | 不具备资格。 |
| 带有进行中 `lastTurnId` 的 A' | 在 Advisor 执行之前分叉被拒绝。 | 没有 Advisor 请求。 | 拒绝之后未经测试。 | 拒绝之后未经测试。 | 拒绝之后未经测试。 | 主代理请求已测试；委派对象未经测试。 | 不具备资格。 |
| 没有 `lastTurnId` 的 A'，随后恢复并回合 | 存储的分叉包含已完成的 nonce 输出，但恢复后的模型回答 `MISSING`。 | 恢复选择了 `gpt-6-astra`；后续回合显式请求 `low`，且回合上下文与之匹配。 | nonce 失败后未经测试。 | 未经证明；一条已存储的动态工具定义并不是空的请求工具集。 | nonce 失败后未经测试。 | 主代理已测试；委派对象未经测试。 | 不具备资格。 |
| B1 执行器前提：`codex exec` 使用下面的第一组工具禁用配置 | 上下文重建未实现。 | 回合上下文中的 `gpt-6-astra[low]`。 | 未经测试。 | 失败：实际的 `exec` 自定义工具调用成功返回了时钟结果。 | 未经测试。 | 仅直接执行器；零参数 MCP 调用方路线未经测试。 | 该执行器配置不具备资格。 |
| B2 执行器前提：扩展的禁用配置加上请求工具元数据标志 | 上下文重建未实现。 | 回合上下文中的 `gpt-6-astra[low]`。 | 未经测试。 | 未经证明：`exec` 返回 `code-mode host is disabled`；没有取得实际的空请求清单。一次被拒绝的调用在 D44 下不构成证明。 | 未经测试。 | 仅直接执行器；零参数 MCP 调用方路线未经测试。 | 没有建立资格。 |

原生 P4 使用 P3 的父项。一次 shell 调用生成了 `9b589de4d990476b0114f442f0a77bb2`，并且父项在同一次未完成的回合期间派发了每一个候选，而没有把 nonce 放进子项消息。A1 子项：`01a0d991-45ea-7a70-91c0-4bcf393d0490`；A8 子项：`01a0d991-7641-72a3-b6ea-68eb961f0723`。

App Server 在同一个临时主目录中通过 stdio 上的 JSON-RPC 使用。`thread/start` 提供了两个夹具动态工具；来源调用了 `probe_nonce`，收到一个随机结果，然后保持挂起在 `probe_hold`。来源线程：`01a0d992-8350-7333-bb40-4fbcd9306dad`。活动回合：`01a0d992-83ab-7933-9eff-f8cde154c322`。带有该 `lastTurnId` 的 `thread/fork` 返回错误 `-32600`：`lastTurnId '01a0d992-83ab-7933-9eff-f8cde154c322' identifies an in-progress turn`。省略该参数创建了 `01a0d992-9699-70e1-a066-660583a805d7`，带有一个被中断的回合以及已完成的 nonce 工具条目。`thread/resume` 与一次新的 `turn/start` 询问继承的 nonce，且没有提供它；回答是 `MISSING`。来源回合在停止服务器之前被释放并中断。不从存储的分叉内容推断任何面向模型的完整性声称。

B1 线程：`01a0d995-087a-75d0-aa94-2f068127bcd6`。配置覆盖是 `features.shell_tool=false`、`features.apply_patch_freeform=false`、`features.view_image=false`、`features.goals=false`、`features.request_permissions_tool=false`、`features.default_mode_request_user_input=false`、`features.image_generation=false`、`features.apps=false`、`agents.enabled=false`、`tools.update_plan.enabled=false`、`tools.experimental_request_user_input.enabled=false`，以及 `web_search="disabled"`。它的会话记录包含已完成的、名为 `exec` 的 `custom_tool_call`，输入 `text(await tools.clock__curr_time({}));`，以及带有 `current_time="2026-09-25 17:20:22 UTC"` 的匹配工具输出。这是实际成功的工具执行，而不是一份可用性自我报告。

B2 线程：`01a0d998-b0a8-73f1-86b4-5691c8070cb2`。它增加了 `features.code_mode=false`、`features.code_mode_host=false`、`features.code_mode_only=false`、`features.sleep_tool=false`、`features.current_time_reminder=false`、`features.browser_use=false`、`features.computer_use=false`、`features.tool_suggest=false`，以及 `features.tool_registry.turn_metadata_includes_tool_info=true`。请求工具标志在获取到的 schema 中被描述为：在每个回合的请求元数据中包含权威工具信息。它没有在检查过的会话记录或 CLI 输出中暴露一份实际请求清单。同一次自定义工具调用收到 `code-mode host is disabled`；该拒绝被有意不归类为空工具集，也不归类为一次成功的工具调用。

其他原生窗口值、带有钉选 Advisor 设置的完整历史咨询、替代的 App Server 配置、强制压缩、长会话的最早上下文情形、MCP 会话发现/重建，以及来自 worker/explorer 的咨询，仍然未经测试。没有确立有界窗口完整性规则或空工具配置。这些缺口并不能成为用数据包、带工具的 Advisor 或另一张模型表来替代的理由。

### 裁定建议

在得出 S3 结论之前，主代理使用已安装的 `ca_advisor_standard`、全新上下文、钉选的 `gpt-6-astra[medium]`，请求了一次只读的裁定咨询。父项：`01a0d996-7299-7c33-8a8b-ce0a80c482c9`；Advisor：`01a0d996-b595-7a73-bf41-a6de466fb605`。角色感知检查器退出码为 0。Advisor 把工具元数据标志以及剩余的 code-mode 开关识别为一次廉价的附加探测；主代理运行了 B2。Advisor 还区分了模板优先级与混合历史检查器失败。这是裁定建议，而不是独立的交付验收。

### P5 钩子与信任边界

已跟踪检出文件的一份一次性副本只在其插件下增加了一个夹具 `hooks/hooks.json` 与一条夹具命令。该命令会在一次性探测目录内记录其事件，并注入 `HOOK_CONTEXT_62417`。第二个临时主目录通过本地市场路线安装了该副本。第一次市场添加尝试失败，因为复制的配置保留了原始市场路径；在临时主目录中移除该注册并添加一次性副本后，问题得到解决。`codex plugin list --json` 随后报告该副本已安装且已启用。在该修正之前的一次介于其间的运行被排除在钩子证据之外。

| 能力 / 已记录的事实 | 信任状态 | 观察到的结果 | 证据 / 剩余检查 |
|---|---|---|---|
| 全新的插件钩子需要 `/hooks` 信任，并在带有警告的情况下被跳过。 | 不受信任；没有创建信任记录，也没有使用绕过。 | 夹具没有运行。在捕获的 `codex exec` 输出或检查过的会话记录中没有观察到 `/hooks` 警告；因此完整的跳过并警告要求未经验证。 | 线程 `01a0d995-03cb-7250-8bf1-ca2e7a4f7c8e`；没有夹具输出文件。 |
| 交互式信任/警告界面 | 不受信任 | CLI 停在其文件夹信任关卡。主代理在未信任该文件夹或钩子的情况下退出。 | 该次尝试没有模型请求或已信任钩子的证据。 |
| 在已授权的临时绕过下执行插件钩子 | 在用户回复之后，按 O4(a) 绕过。 | 通过：夹具已运行，且主代理报告了其注入的 `HOOK_CONTEXT_62417`。 | 线程 `01a0d99f-4d47-76b3-8124-5fb7ec7e25f6`。宿主发出了其绕过警告。这不能代替一次由用户信任的运行。 |
| `SessionStart` 输入与新会话注入 | 按 O4(a) 绕过。 | 捕获了 `session_id`、`transcript_path`、`cwd`、`hook_event_name`、`model`、`permission_mode`、`source`；`source=startup`。注入的标记到达了主代理。 | 最初的探测以及下面的多事件探测。 |
| 已恢复会话的注入 | 按 O4(a) 绕过。 | 观察到钩子以 `source=resume` 被调用。下面记录了一次单独的不同标记检查。 | 父项 `01a0d9a1-0ecb-7473-8dc7-cf8dd765793a`。 |
| 子代理中的 `SessionStart` | 按 O4(a) 绕过。 | 在两条已测试的原生子路线中都没有观察到子项 `SessionStart` 事件；两者都发出了 `SubagentStart`。 | 仅为限定范围的观察；其他入口与派发配置仍然未经测试。 |
| `SubagentStart` 字段以及模型/推理等级可见性 | 按 O4(a) 绕过。 | 捕获了 `session_id`、`turn_id`、`transcript_path`、`cwd`、`hook_event_name`、`model`、`permission_mode`、`agent_id`、`agent_type`。`model` 在模型不同的情形中识别出了子项。不存在推理等级字段。 | Luna 子项在 Astra 父项下发出了 `model=gpt-6-luna`。 |
| `SubagentStop` 阻止与循环预防 | 按 O4(a) 绕过。 | `decision=block` 使每个 worker 继续、调用时钟，并以 `PROBE_CONTINUED` 结束。第一次停止的 `stop_hook_active=false`；第二次为 `true`。 | 捕获了 `agent_transcript_path`、`agent_id`、`agent_type`、`last_assistant_message`，以及共同/回合字段。退出码 2 的阻止未经测试。 |
| 派发 `PostToolUse` 的输入与响应 | 按 O4(a) 绕过。 | 实际工具名称是 `collaborationspawn_agent`；输入包含 `agent_type`、`task_name`、`fork_turns`，以及在调用方推理等级情形中被显式传入的 `reasoning_effort`。响应包含规范任务路径，而不是子 UUID。 | 子 UUID 可在 `SubagentStart` 中取得。连接事件与自动比较既未实现也未被验收；S6 仍然未确定。 |
| `SessionEnd` | 按 O4(a) 绕过。 | 主线程事件以 `reason=other` 触发；字段是 `session_id`、`transcript_path`、`cwd`、`hook_event_name`、`reason`。 | 这证明事件可用，并不能证明未来组件的完整状态清理行为。 |
| 用户通过 `/hooks` 信任的钩子运行 | 尚未被用户信任。 | 待定。 | O4(a) 保留这一必需的人工关卡。 |

用户在 2026-09-26 通过结构化回复解决了 O3 与 O4。O3(a) 只把一次成功的咨询计算在内；失败仍然阻塞一次，并使该工作在成功或用户放行之前保持待定。O4(a) 只允许在临时主目录的实况检查中使用信任绕过，保留一次由用户通过 `/hooks` 信任的运行，并保留不受信任的跳过并警告情形。这些明确裁定授权对规格的 AC-12/Open Decisions 文本以及 `sources.md` 第 2.5 节做相应更新，超出了工单 01 原来的两文件证据范围。它们并不豁免 S3。没有使用已信任状态编辑或主代理停止钩子。

在该授权之后，夹具扩展到 `SessionStart`、`SubagentStart`、`SubagentStop`、`PostToolUse` 与 `SessionEnd`。每一次夹具变更都通过临时本地市场移除并重新添加插件来暴露，而从不通过编辑其已安装副本。命令使用 P2 父项形态加上 `--dangerously-bypass-hook-trust`。多事件父项是 `01a0d9a1-0ecb-7473-8dc7-cf8dd765793a`；它的 `ca_worker_standard_h` 子项是 `01a0d9a1-2dc6-71b3-8ace-6991282d0698`，观察到位于 `gpt-6-astra[low]`，角色感知检查器退出码为 0。第二个父项 `01a0d9a2-7b22-76e0-b546-9af77c98d85d` 派发了一个新建的一次性 `ca_worker_probe` 模板，该模板钉选 `gpt-6-luna`，但把推理等级留给调用方。显式 `reasoning_effort=high` 产生子项 `01a0d9a2-8f95-7d91-8c26-995a0c36d623`，观察到位于 `gpt-6-luna[high]`，通用检查器退出码为 0。夹具对每个子项 ID 阻止一次；它没有实现产品文件变更或咨询检测。

第一次恢复复用了启动标记，该标记本身并不能证明全新上下文的送达。不同标记探测把临时夹具改为只在 `source=resume` 时注入一个新值，重新安装了该副本，并恢复了现有父项，且没有把该标记的值放进提示。模型返回了新注入的 `HOOK_RESUMED_99031`；命令退出码为 0。这确立了该绕过路线的已恢复注入。

### 停止条件与交接

| 条件 | 状态 | 证据 |
|---|---|---|
| S1 | 对全部十一个必需拨档均未触发。 | P2：全部完成；实际模型/推理等级匹配；全部检查器退出码为 0。 |
| S2 | 在已测试的钉选/调用方推理等级情形中未触发。 | P3。完整历史检查仍然未经认证，并且不被推广到模板优先级。 |
| S3 | 已触发：没有建立具备资格的配置。 | P4。保持该机制为待定；不要启动工单 02。 |
| S4 | 未确定。 | 尚不存在其 worker/explorer 路线可以被验收的具备资格的机制。 |
| S5 | 在已测试的绕过运行中未触发；用户信任路线待定。 | 插件加载、主代理注入以及 JSON 停止阻止在 O4(a) 下有效。不受信任的跳过并不是一次失败。 |
| S6 | 未确定。 | 按每次派发的自动钩子路线未经测试。 |
| S9 | 对当前插件/入口以及钩子夹具未触发。 | 本地安装与更新后的钩子执行成功。用户信任的执行以及未来的咨询组件仍然未经验证。 |

工单 01 在 S3 已触发且钩子行仍然待定时，不能满足其全部清除的验收。产品实现、类型检查、产品测试、版本变更、最终独立验收、提交、推送以及真实主目录更新都没有执行。本项目没有带类型的应用程序；本工单只产生了证据。`implement` 的最终产品测试/评审/提交步骤仍然与被阻塞的实现一起待定。

范围验证由主代理在 2026-09-26 完成。探测工作只更改 `acceptance.md` 第 01 节以及 `spec.md` 的机制状态。随后的明确用户裁定还更改规格的 AC-12/Open Decisions 文本以及 `sources.md` 第 2.5 节。哈希比较确认其余七个任务文件未更改，并且没有新的任务文件。只回退已授权的账本编辑后，复现了它原来的 SHA-256；在计入机制状态以及明确的 O3/O4 裁定之后，规格与其原始快照匹配。验收第 02 节直至最终一节保持未更改。主代理把全部十一行 P2 与已完成的子项元数据匹配，并检查了两份原生分叉 nonce 记录以及不同的恢复结果。这些检查验证该记录及其范围；它们并不验收一项产品实现。

`git diff --check` 退出码为 0，已跟踪的 `git diff --stat` 为空，并且 `git status --short` 仍然与两个起始未跟踪目录匹配。一次直接的空白/分节检查覆盖了未跟踪的 Markdown 文件，而 Git 的空已跟踪差异不能验证这些文件。本证据文档没有专用解析器或 schema；产品测试与实现代码评审仍然与工单 02–06 一起待定。

清理在 2026-09-26 完成并得到验证。没有剩余的、绑定到该临时目录的 Codex 进程。两个一次性主目录、复制的凭据、缓存的插件、工作区、探测模板/脚本、下载的 schema/文档、钩子状态、原始日志，以及临时目录指针都被删除。`/home/hyy/ca-tier-probe-ou6tpics/` 不再存在。上面的表保留非机密发现与线程 ID；它们底层的临时会话记录被有意不再提供。下一次执行必须在启动依赖实现之前，就 S3 取得用户指示。用户信任的钩子运行以及不受信任警告证据也仍然待定。

### P6 已授权的延续与选定机制

用户在 2026-09-26 明确授权继续调查：“没看到结构化选项；授权继续”。这重新打开了调查，且没有削弱 AC-3。全部延续探测使用 `codex-cli 0.157.0`，以及 `/home/hyy/ca-consult-reprobe-pfgxoqcr/` 之下的一次性主目录。仓库 HEAD 与起始 Git 状态未更改。一份新的 SHA-256 基线覆盖全部十个任务文件。保留了本地市场路线、每次夹具变更之后的移除/添加，以及配套安装器。真实安装与其信任状态都没有被更改。

#### 空工具与自动调用方身份

官方配置参考/schema 以及 App Server 文档已在 2026-09-26 获取。该 schema 把 `model_catalog_json` 描述为进程启动设置，而不是按线程的覆盖。`codex debug models --bundled` 暴露了默认模型的实验性时钟工具，这解释了为什么更早的功能开关单独使用是不够的。一份保留确切模型 ID、但把 `shell_type="disabled"`、`apply_patch_tool_type=null`、`experimental_supported_tools=[]`、`supports_search_tool=false` 以及工具使用指令标志设为 false 的启动目录，与常规工具功能开关结合后，产生了一份实际的空清单。尝试加入的 `tool_mode` 目录字段并不存在于已加载的目录中，并且不是该机制的一部分。

额外的功能开关是 `shell_tool`、`view_image`、`goals`、`request_permissions_tool`、`default_mode_request_user_input`、`image_generation`、`apps`、`code_mode`、`code_mode_host`、`code_mode_only`、`sleep_tool`、`current_time_reminder`、`browser_use`、`computer_use`、`tool_suggest`、`multi_agent_v2` 与 `plugins`，全部为 false；`agents.enabled`、`tools.update_plan.enabled` 与 `tools.experimental_request_user_input.enabled` 为 false，并且 `web_search` 为 `disabled`。这些设置是被一起认定为合格的，而不是被逐个认证的禁用开关。

宿主的 `CODEX_ROLLOUT_TRACE_ROOT` 通过 `inference_started.request_payload.path` 记录实际推理请求体。一个本地未认证的 HTTP 夹具首先确认，捕获的载荷是请求体，而不是传输认证头。已认证的空工具探测，线程 `01a0d9af-e0bd-7562-b0e7-e83b4a7606c6`，随后在实际 `gpt-6-astra[low]` 返回 `PROBE_OK`，带有 `additional_tools.tools=[]`，并且没有顶层工具。这是宿主请求证据，而不是 Advisor 的自我报告。该组件调用原生 Codex 认证；它从不读取、复制或传输凭据。只有测试准备复制了必要的认证配置。

零参数 MCP 调用方识别在线程 `01a0d9b5-5305-7980-a4eb-c5a22b523a81` 中成功。宿主 `tools/call.params._meta` 提供了 `threadId`、`sessionId`、`itemId`，以及包含线程、回合、模型与推理等级的 `x-codex-turn-metadata`。MCP 进程没有收到 `CODEX_HOME`、`CODEX_THREAD_ID`、`CODEX_SESSION_ID` 或 `PLUGIN_ROOT`；那些环境变量并不是发现契约。在一次没有注解的调用于审批策略 `never` 下被拒绝之后，该探测使用了准确的只读/非破坏性注解。

#### 配置比较与裁定

一次 A′ 修订在活动回合之前分叉（`ephemeral=true`，`excludeTurns=true`），然后使用 `thread/inject_items` 追加当前回合的原始响应条目。官方 App Server 文档明确说明，该方法把预先构建的 Responses API 条目追加到模型可见的历史。来源 `01a0d9bd-6013-7b01-b15f-d86c8e44c571` 与 Advisor `01a0d9bd-b483-7f83-ab92-d944216c8049` 通过了 nonce 与空工具检查。一个十二回合序列以及手动压缩也通过了。然而，一个活动回合内部的自动压缩暴露了一个真实失败：来源 `01a0d9c1-9429-7171-98f8-312810a4417b` 有七个有效输入条目，而 Advisor `01a0d9c1-e32b-7e82-951c-94a19bda5203` 只保留了其中六个，省略了新的摘要，并恢复了已被移除的大工具结果。仅 nonce 仍然通过。这一 A′ 修订不具备资格。

选定 **B′：零参数 MCP、单次快照的有效历史重建，以及原生 App Server 结构化注入**。它扩展候选 B，使用 `thread/start` 加上 `thread/inject_items`，而不是把上下文压平进一条 `codex exec` 提示。它不使用回合数窗口，也不使用调用方撰写的摘要：

1. 把宿主提供的调用方身份绑定到恰好一个会话记录以及当前咨询边界。
2. 按顺序重放 `response_item` 记录，在每一个 `compacted.replacement_history` 处替换累积历史。在进行中的咨询条目之前停止。保留结构化内容、工具配对以及不透明推理；不要恢复压缩前的条目。
3. 以空工具启动配置以及来源基础指令，启动一个全新的临时 App Server 线程。注入重建后的结构化条目，然后是咨询者专用的开发者指令与咨询请求。全新的宿主脚手架是附加上下文；它不得削弱调用方约束。
4. 从宿主追踪中检查每一个实际 Advisor 请求的模型、推理等级与工具清单。缺失或相互矛盾的证据是一次显式失败。追踪/目录是临时的实现输入，而不是持久的观察日志。

该探测拒绝缺失的咨询边界、缺失的压缩替换历史，或它尚未认定为合格的回滚重建。生产环境还必须校验线程/回合/条目绑定、受支持的条目形态、截断、上下文溢出、取消，以及它的确切输出契约。AC-3 允许显式失败；静默缩短或重建一份摘要则不被允许。这些是工单 04 的义务，并不是声称该一次性探测是一个已完成的组件。

主代理比较了实际的调用方请求与 Advisor 请求，保留条目顺序、角色、内容、工具输出以及加密推理。比较规范化只移除传输 ID、内部归属元数据以及可选的空值字段。按照规格中明确的 Implementer 选择，调用方工具清单被省略。下面的计数是有序的源条目包含，而不是整个请求的相等：Advisor 会加入它自己的宿主脚手架与咨询指令。

| B′ 检查 | 来源线程 | Advisor 线程 | 实际结果 |
|---|---|---|---|
| 十一个未压缩回合之后的最早上下文，随后是同回合工具 nonce | `01a0d9c4-4596-72e3-9b6c-16b68d188f89` | `01a0d9c5-198a-78d1-9442-c5f3bb00fc7a` | 31/31 个有序输入条目被保留；最早约束与 nonce 已恢复。 |
| 强制压缩、较晚标记，以及一个全新的同回合 nonce | 同一来源 | `01a0d9c5-9dec-7da1-8a80-4164d80fb69a` | 22/22 个条目被保留；摘要、最早被保留的约束、较晚标记以及 nonce 已恢复。 |
| 未完成回合期间的自动压缩 | `01a0d9c3-992a-7082-992f-eb2d14b94527` | `01a0d9c3-f1b2-7501-aa93-ddceab634365` | 7/7 个压缩后条目被保留；一个有效摘要；被移除的大工具输出不存在。 |
| 位于 `gpt-6-luna[high]` 的原生 worker | `01a0d9c6-f8b2-78d3-908f-afd54d2c448d` | `01a0d9c7-2b54-78b3-8999-ea4e66a687d1` | 零参数调用；10/10 个条目被保留；nonce 已恢复；加密的推理字节跨模型边界被保留。 |
| 位于 `gpt-6-luna[high]` 的原生 explorer | `01a0d9c7-b50d-7623-8301-105a9b687b65` | `01a0d9c7-e337-7a90-ad8e-0c4fe6ae2dce` | 零参数调用；9/9 个条目被保留；nonce 已恢复。 |
| 相对的已安装组件路径以及被截断的工具输出 | `01a0d9cc-b9fc-7821-a450-464d20edeca2` | `01a0d9cc-f687-78b0-8f94-b8f5c5067b21` | 9/9 个条目被保留，包括被截断到 1,500 个输出 token 的调用方可见结果；nonce 已恢复。 |
| 没有调用方转写的图像附件 | `01a0d9cf-3da4-74f0-bfff-59acd2249ee5` | `01a0d9cf-6b19-7613-a8fe-cfba163e3ea7` | 9/9 个条目被保留，包括图像内容；Advisor 从图像中读出 `coral-pine-68317`，并恢复了单独的工具 nonce。 |

本表中的每一个 Advisor 请求都通过原生 `official` 提供方以 `gpt-6-astra[low]` 运行，匹配低推理等级的主代理或 mainstay 探测调用方的 AC-4 目标，实际 `additional_tools.tools=[]`，并且没有顶层工具。每一个已完成的探测命令退出码都为 0。worker/explorer 父项是 `01a0d9c6-7588-74a0-8a4f-4e0dc3cecec5`；每一个临时角色都钉选 Luna high，并保留其角色的开发者指令。两个角色感知检查器都以退出码 0 结束，并带有预期的父项、角色、模型、推理等级、临时工作目录，以及观察到的 read-only/managed 权限元数据。这并不能独立证明隔离。

可移植加载通过 `.mcp.json` 测试，其中 `command="python3"`、`args=["./scripts/consult-probe.py"]`、`cwd="."`。宿主把该工作目录解析为已安装的插件根。脚本根据已验证的带版本缓存布局识别其临时主目录，而不是根据凭据或调用方提供的路径。两次 `${CLAUDE_PLUGIN_ROOT}`/`${PLUGIN_ROOT}` 参数尝试以及一个没有 `cwd` 的相对参数未能完成 MCP 初始化；它们没有被选定。App Server `mcpServerStatus/list` 对选定配置报告 `connected` 以及零属性工具 schema，并且截断输出的实况调用在重新安装之后确认了执行。

第一个延续裁定 Advisor，`01a0d9c0-6b07-7a23-bf24-2c13d5deeebf`（父项 `01a0d9c0-1bde-75d2-bff3-451fdbc9e6cf`），独立识别出回合内压缩缺陷，并建议进行决定性的实际请求比较。一个新的 Advisor，`01a0d9cb-0033-70e2-9c5f-079ae9ff5c79`（父项 `01a0d9ca-9387-7a61-b53e-1f53279f317f`），检查了 B′ 并重跑了最初的五项比较。它建议在可移植加载与截断通过之后再做选定；主代理随后验证了这两者以及图像情形。两者都是实际 `gpt-6-astra[medium]` 的 `ca_advisor_standard`，角色感知检查器退出码为 0，read-only/managed。这些是裁定咨询，而不是独立的产品验收。

选定 B′，因为它是唯一在全部五项资格检查以及全部三条调用方路线上都合格的配置。结构化注入保留角色、图像、工具条目以及不透明推理，而文本序列化会把它们压平。其余未经测试的配置保持未经测试；不对其他原生分叉或传输做出普遍声称。在宿主版本、会话记录 schema、模型目录、MCP 元数据、缓存布局或请求追踪格式发生变更之后，重新认定资格。音频/视频输入、回滚、并行工具竞态以及其他未行使的形态没有被这些探测认证；组件必须显式失败，而不是在它无法确立完整重建的地方声称完整重建。

#### 自动派发检查与剩余信任关卡

同一个临时插件也随附了一个 `PostToolUse` 夹具。它使用父 UUID 与原生任务路径，把实际派发参数连接到子会话元数据，然后读取子项的实际 `turn_context`。这条路线不需要持久的连接状态。该夹具比较钉选或显式的调用方推理等级，并通过 `hookSpecificOutput.additionalContext` 注入其裁定。在已授权的临时钩子信任绕过之下：

- 上面的 Worker 与 Explorer 派发产生了 `DISPATCH_MATCH`，实际为 Luna high。
- 一次有意的 `ca_worker_senior` 派发省略了调用方选定的推理等级。子项 `01a0d9c8-470a-7492-bad3-92fb309a0893` 实际继承了 Astra low。钩子报告了 `DISPATCH_MISMATCH_WORK_PENDING`，其中包括缺失的预期推理等级以及观察到的 low；父项引用了该警告，并使验收保持待定。这演示了 AC-10 的一条自动同会话路线，并消除了 S6 的宿主能力关切。它并不验收未来的完整钩子实现。

不受信任的 CLI 运行跳过了夹具的 `SessionStart`，但在捕获的输出中仍然没有暴露文档所述的 `/hooks` 警告。一次交互式启动再次停在文件夹信任关卡；主代理在没有选择信任的情况下退出。用户信任的 `/hooks` 运行以及交互式不受信任警告仍然待定。主代理没有写入或选择任何钩子信任。按照工单 01 明确的等待行规则，这些检查不阻塞工单 02，但必须在工单 05 开始之前解决。

当前停止条件评估：S1 与 S2 保留 P2/P3 的已通过证据；S3 与 S4 由 B′ 清除；S5 仍然没有被已行使的绕过路线触发，用户信任的执行待定；S6 没有被自动的正/负派发探测触发；S9 没有被已安装的相对路径组件与钩子执行触发。本节不验收任何产品实现、发布或真实主目录更新。

延续范围验证在工单 02 之前完成：恰好 `acceptance.md` 与 `spec.md` 不同于延续的十文件 SHA-256 基线；其余八个任务文件未更改。没有已跟踪文件更改。主代理检查了新的请求比较结果与原生路线检查、任务文件空白，以及 `git diff --check`（退出码 0）。没有专用的 Markdown 解析器/schema 适用于该证据记录。产品测试与实现评审仍然与产品实现一起待定。

延续清理在 2026-09-26 完成。一次进程检查发现，没有剩余的、绑定到该临时根的 Codex/探测进程。`/home/hyy/ca-consult-reprobe-pfgxoqcr/` 与 `/tmp/ca-consult-reprobe-path` 已被删除，并验证了它们不存在，包括两个主目录、复制的凭据、已安装夹具、原始日志/追踪、脚本、schema/文档以及图像。本节保留非机密结果与 ID；临时的底层记录在清理之后被有意使其不可用。必需的用户信任钩子与警告检查必须在工单 05 之前使用一个新准备的临时主目录。

### P7 用户信任的执行与不受信任跳过

在 2026-09-26 从未经更改的已跟踪 HEAD 准备了 `/home/hyy/ca-hook-trust-jw6yp7ek/`，使用一个新的临时主目录、必需的本地市场安装路线，以及仅必要的认证配置。这与已删除的 P6 环境分开。它唯一的夹具钩子是 `SessionStart`：它把会话/事件/来源/模型元数据记录到一份临时回执，并注入一个固定标记。它既不修改项目，也不处理凭据或信任。用户被给予捕获交互式 CLI 的 `script -q -f` 命令，并被要求保留不受信任警告、通过 `/hooks` 评审/信任该钩子，然后退出。本次检查不使用绕过。用户动作以及随后的已信任执行待定；主目录、复制的凭据与记录稿必须在检查之后移除。工单 02–04 可以在等待期间继续；在该关卡解决之前，工单 05 不能开始。

用户报告已完成信任并退出。主代理随后的无绕过检查，线程 `01a0d9dd-47af-72c1-942a-cc7b1fb6c613`，返回 `MISSING`，并且不存在夹具回执。捕获的交互式命令解释了这一不符：它设置的是 `C0DEx_HoME`，而不是 `CODEX_HOME`，因此那次启动没有使用准备好的临时配置。宿主的钩子功能在临时主目录中已启用。一份准备好的 `trust-check.sh` 现在在内部设置确切的环境键，从而避免再一次人工抄写它。修正后的用户信任动作仍然待定；主代理没有改变任何信任状态。

用户随后运行了修正后的脚本并报告完成。捕获的宿主界面显示，用户在启动时的 **Hooks need review** 对话框中选择 **Trust all and continue**。这是进入会话之前呈现的宿主交互式信任关卡；本记录并不声称用户输入了 `/hooks`。随后一次没有绕过的 `codex exec`，线程 `01a0d9e1-e5d5-7fa0-9f66-56fbd8cc2b9b`，返回 `HOOK_USER_TRUST_30941`，退出码为 0，并产生了匹配的回执：`SessionStart`、`source=startup`、`model=gpt-6-astra`。

主代理只把临时夹具的超时从 5 改为 6，并通过移除/添加重新安装，产生了新的钩子哈希，且没有编辑信任状态。在下一次交互式启动中，主代理选择了 **Continue without trusting**。宿主为一个新的/已更改的钩子显示了 **Hooks need review**。线程 `01a0d9e3-0490-7a80-9788-0e3802b681aa` 返回 `MISSING`；回执文件仍然只包含更早的已信任执行。`/hooks` 概览显示 `SessionStart: Installed 1, Active 0, Review 1` 以及 `1 hook needs review before it can run`。主代理在没有授予信任的情况下退出。这些观察确立了一次不受信任的跳过以及宿主的交互式警告；没有观察到额外的、指向 `/hooks` 的字面启动消息。

O4 的用户信任情形与不受信任警告情形已经完成。具体的启动对话框是当前宿主对同一用户所有的信任动作的呈现。S5 未被触发。产品钩子验收仍然是工单 05 的责任。在 2026-09-26，主代理停止了属于该临时主目录的两个受管理守护进程，移除了 `/home/hyy/ca-hook-trust-jw6yp7ek/` 与 `/tmp/ca-hook-trust-path`，并验证了不存在。复制的凭据、原始捕获、回执、夹具来源以及已安装副本已被删除；只留下这些非机密发现。

## 02 原则、姿态文本、术语表、ADR-0006

Status: 工单 02 已由主代理验收于
2026-09-26。本记录只覆盖原则、规范姿态文本、术语表与 ADR 记录。工单 03–06 以及最终产品验收也仍然待定。

工单 02 的 worker 运行于线程 `01a0d9d5-0103-7373-87a4-520488baf6d8`，父项 `01a0d989-47e5-7562-9ba3-373aef463838`，通过已安装入口 `ca_worker_standard_m`，观察到位于 `gpt-5.6-sol[high]`。角色感知检查器退出码为 0。观察到的沙箱与权限元数据是 `danger-full-access` 与 `disabled`；工作目录是本仓库。该 worker 没有做提交、分支、推送、真实主目录安装或外部更改。

### 变更与裁定

- 用 `mainstay`/`crux`/`rescue` 准入、下一档位升级、失败计数、零参数过程咨询、姿态/采纳规则指针，以及 AC-2 验收选择，替换了运行时 `SKILL.md` 中旧的分配与恢复原则。完整尝试、新线程、Architect 模式以及主代理验收所有权的含义保持不变。
- 增加了 `references/consult-posture.md`，在完整姿态块、精简姿态块与采纳规则周围正好有六条相互匹配的分隔符行。确切的模型身份选择姿态；未知模型遵循同一种比较，以 `gpt-5.6-terra` 为示例，并且没有家族列表。精简姿态块明确地只有它的两个多步骤触发条件。该文本包括调用前耐久化、下一次可见回复、调和、每一个 AC-6 例外，以及没有提交步骤。
- Explorer 与 Worker 数据包保持逐字节不变。Advisor 契约现在只包含独立验收；咨询不使用数据包。只更新了两个由工单拥有的操作节；一次自动比较确认，两种语言中这两节之外的每一个字节都未更改。
- 重写了 DR-6 所要求的术语表术语。退役术语只保留在 `_Avoid_` 行上。增加了 ADR-0006，包含十三项裁定、B-prime 机制及其限度、宿主事实与失效检查、`/hooks` 用户关卡、`0.4.0` grok 车道，以及来自 ADR-0003/4/5 的每一句被取代句子的精确引文。
- 使用 `<!-- consult-posture:<variant>:start/end -->` 作为稳定的分隔符语法。英文文件与中文文件逐字符保留这些分隔符。`openai.yaml` 没有点名一个退役概念，并且没有被更改。ADR-0005 的所有权、证据复用、分批以及场景选择规则保持不变；只有它过时的委派检查档位选择条款被取代。

已更改的交付路径是 `CONTEXT.md`、`docs/adr/0006-mainstay-crux-rescue-and-process-consultation.md`、运行时 `SKILL.md`、`references/consult-posture.md`、`references/role-contracts.md` 与 `references/operations.md`，加上 `docs/zh/` 下四个匹配的运行时 Markdown 孪生文件。

### 验证

`python3 tests/test_zh_mirror.py` 退出码为 0：`27/27 passed, 0 failed`，包括本工单更改或增加的全部四对运行时 Markdown。

`sh plugins/codex-advisor/scripts/verify.sh` 退出码为 0：

```text
PASS: fork metadata, overwrite, unchanged, retire, check drift/residue, preservation, refusals
PASS: generic inspector, table-driven templates, retired options, payload filtering
VERIFY PASSED: selected deterministic checks (no live routing claim)
```

限定范围的退役术语搜索使用下面这条命令，两个操作节按其标题被提取，并且排除了 `CONTEXT.md` 的 `_Avoid_` 行：

```sh
set -o pipefail
pattern='first-round pool|senior gate|decision packet|DECISION packet|Proactive advice is allowed|\b(light|standard|senior)\b'
failed=0
if rg -n -i "$pattern" plugins/codex-advisor/skills/orchestration/SKILL.md plugins/codex-advisor/skills/orchestration/references/consult-posture.md plugins/codex-advisor/skills/orchestration/references/role-contracts.md docs/zh/skills/orchestration/SKILL.md docs/zh/skills/orchestration/references/consult-posture.md docs/zh/skills/orchestration/references/role-contracts.md; then failed=1; fi
if awk '/^## Recover and hand off actual state$/{on=1} /^## Schedule and check combined work$/{on=0} /^## Advice and independent acceptance$/{on=1} /^## Observe permissions$/{on=0} on' plugins/codex-advisor/skills/orchestration/references/operations.md | rg -n -i "$pattern"; then failed=1; fi
if awk '/^## 恢复并把实际状态交接出去$/{on=1} /^## 调度并检查合并后的工作$/{on=0} /^## 建议与 independent acceptance$/{on=1} /^## 观察权限$/{on=0} on' docs/zh/skills/orchestration/references/operations.md | rg -n -i "$pattern"; then failed=1; fi
if rg -n -i "$pattern" CONTEXT.md | rg -v '_Avoid_'; then failed=1; fi
exit "$failed"
```

该组合命令以退出码 0 结束，且没有匹配。单独的 `SKILL.md` 与孪生文件搜索也以退出码 0 结束，且没有匹配：

```sh
if rg -n 'gpt-|[[:alnum:]._-]+\[(low|medium|high|xhigh|max)' plugins/codex-advisor/skills/orchestration/SKILL.md docs/zh/skills/orchestration/SKILL.md; then exit 1; else exit 0; fi
```

`git diff --check` 以退出码 0 结束，且没有输出。因为新的 ADR 与姿态文件未被跟踪，补充的 `git diff --no-index --check /dev/null <file>` 运行覆盖了每一个新交付物以及验收记录，并在把正常的 no-index 差异状态当作成功之后以退出码 0 结束。

补充结构检查也通过了：两份姿态参考都包含六条分隔符行；18 个 ADR 引文块中的每一个都是 ADR-0003、ADR-0004 或 ADR-0005 的一个精确规范化子串；无主操作字节以及 Explorer/Worker 契约前缀在两种语言中都等于 `HEAD`。

两条最初的补充检查命令失败，原因是命令缺陷，发生在它们评估交付物之前：第一个 ADR 引文校验器有一个无效的 Python 生成器表达式（`SyntaxError`），并且第一个 no-index 包装器赋值给了 zsh 的只读变量 `status`。它们修正后的重跑就是上面的通过结果。

### 缺口

按照该工单，没有增加新的文档测试。验证器声明它不做实况路由声称；本工单的原则由镜像、结构、精确文本、范围以及差异检查确立。运行时咨询、入口路由、钩子、README/手册以及集成验收属于后续工单。主代理检查了全部已更改与新增的英文和中文交付物，包括修正后的建议尝试定义与信任来源。上面对本状态所要求的检查仍然有效；修正后的镜像测试通过 27/27，并且主代理的空白检查退出码为 0。工单 02 已被验收；工单 03 可以开始。

用户信任与不受信任跳过的钩子路径现在已在正确的临时 `CODEX_HOME` 中通过：用户在启动评审对话框中信任了该钩子；主代理对哈希已更改的情形选择了 "Continue without trusting"。已信任的无绕过线程返回了注入的标记，并写下一份 `SessionStart` 回执；哈希已更改的不受信任线程返回 `MISSING`，且没有新回执，同时 `/hooks` 概览显示有一个钩子等待评审。ADR-0006 记录了非机密结果与线程 ID。这确立的是宿主信任边界，而不是未来的产品钩子实现。旧档位术语仍然留在路由配置、模板、脚本、README、无主操作节、历史 ADR 以及更早的发布材料中，因为后续工单拥有那些位置。

## 03 路由配置、入口、安装器、检查器

Status: 工单 03 在确定性验证、完整的差异检查以及全部十三条实况路线通过之后，
由主代理于 2026-09-26 验收。模型设置的证据来自实况检查，而不是确定性测试。

工单 03 的 worker 运行于线程 `01a0d9eb-7cd5-7fe0-8b1e-b2cbd0602159`，父项 `01a0d989-47e5-7562-9ba3-373aef463838`，通过已安装的 0.2.0 入口 `ca_worker_standard_m`，观察到位于 `gpt-5.6-sol[high]`。角色感知检查器退出码为 0。观察到的沙箱与权限元数据是 `danger-full-access` 与 `disabled`；工作目录是本仓库。

### 变更与裁定

- 英文与中文路由配置现在逐单元格承载 TR-3 表，包括 worker `crux` 的 Astra 默认值 `low`、候选顺序、AC-4 咨询映射、AC-2 验收映射及其 Derived 情形、针对 "not weaker" 的模型/推理等级排序、两项 TR-9 假设及其下一代模型失效触发条件，以及调整方法。这些配置既不包含 5.6 模型，也不包含 Terra。
- 十三个以档位命名的模板与十三个中文孪生文件替换了十一对 0.2.0。六个单一推理等级入口钉选推理等级；所有其他入口把它留给调用方。Explorer 与 Advisor 入口请求只读沙箱，worker 继承父沙箱，同一角色的指令正文相同，Advisor 指令只回答 REVIEW 数据包，并且在工单 04 之前不存在姿态节。
- `retire.txt` 保留八个 0.1.0 文件名，并加入恰好十一个 0.2.0 文件名。安装器仍然由清单驱动，并保持其覆盖、未更改、退役、检查、选择性检查、保留、原子写入以及拒绝行为。它的选择器来自这十三个文件名。
- 检查器接口与实现没有更改。运行时测试发现全部模板，因此现在行使十三个情形。由工单拥有的操作节列出全部入口与选择器，只对钉选入口显示钉选的推理等级，保留通用检查器接口，并保留一般的 ADR-0005 场景选择、证据复用以及未行使路径规则。

### 确定性验证

`sh plugins/codex-advisor/scripts/verify.sh` 退出码为 0：

```text
PASS: profile/template equality, negative model fixture, exact retire set, negative retire fixtures
PASS: fork metadata, overwrite, unchanged, retire, check drift/residue, preservation, refusals
PASS: generic inspector, table-driven templates, retired options, payload filtering
VERIFY PASSED: selected deterministic checks (no live routing claim)
```

路由配置检查在一个模型被替换为 `fixture-wrong-model` 之后，拒绝一份复制的模板映射。退役检查从 ADR-0004 导出固定的十一文件历史集合，并同时拒绝缺少文件的夹具以及包含 `ca-fixture-typo.toml` 的同等大小夹具。安装器夹具种入全部十九个退役文件，断言十九次移除，保留一个无关文件，并通过最终的 `--check`。

`python3 tests/test_zh_mirror.py` 以 `31/31 passed, 0 failed` 退出码为 0：五对 Markdown、按存在性的十三对模板，以及按相等配置键加中文正文的十三对模板。

一次补充结构检查在比较 `spec.md` 中的三行 TR-3 与去掉入口名前缀之后的路由配置之后，以退出码 0 结束。它还解析了两套模板并报告：

```text
PASS: TR-3 cells, 13-entry role counts, identical role bodies, REVIEW-only Advisors, no posture sections
```

对 `plugins/codex-advisor/` 与 `docs/zh/` 的阶段搜索，只排除 `agents/retire.txt` 与 `.codex-plugin/plugin.json`，以退出码 0 结束，没有旧入口名，也没有旧档位词。对两份路由配置的单独搜索以退出码 0 结束，没有 `gpt-5.6` 或 Terra。`git diff --check` 退出码为 0；一次补充的 `git diff --no-index --check` 循环覆盖了全部二十六个未跟踪模板，并且也通过了。

在开发期间，第一次补充 TR-3 比较失败，因为它的临时解析器没有规范化缩进与 Markdown 反引号。一次机械的文件末尾清理随后把一个字面 `\\n` 写进了新模板；完整验证器与镜像测试拒绝了无效的 TOML。模板已被修正，并且上面的每一项最终检查都在当前字节上重跑。

### 实况路由检查

主代理在 2026-09-26 以 Codex `0.157.0` 运行了全部十三条原生路线，位于 `/home/hyy/ca-tier-routes-rcwpu1wb/home`，通过必需的本地市场路线与配套安装器从本次检出安装。每一个父项以 `gpt-6-astra[low]` 运行，带有一个全新子项、`fork_turns=none`，并且只对调用方选定的入口传递推理等级。每一个父项与检查器退出码都为 0，并且每一个父项都返回了夹具第一行 `ROUTE_FIXTURE_74216`。

| 入口 | 传入的推理等级 | 实际模型 | 实际推理等级 | 沙箱 / 权限 | 子线程 | 检查器 |
|---|---|---|---|---|---|---|
| `ca_advisor_crux` | `omitted` | `gpt-6-astra` | `high` | read-only / managed | `01a0d9f5-f781-78c2-8529-b6e458f9bed5` | 0 |
| `ca_advisor_mainstay` | `low` | `gpt-6-astra` | `low` | read-only / managed | `01a0d9f6-4a88-7403-9165-74c8f7a1621d` | 0 |
| `ca_advisor_rescue` | `omitted` | `gpt-6-astra` | `xhigh` | read-only / managed | `01a0d9f6-8bcf-7ca2-8f2c-97d4739d81af` | 0 |
| `ca_explorer_crux_h` | `omitted` | `gpt-6-sol` | `xhigh` | read-only / managed | `01a0d9f6-d8f9-7a83-8361-da28c2c9095c` | 0 |
| `ca_explorer_crux_m` | `omitted` | `gpt-6-luna` | `max` | read-only / managed | `01a0d9f7-261a-7e93-a2de-2ba109cd926a` | 0 |
| `ca_explorer_mainstay_h` | `medium` | `gpt-6-sol` | `medium` | read-only / managed | `01a0d9f7-87a9-7331-ad99-893e807dca2c` | 0 |
| `ca_explorer_mainstay_m` | `high` | `gpt-6-luna` | `high` | read-only / managed | `01a0d9f7-cf48-70b1-a449-34584f890c12` | 0 |
| `ca_explorer_rescue` | `medium` | `gpt-6-astra` | `medium` | read-only / managed | `01a0d9f8-1bb5-7f11-b4f7-4667f6fc7f06` | 0 |
| `ca_worker_crux_h` | `low` | `gpt-6-astra` | `low` | read-only / managed | `01a0d9f8-62ee-73f2-8228-f9888d82ce9d` | 0 |
| `ca_worker_crux_m` | `xhigh` | `gpt-6-sol` | `xhigh` | read-only / managed | `01a0d9f8-a7a2-7871-a9d0-87900dfa8ad0` | 0 |
| `ca_worker_mainstay_h` | `omitted` | `gpt-6-sol` | `high` | read-only / managed | `01a0d9f8-fa28-79c1-b392-7151673ebbc1` | 0 |
| `ca_worker_mainstay_m` | `omitted` | `gpt-6-luna` | `max` | read-only / managed | `01a0d9f9-4a14-7cb3-97dc-1032b56d31f8` | 0 |
| `ca_worker_rescue` | `high` | `gpt-6-astra` | `high` | read-only / managed | `01a0d9f9-a0c8-7ae0-a3ee-9d8a30ba3e09` | 0 |

每一个子项所记录的父项与工作目录都匹配其实际 CLI 父项以及一次性工作区。父项 ID 按表顺序为：`01a0d9f5-d7fb-7402-9991-c775989f44aa`、`01a0d9f6-29cb-7790-89a8-62b995e874f9`、`01a0d9f6-6de6-7c01-a8ed-f4affaa3be16`、`01a0d9f6-b749-75a3-a479-147d4f3a2244`、`01a0d9f7-0509-73a3-b3ec-f19a4708f867`、`01a0d9f7-64f0-7461-bf89-e3de8b179e1b`、`01a0d9f7-ac5a-70b1-9d0c-5a46d0425fbd`、`01a0d9f7-f9c0-7f00-a278-89b645e444c2`、`01a0d9f8-4224-7cb0-9da5-62acc1d5f390`、`01a0d9f8-883c-7553-866c-46baf25bfc6d`、`01a0d9f8-d210-77b1-a6c3-2e2f9eba5fdf`、`01a0d9f9-22a1-7ba0-982e-f839489f593b`、`01a0d9f9-7ec6-7da3-9782-4ea1f569831b`。

安装器移除了从 `HEAD` 种入的全部十一个旧文件名，并恰好安装了十三个新模板。在 worker 只调整了 TOML 值之外的空白之后，主代理确认全部十三个已缓存模板与工作区模板的每一个已解析字段都相等，通过移除/添加刷新了插件，并重跑了配套安装器。已完成的调用仍然适用，因为模型、推理等级、描述以及开发者指令的值未更改。没有已安装文件被手工编辑。

主代理检查了两种语言的全部新模板、两份配置、安装器/验证器差异，以及由工单拥有的操作节。新的负向检查拒绝预定的错误模型、缺失退役以及同等数量的错误退役情形。工单 03 通过其交付物检查与实况路由检查。观察到的只读策略来自夹具父项；这验证的是路由与接线，而不是一般的隔离、质量、成本或稳定性。咨询与钩子仍然是未经测试的产品工作。

路由清理在 2026-09-26 完成：主代理停止了临时主目录的受管理守护进程，移除了它的主目录（包括凭据与会话）、工作区、路由日志、结果 JSON、安装器输出以及路由测试具，并验证了它们不存在。同一个外层临时根只保留工单 04 所需的非机密官方 schema/文档以及单独的未认证隔离夹具；那些内容在该探测批次结束时移除。没有真实安装或信任状态被更改。

## 04 过程咨询

Status: 工单 04 已由主代理于 2026-09-26 验收。确定性检查、
真实的主代理/worker/explorer 咨询、隔离、取消以及清理均已通过。

- 来自主代理、一个 worker 与一个 explorer 的实况咨询：调用方、调用方模型、预期拨档、观察到的 Advisor 模型与推理等级、nonce 结果、压缩结果、最早上下文结果、该请求的实际工具集，以及线程 ID。

### 实现与确定性证据

该 worker 运行于线程 `01a0d9fc-4bc5-7a51-9b93-1ee293114827`，父项 `01a0d989-47e5-7562-9ba3-373aef463838`，通过一个已安装的 0.2.0 worker 入口，观察到位于 `gpt-6-astra[low]`。主代理的角色感知检查器退出码为 0，并报告 `danger-full-access` / `disabled`，工作目录是本仓库。该 worker 使用合成主目录与一个替代的原生可执行文件；它没有读取真实凭据/配置或调用方记录稿，没有调用模型，没有安装到真实主目录，也没有提交、分支或推送。

该实现增加 `.mcp.json`、清单的 `mcpServers` 字段，以及 `scripts/` 下的三个运行时模块：`process-consultation.py` 提供零参数 MCP 边界与取消；`consult_context.py` 绑定宿主身份、重建一个会话记录快照、校验内容/配对，并从配置读取拨档；`consult_native.py` 处理原生已认证执行、隔离、结构化输出、实际请求检查以及清理。没有增加依赖。版本与清单描述未被触碰。

归约器不使用窗口或调用方摘要。它在 `compacted.replacement_history` 处替换更早的历史，保留原始角色、图像、不透明推理以及成对的工具调用/结果，包括调用方可见的截断输出，并在被识别的咨询条目之前停止，包括 code-mode 包装。未知内容/事件、回滚、缺失的替换历史、不一致的身份以及未配对的并行调用都会失败。按照规格所允许的，调用方工具清单被省略。每一个实际 Advisor 请求都必须按顺序包含来源条目；比较只忽略条目级传输 `id`、已认定的 `internal_chat_message_metadata_passthrough`，以及可选的空字段。它从不移除 `call_id`，也不更改内容。静默的自动压缩会显式失败。

执行器在没有调用方上下文的情况下枚举全部 MCP 清单页，关闭该原生进程，通过一个加引号的 TOML 内联映射禁用每一个名称，并在注入之前验证空的 MCP 能力与钩子。它使用捆绑目录的确切 slug，配合已禁用的工具以及已认定的功能向量，包括已禁用的记忆与宿主技能发现。每一个实际推理请求都必须显示预期的模型/推理等级以及一个显式的空工具集。按照主代理的指示，验证器接受 P6 的空 `additional_tools.tools` 或显式的顶层 `tools=[]`，拒绝任一位置上的非空清单，并拒绝缺失的证据。

主代理随后隔离出一个捆绑目录字段 `tool_mode=code_mode_only`，尽管功能标志为 false，它仍然保留了 code-mode 包装。原生未认证目录检查表明，省略该字段会恢复 P6 已认定的目录形态。该组件现在移除该字段，而不是发明一个禁用值。可执行夹具提供该字段，并拒绝任何仍然保留它的生成目录。实际请求的工具校验仍然严格。

既有的调用方工具调用事件意味着已经开始。返回的 `structuredContent.status=succeeded` 带有一份有效的计划/更正/停止，并且预期/实际拨档匹配，即意味着成功。返回的 `status=failed` 且 `isError=true` 带有代码/消息并且没有建议；缺失的终态结果并不是成功。一次有效的停止计为成功的咨询。没有重试。原生期限是 180 秒。取消会终止原生进程树，并移除该调用的临时目录。目录、追踪载荷、捕获的输出、日志以及 SQLite 状态都是临时的；该组件不打开凭据文件。

全部十个 explorer/worker 模板及其中文孪生文件，都在 `process-consultation:start/end` 分隔符之内承载确切的规范完整姿态块或精简姿态块，加上采纳规则。确切的配置模型身份选择变体。Advisor 没有姿态节。安装组在两种语言中检查这些规则以及该节之外的同一角色身份。它的三个负向夹具拒绝一个单字符编辑、一个被给予精简变体的完整姿态入口，以及一个被给予该节的 Advisor。与已验收的工单 03 快照所做的单独比较证明，每一个其他模板字节都未更改。操作节及其孪生文件记录使用、路由、结果、失败、会话可观察性、隔离、清理，以及额外的原生初始化成本；它们的验证器节包括这个新组。

worker 在 2026-09-26 的验证：

- `sh plugins/codex-advisor/scripts/verify.sh`：最终重跑退出码 0，在第一次实况形态修正之后，全部安装、姿态、检查器情形以及 **45 项 MCP 边界测试** 通过。
- `sh plugins/codex-advisor/scripts/verify.sh --consultation`：退出码 0，在加入主代理观察到的 `world_state` / `token_usage_record` 形态以及已认定的归属规范化之后，**45 项测试** 通过，然后在捆绑的 `tool_mode` 修正之后再次通过。那些修正没有改变既有的安装/运行时检查。
- `python3 tests/test_zh_mirror.py`：退出码 0，**31/31 passed, 0 failed**。
- `git diff --check`：退出码 0。补充的 Python 编译以及已验收基线的模板字节比较也退出码为 0。该 worker 检查了限定范围的差异以及全部新的实现/夹具文件。

边界套件从一个合成的带版本缓存启动一个被复制的组件，并替换原生可执行文件，而不导入私有函数。覆盖包括每一个档位、主代理 Astra xhigh/Sol high/未知 Terra/Astra medium、通过 80 条未压缩消息的最早上下文、未完成工具、压缩、图像、不透明推理与截断；全部结果变体以及错误/中止/空/溢出/畸形输出；包括一个更早请求在内的实际拨档不匹配；缺失/已更改的上下文；缺失/非空的工具证据以及缺失的追踪；MCP/钩子泄漏；身份/布局/内容/回滚/配对失败；带有一个后代的取消；以及未更改的合成 `CODEX_HOME` 加上已清理的临时目录。清单夹具包括分页，以及带有点、引号、一个反斜杠与非 ASCII 文本的名称。

第一次完整运行发现一个测试具 lambda 把已移除的记录作为关键字参数返回；修正后的运行通过了。一次最初的验收记录插入也在没有写入的情况下拒绝了一行过时的预期状态；该 worker 在插入本节之前重新加载了并发的主代理编辑。两者都不确立产品缺陷。实况行为、已安装加载、原生文件系统隔离以及 Windows 执行没有被这些夹具证明。产品验收留在主代理；实况发现与后续修正被分开记录。

主代理的 worker 路线在已经记录的用户任务消息之前暴露了带有 `{"trigger_turn":true}` 的 `inter_agent_communication_metadata`。归约器现在恰好接受该仅布尔值的元数据形态；它的委派夹具仍然断言未更改的原始任务/历史注入。在读取一个请求之后的工具/历史校验失败也保留观察到的 `actual` 模型/推理等级，这是结果契约所要求的。六个聚焦失败情形带着该断言通过；没有观察到请求的更早失败仍然报告 `actual=null`。更新后的 `--consultation` 组在两项修正之后以退出码 0 结束，**46 项测试** 通过。

### 原生隔离探测

委派实况后续把带有非空 `author`/`recipient`、`input_text` 以及不透明 `encrypted_content` 块的原始 `agent_message` 条目认定为合格。该组件校验那些字段，并在不做角色转换或解密的情况下保留完整条目。委派夹具现在包括该原生形态，并比较确切的注入字节；实际请求中一个已更改的加密块会使上下文验证失败，而空的 author/recipient/加密内容会在执行之前失败。主代理从 worker `01a0da16-28aa-7443-a10f-dc4c672c7dd4` 与 explorer `01a0da15-f041-7a12-89c4-012fe1aa7d85` 提供了该形态；该 worker 没有检查那些会话。在该修正之后，`sh plugins/codex-advisor/scripts/verify.sh --consultation` 以退出码 0 结束，**50 项测试** 通过。修改过的 Python 语法与 `git diff --check` 也通过了。未更改的镜像/安装/运行时结果仍然适用。

主代理在 2026-09-26 获取了官方 App Server 与钩子页面以及配置 schema，并用 Codex `0.157.0` 生成了协议 schema。这些准备探测使用现有临时探测根之下的一个未认证一次性主目录；它们没有提供调用方上下文，也没有请求推理。一次原生线程启动尝试了未认证的 WebSocket 连接，该连接返回 401；它并不是一次已认证的咨询或模型可用性结果。

- 一次 `mcp_servers={}` 启动覆盖保留了一个既有夹具服务器。一个空映射并不是清除继承配置的受支持方式。
- 单独的原生 `initialize` 没有启动夹具。`mcpServerStatus/list` 确实启动了它并枚举了它的工具。关闭原生 stdin 并等待正常退出之后，夹具 MCP 进程 ID 没有一个仍然存活。
- 三个已配置名称 `fixture-one`、`fixture_two` 与 `fixture.dot`，以 `limit=1` 分三页返回。第二个进程带有启动 TOML 覆盖 `mcp_servers={"fixture-one"={enabled=false},"fixture_two"={enabled=false},"fixture.dot"={enabled=false}}`，把三者都返回为空工具，并且没有启动夹具服务器。
- 在 `features.hooks`、`features.codex_hooks` 与 `features.plugin_hooks` 为 false 时，`hooks/list` 为临时工作目录返回一份空钩子列表。启用的对照返回一个已启用但不受信任的用户钩子。这证明宿主清单变更，而不是一次已信任钩子的执行：对照没有运行它，并且没有把不受信任的跳过计为执行证据。
- 原生进程使用一个临时工作目录、`log_dir`、`sqlite_home` 与 `CODEX_ROLLOUT_TRACE_ROOT`、`history.persistence="none"`、已禁用的插件、记忆与目标、`skip_host_skill_discovery=true`，以及一个临时线程。第一次线程初始化创建了普通的 `.sandbox_migration` 文件，其中只包含 `v1`。在该普通初始化之后，两阶段探测使来源主目录的文件大小/mtime 快照保持未更改。原生数据库与追踪被限制在临时状态位置。这只确立已行使的已初始化主目录路径；产品的正常、错误与取消路径仍然必须检查。最初的探测包装器在成功的原生关闭之后有一个 PID 换行拆分错误；修正后的重跑通过了。

裁定建议来自全新的已安装 `ca_advisor_standard` 线程 `01a0d9f2-a978-7301-a06f-96f58e3c6086`，实际 `gpt-6-astra[medium]`，父项 `01a0d989-47e5-7562-9ba3-373aef463838`，角色感知检查器退出码为 0。观察到的权限是 `danger-full-access` / `disabled`；数据包禁止写入、模型调用、凭据读取与委派，并且它的活动是只读的。针对新的探测证据，建议确认原生服务初始化并不违反 AC-3 对 Advisor 模型实际工具的限制。它增加启动成本，并且可以运行既有服务的启动行为，这必须被披露。枚举阶段不得被提供任何调用方上下文，并且它的工具/资源描述或错误不得进入 Advisor 输入或持久记录。主代理采纳两阶段原生枚举与禁用，并带有预检与每一次请求检查。这是实现建议，而不是独立验收。

AC-11 没有被豁免：咨询专用内容、线程记录、日志、追踪、数据库、计数器或标记，即使在 Codex 写入它们时也仍然是临时的。不含咨询状态的既有宿主安装/迁移簿记被分开归类；不推断对原生写入的一般豁免。一条要求新的持久咨询状态的产品路径必须失败，或在 S8 下返回给用户。这些探测脚本/文档在产品接线不再需要它们之前保持临时；路由凭据与路由日志已经被移除。

### 进行中的主代理产品检查

主代理通过 X-2 市场移除/添加路线安装了每一个被测试的修订，并在临时主目录 `/home/hyy/ca-consult-product-u9awq0t2/home` 中运行其已缓存的配套安装器。实际原生请求追踪只在该一次性测试根之内，由一个仅测试的 PATH 包装器复制，发生在产品移除其临时状态之前。这不增加产品观察开关。

第一次产品检查暴露了被省略的原生记录类型（`world_state`、`token_usage_record` 与 `inter_agent_communication_metadata`），以及用于加密委派任务送达的结构化 `agent_message`。主代理在把每一种形态认定为合格之前，把实际调用方请求与来源条目做了比较。状态与用量元数据并不是额外消息；渲染后的指令作为响应条目被保留。加密的代理消息保持结构化并且逐字节确切。唯一的比较规范化是条目级传输 `id`、可选空值，以及 `internal_chat_message_metadata_passthrough`；角色、文本、`call_id`、图像与加密字节保持确切。

第一次原生 Advisor 请求正确地未通过空工具检查，因为捆绑目录的 `tool_mode=code_mode_only` 已被复制进自定义目录。一次未认证的原生目录比较确立了原因。省略该字段会恢复 P6 已认定的目录；不使用赋给一个发明出来的禁用值。下面修正后的实际请求具有 `additional_tools.tools=[]`，并且没有顶层工具。这些实现修正并不更改 B′，也不放宽它的成功标准。

| 产品检查 | 调用方 | Advisor | 主代理证据 |
|---|---|---|---|
| 位于其实际所要求拨档的主代理 | `01a0da13-36a5-7792-a9d3-7e95048549c6` | `01a0da13-a5cb-7e01-9083-5f4edbc1bef6` | 实际 `gpt-6-astra[xhigh]`；空工具；16/16 个有效来源条目与来源基础指令被保留；计划包含最早约束与同回合 nonce。 |
| 十一个已完成的未压缩回合，随后咨询 | `01a0da14-7285-72c0-a0b7-ace599a737ab` | `01a0da15-2c9c-7a80-abae-0dde46d9d1c3` | 实际 `gpt-6-astra[low]`；空工具；34/34 个来源条目与基础被保留；最早 token 与全新 nonce 已恢复。不存在回合窗口。 |
| 原生手动压缩与较晚上下文 | 同一调用方 | `01a0da15-ec91-7043-8058-600b07cff276` | 实际 `gpt-6-astra[low]`；空工具；21/21 个压缩后条目与基础被保留；被保留的最早 token、较晚标记以及全新 nonce 已恢复。 |

主代理直接验证了原生追踪载荷，而不是 Advisor 的自我报告。每一个成功的产品响应都有 `status=succeeded`、一份 `plan`、匹配的 `actual`/`expected`，以及不同的调用方/Advisor ID。每一次被测试的正常/失败原生调用都移除了它的临时目录、追踪、日志与数据库。委派、已配置服务隔离以及取消检查仍然在进行中。来源主目录与仅测试保留的追踪在这些检查运行期间尚未清理；工单 04 当时尚未被验收。

### 主代理验收与清理

最终的 worker 与 explorer 产品调用在 X-2 刷新之后通过。Worker `01a0da19-47e9-75b2-bd3f-76133faaf931`，父项 `01a0da19-23e7-7b00-b2a6-7f79d710b930`，运行已安装的 `ca_worker_mainstay_m`，实际 `gpt-6-luna[max]`。Explorer `01a0da19-489d-74d0-9a1d-421ceb9c5368`，父项 `01a0da19-23e7-7d23-aee6-39c1a2f04b18`，运行 `ca_explorer_mainstay_m`，实际 `gpt-6-luna[high]`。两个角色感知检查器退出码都为 0，并带有预期的临时 cwd 与父项。宿主对两者应用了 `danger-full-access` / `disabled`；这些夹具禁止编辑，并且没有执行编辑。这是行为范围证据，而不是沙箱隔离。

它们的 Advisor 分别是 `01a0da19-a095-78b1-a533-3f01e406a55a` 与 `01a0da19-c50f-78e3-9c1c-752ba7c8d02a`，两者实际都是 `gpt-6-astra[low]`，实际请求工具为空。每一个都按顺序保留了 12/12 个有效来源条目，包括加密的 `agent_message` 内容，并返回一份包含其最早约束与同回合工具 nonce 的有效计划。每一个父项都以退出码 0 完成，并报告了确切的结构化结果。

一个单独的合成活动会话记录夹具，以一个额外的已配置 MCP 服务，行使了已安装产品的真实原生已认证执行器。Advisor `01a0da1a-613a-78d0-a32b-b185c2fbd793` 在实际 `gpt-6-astra[low]`、没有工具的情况下成功。哨兵服务在清单期间启动一次，没有收到工具调用，并且在原生关闭之后没有存活进程。一份已初始化主目录的大小/mtime 快照在整个咨询之前与之后相同（`homeDelta=[]`），包括插件缓存。MCP 边界上的一次取消返回 `status=failed`、`code=cancelled`，并且没有建议；它的主目录快照也保持相同，并且服务器退出码为 0。确定性取消场景单独启动一个后代，并证明进程树终止。已配置钩子抑制由更早的原生清单探测以及产品钩子泄漏负向夹具覆盖；这并不是声称产品钩子已经被实现或验收。

在最终的工单 04 字节上，主代理运行了不带限定的 `verify.sh`（退出码 0，50 项咨询边界测试加上安装/姿态/运行时检查）、`tests/test_zh_mirror.py`（退出码 0，31/31）以及 `git diff --check`（退出码 0）。主代理检查了全部新的运行时与夹具代码、验证器变更、两种语言的操作，以及全部模板姿态变体；确定性检查证明规范字节相等以及各节之外的身份。三个所要求的负向姿态夹具以及畸形上下文/输出/拨档/工具情形，都因预定的要求而失败。不受支持的回滚、并发的未完成调用以及未认定的内容会显式失败。Windows 实况行为没有被行使，并且位于本工单已授权的实况范围之外。

每一次产品临时原生目录在其调用之后都不存在。批次之后，主代理没有发现绑定到两个一次性根中任何一个的进程，并删除了 `/home/hyy/ca-consult-product-u9awq0t2` 与 `/home/hyy/ca-tier-routes-rcwpu1wb`、它们的指针、凭据、会话、追踪、日志、工作区、schema 以及夹具。没有发生真实主目录安装、信任编辑、提交、推送或发布。工单 04 满足 AC-3/AC-4、咨询 AC-10、EN-5 及其 AC-11 范围。更早的进行中段落是带日期的执行历史；本段是当前验收状态。
## 05 插件钩子

Status: 所保留的 AC-8 与派发 AC-10 行为已于 2026-09-26 通过，
带有确定性检查、绕过的实况检查以及用户信任的产品检查。一次更晚的跨平台启动器变更通过当前的确定性检查与绕过检查；用户放弃了对已更改定义重新执行人工信任（D49），该项仍然被明确标为未验证。在一次更早的 defer 之后，用户明确取消了 AC-9 的自动完成阻止，授权了工单 06 与全新的 Astra xhigh 最终验收，并授权在验收之后进行提交/推送以及 WSL/Windows 更新。范围变更是裁定账本中的 D47。只有成功的咨询才计数；失败在成功或用户放行之前保持待定，并且没有停止钩子。随后的一条用户指令把交付收窄为仅本地提交（D48）：不推送，也不做真实安装更新。临时环境清理已经完成；最终一节记录其范围。

### 原生文件效应与派发探测

主代理在 2026-09-26 重新获取了 https://learn.chatgpt.com/docs/hooks，并在 Codex 0.157.0 上运行了一个临时主目录钩子夹具，使用 O4 所授权的信任绕过。当前检出经由 X-2 与已缓存的配套安装器安装。该夹具只记录临时测试输入；它不是产品代码。父项 `01a0da1f-54a7-73b0-8d86-490047e7c0c2` 以显式 `low` 推理等级派发了 `ca_worker_crux_h` 子项 `01a0da1f-7756-7960-8e93-43798cc9d525`。CLI 以退出码 0 完成。

- Shell Python `Path.write_text` 创建了 `shell-write.txt`。它的 `PostToolUse` 输入具有 `tool_name=Bash` 以及该命令；`tool_response` 是一个空字符串。它不包含已更改文件或按进程的写入归属。
- `apply_patch` 创建了 `patch-write.txt`；响应显式点名了成功添加的文件。随后的只读 `cat` 命令返回了文件内容，同样没有文件效应字段。
- 子项会话记录具有 `session_meta`、`event_msg`、`response_item`、`world_state`、`turn_context`、`inter_agent_communication_metadata` 与 `token_usage_record`。事件子类型只有 `task_started`、`item_completed`、`token_count`、`task_complete`；本样本中不存在补丁/文件写入事件。
- 派发 `PostToolUse` 输入包括角色、任务名称与推理等级。它的响应是一个包含规范任务路径的 JSON 字符串。`SubagentStart` 随后给出子 UUID、角色、模型、子记录稿路径以及父会话 UUID。Worker 工具钩子也携带子项 `agent_id`/`agent_type`。第一次停止报告 `stop_hook_active=false`。

确切的 AC-9 条件不能仅从已行使的 shell 钩子输出确立。命令文本/退出状态并不是文件效应记录；工作区快照可以把另一个 worker 的更改归属到一个只读 worker。这不是 S5：宿主阻止一次停止的能力仍然得到证明。如果产品必须收窄已更改文件的含义，或引入一项新的执行限制，那就是 S8。未行使的操作系统级追踪以及任意 MCP 编辑路径并没有被声称不可能；没有确立已认定的一般归属机制。

一个全新的只读裁定 Advisor，`01a0da1d-f1bc-7712-bfcf-b4bf81c75699`，作为已安装的 `ca_advisor_standard` 运行，实际 `gpt-6-astra[medium]`，父项 `01a0d989-47e5-7562-9ba3-373aef463838`；角色感知检查器退出码为 0。观察到的权限是 `danger-full-access` / `disabled`；它的活动是只读的。它建议继续 AC-8/AC-10，使用已证明的父项/路径/子项连接，并把确切的 AC-9 缺口返回给用户，而不是发明一种写入启发式。主代理采纳了该建议，并询问是保持 AC-9 待定，还是把强制明确限制为可证明的更改。用户选择保留确切条件并 defer AC-9。没有采纳命令启发式、共享工作区快照规则或收窄的强制范围。

一次进一步的启动时序探测，父项 `01a0da24-6ca3-7400-98f2-bba08e7db4af`，从实际的 `SessionStart` 回调内部读取了记录稿的第一个头。它存在，匹配会话 UUID，并且具有 `source=exec`、`thread_source=user`，没有父项或代理角色。这支持在注入之前做身份校验；它并不证明每一种未来的宿主时序形态。被绕过的 CLI 返回了它的标记，并以退出码 0 结束。

实现 worker `01a0da22-5064-7eb2-9aa7-50dd7823537f` 是已安装的 `ca_worker_standard_h`，实际 `gpt-6-astra[low]`，父项 `01a0d989-47e5-7562-9ba3-373aef463838`，角色感知检查器退出码为 0。它的数据包只拥有 AC-8 与派发 AC-10，并禁止实况模型调用、凭据读取、真实安装、信任更改以及进一步委派。实际权限是 `danger-full-access` / `disabled`；主代理保留实况验证。

- 产品实况结果以及尚未完成的用户信任运行出现在下面。
- AC-11 钩子写入点评审没有发现写入；临时测试主目录清理在用户信任运行完成之前仍然待定。

### AC-8 与原生派发 AC-10 实现批次

限定范围的 worker 在 2026-09-26 实现了这两条路径。这是工单 05 的部分交付：AC-9 与整张工单的验收仍然待定。它没有运行真实模型调用，没有安装插件，没有修改信任，也没有读取实况主目录。

- `hooks/hooks.json` 使用宿主的默认插件位置，并在 `SessionStart` 与原生派发 `PostToolUse` 上调用 `scripts/advisor-hooks.py`。没有增加清单覆盖、主代理 `Stop` 或 `SubagentStop` 钩子。
- 会话启动校验所提供的记录稿头，排除委派身份，并发出逐字节相等的规范姿态与采纳规则。路由配置目前在全部拨档上有一个确切的 Advisor 模型；钩子验证该事实，而不是猜测缺失的启动推理等级。多个 Advisor 模型，或缺失的身份/模型/规范证据，会产生待定。
- 派发验证从随附模板读取预期模型与钉选的推理等级；在没有钉选时，要求显式的派发推理等级。钉选覆盖派发推理等级。它把原生响应字符串的任务路径与父身份以及恰好一个子头连接起来。子根会话、父项、角色、嵌套来源身份、模型与推理等级必须一致。一次两秒的有界重试允许延迟的子头/回合可见性。缺失、含糊或相互矛盾的证据保持待定；匹配的派发保持沉默。不使用人工检查器调用。
- AC-11 写入点审计：产品钩子没有写入点。它只读取宿主记录稿、配置、姿态与模板，并在 stdout 上发出其结果。清单的 `python3 -B` 与脚本的字节码设置都防止缓存写入。没有会话计数器、被保留的观察或清理状态。夹具写入者只存在于 `verify-hooks.py`，并使用一个被自动移除的临时目录。不存在信任检测或信任变更。
- 该 worker 阅读了主代理在 2026-09-26 获取的官方 [钩子文档](https://learn.chatgpt.com/docs/hooks)，位于 `/home/hyy/ca-hooks-docs-blutphfr/hooks.txt`：插件默认位置与 `PLUGIN_ROOT`、共同记录稿字段、`SessionStart`、`PostToolUse`、JSON `additionalContext`，以及信任关卡。原生字段形态遵循主代理的 P5 与第 05 节探测；记录稿格式仍然是一条重新认定资格的边界。

worker 检查，全部退出码为 0：

- `sh plugins/codex-advisor/scripts/verify.sh`：安装与检查器组、50 个咨询情形，以及新的钩子组通过。完整输出：`/tmp/codex-advisor-ticket05-verify.log`（临时执行器证据）。
- 钩子组以钉选的 JSON 输入行使实际清单命令：所请求主代理模型的确切完整姿态/精简姿态/采纳规则输出；启动、恢复、压缩与清除；委派排除；全部十三个入口匹配；钉选推理等级优先级；错误的实际模型/推理等级；缺失的调用方推理等级；原生字符串响应/路径/头连接；延迟证据；缺失、重复、冲突以及畸形证据。每一个待定情形在命令被禁用时也会使其断言失败。配置含糊与缺失的规范文本在一个一次性插件夹具中测试。AC-9 情形被有意不运行。
- `python3 tests/test_zh_mirror.py`：31/31 通过。运行时操作及其中文孪生文件记录钩子、信任、有界证据处理与 `--hooks`。
- `git diff --check`：通过。该 worker 检查了实际的限定范围差异以及全部四个新文件，并保留了先前工单在共享文件中的更改。

为了主代理实况验证而冻结的可执行字节：

- `hooks/hooks.json`：SHA-256 `79ee4ecd5ef668687f5f2d4dfe75ad4669cfb66bfa9db7f6fe56cc6e6f233f3b`。
- `scripts/advisor-hooks.py`：SHA-256 `d31c9bebc5011d39c77fdb09ffabd622469ca446fa801913fb9bb9bd05fc6ec4`。

实况钩子信任、启动/恢复送达以及实际原生派发仍然是主代理的检查。确定性夹具并不确立那些宿主行为。

### 对冻结钩子的主代理实况验证

主代理在 2026-09-26 于 Codex 0.157.0 上检查了已安装产品。一次性主目录是 `/home/hyy/ca-hooks-product-amsg5f8z/home`；安装使用 X-2 与已缓存的配套安装器。记录器夹具的 `hooks.json` 在这些运行之前被移除。已安装与检出的钩子/脚本哈希等于上面的冻结哈希。没有随附的已安装模板被手工编辑。

| 情形 | 信任 | 线程 | 实际请求证据与结果 |
|---|---|---|---|
| Astra 启动 | O4 临时绕过 | `01a0da29-b782-79e0-b74e-5cc82c80a78c` | Astra xhigh；开发者输入中有一个逐字节相等的精简姿态块与一份采纳规则；完整姿态块不存在。退出码 0。 |
| Sol 启动 | O4 临时绕过 | `01a0da29-b790-7d13-bcb7-e6229b129270` | Sol high；开发者输入中有一个逐字节相等的完整姿态块与一份采纳规则；精简姿态块不存在。退出码 0。 |
| Astra 恢复 | O4 临时绕过 | 同一 Astra 线程，新回合 `01a0da2a-53a9-7f51-8f36-a85024b2e11c` | 实际请求在条目 6 具有原来的注入，并在先前回答之后的条目 10 具有一个新的、逐字节相等的精简姿态/采纳规则开发者条目。退出码 0；这是全新注入，而不仅仅是被保留的上下文。 |
| 匹配的派发 | O4 临时绕过 | 父项 `01a0da2a-5304-7421-bfa5-6c1a245dc593`；子项 `01a0da2a-6a2b-7e82-853d-49cd71e136eb` | `ca_worker_crux_h`，显式 low，实际 Astra low。随后的父请求中没有待定警告。子项只有其模板姿态。退出码 0。 |
| 缺失调用方推理等级 | O4 临时绕过 | 父项 `01a0da2b-14c5-78a0-a515-4ca4bf5352a7`；子项 `01a0da2b-288b-72a0-a67a-a78b91df49e3` | 调用方省略了推理等级。在任何人工检查器之前，下一个父请求包含开发者文本：`Codex Advisor: affected work remains pending. A caller-effort entry was spawned without reasoning_effort.` 父项报告了它。退出码 0。 |
| 不受信任的产品钩子 | 不受信任；没有绕过 | 交互式 PTY 60038 | 启动显示了 `Hooks need review`，两个新的/已更改的钩子。主代理选择了 `Continue without trusting`。`/hooks` 显示了 `2 hooks need review before they can run`：SessionStart 与 PostToolUse 各自已安装 1、活动 0、待评审 1。主代理以 `/quit` 退出，退出码 0，没有授予信任。 |
| 用户信任的产品钩子 | 用户在宿主启动评审中信任了两个钩子；没有绕过 | `01a0da34-43b2-7d10-9ecd-e20e6f201b34` | Astra low；实际开发者输入恰好包含一个逐字节相等的精简姿态块与一份采纳规则，没有完整姿态块。退出码 0，`POSTURE_RECEIVED`。 |

主代理检查了一次性根中 `evidence/{posture-astra,posture-sol,posture-resume,route-match,route-missing}-trace/` 之下的实际 `inference_started` 请求载荷，而不是依赖模型确认。两个子项随后的角色感知检查器退出码都为 0，父项/路径关联与表匹配。缺失推理等级的子项实际继承的 low 设置，并不能解除显式的调用方推理等级要求。两个子项都观察到 `danger-full-access` / `disabled`；这些有界检查并不是隔离证明。

主代理阅读了最终的钩子操作文本与中文孪生文件、验证器集成，以及实现/测试文件。worker 的完整验证器、31/31 镜像检查以及差异检查仍然适用，因为可执行字节没有更改。钩子写入点评审发现，在会话结束时没有需要保留的产品状态。临时测试主目录及其证据保留到所要求的用户信任运行被验证为止，然后必须移除。Terra、压缩与清除注入由确定性夹具覆盖，这里并不声称它们是实况运行。全部 AC-9 阻止场景按用户裁定仍然未实现且未经测试。

用户的 `trust-check.sh` 记录显示正确的临时主目录、宿主的双钩子评审、对 `Trust all and continue` 的选择，以及在 2026-09-26 04:12:27 +08:00 退出码为 0。随后的主代理检查调用了 `codex exec`，且没有 `--dangerously-bypass-hook-trust`；它的实际请求追踪独立于用户报告与模型确认而确立了注入。交互式宿主在启动时呈现信任动作，与工单 01 中一样；更早的不受信任 `/hooks` 检查识别出同样的两个产品钩子。

用户随后授权在完成之后于 WSL 与 Windows 上进行提交、推送与更新。该授权已被记录，并且不得再次请求。在用户询问 worker 停止钩子是什么意思之后，主代理解释了全部三项拟议的钩子责任。用户明确选择取消自动的 worker 完成阻止、继续到 06、全新的 Astra xhigh 最终验收，然后是提交/推送与 WSL/Windows 更新。这是一次明确的范围变更，而不是推断出来的豁免。该放行指令没有授予任何真实安装的钩子信任；产品在每一个真实主目录中仍然要求宿主评审。

只读延续建议运行于新线程 `01a0da34-06d6-7253-ab23-2599524dc59e`，已安装 `ca_advisor_standard`，实际 Astra medium，检查器退出码为 0。它确认，更早的一般延续指令本身并没有移除明确的依赖或最终评审关卡。它的建议并不是授权或最终验收。标准/规格预评审线程是 `01a0da35-b74d-7cf2-ad3b-9883af800993` 与 `01a0da36-0849-79a1-982e-574b731281f5`，每一个都是全新的 `ca_advisor_light`，实际 Astra low，检查器退出码为 0。三者都观察到 `danger-full-access` / `disabled`；它们的数据包禁止编辑与实况模型调用。预评审并不代替规格所要求的最终 Astra xhigh 验收。

### 跨平台启动与清理验证

标准预评审识别出被忽略的 Windows `taskkill` 失败。同一个工单 04 worker 使用 Windows Job Objects 修正了原生进程生命周期：一个一字节、无缓冲的启动门防止原生后代在收容之前启动；终止要求成功的原生 API 以及零个活动作业进程。失败的清理产生一个显式错误，并在其诊断中保留一个更早的失败代码。Codex 解析为一个原生可执行文件，要么在 PATH 上，要么唯一地位于已认定的官方 npm 包布局之内；`.cmd` 包装器不会带着配置参数被执行。运行时文件读取显式使用 UTF-8。主代理检查了已更改的实现与边界测试。被记为非阻塞风格关切的长重建函数保持未更改，因为它没有确立正确性缺陷。

worker 检查：POSIX 咨询组发现 61 个情形，通过 53 个，并显式跳过八个仅 Windows 的情形；Windows Python 3.12.4 在 `PYTHONUTF8` 未设置的情况下通过全部 61 个。证据捕获于 `/tmp/ca04-cleanup-final-{posix,windows}.log`。Windows 情形使用真实 Kernel32 API 与一个合成原生可执行文件，覆盖正常完成、取消、持有 stdio 的孤儿后代、六次 API 失败、取消加上失败的清理、UTF-8 内容，以及原生 npm 可执行文件查找。它们并不是对已认证 Windows 模型执行的声称。

主代理发现 Windows `python3` 是一个不能工作的 WindowsApps 别名（退出码 9009），而 `python` 解析为 Python 3.12.4。共享的 POSIX 启动器从 `python3`、`python` 或 `py -3` 中选择一个能工作的 Python >=3.11；它设置 UTF-8 stdio，禁用字节码写入，并且如果没有一个合格就显式失败。MCP、钩子与验证器使用它。它的负向测试检查一个失败的首选解释器、被保留的参数/stdin，以及解释器完全不可用。钩子读取也使用显式 UTF-8。这更改钩子定义，因此在安装时要求重新的用户评审；代理没有更改任何信任记录。

主代理在临时 `ca-hooks-win-ps4wyrza` 中的 Windows 检查，通过随附启动器，使用 Git Bash 且没有 `PYTHONUTF8`，通过了随附钩子命令的确切完整姿态/采纳规则输出以及 MCP initialize/tools-list。它们没有读取凭据或调用模型。当前检出通过 X-2 作为 0.3.0 被重新安装到现有的 WSL 临时主目录。一次当前的真实咨询，调用方 `01a0da4b-c156-75f3-a8a8-a094faad1812`，Advisor `01a0da4b-e942-7ac3-a5c7-d5e546fd6d92`，返回了一份结构化的成功计划，带有 `CONSULT_CURRENT_49357` 以及匹配的 Astra low 预期/实际设置。主代理检查了实际工具结果。本次检查使用 O4 的临时绕过；它并不代替对新定义重新执行的用户信任执行。

在 2026-09-26，用户明确拒绝重复人工信任测试（D49）。该重复被放弃，并且不再阻塞交付。对最终启动器定义的人工信任执行仍然未验证。更早的用户信任运行以及不受信任警告/跳过仍然限定在它们所记录的定义上。安装/更新指令仍然要求 `/hooks`；没有信任绕过被随附。

## 06 README、清单、版本说明书、发布准备

Status: 已于 2026-09-26 在 D47/D48 之下实现并由主代理验证；最终
独立验收仍然分开。宿主线程容量阻止了一次新的 worker 派发，因此主代理直接实现了本工单，这是 X-2 所允许的。

README 记录十三个入口且不带拨档值、准入与恢复、咨询/姿态/采纳规则、两个钩子、验收、更新，以及十一个已退役的 0.2.0 名称及其替换。清单版本是 0.3.0；描述与关键词描述当前行为，且不带模型名称。市场清单未更改。中文手册覆盖整个版本及其增量，并带有 ADR-0006 引用。被取消的停止强制既不被呈现为已交付功能，也不被呈现为 defer 的缺陷。

之前与之后的基线 SHA-256：`d89f0f18ccfc0cb42156a5548bc531527372603ea12efb13d759e86589b6d4ea`。主代理在写入之前阅读了随附的基线来源，并打开了它渲染后的首屏。最终手册的 CSS 与 JavaScript 与基线逐字节相等。全部十三对冻结的入口/拨档都与路由配置做了比较并且匹配，包括每一个被允许的推理等级与默认值。没有使用杂志预览。

| 场景 | 设置 | 图像 | 主代理的视觉观察 | 结果 |
|---|---|---|---|---|
| V1 | 1440x900，浅色，首屏 | `visual/V1-baseline.png`，`visual/V1-0.3.0.png` | 相同的侧栏、网格、字体、配色、地图、操作与事实条；版本与正文不同。 | 通过 |
| V2 | 1440x900，浅色，入口 | `visual/V2-baseline.png`，`visual/V2-0.3.0.png` | 相同的节/表/单元格样式与间距；十三个名称与修订后的拨档内容能够放下。 | 通过 |
| V3 | 1440x900，浅色，增量 | `visual/V3-baseline.png`，`visual/V3-0.3.0.png` | 相同的强调边框、标题与变更列表样式；新内容复用既有卡片与表格组件。 | 通过 |
| V4 | 390x844，浅色，首屏 | `visual/V4-baseline.png`，`visual/V4-0.3.0.png` | 相同的粘性紧凑侧栏、水平导航、单列首屏与移动端字体；没有页面溢出。 | 通过 |
| V5 | 1440x900，深色，首屏 | `visual/V5-baseline.png`，`visual/V5-0.3.0.png` | 相同的深色配色、地图/卡片对比度、控件与网格。 | 通过 |

全部五对都被打开并检查。带有已缓存 Chromium 1243 的 Playwright 以相同设置在隔离上下文中渲染了每一个版本。全部十个场景都有零个页面错误、零个外部请求、有效的片段链接，并且没有文档宽度溢出；`visual/checks.json` 记录限定范围的检查。手册测试通过 3/3，镜像测试通过 31/31；`git diff --check` 通过。

发布命令只是准备。在最新的 D48 指令之下，它们 **未获授权执行**：推送、市场升级、重新安装以及真实主目录安装器运行仍然未执行。在未来的发布授权之后：

```sh
git push origin main
# Then run on each installation using its native Codex and home:
codex plugin marketplace upgrade codex-advisor
codex plugin remove codex-advisor@codex-advisor
codex plugin add codex-advisor@codex-advisor
plugin_dir="$(codex plugin list --json | jq -r '.installed[] | select(.pluginId == "codex-advisor@codex-advisor") | .source.path')"
sh "$plugin_dir/scripts/install-agents.sh"
sh "$plugin_dir/scripts/install-agents.sh" --check
```

在每一侧打开一个全新的交互式会话，并在 `/hooks` 中评审已更改的钩子。Windows shell 命令要求 Git Bash 与一个 Windows 主目录，且不继承一个仅 WSL 的 `CODEX_HOME`。本地提交在验收之后被授权。

## 最终验收

Status: 在主代理检查与一次全新的独立 senior 验收之后，由主代理于 2026-09-26
验收。D47 取消 AC-9；D49 只放弃重复的人工信任检查。在 D48 下交付仅为本地提交。

### 主代理验证

主代理运行了不带限定的 `sh plugins/codex-advisor/scripts/verify.sh`（退出码 0，`/tmp/ca03-final-verify.log`），包括安装、运行时、咨询与钩子。咨询发现 61 个情形：53 个通过，八个仅 Windows 的情形被显式跳过。单独的 Windows 运行通过全部 61 个情形，范围如上。主代理检查了它的输出以及全部新增的 Windows 失败断言。在最终的操作文档澄清之后，镜像检查通过 31/31，手册检查通过 3/3，并且 `git diff --check` 退出码为 0。在完整验证器运行之后没有运行时代码更改。本仓库没有应用程序类型检查。

### 需求扫尾

| ID | 证据与结果 |
|---|---|
| TR-1、TR-4、TR-5、TR-6、TR-7、TR-8 | 第 02 节原则检查：档位名称、候选顺序、宽准入、保留的窄准入、向上地板以及完全失败定义。 |
| TR-2、TR-3、TR-9 | 第 03 节配置/模板比较以及 13/13 条原生路线；配置记录受世代约束的假设。 |
| AC-1、AC-2 | 第 02 节技能与验收数据包保留独立评审以及档位/主代理拨档选择。本次交付另行授权的全新 senior 评审仍然在下面。 |
| AC-3、AC-4 | 第 01 节/P6 与第 04 节：零参数边界、包括压缩/当前回合/最早条目在内的有效历史、实际的空请求工具、拨档断言、全部三个调用方角色以及显式失败；上面的当前咨询复查。 |
| AC-5、AC-6、AC-7 | 第 02/04 节：规范的完整姿态/精简姿态/采纳规则、确切身份选择、字节相等以及负向夹具。 |
| AC-8 | 第 05 节实际的启动/恢复请求、委派排除以及确切的规范输出。 |
| AC-9 | 由 D47 取消；没有完成阻止钩子被随附。 |
| AC-10 | 第 04/05 节：原生派发的自动匹配/缺失推理等级证据，以及咨询的实际请求检查。 |
| AC-11 | 下面的写入点审计以及确定性清理/负向情形；没有钩子写入点。 |
| AC-12 | 第 01 节/P7 与第 05 节的已信任/不受信任证据；最终定义的人工重复由 D49 明确放弃。README、操作与手册保留信任关卡。 |
| EN-1、EN-2、EN-3、EN-4 | 第 03 节：十三个入口、十九个退役名称、升级/拒绝/检查行为、未更改的检查器接口以及表驱动检查。 |
| EN-5、EN-6 | 第 03/04/05 节的规范字节比较、同一角色不变性、没有 Advisor 姿态、委派钩子排除；镜像 31/31。 |
| DR-1、DR-3、DR-4、DR-6、DR-7 | 第 02 节来源检查、规范块、数据包、术语表以及明确的 ADR 取代；grok 车道是 0.4.0。 |
| DR-2 | 第 03 节配置与模板检查；拨档值仍然留在配置以及被允许的模板/冻结手册中。 |
| DR-5 | 第 02–05 节操作节及其孪生文件；当前的 Windows 前提/清理行为已记录。 |
| DR-8、DR-9、DR-10、DR-11 | 第 06 节 README、0.3.0 清单、未更改的市场、五对已检查的视觉对比、未更改的基线，以及仅准备的发布命令。 |
| X-1、X-2 | D48 只允许本地提交；临时安装使用了规定路线；任务以已安装的 0.2.0 入口执行。 |
| X-3、X-4、X-5 | 下面的跨组件写入点/临时状态审计、镜像，以及最终的过时文本搜索；没有无关清理。 |

### 写入点与目标漂移检查

钩子读取输入/配置/会话证据并发出 stdout；它们不创建文件。咨询禁用字节码，只在一个 `TemporaryDirectory` 下写入其模型目录，把原生日志/SQLite/请求追踪路由到该目录，启动一个临时线程，并在目录清理之前终止其进程。它读取调用方会话记录与公开配置；它不读取凭据。正常的宿主初始化仍然是一个已记录的前提。确定性测试行使清理、取消、显式 API 失败以及隔离。

每一个目标漂移条目都对照其所属证据做了检查：

1. 实际咨询模型/推理等级从每一个已记录请求得到验证。
2. 零参数与有效历史重建排除调用方摘要，并包括未完成的回合。
3. 实际请求工具清单为空；只读工具不合格。
4. 会话注入等于一个规范变体加上采纳规则；确切的模型身份选择它，包括未知模型夹具。
5. 主代理 `Stop` 与 worker `SubagentStop` 都没有被注册。
6. 模板姿态相等以及没有自我模型推断通过安装检查。
7. 活动配置只包含所声明的第六代模型。
8. 宽的 `crux` 准入处于活动状态；窄准入仍然被保留；第一轮 `rescue` 需要用户。
9. 升级阶梯保留下一档位、模型级以及同一模型的推理等级地板。
10. 咨询不同于独立验收；本次交付通过了下面单独的全新评审。
11. 运行时临时状态被限定范围并清理；仓库验收记录是任务证据，而不是产品观察机器。
12. 全部五对手册比较都被打开，并且基线哈希未更改。
13. 安装器测试与实况升级夹具移除全部十一个已退役的 0.2.0 名称。
14. 最早有效上下文以及压缩/实况 nonce 情形覆盖的多于一个最近回合窗口。
15. 空工具由实际请求追踪确立，而不是由模型自我报告确立。
16. 安装/更新/发布指令保留 `/hooks`；更早的已信任/不受信任运行已被记录；只有最终定义的重复被放弃。
17. 失败结果不包含建议，并且不满足咨询成功。

最终的 X-5 搜索使用 `rg -n 'ca_(explorer|worker|advisor)_(light|standard(_[mh])?|senior)|first-round pool|senior gate|decision packet|\b(light|standard|senior)\b' plugins/codex-advisor docs/zh README.md -g '!retire.txt' -g '!*.pyc'`。它只返回 README 升级行 183–197；没有剩余被禁止的活动运行时或镜像出现。账本中裁定为 reject 的条目 D11/D12/D15/D23/D30/D35/D39/D40 被与升级阶梯、验收、采纳规则、钩子以及配置做了比较：没有一个被重新引入。历史解释与明确禁止仍然被允许。

### 独立验收与最终处置

用户明确授权已安装的 0.2.0 `ca_advisor_senior` 入口位于 `gpt-6-astra[xhigh]`。原生 `spawn_agent` 使用 `fork_turns=none`，并创建了 `/root/final_senior_acceptance`，线程 `01a0da57-35c6-7e03-965e-ffd6c8cb9fd3`。已安装的检查器退出码为 0，并确认该入口、确切的模型/推理等级、父项 `01a0d989-47e5-7562-9ba3-373aef463838`，以及本仓库工作目录。观察到的权限配置是 `disabled` / `danger-full-access`；只读数据包与未更改的状态是行为证据，而不是被强制的隔离。

全新评审者返回 **就绪，高置信度**，且没有实质性发现。它检查了完整的已跟踪差异、新文件、全部运行时实现与边界测试、两份平台日志、已翻译入口、ADR/裁定一致性、完整手册，以及全部十张已保存的截图。它自己的只读检查覆盖 Python 语法、十三对入口/孪生配置、未更改的手册基线，以及 `git diff --check`（退出码 0）。它没有重复模型调用。主代理确认了实际工具活动，以及全部 76 个限定范围的产品/文档文件在之前/之后匹配的哈希。快照 SHA-256 是 `201b744e713baa0d6772cc703c36bde9e402b2b1ae1fd2773e4518bf6ff54e65`。在本次评审之后，只有任务状态与验收记录发生了更改。

主代理验收所保留的范围。残余证据限度：最终定义的人工信任执行被放弃，而不是被证明；Windows 已认证模型咨询没有被行使；先前的原始实况追踪被有意清理，因此评审使用了被保留的观察；宿主兼容性被限定在已认定的 Codex 0.157.0 路径上。没有执行推送或真实安装更新。

### 清理与本地交付

主代理停止并验证退出了两个其命令路径属于临时产品主目录的守护进程。它随后移除并验证不存在 `ca-hooks-product-amsg5f8z`（包括凭据副本、缓存、会话与追踪）、`ca-hooks-docs-blutphfr`、Windows `ca-hooks-win-ps4wyrza`、`ca-manual-verify-ru_i1erh`、`ca04-baseline-aa25432t`，以及 23 个任务专用的临时日志、指针与评审哈希快照。更早的探测环境已经在它们所记录的检查点被移除。没有剩余匹配的临时进程。仓库任务记录与视觉证据作为交付证据保留；预先存在的 `.agent-discuss/` 与真实安装仍然位于本次更改之外。

该提交包括本任务的产品、文档与验收证据。上面的发布命令仍然只是准备。本地提交标识由主代理在 Git 创建它之后报告。
