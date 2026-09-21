# Native 操作

## 安装与发现

插件提供 `codex-advisor:orchestration`；配套安装器提供十一个按档位命名的 native 入口。从已安装 skill 解析脚本：

~~~sh
skill_dir=<directory-containing-SKILL.md>
installer="$skill_dir/../../scripts/install-agents.sh"
runtime_inspector="$skill_dir/../../scripts/inspect-agent-runtime.sh"
sh "$installer" --check-role advisor-standard
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
| Explorer，light | `ca_explorer_light` | `explorer-light` | 调用方 |
| Explorer，standard，默认候选 | `ca_explorer_standard_m` | `explorer-standard-m` | `max` |
| Explorer，standard，更强备选 | `ca_explorer_standard_h` | `explorer-standard-h` | 调用方 |
| Explorer，senior | `ca_explorer_senior` | `explorer-senior` | 调用方 |
| Worker，light | `ca_worker_light` | `worker-light` | `max` |
| Worker，standard，默认候选 | `ca_worker_standard_m` | `worker-standard-m` | 调用方 |
| Worker，standard，更强备选 | `ca_worker_standard_h` | `worker-standard-h` | `low` |
| Worker，senior | `ca_worker_senior` | `worker-senior` | 调用方 |
| Advisor，light（验收默认） | `ca_advisor_light` | `advisor-light` | `low` |
| Advisor，standard（决策默认） | `ca_advisor_standard` | `advisor-standard` | `medium` |
| Advisor，senior | `ca_advisor_senior` | `advisor-senior` | 调用方 |

每个入口都钉死其模型；Effort 列中的值是模板中钉死的值，"调用方"表示由调用方传入。模板的 `model` 和 `model_reasoning_effort` 优先于 spawn 时传入的值，所以钉死的入口无法到达另一个 effort。保持 primary 设置不变，并尊重明确的模型排除。

## 调用与核验

使用 native spawn 接口，带新上下文。入口把 effort 留给调用方时传入 `reasoning_effort`；钉死的入口不传。每次全新 spawn 都设一个能与兄弟线程区分的短 `task_name`。`message` 的第一行是同一名称，原文纯文本、不加 Markdown 标记，空一行，再接角色数据包：

~~~text
agent_type: ca_worker_standard_m
fork_turns: none
reasoning_effort: xhigh
task_name: wire_http_checks
message: <短名称，空一行，再接 role-contracts.md 中的五段 worker 数据包>
~~~

按所选角色替换入口、effort、短名称和数据包。对不含复制会话的显式数据包使用 `fork_turns: none`；每次 spawn 传入的 `model` 和 `reasoning_effort` 只有在它之下才生效。对调用方选择的入口，始终传入 routing profile 中列出的某个 effort，即使是默认值；否则宿主继承可能替你选。不要通过编辑入口文件或 primary 设置来调整 effort。同一线程上的后续调用沿用该名称；新线程用自己的名称。

要求一次被接受的 native 调用和实际路由证据。可识别的检查器输入不能证明宿主/账户支持。公开的 spawn/details 元数据是权威来源；
对其中省略的字段使用窄检查器，且不得覆盖矛盾：

~~~sh
sh "$runtime_inspector" --agent ca_worker_standard_m --effort xhigh <native-thread-id>
sh "$runtime_inspector" --sessions-dir /absolute/path/to/sessions --agent ca_explorer_senior --effort medium <native-thread-id>
sh "$runtime_inspector" --agent ca_advisor_light <native-thread-id>
~~~

`--agent` 指定入口。检查器从脚本旁解析出的同名分发模板中读取预期模型和钉死的 effort。对调用方选择的入口，`--effort` 必须传入，它就是预期 effort。对钉死的入口，省略 `--effort`，或传入与钉死值相等的值；不同的值会被拒绝。检查器不判断某个 effort 是否被允许；这由 routing profile 决定。核验角色、模型、effort、线程、父关联、工作目录和观察到的权限。把父标识和工作目录与预期任务比较。检查器恰好读取一份 UUID 匹配的 rollout，只发出白名单元数据，并拒绝缺失、歧义、畸形或冲突的证据。不带 `--agent` 的泛化检查不能证明角色契约。

检查器不证明用户授权、complete failed attempt、senior gate 资格、全新调用、质量或强制隔离。这些要对照任务证据和 native 事件检查。不要从角色自述推断实际设置，也不要为了确认它们而转储提示词和凭据。缺失入口、不受支持的设置、矛盾或缺失证据时，受影响工作明确保持待定，不要静默替换。直接的独立调查可以继续。

从 primary 推导评审人选择的做法已退役。`--review-primary-effort` 和 `--select-review-effort` 会失败并给出诊断；选择验收 dial 时不要设 primary 下限。primary 为 `max` 时，验收仍可以用 light 档。0.1.0 的八个按角色选项（`--luna`、`--sol-effort`、`--astra-effort`、`--explorer-effort`、`--sol-explorer-effort`、`--astra-explorer-effort`、`--advisor-effort`、`--reviewer-effort`）已退役，由 `--agent` 取代，并会失败且在诊断中指出 `--agent`。

## 恢复并把实际状态交接出去

只有在实现、常规调试和核验之后，以验收失败或确实无法完成为结果，才计入一次 complete worker attempt。
中间失败的测试或工具错误不算。在选择修复、澄清或 ladder 的某一步之前，先诊断环境、缺失事实、契约、推理和执行者是否合适。不要从环境或契约问题推断能力不足；契约缺口在同一线程上以修正后的契约解决，不是 ladder 的一步。

