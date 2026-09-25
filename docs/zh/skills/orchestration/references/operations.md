# Native 操作

## 安装与发现

插件提供 `codex-advisor:orchestration`；配套安装器提供十三个按档位命名的 native 入口。从已安装 skill 解析脚本：

~~~sh
skill_dir=<directory-containing-SKILL.md>
installer="$skill_dir/../../scripts/install-agents.sh"
runtime_inspector="$skill_dir/../../scripts/inspect-agent-runtime.sh"
sh "$installer" --check-role advisor-mainstay
~~~

首次使用每个必要入口前，先做一次不改文件的选择性检查。
成功结果只缓存到当前任务；安装或配置变更后重新检查。用 `--check` 检查全部入口，或用下表中的选择器重复 `--check-role`。
选择性检查忽略无关的已安装文件。失败时，受影响的调用保持待定，直到安装被核对；独立工作可以继续。

开发时，把 marketplace/插件装进临时 `CODEX_HOME`，把入口装进其 `agents` 目录，并开启新的宿主任务。空的临时 `--target-dir` 可以检查安装，而不触碰活动设置。
只复制必要的连接/认证设置，报告中不要出现凭据，测试结束后删除临时凭据副本。

安装器由清单驱动：清单就是随它一起分发的模板集合，退役列表列出早期版本的入口文件。清单中缺失或有差异的目标文件会被写入并报告为已安装；完全相同的报告为未变更；存在的退役文件按文件名删除并报告为已移除。其余任何文件都不读不写，包括上游 Sol Advisor 文件、无关代理和 primary 配置。每个文件的写入是原子的。`--check` 不写任何东西，在出现漂移（清单文件有差异或缺失）或残留（退役文件仍存在）时失败，并逐项列出。符号链接的目标或祖先、非普通文件目标、非目录祖先、含点号段的路径和文件系统根，都在任何写入之前被拒绝。相对目标相对当前目录解析。已安装入口只由安装器写入；不要手工编辑。

## 选择 native 入口

在用户资源范围内，使用 skill 的分配机制和 [routing-profile.md](routing-profile.md) 中的 dial。任一 primary 都可以选择这些入口。名称说明角色与档位；在有两个模型的档位内，`_m` 是默认候选，`_h` 是更强的备选。Explorer 和 Advisor 入口也可以在不加载 skill 的情况下调用；仅安装并不会形成全局路由默认。

| 职责 | Native 入口 | 安装选择器 | Effort |
|---|---|---|---|
| Explorer，`mainstay`，默认候选 | `ca_explorer_mainstay_m` | `explorer-mainstay-m` | 调用方 |
| Explorer，`mainstay`，更强备选 | `ca_explorer_mainstay_h` | `explorer-mainstay-h` | 调用方 |
| Explorer，`crux`，默认候选 | `ca_explorer_crux_m` | `explorer-crux-m` | `max` |
| Explorer，`crux`，更强备选 | `ca_explorer_crux_h` | `explorer-crux-h` | `xhigh` |
| Explorer，`rescue` | `ca_explorer_rescue` | `explorer-rescue` | 调用方 |
| Worker，`mainstay`，默认候选 | `ca_worker_mainstay_m` | `worker-mainstay-m` | `max` |
| Worker，`mainstay`，更强备选 | `ca_worker_mainstay_h` | `worker-mainstay-h` | `high` |
| Worker，`crux`，默认候选 | `ca_worker_crux_m` | `worker-crux-m` | 调用方 |
| Worker，`crux`，更强备选 | `ca_worker_crux_h` | `worker-crux-h` | 调用方 |
| Worker，`rescue` | `ca_worker_rescue` | `worker-rescue` | 调用方 |
| Advisor，`mainstay` | `ca_advisor_mainstay` | `advisor-mainstay` | 调用方 |
| Advisor，`crux` | `ca_advisor_crux` | `advisor-crux` | `high` |
| Advisor，`rescue` | `ca_advisor_rescue` | `advisor-rescue` | `xhigh` |

