# 0.3.11 发布与双端安装验收

日期：2026-11-20（UTC）。用户授权：“提交推送，重装，验收”。

## 发布范围

版本为 `0.3.11`，沿用 GitHub 市场源码发布方式。本版包含两项改动：

- 删除 `consult_context.py` 中“咨询边界之后不得出现 `response_item`”的检查。
  代码模式 `exec` 以短 `yield_time_ms` 调用咨询时，宿主先写入后台输出，
  咨询进程随后才读取会话记录，旧检查因此以 `pairing` 失败。诊断见
  `.scratch/consultation-exec-yield/diagnosis.md`，决定见 ADR-0006 “Consultation boundary”一节。
- 版本手册收录 `fa63c8c` 的 Windows npm CLI 目录回退。

批量检查记录在 `.scratch/consultation-robustness/plan.md`。

## 发布与安装

发布提交为 `387e0cec362dda2a3a5c65034fd11e819b3d20af`，已推送到 `origin/main`。
`git ls-remote origin refs/heads/main` 核对该提交，两侧市场快照也都指向该提交
（`evidence/market-commit-*.txt`）。发布源码的逐文件摘要保存在 `evidence/source-manifest.json`。

| 边界 | WSL | Windows |
|---|---|---|
| CLI | `0.170.0` | `0.170.0` |
| 标准市场升级 | 退出零 | 退出零 |
| 标准移除与安装 | 均成功，版本 0.3.11 | 移除报 os error 32（文件被占用），安装报 os error 5；`codex plugin list` 显示 0.3.11 |
| 配套安装器与检查 | 均通过 | 以 `--target-dir /c/Users/Shy/.codex/agents` 运行，均通过 |
| 逐字节源码比较 | 37 个插件文件、17 个入口一致 | 37 个插件文件、17 个入口一致 |
| 入口模型 | `gpt-6.2-sol` 8、`gpt-6.2-astra` 6、`gpt-6-luna` 3 | 同左 |
| 新 MCP 进程启动 | 初始化与工具清单通过，退出零 | 初始化与工具清单通过，退出零 |

Windows 安装命令虽然报 os error 5，`0.3.11` 缓存与发布提交逐字节一致
（`evidence/install-windows.json`）。旧的 `0.3.10` 缓存目录仍在，因为两个运行中的 Codex 进程占用它。
本轮没有停止这些进程，也没有手改托管缓存；它们重启前仍使用 `0.3.10`。

钩子定义未改变，本轮不需要在 `/hooks` 重新审核。

## 安装后真实咨询

两侧各开一个新的 `codex exec` 任务，用代码模式 `exec` 以 `yield_time_ms: 1` 调用
`process_consultation`，这正是旧检查失败的调用方式。

| 项目 | WSL | Windows |
|---|---|---|
| 会话 | `01a1f6d1-1b3b-7b61-bb38-9f8bf37b64fa` | `01a1f6d2-4b71-7430-95e0-7a9f1eaac65d` |
| 咨询边界 | 第 19 条记录 | 第 15 条记录 |
| 后台输出写入 | 边界后 100 毫秒 | 边界后 238 毫秒 |
| 结果 | 成功，`plan`，`gpt-6.2-sol[high]`，18.7 秒 | 成功，`stop`，`gpt-6.2-sol[medium]`，约 126 秒 |

对 WSL 会话记录做差异回放：`0.3.10` 代码报
`pairing: History changed beyond the unfinished consultation boundary.`，
`0.3.11` 代码重建成功，共 8 项。

Windows 线程 `01a1f678-71ae-7ce1-aade-ec2b7a3575b1` 的失败计数已清除（删除 1 行，原值 3）。
该线程本身的恢复使用未验证。

## 与本版无关的观察

- 2026-11-20 01:36 UTC 起，`codex exec` 任务显示 `hook: SessionStart Failed`，会话记录中没有咨询姿态注入。
  01:18 UTC 的车道会话仍有注入。现象早于 02:12 UTC 的重装，本版也没有改变钩子。
  手动运行插件钩子能输出姿态并退出零。宿主有两个 `SessionStart` 钩子（本插件与用户的 orca 钩子），
  哪一个失败未查明，宿主日志库没有这段时间的记录。
- Windows 验收输出有一行 `collab spawn failed: no thread with id: 01a1f6d2-6929-7da1-9c5d-6a5d5372967e`，
  原因未查明，咨询本身成功。
- Windows 咨询用时约 126 秒，总时限为 180 秒。时限候选改动见
  `.scratch/consultation-robustness/timeout.md`。

## 未验证

- 两侧既有会话的重新加载。
- Windows 上的批量检查（只在 WSL 运行）。

## 保留的无关工作

`.scratch/consultation-empty-tools/acceptance.md` 与 `.scratch/release-0.3.10/acceptance.md` 的既有改动，
`.agent-discuss/`、`.fable-advisor/`、`.scratch/consultation-stale-cell/`、
`.scratch/consultation-empty-tools/evidence/reinstall-windows.json` 和两个
`.scratch/consultation-native-error/audit-native-*.patch` 均不纳入本次提交。
