# 咨询空工具集合兼容性验收

日期：2026-10-12。基线：`51bcac15121cfe20ed08bbcba6fe3698b38835c1`。

## 范围与原因

用户报告 Windows 咨询反复失败，消息为 `Actual consultation request did not prove an empty tool set.`。本轮只修复仓库中的请求校验，更新相应检查与维护契约。不提交、推送、发布或更新真实安装，不清除真实线程失败计数，不终止用户进程。原有 `.agent-discuss/` 和 `.scratch/consultation-native-error/` 中的两个未跟踪补丁保留。

主会话只读核对 Windows 当日四份原始会话。其中桌面宿主记录 `0.162.0-alpha.17.2`，命令行宿主记录 `0.162.1`，均有相同错误。目录为 `C:\Users\Shy\.codex\sessions\2026\10\12\`。未保存用户上下文或凭据副本。

主会话在 WSL `0.162.1` 与 Windows 桌面实际使用的 Codey 原生程序 `0.162.0-alpha.17.2` 分别执行 `tests/verify-consultation-host.py NativeHistory.test_empty_tool_text_block_is_lossless`，修复前均退出 1，错误与用户报告相同。新增 `NativeRequest.test_lite_empty_tools_may_omit_both_inventories` 在修复前也退出 1，命中相同校验。

本机无认证端点捕获的真实请求既没有顶层 `tools`，也没有 `additional_tools` 项。Codex `rust-v0.162.1` 的[请求构造源码](https://github.com/openai/codex/blob/rust-v0.162.1/codex-rs/core/src/client.rs#L915)表明，`use_responses_lite=true` 时只为非空工具集合添加 `additional_tools`，顶层工具值为 `None`。[序列化源码](https://github.com/openai/codex/blob/rust-v0.162.1/codex-rs/codex-api/src/common.rs#L287)省略值为 `None` 的顶层工具字段。两份源码均于本轮直接读取。官方[请求参考](https://developers.openai.com/api/reference/resources/responses/methods/create)也已读取；具体宿主序列化结论以源码与真实请求为依据。

## 交付契约

仅当临时原生模型目录中 `use_responses_lite` 严格等于布尔值 `true` 时，允许两处工具集合同时省略。顶层工具字段一旦存在就必须严格等于空数组；每个 `additional_tools` 项必须含有严格等于空数组的 `tools`。非 Lite 模式仍须至少提供一处明确的空集合。请求追踪、模型与推理强度、基础指令、完整历史及咨询指令的校验继续执行。

六个交付文件为 `plugins/codex-advisor/scripts/consult_native.py`、`docs/agents/plugin-maintenance.md`、`tests/verify-consultation-native.py`、`tests/verify-consultation-env.py`、`tests/fixtures/consult-codex.py` 和 `tests/verify-consultation.py`。新增检查覆盖省略字段、旧显式空集合、两处非空及异常字段、缺少子字段和第二个非空集合。完整输入缺失的场景仍失败，失败分类为 `context`。

## 主会话验证

全部检查由主会话执行，退出码均为 0。日志位于本文件同级 `evidence/`。

| 范围 | 命令或入口 | 结果 | 日志 |
|---|---|---|---|
| WSL 咨询边界、生命周期、失败计数、原生校验与后代清理 | `sh tests/verify.sh --consultation` | 164 项通过，8 项 Windows 专属跳过 | `consultation.log` |
| WSL 真实原生请求 | `python3 tests/verify-consultation-host.py` | 8 项通过 | `host-wsl.log` |
| WSL 真实宿主到 MCP 到咨询进程 | `python3 tests/verify-consultation-env.py` | 3 项通过 | `env-wsl.log` |
| Windows 桌面原生请求 | Windows Python 执行 `tests/verify-consultation-host.py`，进程 PATH 首项为 Codey 原生目录 | 8 项通过 | `host-windows.log` |
| Windows 桌面完整宿主链 | 同一 Windows 环境执行 `tests/verify-consultation-env.py` | 3 项通过 | `env-windows.log` |
| Windows 原生校验与生命周期 | 同一 Windows 环境执行 `tests/verify-consultation-native.py` | 21 项通过 | `native-windows.log` |
| Windows 命令行原故障场景 | Windows 默认 PATH 执行 `tests/verify-consultation-host.py NativeHistory.test_empty_tool_text_block_is_lossless` | 1 项通过 | `cli-windows.log` |
| 中文镜像、发布文案及差异空白 | `python3 tests/test_zh_mirror.py`、`python3 tests/test_shipped_wording.py`、`git diff --check` | 全部通过 | 主会话工具结果 |

Windows Python 为 `D:\Environment\Python\Python312\python.exe`，启用 `PYTHONUTF8=1` 与 `-B`。Codey 原生目录为 `C:\Users\Shy\AppData\Local\Codey\codex-runtime\aee24b2e623d01fc`；默认命令行程序为官方 npm 包内 `codex.exe`，版本 `0.162.1`。这些环境假设于本轮核对；原生程序或模型目录变化后应重跑真实宿主检查。

真实宿主检查只访问本机无认证端点并自动删除临时主目录、市场与请求记录。没有认证模型服务调用的成功证据，也没有真实安装更新、既有会话重新加载或已停用线程恢复的证据。四次累计失败的停用状态保持，成功调用也不重置计数。

## 独立验收

独立验收结论为仓库修复可交付，没有需修改的发现。主会话实际拨盘为 `gpt-6.1-sol[high]`，验收映射选择 `ca_advisor_mainstay_m` 的 `high`；路由钩子与执行身份钩子均确认实际模型与强度一致。审查者使用新线程 `/root/empty_tools_acceptance`，保持只读。

审查者读取六文件完整差异、记录、全部检查日志及快照；直接复核官方源码；以纯内存方式执行 80 个场景，覆盖非布尔模式字段、异常工具字段和其余请求校验，退出 0；中文镜像 41 项、发布文案 66 项和差异空白检查均通过。六个交付文件在审查前后均匹配快照。审查者没有调用模型服务、修改文件或计数器，也没有重跑会创建临时文件的宿主检查；主会话执行的真实宿主结果依然属于主会话验证。

主会话收尾再次调用当前安装的 `codex_advisor` MCP，返回相同 `tools` 错误、失败数 2、未停用，未返回建议，原始结果保存于 `evidence/final-consultation.json`。这次调用执行的是尚未更新的真实安装，未执行仓库冻结源码。审查者指出 JSON 自身未注明源码版本；执行来源由主会话的工具调用记录确认，不能将该结果当作修复后的源码失败或安装恢复证据。向独立审查线程追加此说明时，编排钩子按新线程规则拒绝了消息；审查者仍依据原记录给出限定范围的可交付结论，主会话核对后接受。

主会话保留本目录中的验收记录、源码快照、检查日志及咨询失败结果供后续发布核对。其他本轮临时输出已清理，用户已有文件、进程、安装和失败计数未被修改。发布与部署未获本轮授权。

## 发布与部署授权

用户随后明确要求：“提交并发布，然后部署”。此授权覆盖本次修复的提交、补丁版本 `0.3.5`、向 `origin/main` 推送，以及 WSL 和 Windows 两侧的市场升级、插件安装与重装、配套安装器和安装核验。仓库既有发布方式为推送市场源码，没有 Git 标签或 GitHub 发布页；本次沿用该方式。

主会话负责所有发布与部署操作。先补齐版本清单、README 和完整中文版手册，并执行最终全组检查与手册结构检查；复用仍匹配源码的独立验收及两侧真实请求证据。推送后分别执行标准市场升级和插件安装、重装，核对每个受版本控制的插件文件及十七个入口，再验证新进程中的实际咨询。保留用户进程与已停用线程的计数；现有会话重新加载独立报告。钩子定义未改变，已有信任是否适用不靠安装结果推断。

发布前流程咨询仍返回旧校验错误，失败数 3，未返回建议；用户授权与已完成独立验收保持有效。

最终 `sh tests/verify.sh` 退出 0，包含安装、入口、咨询和钩子四组；咨询相关 164 项通过、8 项 Windows 专属跳过，路由门禁 19 项通过，日志为 `evidence/release-verification.log`。手册结构 3 项、中文镜像 41 项、发布文案 66 项、HTML 内部锚点与本地链接、差异空白全部通过。六个已独立验收的修复文件仍匹配原快照；本轮新增的是版本清单、README 版本与已验证宿主范围、`docs/releases/0.3.5.html`，没有追加运行逻辑。手册沿用上一版样式，未做页面视觉验收。

Windows 原生程序从 WSL 启动时会继承指向 WSL 的 `CODEX_HOME`。主会话只读探针确认该情况，并在后续 Windows 操作中明确选用 `C:\Users\Shy\.codex`，避免更新错误的一侧。Windows 配套安装器使用明确的 Git Bash 目标 `/c/Users/Shy/.codex/agents`，避免将 Windows 盘符路径解释为相对路径。