每个入口都钉死其模型；Effort 列中的值是模板中钉死的值，"调用方"表示由调用方传入。模板的 `model` 和 `model_reasoning_effort` 优先于 spawn 时传入的值，所以钉死的入口无法到达另一个 effort。保持 primary 设置不变，并尊重明确的模型排除。

## 调用与核验

使用 native spawn 接口，带新上下文。入口把 effort 留给调用方时传入 `reasoning_effort`；钉死的入口不传。每次全新 spawn 都设一个能与兄弟线程区分的短 `task_name`。`message` 的第一行是同一名称，原文纯文本、不加 Markdown 标记，空一行，再接角色数据包：

~~~text
agent_type: ca_worker_crux_m
fork_turns: none
reasoning_effort: <listed-effort>
task_name: wire_http_checks
message: <短名称，空一行，再接 role-contracts.md 中的五段 worker 数据包>
~~~

按所选角色替换入口、effort、短名称和数据包。对不含复制会话的显式数据包使用 `fork_turns: none`；每次 spawn 传入的 `model` 和 `reasoning_effort` 只有在它之下才生效。对调用方选择的入口，始终传入 routing profile 中列出的某个 effort，即使是默认值；否则宿主继承可能替你选。不要通过编辑入口文件或 primary 设置来调整 effort。同一线程上的后续调用沿用该名称；新线程用自己的名称。

要求一次被接受的 native 调用和实际路由证据。可识别的检查器输入不能证明宿主/账户支持。公开的 spawn/details 元数据是权威来源；
对其中省略的字段使用窄检查器，且不得覆盖矛盾：

~~~sh
sh "$runtime_inspector" --agent ca_worker_crux_m --effort <listed-effort> <native-thread-id>
sh "$runtime_inspector" --sessions-dir /absolute/path/to/sessions --agent ca_explorer_rescue --effort <listed-effort> <native-thread-id>
sh "$runtime_inspector" --agent ca_advisor_crux <native-thread-id>
~~~

`--agent` 指定入口。检查器从脚本旁解析出的同名分发模板中读取预期模型和钉死的 effort。对调用方选择的入口，`--effort` 必须传入，它就是预期 effort。对钉死的入口，省略 `--effort`，或传入与钉死值相等的值；不同的值会被拒绝。检查器不判断某个 effort 是否被允许；这由 routing profile 决定。核验角色、模型、effort、线程、父关联、工作目录和观察到的权限。把父标识和工作目录与预期任务比较。检查器恰好读取一份 UUID 匹配的 rollout，只发出白名单元数据，并拒绝缺失、歧义、畸形或冲突的证据。不带 `--agent` 的泛化检查不能证明角色契约。

检查器不证明用户授权、complete failed attempt、升级资格、全新调用、质量或强制隔离。这些要对照任务证据和 native 事件检查。不要从角色自述推断实际设置，也不要为了确认它们而转储提示词和凭据。缺失入口、不受支持的设置、矛盾或缺失证据时，受影响工作明确保持待定，不要静默替换。直接的独立调查可以继续。

通用接口是 `--agent NAME [--effort EFFORT] THREAD_ID`。早期的评审选择选项和按角色选项都会失败，并在诊断中指出 `--agent`。通过 routing profile 选择验收入口。

## 恢复并把实际状态交接出去

只有在实现、常规调试和核验之后，以验收失败或确实无法完成为结果，才计入一次 complete worker attempt。
中间失败的测试或工具错误不算。在选择修复、澄清或 ladder 的某一步之前，先诊断环境、缺失事实、契约、推理和执行者是否合适。不要从环境或契约问题推断能力不足；契约缺口在同一线程上以修正后的契约解决，不是 ladder 的一步。

