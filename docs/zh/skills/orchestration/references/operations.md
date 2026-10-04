# Native 操作

每次原生派发之前阅读本文件，包括独立验收派发；向已有线程送入工作之前也要阅读。

## 检查入口

插件提供 `codex-advisor:orchestration`；配套安装器提供十七个按档位命名的 native 入口。从已安装 skill 解析脚本：

~~~sh
skill_dir=<directory-containing-SKILL.md>
installer="$skill_dir/../../scripts/install-agents.sh"
runtime_inspector="$skill_dir/../../scripts/inspect-agent-runtime.sh"
sh "$installer" --check-role advisor-mainstay-m
~~~

首次使用每个必要入口前，先做一次不改文件的选择性检查。成功结果只缓存到当前任务；安装或配置变更后重新检查。用 `--check` 检查全部入口，或用选择器重复 `--check-role`：选择器是去掉 `ca_`、并把下划线换成连字符的入口名，因此 `ca_worker_crux_m` 变为 `worker-crux-m`。选择性检查忽略无关的已安装文件。失败时，受影响的调用保持待定，直到安装被核对；独立工作可以继续。

Explorer 和 Advisor 入口也可以在不加载 skill 的情况下调用；仅安装并不会形成全局路由默认。

## 派发

使用原生派发接口，带新上下文；探索调用总是开启新线程。入口把推理强度留给调用方时传入 `reasoning_effort`；固定强度的入口不传。每次全新派发都把 `task_name` 设为一个能与兄弟线程区分的短名称。`message` 的第一行是同一名称，原文纯文本、不加 Markdown 标记，空一行，写下述路由声明，再空一行，接角色数据包：

~~~text
agent_type: ca_worker_crux_m
fork_turns: none
task_name: wire_http_checks
message: <短名称，空一行，路由行，空一行，五段工作代理数据包>
~~~

按所选角色替换入口、effort、短名称和数据包。对不含复制会话的显式数据包使用 `fork_turns: none`；每次 spawn 传入的 `model` 和 `reasoning_effort` 只有在它之下才生效。对调用方选择的入口，始终传入 routing profile 中列出的某个 effort，即使是默认值；否则宿主继承可能替你选。模板的 `model` 和 `model_reasoning_effort` 优先于 spawn 时传入的值，所以钉死的入口无法到达另一个 effort。不要通过编辑入口文件或 primary 设置来调整 effort。已安装入口只由安装器写入；不要手工编辑。

## 声明每次路由

使用下列单行格式。角色、档位、型号和单个推理强度取自路由配置：

~~~text
Route: role=<角色> tier=<档位> dial=<型号>[<强度>] basis=<种类> ref=<证据引用>
~~~

`mainstay` 省略 `basis` 和 `ref`。其他档位需要非空引用，并从下表选取依据种类：

| 角色 | `crux` 依据 | `rescue` 依据 |
|---|---|---|
| 工作代理或探索代理 | `key-difficulty`、`failure`、`user-declaration` | `failure`、`user-declaration` |
| 验收顾问 | `acceptance-mapping`、`user-declaration` | `acceptance-mapping`、`user-declaration` |

`key-difficulty` 引用已识别的约束；`failure` 引用失败尝试及诊断；`user-declaration` 引用用户声明；`acceptance-mapping` 引用验收范围和路由配置中的映射。仅声明型号不授权 `rescue`。独立验收按其映射选档，即使这是该顾问的第一次调用。

