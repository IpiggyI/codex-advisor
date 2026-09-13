# Native 操作

## 安装与发现

插件提供 `codex-advisor:orchestration`；配套安装器提供八个钉死模型的 native 入口。从已安装 skill 解析脚本：

~~~sh
skill_dir=<directory-containing-SKILL.md>
installer="$skill_dir/../../scripts/install-agents.sh"
runtime_inspector="$skill_dir/../../scripts/inspect-agent-runtime.sh"
sh "$installer" --check-role advisor
~~~

首次使用每个必要角色前，先做一次不改文件的选择性检查。
成功结果只缓存到当前任务；安装或配置变更后重新检查。用 `--check` 检查全部角色，或按下表重复选择器。
选择性检查忽略无关的已安装角色。失败时，受影响的调用保持待定，直到安装被核对；独立工作可以继续。

开发时，把 marketplace/插件装进临时 `CODEX_HOME`，把角色装进其 `agents` 目录，并开启新的宿主任务。空的临时 `--target-dir` 可以检查安装，而不触碰活动设置。
只复制必要的连接/认证设置，报告中不要出现凭据，测试结束后删除临时凭据副本。

安装器在写入前预检目标。完全相同的文件保持不变；已修改、冲突、非普通文件，以及符号链接文件或其祖先会被拒绝。
含点号段的路径和文件系统根会被拒绝。相对目标相对当前目录解析。检查模式既不创建目录也不改文件。
更新后的模板视为与已安装副本冲突：先检查并明确核对，再重试。不会自动覆盖、迁移、删除另一套安装，也不会改写 primary 配置。

## 选择 native 入口

在用户资源范围内使用 skill 的分配策略。任一 primary 都可以选择这些入口；安装名称区分模型和职责，不是额外档位。Explorer 和判断入口也可以在不加载 skill 的情况下调用；仅安装并不会形成全局路由默认。

| 职责 | Native 入口 | 安装选择器 | 检查器选项 | 允许的 effort |
|---|---|---|---|---|
| light worker | `codex_advisor_luna_implementer` | `luna` | `--luna` | `max` |
| standard worker | `codex_advisor_sol_implementer` | `sol` | `--sol-effort` | `high`、`xhigh`，含首次 |
| senior worker | `codex_advisor_astra_implementer` | `astra` | `--astra-effort` | `medium`、`high`；具备资格后可用 `xhigh` |
| light 或偏好的实质性探索 | `codex_advisor_luna_explorer` | `explorer` | `--explorer-effort` | light 用 `high`；其余用 `max` |
| 直接的实质性探索 | `codex_advisor_sol_explorer` | `sol-explorer` | `--sol-explorer-effort` | `medium`、`high` |
| 直接的实质性探索 | `codex_advisor_astra_explorer` | `astra-explorer` | `--astra-explorer-effort` | `medium`、`high` |
| senior 决策建议 | `codex_advisor_astra_advisor` | `advisor` | `--advisor-effort` | `medium`、`high`；具备资格后可用 `xhigh` |
| senior independent acceptance | `codex_advisor_astra_reviewer` | `reviewer` | `--reviewer-effort` | `medium`、`high`；具备资格后可用 `xhigh` |

Luna 入口钉死 `gpt-5.6-luna`，Sol 入口钉死 `gpt-5.6-sol`，Astra 入口钉死 `gpt-6-astra`。只有 Luna worker 固定 `model_reasoning_effort=max`；
其余模板省略该字段，以便调用方选择生效。保持 primary 设置不变，并尊重明确的模型排除。Luna 探索是大多数实质性调查的偏好，不是使用 Sol 或 Astra 的强制前置。

## 调用与核验

使用 native spawn 接口，带显式 effort 和新上下文：

~~~text
agent_type: codex_advisor_sol_implementer
fork_turns: none
reasoning_effort: xhigh
message: <five-part worker packet from role-contracts.md>
~~~

按所选角色替换入口、effort 和数据包。即使 effort 看起来像默认值，也始终传入；否则宿主继承可能替你选。
对不含复制会话的显式数据包使用 `fork_turns: none`。
首次 Sol worker `xhigh` 不需要失败记录，也不需要单独的用户选择。Astra `xhigh` 需要 skill 中该角色策略下的相关 complete failure。
不要通过编辑角色文件或 primary 设置来调整 effort。

要求一次被接受的 native 调用和实际路由证据。可识别的检查器输入不能证明宿主/账户支持。公开的 spawn/details 元数据是权威来源；
对其中省略的字段使用窄检查器，且不得覆盖矛盾：

~~~sh
sh "$runtime_inspector" --sol-effort xhigh <native-thread-id>
sh "$runtime_inspector" --sessions-dir /absolute/path/to/sessions --sol-explorer-effort medium <native-thread-id>
sh "$runtime_inspector" --reviewer-effort medium <native-thread-id>
~~~

传入实际选择的 effort（`--luna` 后面不要跟 effort 参数）。核验角色、模型、effort、线程、父关联、工作目录和观察到的权限。把父标识和工作目录与预期任务比较。
检查器恰好读取一份 UUID 匹配的 rollout，只发出白名单元数据，并拒绝缺失、歧义、畸形或冲突的证据。不带角色选项的泛化检查不能证明角色契约。

检查器不证明用户授权、complete failed attempt、`xhigh` 资格、全新调用、质量或强制隔离。这些要对照任务证据和 native 事件检查。不要从角色自述推断实际设置，也不要为了确认它们而转储提示词和凭据。缺失角色、不受支持的设置、矛盾或缺失证据时，受影响工作明确保持待定，不要静默替换。直接的独立调查可以继续。