skill 的 escalation ladder 管辖验收失败。R1 是在同一线程、同一 dial 上发返工工单。返工也失败，且诊断把原因归为能力时，原尝试和返工合计为一次能力失败。把工作移到下一个档位，并在新线程中携带下面的 handoff。除非没有其他选择，否则不要切换失败档位内的模型。除非没有其他选择，下一个 dial 的模型等级不能低于失败的 dial；模型不变时使用更高 effort。R3 把同一模型提档限制为最多一次。按 R4，重大执行问题可以跳过返工，并计为一次能力失败。

路径为 `mainstay` -> `crux` -> `rescue` -> 用户。`rescue` 只能经 `crux` 或用户声明到达。从 `crux` 开始的工作在一次 `crux` 能力失败后到达 `rescue`。环境问题和契约缺口不会让工作沿该路径移动。

同模型、同 effort 的 worker 修正可以使用 native 后续/resume。
任一方向的 effort 变更、模型变更或角色改派，都使用带显式设置和匹配入口的新 native 线程。
探索和建议调用重新开始；independent acceptance 一律重新开始，含 dial 未变的修正之后。带不同请求 effort 的已恢复线程不能满足本策略。

替换写入者之前，结束或停止其冲突活动，并取得可用证据。检查范围内的实际变更，保留有用的部分结果和无关编辑。把这份紧凑 handoff 与角色契约一起交给后继者：

~~~text
OBJECTIVE AND BINDING DECISIONS
<Original task, authorized scope, ownership, retained interfaces, and constraints.>

CURRENT STATE
<Actual changed/new files, useful partial changes, relevant task/source references,
and confirmation that the predecessor no longer writes this scope.>

ATTEMPT AND DIAGNOSIS
<Previous role/model/effort/thread, completed checks, failed acceptance or inability,
reproducible evidence, diagnosed cause, and any unresolved contract gap.>

REMAINING WORK
<Corrections and verification still needed without lowering acceptance conditions.>
~~~

过程咨询使用的 Advisor 没有自己的升级路径。失败的咨询会返回明确失败，不能算作建议或验收。低置信度的 independent-acceptance 裁定会使验收保持待定并交给用户，不会自动触发另一个 dial 的复审。

记录前任/后继标识、观察到的 effort，以及新 spawn 对比后续事件。比较真实标识，而不是标签或散文。缺失或矛盾的转换证据使该转换未核验。全新会话是明确策略，不是主张所有宿主都会使缓存失效，也不是保证节省。

## 调度并检查合并后的工作

记录依赖、拥有的文件/模块、生成输出、核验副作用、验收检查，以及范围内的起始状态。识别需要保留的并发或用户编辑。根据宿主限制和活动代理确定可用槽位；不要创建嵌套 worker 来规避限制。容量未知时，先只用一个 worker 直到确认；若没有可用槽位，把工作保持待定并报告等待。

在容量内派发所有权不相交的独立委派任务。
在检查前置结果、并核对依赖工作所依据的前提之后，再串行依赖任务；不要为了减少运行次数而累积未核实的前提。共享所有权在先前写入者结束后再串行，并用实际状态更新下一份数据包。需要时，在保留其报告和证据之后，通过宿主生命周期释放已完成的代理。

核验批次与工单边界、委派边界分别确定。把共用高成本准备的检查合并，前提是范围仍可理解、失败仍可定位。为每个批次指定一个执行者：primary 本人，或者一个获得完整批次需求、合并后变更和已收集证据的受派者。受派的检查执行使用 Worker 入口；只读的 Explorer 和 Advisor 入口只承担不写盘的检查。

收集每个 worker 的变更、检查、判断调用和缺口。失败、受阻、缺失或不完整的工作及其依赖保持待定；独立工作可以继续。亲自检查完整的合并 diff，含新文件和 worker 撰写的测试。每个核验批次由其执行者运行一次，然后核对覆盖范围、实际输出与当前合并状态，再作验收。相关代码、产物、检查、输入和环境仍支持原结论时，复用该结果；依赖变化、证据缺口、未解释的失败或已识别的风险，则要再次检查。只有 native 事件或活动显示 worker 生命周期重叠时，才声称并行执行；请求本身只确立意图。