向工作线程调用 `followup_task` 或 `send_message` 时，`message` 从路由行开始，空一行，再接数据包或修正。两种调用之前都检查[续用窗口](recovery.md#保留或更换线程)；新工单还需写明共享区域以及确实需要已有上下文的原因。目标可用 UUID、规范任务路径或相对任务路径。钩子要求目标在调用者所属宿主会话中唯一匹配；无法解析或存在歧义时拒绝。探索调用和独立验收使用新线程。发给已识别的主代理或非插件入口的消息不需要路由。

`PreToolUse` 钩子拒绝缺失或格式错误的声明、入口与档位或拨盘冲突、未列出的强度、错误依据种类，以及超窗或缺少有效宿主证据的工作线程续用。检查通过时输出路由确认。程序核对依据格式；依据真假、任务适配、用户授权和所选档位是否为最低兼容档位，由调用者对照任务记录判断。钩子从目标会话记录读取实际拨盘和活动时间，不写持久状态。

## 读取派发检查

`PostToolUse` 钩子把每个 `ca_*` 派发与其随插件发布的模板中的模型和钉死 effort 比较，或与调用方明确传入的 effort 比较；钉死的 effort 优先于 spawn 参数。它还对照宿主记录检查子线程的角色、父级、会话和任务路径。匹配时，钩子向发起 spawn 的会话添加一行确认：身份、模型和 effort 与宿主记录一致，工作目录和权限未检查。缺少调用方 effort、设置不匹配，或证据缺失或冲突时，钩子添加一条消息，说明受影响工作保持待定。派发到任何其他入口都不会收到消息。对 `ca_*` 派发而言，没有消息表示钩子没有运行，例如因为它未被信任；该派发属于未检查，而不是已核验。

路由确认和实际拨盘确认分别证明不同事实。检查器通过不能证明调用前的路由检查已执行。缺少路由确认时，手动检查声明和准入条件，并把自动阻断标为未核实。新增或变更的钩子需要用户在 `/hooks` 中评审信任。被跳过或执行失败的钩子不能保证阻断。

## 核验路由证据

要求一次被接受的 native 调用和实际路由证据。可识别的检查器输入不能证明宿主/账户支持。对每次派发核验角色、模型、effort、线程、父关联、工作目录和观察到的权限；把父标识和工作目录与预期任务比较。公开的 spawn/details 元数据是权威来源；对其中省略的字段使用窄检查器，且不得覆盖矛盾。`ca_*` 派发没有显示钩子消息时，以及 native 元数据省略了工作目录或权限时（钩子从不检查这两项），亲自运行检查器：

~~~sh
sh "$runtime_inspector" --agent ca_worker_crux_h --effort <listed-effort> <native-thread-id>
sh "$runtime_inspector" --sessions-dir /absolute/path/to/sessions --agent ca_explorer_rescue --effort <listed-effort> <native-thread-id>
sh "$runtime_inspector" --agent ca_advisor_crux_h <native-thread-id>
~~~

通用接口是 `--agent NAME [--effort EFFORT] THREAD_ID`。`--agent` 指定入口。检查器从脚本旁解析出的同名分发模板中读取预期模型和任何钉死的 effort。对调用方选择的入口，`--effort` 必须传入，它就是预期 effort。对钉死的入口，省略 `--effort`，或传入与钉死值相等的值；不同的值会被拒绝。检查器不判断某个 effort 是否被允许；这由 routing profile 决定。检查器恰好读取一份 UUID 匹配的 rollout，只发出白名单元数据，并拒绝缺失、歧义、畸形或冲突的证据。不带 `--agent` 的泛化检查不能证明角色契约。

检查器不证明用户授权、complete failed attempt、升级资格、全新调用、质量或强制隔离。这些要对照任务证据和 native 事件检查。不要从角色自述推断实际设置，也不要为了确认它们而转储提示词和凭据。缺失入口、不受支持的设置、矛盾或缺失证据时，受影响工作明确保持待定，不要静默替换。直接的独立调查可以继续。

## 在容量内调度

记录范围内的起始状态和每次派发所依据的验收检查，并识别需要保留的并发或用户编辑。根据宿主限制和活动代理确定可用槽位。容量未知时，先只用一个 worker 直到确认；若没有可用槽位，把工作保持待定并报告等待。受派的检查执行使用 Worker 入口；只读的 Explorer 和 Advisor 入口只承担不写入任何内容的检查。需要时，在保留其报告和证据之后，通过宿主生命周期释放已完成的代理。只有 native 事件或活动显示 worker 生命周期重叠时，才声称并行执行；请求本身只确立意图。

## 观察权限

Explorer 和 Advisor 入口请求只读访问。宿主可能重新施加更宽的父权限。记录实际沙箱策略和权限配置；检查工具活动，以及范围内文件和产物的确切前后状态。

- 仅当宿主强制隔离且观察结果一致时，才声称强制隔离。
- 在更宽权限下，仅当不要求硬隔离、数据包禁止编辑、且范围内状态确认无变更时才继续。报告在观察到的权限下按行为只读运行。
- 权限缺失/冲突、必要隔离不可用，或观察到变更，都会阻止受影响的验收，并且必须报告。

范围内文件未变，不能证明该范围之外没有写入。
