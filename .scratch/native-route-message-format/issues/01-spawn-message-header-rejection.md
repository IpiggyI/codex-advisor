# 01 原生审查派发被消息头校验拒绝

Status: resolved

记录日期：2026-10-08。初次记录时仅获准建立工单；用户现已要求排查并修复，并授权本次一次性主目录中的钩子信任绕过探针。

## 现象与影响

在 Codey 的 Fast、Work 会话按钮及历史删除修复任务中，三次原生独立审查派发被 `PreToolUse` 拒绝，未启动审查线程。错误原文如下：

```text
Tool call blocked by PreToolUse hook: Codex Advisor route check: Start message with task_name, a blank line, then Route:.. Tool: collaborationspawn_agent
```

调用入口为 `spawn_agent`，原生角色为 `ca_advisor_crux_m`，请求拨盘为 `gpt-6.1-sol[xhigh]`，`fork_turns` 为 `none`。未产生子线程的实际模型或审查结论。相同主会话中的零参数 `process_consultation` 调用仍成功；该入口不等于原生独立审查派发。

## 已核实的环境与证据

- 插件仓库：`/home/hyy/develop/personal/GitHub/codex-advisor`，核对时基线为 `c28af93`，插件版本 `0.3.3`。
- 当时加载的插件：`/home/hyy/.codex/plugins/cache/codex-advisor/codex-advisor/0.3.3`。
- 仓库与安装缓存的 `scripts/advisor-hooks.py` 内容一致，SHA-256 均为 `5ecb74fc2d486adca280d94c5ef64143b4b8232cc3854bd3d789f902e5413e72`。
- 主会话标识：`01a11a79-27f4-7dd0-bf3c-0dd0cd50322f`。
- 本机会话记录：`/home/hyy/.codex/sessions/2026/10/08/rollout-2026-10-08T15-45-10-01a11a79-27f4-7dd0-bf3c-0dd0cd50322f.jsonl`。
- 不复制完整不透明消息或会话正文；以下仅保留定位字段和形态摘要。

| 调用时间（UTC） | 任务名 | 调用记录行 | 结果记录行 | `message` 字符数 |
| --- | --- | --- | --- | --- |
| 2026-10-08 10:07:21.811 | `fast_tier_acceptance` | 1181 | 1183 | 5496 |
| 2026-10-08 10:09:14.841 | `fast_tier_acceptance` | 1225 | 1227 | 1804 |
| 2026-10-08 11:40:50.139 | `review_session_delete` | 2653 | 2655 | 5412 |

三条调用记录中的 `message` 均只有一行，且以 `gAAAA` 开头。对应 `call_id` 依次为 `call_1117c8d44c7f418c85dcacfd8979acb5`、`call_30a8146b049244ee82b0205d113d651e`、`call_85e8ad584a624f3ca147bf1f48e5735c`。三条结果均报告上述消息头错误。

## 已确认的拒绝点