## 建议与 independent acceptance

过程咨询不使用数据包。在按调用者与 Advisor 的精确模型标识选择的 full 或 reduced 姿态触发点，以无参数方式调用。使用 routing profile 中的咨询映射，以及 [consult-posture.md](consult-posture.md) 中的规范姿态和 adoption 规则。咨询返回 plan、correction、stop signal 或明确失败。它不授予授权，绝不能代替 independent acceptance。

在 primary 检查 diff 和核验之后，普通工作可以在没有 independent acceptance 的情况下完成。高风险工作或明确的独立评审请求，要求在新线程中把验收数据包发给一个 Advisor 入口。单一档位产出的工作使用该档位的 Advisor 入口；多个档位共同产出的工作使用其中最高档位。primary 自行产出的工作使用不弱于 primary dial 的最低 Advisor dial；没有合格 dial 时，使用最强 Advisor dial。若 routing profile 中没有 primary 的精确模型标识，也使用最强 Advisor dial。风险跟随后果、可逆性和确立正确性的难度，而不是步数、文件数或模型。

捕获范围内状态，spawn 全新的 Advisor 线程，核验设置和工具活动，并检查它是否查看了实际完整 diff 及其发现。咨询、探索、worker 自评和委派的检查执行都不能替代。处理实质性发现，检查并再核验修正，然后即使 dial 未变，也要对修订后的交付物取得新的 independent acceptance。普通模式允许 primary 修正；Architect mode 把修正委派出去。缺失必要评审、低置信度裁定或未解决的实质性发现会使完成保持待定并交给用户。

## 过程咨询

使用 `{}` 调用 `codex_advisor` MCP 服务器的 `process_consultation` 工具。
主会话、执行者和探索者使用同一个调用。工具不接受摘要、提示、路径或档位参数。
安装后的 `.mcp.json` 从插件根目录通过 `scripts/run-python.sh` 启动 Python。
启动器需要 POSIX 命令行，并从 `python3`、`python`、`py -3` 中选择可用的 Python
3.11 或更新版本，使用 UTF-8 协议输出并禁用字节码写入。没有可用解释器时明确失败。
组件只支持已验证的 Codex
版本化插件缓存布局；未知布局会明确失败。Codex 通过 MCP 元数据提供调用者的
线程、会话、轮次和消息项身份。组件读取唯一匹配的会话记录快照，在尚未完成的
咨询项之前截止。宿主的代码执行包装项也可以作为这个边界。

快照保留全部有效原始消息、角色、图片、不透明推理内容和配对的工具调用与结果，
包括调用者实际看到的截断输出。压缩事件用 `replacement_history` 替换此前历史。
组件不使用轮次窗口，不退回摘要，也不恢复已被压缩移除的历史。遇到不支持的回滚、
内容类型、不完整配对、缺失替换历史或身份不一致时，组件返回失败。组件不转发调用者
的工具清单。

路由配置选择调用者层级对应的咨询档位。主会话使用不弱于其实际档位的最低顾问档位；
没有合适档位或模型未知时，使用最强顾问档位。组件使用 Codex 原生认证，绝不自行
读取、复制或传输凭据。组件创建临时 App Server 线程，传入原会话的基础指令，注入
有效原始历史和咨询指令，然后要求返回一个结构化的 `plan`、`correction` 或 `stop`。

传递调用者上下文之前，原生发现进程遍历清单的全部分页，取得每个已配置 MCP 服务器
的名称，然后连同子进程一起退出。发现阶段可能启动已配置服务器，但不接收调用者
上下文；工具和资源描述会被丢弃。第二个原生进程禁用所有已发现名称，确认 MCP 能力
和钩子均为空，并通过临时模型目录与功能设置禁用内置工具。每次实际推理请求都必须
证明模型和推理强度符合预期，并由空的 `additional_tools.tools` 或明确的顶层
`tools=[]` 证明工具集合为空；两处都不得有非空工具集合。每次请求还必须按顺序保留
调用者的完整历史；宿主静默自动压缩会导致上下文失败。缺少请求记录、工具清单不为空或任何档位不匹配，都会使咨询失败。

