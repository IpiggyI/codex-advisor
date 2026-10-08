顾问完整报告如下：

**READINESS：changes required（需要修改）**

不透明载荷的原始故障已有充分修复证据，上一轮发现的“调用之后”生命周期缺口也已关闭。但当前解析器仍会接受另一种已失效的声明，不满足“陈旧声明必须拒绝”的验收契约。对代码行为和复现结果置信度高；原生宿主产生该时序的可达性尚未验证。

**FINDINGS**

1. **P2：声明与调用之间的回合结束、中断事件被忽略。**

   [advisor-hooks.py:209](/home/hyy/develop/personal/GitHub/codex-advisor/plugins/codex-advisor/scripts/advisor-hooks.py:209)只将 `turn_context`、`compacted` 作为调用前的边界；随后只提取 `response_item`，忽略 `event_msg`。[current_call:189](/home/hyy/develop/personal/GitHub/codex-advisor/plugins/codex-advisor/scripts/advisor-hooks.py:189)新增的生命周期检查则仅覆盖调用之后。

   我通过实际钩子 `main()` 入口、用内存代替日志文件读取，复现以下序列：

   ```text
   turn_context(T)
   assistant：合法 Route 声明
   event_msg：task_complete(T) 或 turn_aborted(T)
   function_call：与事件完整匹配的调用
   ```

   `spawn_agent`、`followup_task`、`send_message` 均输出 `route declaration checked`，没有拒绝。声明之后插入 `task_started` 也得到放行。

   影响是：即使快照已明确记录回合结束或中断，旧声明仍可获得准入确认，违背[工单:125](/home/hyy/develop/personal/GitHub/codex-advisor/.scratch/native-route-message-format/issues/01-spawn-message-header-rejection.md:125)的陈旧声明拒绝要求。当前[生命周期回归:218](/home/hyy/develop/personal/GitHub/codex-advisor/tests/verify-routing.py:218)只把这些事件追加在调用之后，未覆盖此处。需要检查调用之前的活动回合状态。

未发现其他已证实、需要修改的产品问题。

**VERIFICATION**

我亲自完成：

- 阅读 `git diff c28af93 --` 的全部 8 个修改文件，包括运行时实现、路由测试、README、维护说明及双语运行时文档；完整阅读新增的 [verify-routing-host.py](/home/hyy/develop/personal/GitHub/codex-advisor/tests/verify-routing-host.py)、工单，以及宿主探针和历史回放脚本。
- 核对 `HEAD=c28af93e020032717bd35286de79dbdf45156e43`。通过 `python3 -B -c …` 检查范围摘要，审查前后 **10/10 文件与 `review-state.json` 一致**；最终宿主证据中的三个安装文件摘要均匹配当前文件。
- `python3 -B tests/test_zh_mirror.py`：退出 0，**41/41**；`python3 -B tests/test_shipped_wording.py`：退出 0，**66/66**；`git diff --check`：退出 0。
- 只读链接检查：**62 个本地目标存在**，未验证锚点。初版检查误识别了代码块中的函数调用；排除代码块后通过。
- 内存快照检查：三个入口的合法不透明载荷均通过；调用之后的五种生命周期边界 **15/15 拒绝**，确认上一轮具体发现已关闭；调用之前的结束、中断事件仍被放行，形成上述发现。
- 检查新增宿主脚本的真实断言，并在内存中验证失败能力：修改或丢失载荷摘要、错误角色、错误 effort、缺失调用结果及模拟钩子失效，均被拒绝。保存的子线程证据与公开 11 场景的预期摘要一致；三条历史载荷的修复前后摘要一致。此检查重建了工具结果输入，没有重新执行原生宿主。
- 从本次直接宿主记录核实：新线程 `01a11bd0-4803-76c0-8e1f-91e2e2d5c8d8`，入口 `ca_advisor_rescue_h`，实际 `gpt-6-astra[xhigh]`，`fork_turns=none`，只读沙箱，审批策略 `never`。未实施、委派或修改文件。heredoc 命令曾因 shell 无法创建临时文件而失败，随后改用 `python3 -B -c` 完成检查。

经审阅的主会话证据：

- [verify.log](/home/hyy/develop/personal/GitHub/codex-advisor/.scratch/native-route-message-format/verify.log)记录完整验证通过，包含 **18 项路由测试**；**8 项 Windows 检查跳过**。
- [historical-host-after.json](/home/hyy/develop/personal/GitHub/codex-advisor/.scratch/native-route-message-format/historical-host-after.json)记录最终版本 **14 项场景通过**，覆盖三个入口、拒绝路径、子线程角色和拨盘，以及载荷摘要。
- `lifecycle-red.log`记录修正前 **15 个失败子例**。`host-red.log`记录基线在合法不透明派发处失败，但仅保留一行摘要。
- 较早的 `host-after.json` 不作为最终钩子状态的验证依据。

**GAPS**

- 未重跑会创建临时文件、安装插件或启动宿主的完整测试；本次采用主会话保存的证据，并核对当前文件、断言及摘要。
- 上述前置生命周期缺口已在实际解析逻辑中复现；原生宿主是否会投递这种时序尚未验证，不能声称已复现真实环境中的错误派发。
- 固定响应服务无法证明历史载荷解密成功、Windows 路由恢复或用户实际安装已更新。
- 当前仍有一项实质契约缺口，因此验收保持待完成。