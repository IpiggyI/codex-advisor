# 0.3.10 发布与双端安装验收

日期：2026-11-17。用户授权：完成后提交并推送，再部署到两侧；随后要求补发布记录并提交推送。

## 发布范围

版本为 `0.3.10`，沿用 GitHub 市场源码发布方式。用户声明 GPT 已更新到 6.2 系列
（`gpt-6.2-astra`、`gpt-6.2-sol`），并作出三项决定：直接替换模型、所有拨档不变；
6.2 模型沿用被替换模型的定位与两条声明假设；档位表保留 `gpt-6.1-sol` 与 `gpt-6-astra`，
供仍运行在这两个模型上的主会话排名。决定与依据记录在
`docs/adr/0012-gpt-6-2-across-the-routing-profile.md`。

十七个入口与两份路由配置中，`gpt-6.1-sol` 换成 `gpt-6.2-sol`，`gpt-6-astra` 换成
`gpt-6.2-astra`；`gpt-6-luna` 不变，因为模型目录没有 6.2 Luna。本版补齐 README、
AGENTS.md 规范记法示例、清单及 `docs/releases/0.3.10.html`，旧版手册保持冻结。

主会话执行全部外部操作，不停止用户进程，不编辑托管缓存，不修改钩子信任。
安装验证只检查目录、新进程启动、已安装文件和入口，不增加真实模型请求。

## 前置检查

- 2026-11-17，WSL 上 Codex CLI `0.169.0` 的刷新目录（`codex debug models`）列出两个 6.2 模型，
  推理强度为 `low` 到 `ultra`；同一程序的内置目录（`--bundled`）没有这两个模型。
  过程咨询只读内置目录，缺少顾问模型时以 `catalog` 失败。
- 两侧 CLI 均经 npm 从 `0.169.0` 升级到 `0.169.1`。升级后两侧内置目录都列出
  `gpt-6.2-sol` 与 `gpt-6.2-astra`，推理强度 `low` 到 `ultra`，`use_responses_lite` 为真，
  见 `evidence/catalog-wsl.json` 与 `evidence/catalog-windows.json`。回退命令为
  `npm i -g @openai/codex@0.169.0`。
- 改动前基线：离线测试全部通过；`verify-routing-host.py` 需要钩子信任绕过授权，按设计退出 2，未运行。
- 改动后在 WSL 的 CLI `0.169.1` 上，14 个 `tests/test_*.py` 与 `tests/verify-*.py` 脚本退出零，
  `sh tests/verify.sh` 退出零，`git diff --check` 通过。
- 宿主模式差异检查覆盖 18 类，缺失类型为零。
- 全量语料扫描 851 份记录，回放 31913 个位置：31818 个通过，95 个回滚位置按设计拒绝，普通失败为零；
  8697 个位置跳过，保持未验证。
- 原生语料链 11 项通过，覆盖实际存在的 11 类历史项，顾问模型为 `gpt-6.2-astra` 与 `gpt-6.2-sol`，
  均使用 Responses Lite；没有顾问使用的非 Lite 模式没有强行覆盖。
- 反向检查：临时删除档位表中 `gpt-6.1-sol` 与 `gpt-6-astra` 两行后，
  `test_route_primary_legacy_sol` 与 `test_route_primary_legacy_astra` 均失败；恢复后通过。
- 测试固定样例 `tests/fixtures/hooks.json` 只更新子线程派发记录的模型，因为钩子与路由测试从它推导期望结果；
  `SessionStart` 事件的模型保持录制值。
- 版本手册结构检查通过；页面视觉未重新验收。`verify-routing-host.py` 已更新模型标识，未运行。

## 发布与安装

发布提交为 `0359f7c5124738ef34862776625ee2a07a83aec0`，已推送到 `origin/main`。
`git ls-remote origin refs/heads/main` 核对该提交，两侧市场快照也都指向该提交。
发布源码的逐文件摘要保存在 `evidence/source-manifest.json`。

| 边界 | WSL | Windows |
|---|---|---|
| CLI | `0.169.1` | `0.169.1` |
| 标准市场升级 | 退出零 | 退出零 |
| 标准移除与安装 | 移除与安装均成功，版本 0.3.10 | 移除报 os error 32（文件被占用），安装成功，版本 0.3.10 |
| 配套安装器与检查 | 均通过 | 显式 `--target-dir` 后均通过 |
| 逐字节源码比较 | 37 个插件文件、17 个入口一致 | 37 个插件文件、17 个入口一致 |
| 入口模型 | `gpt-6.2-sol` 8、`gpt-6.2-astra` 6、`gpt-6-luna` 3 | 同左 |
| 新 MCP 进程启动 | 初始化与工具清单通过，退出零 | 初始化与工具清单通过，退出零 |

Windows 有三个运行中的 Codex 进程，移除时文件被占用，旧的 `0.3.9` 缓存目录仍在。
本轮没有停止这些进程，也没有手改托管缓存；它们重启前仍使用 `0.3.9`。

Windows 配套安装器的第一次运行由 WSL 调起的 PowerShell 设置
`CODEX_HOME=C:\Users\Shy\.codex`。Git `sh` 把这个路径当成相对路径，
接在当前目录 `/c` 之后，写入了 `C:\C:\Users\Shy\.codex\agents`，并对该目录报告通过。
该目录只含本轮写入的 17 个模板，已删除。随后以
`--target-dir /c/Users/Shy/.codex/agents` 重装，真实目录的 14 个入口被更新，3 个 Luna 入口不变。
今后在 Windows 运行安装器时，应传 POSIX 形式的 `--target-dir`。

`probe-mcp.py` 只执行初始化和工具清单请求，没有请求咨询或访问模型提供方。
`compare-install.py` 从发布提交读取插件文件，与已安装缓存和入口逐字节比较。

## 未验证

- 两侧都没有发出调用 6.2 模型的真实认证请求；原生语料链只使用本机固定响应服务，
  提供方是否已经提供 6.2 模型未验证。
- 钩子定义未改变，本次没有修改用户信任；新版本位于新的缓存目录，钩子信任是否沿用未验证。
- 两侧既有会话的重新加载未验证。

本轮创建的检查与探针进程已退出，临时下载与草稿文件已清理。源代码与版本手册没有待办检查。

## 保留的无关工作

`.scratch/consultation-empty-tools/acceptance.md` 的既有改动，`.agent-discuss/`、
`.fable-advisor/`、`.scratch/consultation-stale-cell/`、旧 Windows 重装 JSON 和两个
`.scratch/consultation-native-error/audit-native-*.patch` 均不纳入本次提交。