在调用者已有的会话记录中，工具调用事件表示咨询已经开始。MCP 返回对象中的
`structuredContent.status=succeeded` 且 `isError=false` 表示输出恰好包含一个有效
`kind` 和非空 `advice`，并且全部实际请求的模型与推理强度都与 `expected` 和
`actual` 一致。有效的 `stop` 也是成功结果：调用者必须按建议停止并上报用户。
结果还包含 `callerThreadId` 和 `advisorThreadId`。`status=failed` 且 `isError=true`
表示失败；结果包含 `code`、`message`、`expected`，以及可观察到时的 `actual`，
不包含建议。文本内容重复同一个结构化对象，调用者和会话钩子因此能读取相同结果。
没有终态结果的调用只表示已经开始，不表示成功。只有成功结果才满足调用者的咨询要求。

错误、中止、取消、上下文溢出、空输出、输出格式无效和档位不匹配都会使工作保持待定。
调用者应在下一条可见回复中说明失败，不得把失败呈现为建议，也不得声称咨询完成。
组件不自动重试。MCP 取消通知会终止原生进程树并返回失败。原生执行期限为 180 秒。
模型目录、请求记录、捕获输出、日志和 SQLite 状态都存放在一个临时目录中，并在
调用结束或取消时删除。组件不写入会话标记、仓库文件或凭据文件。

Windows 咨询要求 PATH 中存在原生 `codex.exe`，或在找到的 Codex 启动包装程序旁，
能从官方 npm 包布局中定位唯一的原生执行程序。组件不通过 `.cmd` 包装程序传入
配置参数。Windows 作业对象负责约束原生进程树；约束或清理 API 不可用或执行失败时，
组件会明确返回失败。

两阶段隔离会让每次调用多进行一次原生初始化。正常调用者启动必须已经初始化 Codex
主目录；咨询不负责初始化全新的主目录。宿主会话记录、元数据、模型目录、请求记录
或缓存布局发生变化后，必须重新验证。运行
`sh plugins/codex-advisor/scripts/verify.sh --consultation` 可以通过替代原生执行程序
检查 MCP 边界的确定性行为。这些检查不证明真实路由或已安装宿主行为。

## 钩子

插件从默认位置加载 `hooks/hooks.json`。首次安装之后，应在 `/hooks` 中检查并信任
这些钩子。更新改变钩子定义后，应再次检查。安装不授予信任；宿主跳过尚未信任的钩子，
并在启动时显示指向 `/hooks` 的警告。插件不修改信任状态，也不自行检测未信任状态。

`SessionStart` 注入所选规范姿态段和采纳规则段的原文，包括恢复和压缩之后的启动。
它比较会话的精确模型标识与路由配置中的顾问模型。当前所有顾问档位使用同一个模型，
因此选择姿态不需要推断推理强度。如果这一条件不再成立，缺失选择证据会使工作保持
待定。原生委派身份会排除第二次姿态注入；入口自带姿态。缺失会话身份也会使工作待定。

原生派发后的 `PostToolUse` 自动比较每个 `ca_*` 委派的实际设置与随插件发布的模板
模型和固定推理强度；没有固定值时，使用调用方明确传入的推理强度。固定值优先于派发
参数。匹配时保持静默。缺少调用方推理强度、设置不匹配、证据缺失或冲突时，钩子向
派发会话补充消息，说明受影响工作保持待定。这项比较不需要手动运行检查器。钩子将
原生响应中的任务路径和父会话记录身份关联到唯一子会话头，再读取实际轮次模型与
推理强度。它最多等待两秒，以容许子会话证据落盘。之后尚未观察到的写入不算核验成功。