[`route_gate`](../../../plugins/codex-advisor/scripts/advisor-hooks.py#L241)在原生派发入口读取 `tool_input.message` 与 `tool_input.task_name`，先调用 [`route_line`](../../../plugins/codex-advisor/scripts/advisor-hooks.py#L163)。后者要求前三行为任务名、空行和规范 `Route:` 声明；消息头不匹配时，尚未进入角色、档位、模型和依据的后续校验。

2026-10-08 已使用实际安装的校验器离线回放上述三条记录。三条均复现完全相同的消息头拒绝。保持其余原生派发参数，只将 `message` 换成规范明文声明后，三条均通过本地 `route_gate`。回放没有启动子代理、改动插件或绕过真实派发钩子。

复现命令如下。该命令只读取会话记录并执行本地解析器，不输出消息正文，不进行模型调用。

```bash
python3 - <<'PY'
from pathlib import Path
import json
import runpy
import sys

scripts = Path('/home/hyy/.codex/plugins/cache/codex-advisor/codex-advisor/0.3.3/scripts')
trace = Path('/home/hyy/.codex/sessions/2026/10/08/rollout-2026-10-08T15-45-10-01a11a79-27f4-7dd0-bf3c-0dd0cd50322f.jsonl')
sys.dont_write_bytecode = True
sys.path.insert(0, str(scripts))
hook = runpy.run_path(str(scripts / 'advisor-hooks.py'))
calls = {
    'call_1117c8d44c7f418c85dcacfd8979acb5',
    'call_30a8146b049244ee82b0205d113d651e',
    'call_85e8ad584a624f3ca147bf1f48e5735c',
}
seen = set()
for line in trace.open():
    item = json.loads(line).get('payload', {})
    if item.get('type') != 'function_call' or item.get('call_id') not in calls:
        continue
    args = json.loads(item['arguments'])
    event = {'tool_name': 'collaborationspawn_agent', 'tool_input': args}
    try:
        hook['route_gate'](event)
    except hook['Pending'] as error:
        assert str(error) == 'Start message with task_name, a blank line, then Route:.'
    else:
        raise AssertionError('记录参数未复现预期拒绝')
    valid = dict(args)
    valid['message'] = (
        args['task_name'] + '\n\n'
        'Route: role=advisor tier=crux dial=gpt-6.1-sol[xhigh] '
        'basis=acceptance-mapping ref=isolated-read-only-replay\n\n本地解析器核对。'
    )
    hook['route_gate']({'tool_name': 'collaborationspawn_agent', 'tool_input': valid})
    seen.add(item['call_id'])
    print(args['task_name'] + '：记录参数被拒绝，规范明文参数通过')
assert seen == calls
PY
```

## 初次记录时尚未确认

- `gAAAA` 前缀和单行形态不能单独证明具体编码、加密算法或转换责任方。
- 会话日志中的参数是否与 `PreToolUse` 实际收到的原始参数逐字节相同，尚无钩子输入边界证据。日志序列化、脱敏或展示层转换仍须与真实派发输入区分。
- 未确认转换发生在模型输出、工具参数封装、宿主传输、日志记录还是钩子适配阶段。
- 合法明文通过本地解析器不证明真实宿主派发已经恢复；没有子线程启动成功的证据。

## 后续排查与验收入口

1. 核对当前插件版本、宿主版本和实际钩子脚本，避免把上述 `0.3.3` 快照直接当成当前状态。
2. 沿模型工具调用参数、宿主派发、`PreToolUse.tool_input` 和会话日志四处边界取最小证据。优先记录字符数、行数、摘要及消息头是否满足格式；避免记录完整任务正文或凭据。
3. 对比仓库已有的[原生探针](../../plan-route-reuse-window/probe-host.py)与本次真实调用的工具名和事件结构，检查哪个边界首次出现不透明消息。仅解析 `Route:` 的合成样例不足以覆盖这类问题。
4. 在证据确认责任边界后决定修复位置，保留无效声明被拒绝的契约，不通过删除钩子或无条件放行处理。
5. 修复验收同时覆盖真实宿主的合法派发成功与畸形声明拒绝，并从子线程记录核对角色、模型和推理强度。新增回归须覆盖已确认的实际故障边界。

## 相关记录

- [既有路由校验工单](../../plan-route-reuse-window/issues/02-route-gate.md)已完成；本问题单独记录，不重开其历史验收。
- [既有路由与续用验收](../../plan-route-reuse-window/acceptance.md)。
- [钩子回归入口](../../../tests/verify-hooks.py)。
- Codey 的 `docs/handoffs/2026-10-08-fast-service-tier.md`记录了这些派发对原任务验收的影响；Codey 的用户验收、发布及主会话检查不构成本插件的独立审查恢复证据。

## Comments

2026-10-08：用户要求在本仓库记录此问题，后续再排查。本轮仅建立待排查工单，未修改产品代码、安装缓存或既有问题记录。

2026-10-08：开始修复。当前基线仍为 `c28af93`，宿主为 `codex-cli 0.161.0`，仓库和实际安装的钩子摘要均与初始记录一致。三条历史参数离线重放均被相同消息头检查拒绝。

### 本次已核实的原因

已运行 `python3 .scratch/native-route-message-format/probe-host.py --allow-hook-trust-bypass --output .scratch/native-route-message-format/host-before.json`。探针从临时本地市场安装插件和入口，包装器只记录输入形态，再原样调用产品脚本。它不复制凭据，也不连接模型服务。结果见 [宿主边界证据](../host-before.json)。

- 三条历史参数从本地响应服务到 `PreToolUse.tool_input` 再到会话记录，消息摘要、长度和行数完全一致，均被旧消息头检查拒绝。
- 三条规范明文对照能启动 `ca_advisor_crux_m`，实际拨盘均为 `gpt-6.1-sol[xhigh]`；但其消息也原样进入子线程的 `agent_message.encrypted_content`，未成为普通文本内容块。
- 把一条历史参数的入口改为不受插件准入限制的 `default` 后，宿主能启动子线程，并将原始不透明消息逐字节放入同一内容块。插件将宿主的不透明载荷字段当作明文路由头解析，是已核实的不兼容点。
- 钩子边界的会话快照已包含当前 `function_call`、`call_id` 和此前的可见助手消息；事件同时提供 `turn_id` 和 `tool_use_id`。这些字段允许声明与当前回合和实际调用绑定。
- 尚未核实历史消息在模型服务链的哪个位置生成或转换。回放不能证明三次历史钩子输入，也不能证明模型解密成功；这些限制不影响上面已直接观测到的接口不兼容结论。

### 修复与验收范围

路由声明迁移到每次派发前的可见助手消息，并明确工具和目标。钩子将它与本回合唯一的当前调用、事件参数和目标绑定；正文保持原样。声明缺失、畸形、陈旧、目标不符、错拨盘、无效依据以及超时续用都继续拒绝。三种入口共同修改，不添加持久化准入状态。

主会话执行以下检查；独立审查在这些检查完成后进行。

| 检查 | 覆盖范围 | 执行节点 |
| --- | --- | --- |
| `python3 tests/verify-routing.py` | 不透明消息、声明绑定、原有拨盘和续用限制 | 先证实新增回归失败，再验证修复 |
| 原生隔离回归探针 | 三种工具的合法与拒绝路径、消息摘要、子线程身份及拨盘 | 完成实现后 |
| `sh tests/verify.sh` | 仓库完整验证 | 最终代码状态 |
| `python3 tests/test_shipped_wording.py`、`python3 tests/test_zh_mirror.py`、文档链接及 `git diff --check` | 发布措辞、镜像及结构 | 最终文档状态 |

原生探针的临时主目录、配置和进程在结束时清理。真实安装缓存、钩子信任状态及已有未跟踪文件保持原状；本轮未获准提交或发布。

### 主会话验证结果

- 钩子先确认本回合唯一的当前调用及其完整参数，再读取紧邻调用的可见助手消息。声明显式携带工具和目标；原生任务正文不参加路由解析。
- 新增回归 `RoutingGate.test_opaque_message_with_bound_visible_route` 在修改前因旧消息头拒绝而失败，修改后通过。原生回归换回 `c28af93` 的钩子也在合法不透明派发处失败，见 [原生失败证据](../host-red.log)。
- `sh tests/verify.sh` 在最终生命周期修正后退出 0，含 19 项路由测试及其参数化负例。完整结果见 [验证日志](../verify.log)；8 项 Windows 专用检查按环境跳过。
- `python3 tests/verify-routing-host.py --allow-hook-trust-bypass --output .scratch/native-route-message-format/host-after.json` 退出 0。[11 项原生场景](../host-after.json)覆盖三种工具的拒绝和合法路径，以及实际角色、拨盘和载荷摘要。
- 在同一宿主回归中追加三条历史载荷，只给重复任务名加唯一后缀，并在调用前提供匹配的可见声明。三条均启动 `ca_advisor_crux_m`，实际为 `gpt-6.1-sol[xhigh]`，子线程的不透明载荷摘要与历史消息相同。最终生命周期修正后重新运行，共 14 项场景通过，见 [历史载荷回归](../historical-host-after.json)和[结果摘要](../historical-host.log)。可通过 `python3 .scratch/native-route-message-format/replay-historical.py --allow-hook-trust-bypass` 重现；该入口仍须有用户对隔离钩子信任绕过的授权。
- 中文镜像检查为 41/41，发布措辞检查为 66/66；54 个本地文档链接目标存在，`git diff --check` 通过。镜像中未涉及本次修改的既有英文术语保持原样。
- 主会话已检查全部差异及新增宿主回归脚本。独立验收尚未完成，不能将本地固定响应服务的结果当作真实模型解密或审查成功。

### 独立审查与生命周期修正

用户另行授权在一次性主目录中安装当前修复，临时绕过该进程的钩子信任，用 `gpt-6-astra[xhigh]` 进行真实模型只读独立审查。真实安装与信任配置不变。第一次因临时环境关闭代码执行模式而未核实；第二次成功派发并读取材料，但超过等待上限，没有验收结论。这两次均未计为通过。

第三次独立审查完成，见 [审查结论](../review-attempt-3.md)和[宿主证据](../review-attempt-3-evidence.json)。顾问线程为 `01a11bc0-64ac-7ab2-ac02-fce51a6de54c`，实际入口为 `ca_advisor_rescue_h`，拨盘为 `gpt-6-astra[xhigh]`，沙箱只读，审批策略为 `never`。顾问执行 11 次工具调用，审查前后 10 个范围内文件摘要一致。

顾问在实际解析逻辑中发现：当前调用没有结果记录时，调用之后出现回合完成、中断、新回合或压缩记录仍可能接受旧事件。原生宿主是否会投递该时序尚未验证。主会话已补充调用之后的生命周期检查；三种入口分别覆盖 `turn_context`、`compacted`、`task_started`、`task_complete`、`turn_aborted`。新增测试修改前失败，见 [失败证据](../lifecycle-red.log)，修正后的全量和原生回归均通过。

最终验收将使用新线程检查完整修订版本。`host-after.json` 对应较早的 11 项场景；最终钩子的宿主验证以 `historical-host-after.json` 为准。

第四次审查核实调用之后的缺口已关闭，又复现了同类事件出现在调用之前的缺口，见 [审查结论](../review-attempt-4.md)和[宿主证据](../review-attempt-4-evidence.json)。顾问线程为 `01a11bd0-4803-76c0-8e1f-91e2e2d5c8d8`，实际入口、拨盘、只读沙箱及审批策略与第三次一致，执行 15 次工具调用，范围摘要仍为 10/10 一致。

主会话已补齐当前回合的有效性检查：从本回合上下文到当前调用之间，只要出现新的回合开始、完成或中断事件，就拒绝调用。结束事件之后新写的声明也不能恢复准入；正常新回合仍允许。新增回归覆盖三入口、三种事件及声明前后两个位置，修改前 18 个子例失败，见 [活动回合失败证据](../active-turn-red.log)。修正后完整验证的 19 项路由测试及原生 14 项场景均通过。最终版本将另开线程验收。

### 最终验收

第五次派发因宿主漏写可见路由声明而被准入钩子拒绝，未启动顾问，未计为验收。第六次使用新线程完成，结论为可验收，见 [完整结论](../review-result.md)和[实际执行证据](../review-host-evidence.json)。

- 顾问线程为 `01a11be0-3776-70a1-9da0-5ccc80fec593`，父线程为 `01a11bde-d170-7bc0-9409-562f336b0e72`。主会话已核对原生派发的 `fork_turns=none`、实际入口 `ca_advisor_rescue_h`、实际拨盘 `gpt-6-astra[xhigh]`、只读沙箱、审批策略 `never`，以及调用前准入和调用后身份确认。
- 顾问执行 10 次工具调用，读取全部实际差异及新增脚本。审查前后 10 个范围内文件摘要一致；工具活动未写入、实施或再次委派。主会话在采纳结论前再次核对了摘要和执行记录。
- 独立解析器检查为 93/93；调用后 15 个边界子例和调用前 18 个子例全部拒绝，正常新回合与压缩后新声明仍通过。宿主验证器的七类负例均触发失败。两次具体发现均已关闭，没有未解决的实质问题。
- 最终主会话全量验证通过，包含 19 项路由测试；原生 14 项场景及三条历史载荷摘要检查通过。独立复核中文镜像 41/41、发布措辞 66/66、差异空白检查均通过。8 项 Windows 专用检查按环境跳过。
- 隔离审查启动器已报告正常退出并删除临时安装、配置和认证副本。真实安装钩子的摘要仍为初始记录值。本轮未提交、推送、发布或更新真实安装。
- 保留根因、失败回归、最终回归和独立审查证据，以及本地固定响应服务的复现脚本。审查结束后仅更新本工单的状态和结论，产品范围保持审查时的摘要。

兼容性结论限定为本次 `codex-cli 0.161.0` 的已执行路径。历史载荷的具体生成或转换责任方、历史载荷的真实模型解密、原生宿主是否投递上述异常生命周期时序、Windows 路由及现有安装恢复均未验证。宿主预调用日志刷新、回合身份、工具格式或消息传输改变时，须重新执行原生回归。

完成前流程咨询成功，实际拨盘为 `gpt-6-astra[xhigh]`，咨询线程为 `01a11be8-d52a-7e51-abf9-dda3fc1ab171`。建议在记录清理结果和验证边界后收尾，并复用仍然有效的验证；主会话采纳。最终 67 个本地文档链接目标存在，差异空白检查通过。一次性真实审查启动器及重复原始日志已删除；三类探针与审查临时目录、隔离进程均无残留，任务目录无字节码缓存。原有 `.agent-discuss/` 和两份咨询审计补丁保持原状。

### 发布与两侧部署

2026-10-08，椰椰追加授权“提交并部署到两侧”。版本更新为 `0.3.4`，通过 `origin` 发布后，分别升级 WSL 和 Windows 的 GitHub 市场，安装、重装插件并运行配套安装器。真实信任配置保持用户管理；既有会话重载不由文件一致性证明。此前的未发布结论是修复验收时的状态，部署结果以本节后续记录为准。

发布前流程咨询成功，实际为 `gpt-6-astra[xhigh]`，顾问线程为 `01a11bf3-74c3-7213-93c6-565b3d6853c9`。建议补齐补丁版本材料，复用有效功能验收，只提交任务文件和必要证据，先推送再部署两侧，保留缓存占用或未验证边界；主会话采纳。

发布前已重新获取远端，`HEAD` 与 `origin/main` 均为 `c28af93`，没有其他未发布提交。两侧原生宿主均为 `codex-cli 0.161.0`，已安装插件均为 `0.3.3`，市场均来自 `https://github.com/IpiggyI/codex-advisor.git`。Windows 探测进程先移除继承的 WSL `CODEX_HOME`，再检查 Windows 用户和系统值，确认原生目录为 `C:\Users\Shy\.codex`，命令由 `D:\Environment\nodejs\node_global\codex.ps1` 提供，`sh` 为 Git for Windows 的原生启动器。

发布材料只增加版本与手册说明，没有改变已验收的运行逻辑。版本手册 3/3、成品措辞 66/66、中文镜像 41/41 均通过；新手册 14 个链接、12 个唯一锚点通过解析检查，冻结的 `0.3.3` 手册逐字节未变，`git diff --check` 通过。新页面沿用原样式，未做浏览器视觉验收。
