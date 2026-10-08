以下为独立顾问的完整报告：

**验收结论：可验收（ready）。** 当前十个文件组成的产品范围满足本次修复契约；第三、第四次审查发现的生命周期缺口均已关闭。未发现需要修改的实质问题。结论限于当前产物和已验证路径，不代表发布或真实安装更新。

**具体判断**

- 调用绑定有效：[advisor-hooks.py:177](/home/hyy/develop/personal/GitHub/codex-advisor/plugins/codex-advisor/scripts/advisor-hooks.py:177)核对唯一调用标识、工具命名空间、工具名和完整参数；声明另与宿主会话、回合及精确目标绑定。缺失、畸形和不匹配证据进入拒绝分支。
- 第三次发现已关闭：[调用后检查:189](/home/hyy/develop/personal/GitHub/codex-advisor/plugins/codex-advisor/scripts/advisor-hooks.py:189)拒绝调用之后的回合上下文、压缩、开始、完成和中断记录。三个入口的 **15/15** 个内存复现子例均被拒绝。
- 第四次发现已关闭：[活动回合检查:209](/home/hyy/develop/personal/GitHub/codex-advisor/plugins/codex-advisor/scripts/advisor-hooks.py:209)检查回合上下文至调用之间的生命周期事件。三个入口、三种事件、声明前后两个位置的 **18/18** 个子例均被拒绝；正常新回合通过，结束后补写声明不能恢复准入。
- 载荷传递证据成立：[宿主回归:135](/home/hyy/develop/personal/GitHub/codex-advisor/tests/verify-routing-host.py:135)从子线程实际 `agent_message.encrypted_content` 提取摘要；[验证逻辑:153](/home/hyy/develop/personal/GitHub/codex-advisor/tests/verify-routing-host.py:153)比较预期载荷、子线程角色及实际拨盘。运行时说明、维护说明和中文镜像与实现一致。

**实际检查与复用证据**

| 检查 | 结果 |
|---|---|
| `git diff --`、基线解析、索引及未跟踪文件清单 | 完整阅读全部八个已跟踪文件差异，以及新增宿主脚本和工单；`HEAD=c28af93e020032717bd35286de79dbdf45156e43`，暂存差异为空 |
| `python3 -B -c …` 范围摘要检查 | 审查前后 **10/10** 文件均匹配 `review-state.json` |
| `python3 -B -c …` 实际钩子 `main()` 内存检查 | **93/93** 通过；只替代日志文件读取，覆盖合法载荷、绑定错误、畸形输入、声明失效及上述生命周期边界 |
| `python3 -B -c …` 宿主验证器检查 | 当前公开 11 场景与保存的子线程证据一致；改动或丢失载荷、错误角色、错误强度、缺失结果、钩子失效及缺失子线程，七类负例全部触发失败 |
| `python3 -B tests/test_zh_mirror.py` | 退出 0，**41/41** |
| `python3 -B tests/test_shipped_wording.py` | 退出 0，**66/66** |
| `git diff --check` | 退出 0 |

复用并检查了主会话的以下证据：

- [verify.log](/home/hyy/develop/personal/GitHub/codex-advisor/.scratch/native-route-message-format/verify.log)：完整验证通过，包含 **19 项路由测试**；**8 项 Windows 检查跳过**。本次未重跑会创建临时文件的完整套件。
- [historical-host-after.json](/home/hyy/develop/personal/GitHub/codex-advisor/.scratch/native-route-message-format/historical-host-after.json)：`codex-cli 0.161.0` 的 **14 项场景通过**。三个安装文件摘要均匹配当前文件；三条历史载荷的修复前边界摘要与最终子线程摘要 **3/3 一致**。
- `lifecycle-red.log`、`active-turn-red.log`：分别记录修正前 **15、18** 个失败子例。`host-red.log`记录基线消息头拒绝；修复前钩子摘要与 `c28af93` 一致。
- 较早的 `host-after.json` 未用作最终钩子的验证依据。

直接宿主记录确认本线程为 `01a11be0-3776-70a1-9da0-5ccc80fec593`，入口 `ca_advisor_rescue_h`，实际 `gpt-6-astra[xhigh]`，`fork_turns=none`，沙箱 **read-only**，审批策略 **never**。本次仅使用读取命令及不落盘检查，没有写入、格式化、实施、委派、发送任务或读取凭据；未观察到比只读更宽的权限。

**证据缺口与剩余风险**

- 生命周期异常时序已在实际解析器中验证；原生宿主是否会投递这些延迟或重放事件，仍未验证。
- 原生宿主运行复用主会话保存的结果，本次没有重新安装插件或启动回归宿主。保存结果不是完整原始执行轨迹，基线失败日志尤其仅有摘要。
- 固定响应服务不能证明历史载荷被真实模型成功解密、原任务审查完成、Windows 路由恢复或用户真实安装已经更新。
- 宿主预调用日志刷新、回合身份、工具格式或消息传输发生变化后，需要重新确认兼容性。