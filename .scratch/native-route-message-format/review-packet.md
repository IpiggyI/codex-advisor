# 原生路由消息修复的独立验收

## 审查范围

工作区为 `/home/hyy/develop/personal/GitHub/codex-advisor`，基线为 `c28af93`。用户要求排查并修复 `.scratch/native-route-message-format/issues/01-spawn-message-header-rejection.md`。本次修改涉及工具调用前的准入规则，需要独立验收。

请先读工单中的本次原因、修复范围和主会话验证结果。宿主把原生 `message` 放入子线程的 `agent_message.encrypted_content`，旧钩子却从它读取明文消息头。新实现改为读取调用前的可见助手声明，以宿主回合、调用标识、完整参数、工具和目标绑定。任务正文保持原样。缺失、畸形、陈旧或不匹配的声明，以及原有拨盘、依据和续用限制，都必须拒绝。

## 实际变更

请检查 `git diff --` 的全部修改，并单独阅读新增的 `tests/verify-routing-host.py`。本次范围的文件摘要见同目录 `review-state.json`。工单与同目录证据属于本任务；`.agent-discuss/` 和 `.scratch/consultation-native-error/audit-native-*.patch` 是已有无关文件，保留它们。

产品审查范围就是 `review-state.json` 中的文件。临时审查启动器、审查会话日志及派发宿主自身的操作不属于产品变更。主会话已有的完整测试结果可复用；独立审查以完整差异、契约和必要证据为主，无需重复整个测试套件。

重点检查 `current_call` 和 `declared_route` 的绑定、失效边界、默认拒绝行为，以及宿主回归是否确实核实了载荷原样传递。中文镜像、维护说明和运行时说明需与实现一致。请从当前文件判断，不只依赖主会话结论。

## 主会话验证

执行者均为主会话。

- 新增不透明消息回归已先失败后通过；基线钩子在相同原生回归中失败，证据为 `host-red.log`。
- `sh tests/verify.sh` 在最终生命周期修正后退出 0，日志为 `verify.log`；路由部分为 19 项测试，咨询部分跳过 8 项 Windows 专用检查。
- `python3 .scratch/native-route-message-format/replay-historical.py --allow-hook-trust-bypass` 在最终修正后运行公开宿主回归并追加三条历史载荷，14 项场景全部通过，证据为 `historical-host-after.json`。`host-after.json` 是较早的 11 项场景，钩子摘要对应修正前版本。
- `python3 tests/test_zh_mirror.py` 为 41/41，`python3 tests/test_shipped_wording.py` 为 66/66。本地链接目标和 `git diff --check` 通过。
- 固定响应服务不解密任务载荷。这些结果不能证明真实模型已完成审查、Windows 路由已恢复或当前真实安装已更新。

第三次独立审查 `review-attempt-3.md` 发现调用之后的生命周期失效检查缺口。当前版本已在 `current_call` 中拒绝调用之后出现的回合开始、结束、中断、新回合上下文或压缩记录。新增回归覆盖三入口与五种边界，修改前失败的证据为 `lifecycle-red.log`，修正后全量验证及原生 14 项场景通过。请对当前完整版本作独立判断，核对该发现的关闭情况；原生宿主投递该延迟事件的时序仍未验证。

第四次审查 `review-attempt-4.md` 复现同类事件在声明与调用之间仍能通过。最终版本在 `declared_route` 中检查当前回合上下文至调用之间的生命周期事件；回合已结束时，新声明也不能恢复准入。`RoutingGate.test_call_requires_an_active_host_turn` 覆盖三入口、三种事件及声明前后两个位置，并保留正常新回合通过的对照。修改前 18 个子例失败，见 `active-turn-red.log`；修正后 19 项路由测试及原生 14 项场景通过。请核查这两次具体发现，并审阅完整最终差异。

## 设置与权限

请求 `ca_advisor_rescue_h`，其模板固定 `gpt-6-astra[xhigh]`。主会话的宿主记录也是 `gpt-6-astra[xhigh]`，所以该入口符合主代理编写工作的验收映射。要求全新线程和按行为只读；若宿主继承更宽权限，须报告实际权限及工具活动。

你不是工作区中唯一的代理。只读取本次范围，不写文件、不格式化、不实施、不委派；不得恢复、撤销或覆盖其他人的修改。可以运行不会修改文件的检查。不读取凭据或无关会话正文。

## 返回要求

用中文返回验收结论、按严重程度列出的具体问题及文件行号、实际检查命令和结果、证据缺口。结论为可验收、需要修改或未核实之一。不要用流程咨询代替本次独立审查。