这些钩子不写文件或持久状态，也不写 Python 字节码，不读取配置或凭据。宿主提供的
会话记录目录必须符合已验证的 `sessions` 布局；宿主事件或会话记录结构变化后，需要
重新验证。插件没有主会话 `Stop` 或执行者 `SubagentStop` 钩子。调用者按咨询姿态
执行，不会被钩子自动拦截结束。咨询组件负责校验咨询结果。

## 观察权限

Explorer 和 Advisor 入口请求只读访问。宿主可能重新施加更宽的父权限。记录实际沙箱策略和权限配置；检查工具活动，以及范围内文件和产物的确切前后状态。

- 仅当宿主强制隔离且观察结果一致时，才声称强制隔离。
- 在更宽权限下，仅当不要求硬隔离、数据包禁止编辑、且范围内状态确认无变更时才继续。报告在观察到的权限下按行为只读运行。
- 权限缺失/冲突、必要隔离不可用，或观察到变更，都会阻止受影响的验收，并且必须报告。

范围内文件未变，不能证明该范围之外没有写入。

## 核验变更

从仓库根目录开始，按改动触及的行为选择检查。编辑某一部分时，跑它对应的聚焦分组：

~~~sh
sh plugins/codex-advisor/scripts/verify.sh --installation
sh plugins/codex-advisor/scripts/verify.sh --runtime
sh plugins/codex-advisor/scripts/verify.sh --consultation
sh plugins/codex-advisor/scripts/verify.sh --hooks
~~~

installation 分组覆盖安装器、十三个入口模板、清单、routing profile 中名称、模型和固定 effort 与模板是否一致，以及完整退役集合。它包含模型不一致和遗漏退役入口的反例夹具。runtime 分组以十三个模板驱动 inspector，并覆盖它的选项、从模板读取的预期、拒绝路径和输出元数据。模板改动同时触及两组，所以直接用不带参数的那次运行。文档改动在这里没有对应分组：检查结构、链接，以及文字是否仍与实际行为相符。

安装分组还检查姿态与规范文本一致、顾问没有姿态段，以及同角色在姿态段之外的正文
一致，并包含对应反例。咨询分组通过替代原生执行程序检查 MCP 边界，覆盖完整上下文、
路由、实际请求校验、隔离、结果、明确失败、取消和临时状态清理。
钩子分组使用固定的 JSON 事件运行随插件发布的命令，检查规范姿态注入、委派排除、
全部入口档位、延迟出现的子会话证据和明确的待定结果。每个告警场景还用关闭钩子的
反例证明断言有效。这些检查不证明已安装宿主的信任状态或真实委派行为。

在最终状态上把不带参数的核验器跑一次。它本身包含四个分组，所以它替代聚焦运行，而不是跟在聚焦运行之后：

~~~sh
sh plugins/codex-advisor/scripts/verify.sh
git diff --check
~~~

公开脚本检查安全安装、角色分配、有界诊断和证据一致性。适用的静态检查是 shell 语法和 JSON/TOML 解析；本项目没有带类型的应用程序。夹具确立解析器和拒绝行为，不确立模型行为。

路由发生变化时，使用临时 `CODEX_HOME`，通过公开安装器安装，并为每个受影响入口各 spawn 一次。只有入口把 effort 留给调用方时才传入 effort，然后对该子线程运行检查器。记录入口、传入的 effort、观察到的模型和 effort、沙箱与权限、子线程、检查器退出状态，以及已植入退役文件的移除结果。这些实时检查确立分发与接线；它们不确立总体质量、成本或稳定性。

从以下一次性最小 native 场景中选择：普通的直接、委派或混合完成，明确的 Architect 委派，按档位探索，complete 对比中间失败，修复或澄清，同一分配下的返工，两个方向的 effort 变更，过程咨询，以及 independent acceptance。运行本次改动可能破坏的场景，并把其余场景记录为未行使。在检查之间复用实际调用和元数据；修正之后重复受影响的检查，而不是整组重跑。在功能验收记录中记下预期和观察行为、native 设置、标识、来源、权限、测试过的修订与宿主，以及未行使的路径。
