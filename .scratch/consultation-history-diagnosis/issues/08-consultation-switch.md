# 08：咨询开关

**要构建：** 用户可以在不卸载插件的情况下临时关闭咨询。开关是调用者 Codex 主目录下插件状态目录中的一个标记文件，存在即关闭。关闭时，咨询调用不读取历史、不启动顾问、不发送请求，立即返回明确失败，`consultationDisabled` 为 `true`，并说明原因是用户关闭了咨询；该结果不计入四次停用计数。删除标记文件后，下一次调用恢复正常，无需重启。WSL 与 Windows 各自的 Codex 主目录分别开关。用户于 2026-10-18 要求此功能并决定最先实施。

宿主自带的 `mcp_servers.codex_advisor` 覆盖方式已于 2026-10-18 在 `codex-cli 0.163.0` 上核对：只写 `enabled = false` 导致配置加载失败（`invalid transport`），必须另写 `command` 覆盖插件定义，且真实会话效果未验证，因此不采用。

**Blocked by:** 无（可以立即开始）。实施顺序在 01 之前。

**Status:** resolved

- [x] 标记文件存在时，调用返回明确的关闭结果和 `consultationDisabled: true`，失败计数不增加，也不读取会话记录或启动原生进程。
- [x] 标记文件不存在时，行为与现有实现完全相同。
- [x] 删除标记文件后，同一 MCP 进程的下一次调用恢复正常。
- [x] 失败输出说明如何重新开启；`plugin-maintenance.md` 或调用方可读的文档说明标记文件位置和效果。若修改 `plugins/codex-advisor/**` 下的 Markdown，同步中文镜像。
- [x] 测试覆盖开、关、恢复三种状态，并证明关闭结果不写入失败计数。

## Comments

2026-10-18：实现由 codex 执行器完成，提交的档位为 `gpt-6.1-sol[medium]`（提交值，未观测实际运行值），会话 `01a14e57-cc4f-7380-ac18-3b5ee3c513a8`，回执 `complete`。执行器运行 `sh tests/verify.sh --consultation`、`python3 tests/test_shipped_wording.py`、`python3 tests/test_zh_mirror.py`，退出码均为 0。主会话逐项核对差异，并做反向检查：把标记判断改为恒假后，`tests/verify-consultation.py` 的两个开关测试失败（144 项中 2 项失败），恢复后改动不变。改动已带回主工作区，未提交，未安装；发布属于工单 07。没有修改 `plugins/codex-advisor/**` 下的 Markdown，因此不涉及中文镜像。
