# 07：真实咨询验证与发布

**要构建：** 新行为在真实顾问模型上得到确认后，以新版本发布到两端安装。分别含 `web_search_call`、`additional_tools`、工具搜索条目的三个历史各做一次真实咨询，确认宿主接受注入、实际请求没有工具、顾问返回结构化结果。随后按版本手册和发布流程发布并在 WSL 与 Windows 安装。依据为 `spec.md` 第 6 节。

**Blocked by:** 04、05、06、09

**Status:** ready-for-agent

- [ ] 执行前取得用户对真实咨询、推送和两端安装的当前授权；每项授权单独确认。
- [ ] 三次真实咨询的结果记录在本目录的验收记录中；未完成的类型标为未验证。
- [ ] `tests/verify.sh` 和工单 05、06 的检查在发布前通过。
- [ ] 版本号、版本手册和中文镜像符合仓库规则；两端安装后的模块哈希与仓库一致。
- [ ] `README.md` 中请求构造的已认定宿主版本更新为实际验证的版本。
- [ ] 10 月 18 日两个已停用线程的计数按用户决定保持不变。

## Comments

2026-10-18：用户授权真实咨询、提交推送和两端安装。真实咨询共发出 5 次，均使用 WSL 的 `~/.codex` 原生认证，结果只记录状态、档位、类型和顾问线程，不含历史或建议正文：

1. `additional_tools` 最小真实样本：成功，`plan`，`gpt-6.1-sol[high]`，注入历史只含消息，线程 `01a14ec9-71a2-79f1-a2ff-12bc7c75fc9f`。
2. 工具搜索最小真实样本：成功，`correction`，`gpt-6.1-sol[xhigh]`，工具搜索一对条目已排除，线程 `01a14ec9-addf-7cf3-9d78-c096b94df2f9`。
3. `web_search_call` 最小真实样本：失败，`executor`，`nativeCode=other`。
4. 同一样本的诊断请求（超出首次授权的 3 次，已向用户说明）：服务端点返回 400，`Hosted tool 'web_search' requires authorization and metering that are not supported by rustponsesapi.`，`param: input`。用户随后决定排除内置工具记录（工单 09），并另行授权最多 3 次验证请求。
5. 修复后的 10 月 15 日真实边界：成功，见工单 09。

前三次结果为 `evidence/real-consult.json`，第 5 次为 `evidence/real-consult-oct15.json`。发布前检查日志为 `evidence/release-verification.log`：`tests/verify.sh`、版本手册、措辞和镜像检查均通过。