skill 的 escalation ladder 管辖验收失败：R1 在同一线程、同一 dial 上发返工工单；R2 返工也失败且原因是能力时，在新线程中提档并携带下面的 handoff，取 routing profile 中同一模型的更高 effort 或另一个模型；R3 同一模型最多提档一次；R4 重大执行问题可以跳过返工工单直接换模型，计为一次失败。first-round pool 内两次归因于能力的 complete failure 就是 senior gate，也是一次必须的咨询；Advisor 的裁定决定 senior 入口是否成立。

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

worker 失败本身永远不能把 Advisor 推到其 senior 入口。complete advisory failure 指未回答其问题，或结论被实质性推翻，而不是分歧。诊断它，并在新线程中为同一问题选择收集事实、澄清或另一个 dial；只有报告低置信度的裁定或用户声明才能打开 Advisor 的 senior gate。

记录前任/后继标识、观察到的 effort，以及新 spawn 对比后续事件。比较真实标识，而不是标签或散文。缺失或矛盾的转换证据使该转换未核验。全新会话是明确策略，不是主张所有宿主都会使缓存失效，也不是保证节省。

## 调度并检查合并后的工作

记录依赖、拥有的文件/模块、生成输出、核验副作用、验收检查，以及范围内的起始状态。识别需要保留的并发或用户编辑。根据宿主限制和活动代理确定可用槽位；不要创建嵌套 worker 来规避限制。容量未知时，先只用一个 worker 直到确认；若没有可用槽位，把工作保持待定并报告等待。

在容量内派发所有权不相交的独立委派任务。
在检查前置结果、并核对依赖工作所依据的前提之后，再串行依赖任务；不要为了减少运行次数而累积未核实的前提。共享所有权在先前写入者结束后再串行，并用实际状态更新下一份数据包。需要时，在保留其报告和证据之后，通过宿主生命周期释放已完成的代理。

核验批次与工单边界、委派边界分别确定。把共用高成本准备的检查合并，前提是范围仍可理解、失败仍可定位。为每个批次指定一个执行者：primary 本人，或者一个获得完整批次需求、合并后变更和已收集证据的受派者。受派的检查执行使用 Worker 入口；只读的 Explorer 和 Advisor 入口只承担不写盘的检查。

收集每个 worker 的变更、检查、判断调用和缺口。失败、受阻、缺失或不完整的工作及其依赖保持待定；独立工作可以继续。亲自检查完整的合并 diff，含新文件和 worker 撰写的测试。每个核验批次由其执行者运行一次，然后核对覆盖范围、实际输出与当前合并状态，再作验收。相关代码、产物、检查、输入和环境仍支持原结论时，复用该结果；依赖变化、证据缺口、未解释的失败或已识别的风险，则要再次检查。只有 native 事件或活动显示 worker 生命周期重叠时，才声称并行执行；请求本身只确立意图。

## 建议与 independent acceptance

对主动建议，以及适用计划未覆盖的关键决定、已失效的关键前提、诊断后仍不清楚的失败原因，和两次 complete failure 之后的 senior gate，使用决策数据包。把它发给 routing profile 指定为决策默认的 Advisor 入口。在前提仍成立时复用适用建议。核对其来源并解释实质性分歧；建议不授予授权、否决权，也不改变用户要求。

在 primary 检查 diff 和核验之后，普通工作可以在没有交付建议的情况下完成。高风险工作或明确的独立评审请求，要求在新线程中把验收数据包发给一个 Advisor 入口；routing profile 指定验收默认。两种数据包是同一组 Advisor 入口的两种请求形态；不存在单独的评审人入口。风险跟随后果、可逆性和确立正确性的难度，而不是步数/文件数或模型。

捕获范围内状态，spawn 全新的 Advisor 线程，核验设置和工具活动，并检查它是否查看了实际完整 diff 及其发现。建议、探索、worker 自评和委派的检查执行，都不能替代。处理实质性发现，检查并再核验修正，然后即使 dial 未变，也要对修订后的交付物取得新的 independent acceptance。普通模式允许 primary 修正；Architect mode 把修正委派出去。缺失必要评审或未解决的实质性发现会使完成保持待定。

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
~~~

installation 分组覆盖安装器、入口模板、清单，以及 routing profile 的 dial 与模板是否一致。runtime 分组覆盖 inspector：它的选项、它从模板读到的预期，以及它输出的元数据。模板改动同时触及两组，所以直接用不带参数的那次运行。文档改动在这里没有对应分组：检查结构、链接，以及文字是否仍与实际行为相符。

在最终状态上把不带参数的核验器跑一次。它本身包含两个分组，所以它替代聚焦运行，而不是跟在聚焦运行之后：

~~~sh
sh plugins/codex-advisor/scripts/verify.sh
git diff --check
~~~

公开脚本检查安全安装、角色分配、有界诊断和证据一致性。适用的静态检查是 shell 语法和 JSON/TOML 解析；本项目没有带类型的应用程序。夹具确立解析器和拒绝行为，不确立模型行为。

极小的一次性 native 场景覆盖已声明路径和关键分支：
普通直接/委派/混合完成、明确的 Architect 委派、按档位探索、complete 对比中间失败、修复/澄清、同分配返工、两个方向的 effort 变更，以及 independent acceptance。
用简短的建议问题覆盖复用/已失效建议、分歧，以及具备资格的建议升级。从这组场景里挑出本次改动可能破坏的部分，其余记为未行使。在检查之间复用实际调用和元数据；修正之后重复受影响的检查，而不是整组重来。
在功能验收记录中记下预期/观察行为、native 设置、标识、来源、权限、测试过的修订/宿主，以及未行使的路径。
这些冒烟检查不确立总体质量、成本或稳定性收益。
