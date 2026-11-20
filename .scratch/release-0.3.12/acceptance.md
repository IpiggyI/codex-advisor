# 0.3.12 发布与双端安装验收

日期：2026-11-20（UTC）。用户授权：“提交推送，重装，验收”。

## 发布范围

版本为 `0.3.12`，沿用 GitHub 市场源码发布方式。改动与决定见
`.scratch/consultation-robustness/plan.md` 的“第二轮”和 ADR-0006
“Excluded payloads, trailing segment, and deadline”一节：

- 原生时限按当前尝试的输出从 180 秒延长到 300 秒，重试撤销延长；`.mcp.json` 声明 `tool_timeout_sec: 330`。
- 被排除条目只校验类型与配对标识。
- 会话记录末尾没有行结束符且无法解码的一段被忽略。
- `internal` 失败报告步骤、异常类名、最内层插件帧和原生阶段。
- 成功结果报告 `nativeExecution`（重试次数、首个输出、末次重试、总耗时）。

批量检查记录在 `plan.md` 的“第二轮状态”。

## 发布与安装

发布提交为 `82f4e30ccbfc026f5ae920477184eea47a245127`，已推送到 `origin/main`。
`git ls-remote origin refs/heads/main` 核对该提交，两侧市场快照也都指向该提交
（`evidence/market-commit-*.txt`）。发布源码的逐文件摘要保存在 `evidence/source-manifest.json`。

| 边界 | WSL | Windows |
|---|---|---|
| CLI | `0.170.0` | `0.170.0` |
| 标准市场升级 | 退出零 | 退出零 |
| 标准移除与安装 | 均成功，版本 0.3.12 | 均成功，版本 0.3.12；`0.3.10` 与 `0.3.11` 缓存目录已不在 |
| 配套安装器与检查 | 均通过 | 以 `--target-dir /c/Users/Shy/.codex/agents` 运行，均通过 |
| 逐字节源码比较 | 37 个插件文件、17 个入口一致 | 37 个插件文件、17 个入口一致 |
| 入口模型 | `gpt-6.2-sol` 8、`gpt-6.2-astra` 6、`gpt-6-luna` 3 | 同左 |
| 新 MCP 进程启动 | 初始化与工具清单通过，退出零 | 初始化与工具清单通过，退出零 |

钩子定义未改变，本轮不需要在 `/hooks` 重新审核。

## Codex Desktop 宿主加载

Windows Codex Desktop `26.1111.2228.0` 自带的 `codex.exe`（`0.169.0-alpha.11.1`）以真实
`CODEX_HOME=C:\Users\Shy\.codex` 启动 `app-server`，`mcpServerStatus/list` 列出 `codex_advisor`
（`pluginId` 为 `codex-advisor@codex-advisor`）和 `process_consultation`，`toolsError` 为空
（`evidence/desktop-mcp-status.json`）。带 `tool_timeout_sec` 的新 `.mcp.json` 在 Desktop 宿主上可以加载。
检查时 Desktop 没有运行；本轮没有在 Desktop 界面中发起咨询。

## 安装后真实咨询

两侧各开一个新的 `codex exec` 任务，用代码模式 `exec` 以 `yield_time_ms: 1` 调用
`process_consultation`，脚本输出完整的工具返回对象。

| 项目 | WSL | Windows |
|---|---|---|
| 会话 | `01a1f70e-b7af-7dc0-b567-eb9a75e83cb3` | `01a1f70f-8c7b-7d83-8c0d-3113d393034c` |
| 后台单元 | 0.2 秒后返回运行中的单元 | 0.08 秒后返回运行中的单元 |
| 结果 | 成功，`plan`，`gpt-6.2-sol[high]` | 成功，`plan`，`gpt-6.2-sol[medium]` |
| `nativeExecution` | `retryCount` 0，`firstOutputMs` 13626，`elapsedMs` 14460 | `retryCount` 4，`firstOutputMs` 122406，`elapsedMs` 123625，`lastRetry` 为 `responseStreamDisconnected` |

Windows 这次调用在 122 秒内没有任何输出，经过 4 次 `responseStreamDisconnected` 重试后成功。
这是第一条成功调用的重试记录：如果“快速放弃”的阈值设在 4 次重试以内，这次调用会被判为失败。

## 与本版无关的观察

Windows 验收输出有 3 行 `exec_command failed: CreateProcess ... CreateProcessAsUserW failed: 5`。
这些命令的工作目录是 `C:\Users\Shy\.codex\memories`，内容是读取 `MEMORY.md`、`memory_summary.md` 和技能目录，
来自宿主的记忆功能（Windows 配置中 `memories.generate_memories = true`），在只读沙箱中被拒绝。
它们与咨询无关，咨询本身成功。0.3.11 验收中的 `collab spawn failed` 可能来自同一机制，未核实。

## 未验证

- 宿主是否按 330 秒执行工具时限；没有超过约 197 秒的咨询调用。
- 在 Desktop 界面中的真实咨询，包括线程 `01a1f678-71ae-7ce1-aade-ec2b7a3575b1` 的恢复使用。
- Windows 上的批量检查（只在 WSL 运行）。

## 保留的无关工作

`.scratch/consultation-empty-tools/acceptance.md` 与 `.scratch/release-0.3.10/acceptance.md` 的既有改动，
`.agent-discuss/`、`.fable-advisor/`、`.scratch/consultation-stale-cell/`、
`.scratch/consultation-empty-tools/evidence/reinstall-windows.json` 和两个
`.scratch/consultation-native-error/audit-native-*.patch` 均不纳入本次提交。