从 primary 推导评审人选择的做法已退役。`--review-primary-effort` 和 `--select-review-effort` 会失败并给出诊断；使用显式 `--reviewer-effort`，不要设 primary 下限。primary 为 `max` 时，评审仍可以是 `medium`。

## 恢复并把实际状态交接出去

只有在实现、常规调试和核验之后，以验收失败或确实无法完成为结果，才计入一次 complete worker attempt。
中间失败的测试或工具错误不算。在选择修复、澄清、返工、调整 effort 或接管之前，先诊断环境、缺失事实、契约、推理和执行者是否合适。不要从环境或契约问题推断能力不足。

同模型、同 effort 的 worker 修正可以使用 native 后续/resume。
任一方向的 effort 变更、模型变更或角色改派，都使用带显式设置和匹配入口的新 native 线程。
探索和建议调用重新开始；independent acceptance 一律重新开始，含 effort 未变的修正之后。带不同请求 effort 的已恢复线程不能满足本策略。

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

相关的 complete worker failure 可以使同一工作的 Astra worker `xhigh` 具备资格，含接管。worker 失败本身永远不能使 Advisor `xhigh` 具备资格。
complete advisory failure 指未回答其问题，或结论被实质性推翻，而不是分歧。诊断并把该证据带到同一问题上、已具备资格的更高 effort 建议尝试。

记录前任/后继标识、观察到的 effort，以及新 spawn 对比后续事件。比较真实标识，而不是标签或散文。缺失或矛盾的转换证据使该转换未核验。全新会话是明确策略，不是主张所有宿主都会使缓存失效，也不是保证节省。

## 调度并检查合并后的工作

记录依赖、拥有的文件/模块、生成输出、核验副作用、验收检查，以及范围内的起始状态。识别需要保留的并发或用户编辑。根据宿主限制和活动代理确定可用槽位；不要创建嵌套 worker 来规避限制。容量未知时，先只用一个 worker 直到确认；若没有可用槽位，把工作保持待定并报告等待。

在容量内派发所有权不相交的独立委派任务。
在检查前置结果并重跑关键检查之后，再串行依赖任务。共享所有权在先前写入者结束后再串行，并用实际状态更新下一份数据包。需要时，在保留其报告和证据之后，通过宿主生命周期释放已完成的代理。

收集每个 worker 的变更、检查、判断调用和缺口。失败、受阻、缺失或不完整的工作及其依赖保持待定；独立工作可以继续。检查完整的合并 diff，含新文件和 worker 撰写的测试。在验收前重跑有意义的检查并核对证据。只有 native 事件或活动显示 worker 生命周期重叠时，才声称并行执行；请求本身只确立意图。

## 建议与 independent acceptance

对主动建议，以及适用计划未覆盖的关键决定、已失效的关键前提，或诊断后仍不清楚的失败原因，使用决策数据包。
在前提仍成立时复用适用建议。核对其来源并解释实质性分歧；建议不授予授权、否决权，也不改变用户要求。

在 primary 检查 diff 和核验之后，普通工作可以在没有交付建议的情况下完成。高风险工作或明确的独立评审请求，要求单独的评审人入口和评审数据包。风险跟随后果、可逆性和确立正确性的难度，而不是步数/文件数或模型。

捕获范围内状态，spawn 全新评审人，核验设置和工具活动，并检查它是否查看了实际完整 diff 及其发现。建议、探索和 worker 自评不能替代。处理实质性发现，检查并再核验修正，然后即使 effort 未变，也要对修订后的交付物取得新的 independent acceptance。普通模式允许 primary 修正；Architect mode 把修正委派出去。缺失必要评审或未解决的实质性发现会使完成保持待定。

## 观察权限

Explorer、Advisor 和 Independent reviewer 请求只读访问。宿主可能重新施加更宽的父权限。记录实际沙箱策略和权限配置；检查工具活动，以及范围内文件和产物的确切前后状态。

- 仅当宿主强制隔离且观察结果一致时，才声称强制隔离。
- 在更宽权限下，仅当不要求硬隔离、数据包禁止编辑、且范围内状态确认无变更时才继续。报告在观察到的权限下按行为只读运行。
- 权限缺失/冲突、必要隔离不可用，或观察到变更，都会阻止受影响的验收，并且必须报告。

范围内文件未变，不能证明该范围之外没有写入。

## 核验变更

从仓库根目录开始，编辑时用聚焦检查，然后跑完整套件：

~~~sh
sh plugins/codex-advisor/scripts/verify.sh --installation
sh plugins/codex-advisor/scripts/verify.sh --runtime
sh plugins/codex-advisor/scripts/verify.sh
git diff --check
~~~

公开脚本检查安全安装、角色分配、有界诊断和证据一致性。适用的静态检查是 shell 语法和 JSON/TOML 解析；本项目没有带类型的应用程序。夹具确立解析器和拒绝行为，不确立模型行为。

用极小的一次性 native 场景覆盖已声明路径和关键分支：
普通直接/委派/混合完成、明确的 Architect 委派、按档位探索、complete 对比中间失败、修复/澄清、同分配返工、两个方向的 effort 变更，以及 independent acceptance。
用简短的建议问题覆盖复用/已失效建议、分歧，以及具备资格的建议升级。在检查之间复用实际调用和元数据。
在功能验收记录中记下预期/观察行为、native 设置、标识、来源、权限、测试过的修订/宿主，以及未行使的路径。
这些冒烟检查不确立总体质量、成本或稳定性收益。
