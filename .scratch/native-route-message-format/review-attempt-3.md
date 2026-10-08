**READINESS：changes required（需要修改）**

不透明载荷的原始故障已有充分修复证据，但当前实现仍会接受已经失效的调用快照，不满足工单要求的“陈旧声明默认拒绝”。对代码行为及复现结果置信度高；尚未在原生宿主中复现其触发时序。

**FINDINGS**

1. **P2：未确认旧调用所在回合仍然有效。**
   [advisor-hooks.py:189](/home/hyy/develop/personal/GitHub/codex-advisor/plugins/codex-advisor/scripts/advisor-hooks.py:189)只检查调用之后是否存在同一 `call_id` 的 `function_call_output`；[advisor-hooks.py:200](/home/hyy/develop/personal/GitHub/codex-advisor/plugins/codex-advisor/scripts/advisor-hooks.py:200)则只从调用之前寻找回合和压缩边界。

   我通过只读、内存快照复现：合法声明与旧调用之后，追加以下任一种记录，钩子仍输出 `route declaration checked`：

   - 旧回合的 `turn_aborted`，随后进入新 `turn_context`；
   - `compacted`；
   - 旧回合的 `task_complete`。

   对照组中，追加匹配的 `function_call_output`，或在调用之前插入压缩记录，均正确拒绝。因此缺口是调用之后的生命周期失效检查。旧调用没有结果记录时，延迟或重放的旧事件仍能获得准入确认。

   [verify-routing.py:199](/home/hyy/develop/personal/GitHub/codex-advisor/tests/verify-routing.py:199)的边界负例都插在调用之前，未覆盖上述情况。这与[工单:125](/home/hyy/develop/personal/GitHub/codex-advisor/.scratch/native-route-message-format/issues/01-spawn-message-header-rejection.md:125)要求拒绝陈旧声明的契约不符。未发现其他需要修改的产品问题。

**VERIFICATION**

我亲自完成：

- 完整审阅 `c28af93` 起的全部产品差异、新增宿主回归脚本及工单，并检查相关证据。`HEAD` 为 `c28af93e020032717bd35286de79dbdf45156e43`。
- 用 `python3 -B -c …` 在审查前后核对 SHA-256：`review-state.json` 的 **10/10 文件一致**。两份宿主结果记录的三个安装文件摘要均匹配当前文件；修复前钩子摘要匹配基线。
- `python3 -B tests/test_zh_mirror.py`：退出 0，**41/41**。
- `python3 -B tests/test_shipped_wording.py`：退出 0，**66/66**。
- `git diff --check`：退出 0。
- 通过 `python3 -B -c …` 调用实际钩子入口，以内存替代父日志读取，得到上述失效边界复现结果；没有修改产品函数实现或文件。
- 检查宿主回归的真实断言，并在内存中验证其失败能力：改变载荷摘要、丢失载荷、错误角色、错误 effort、缺失调用结果及模拟钩子失效，均被拒绝。保存的子线程证据与当前 11 项场景的预期载荷摘要一致。

主会话证据经审阅支持：

- `verify.log` 记录完整验证通过，包含 **17 项路由测试**，跳过 **8 项 Windows 检查**。
- `host-after.json`、`historical-host-after.json` 分别记录 **11、14 项原生场景通过**；三条历史载荷摘要与修复前记录一致。
- `host-red.log` 记录基线在合法不透明派发处失败，但只有摘要行。

隔离与设置已从本次宿主记录核实：入口 `ca_advisor_rescue_h`，实际拨盘 `gpt-6-astra[xhigh]`，`fork_turns=none`，只读沙箱，审批策略 `never`。本次没有委派、实施或文件修改。一次 heredoc 命令因 shell 无法创建临时文件而失败，随后改用 `python3 -B -c` 完成检查。

**GAPS**

- 未重新运行会创建临时文件、安装插件或启动宿主的完整测试；采用已保存证据，并核对当前状态及断言。
- 上述发现已在实际解析逻辑中复现，但原生宿主是否会投递这种延迟或重放事件，尚未验证。
- 基线失败和追加历史场景只保留了摘要结果，缺少完整执行轨迹；当前公开宿主脚本直接生成的是 11 项场景。
- 固定响应服务不能证明真实模型解密成功、Windows 路由恢复或用户实际安装已更新。
- `review-routing-evidence.json` 属于较早的宿主父线程；本次设置判断采用当前线程的直接元数据和派发参数，没有复用该旧记录。