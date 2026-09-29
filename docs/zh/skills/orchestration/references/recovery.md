# 恢复与交接

验收失败后、发出返工或改派工作之前，阅读本文件。改派是一次新的派发：同时遵循 [operations.md](operations.md)。

## 计入一次 complete attempt

一次 complete worker attempt 包含实现、常规调试和核验，然后以验收失败或确实无法完成目标结束。中间失败的测试和单次工具错误不算 complete failed attempt。

## 先诊断再行动

在选择修复、澄清或 ladder 的某一步之前，诊断环境问题、缺失事实、契约缺口、推理失败和执行者是否合适。先修复环境问题。契约缺口（预期行为不明、要求冲突、涉及保留接口）在同一线程上以修正后的契约解决；它不是 ladder 的一步，也不是能力失败。环境问题和契约缺口不会让工作沿下文的路径移动。普通工作允许 primary 接管；Architect mode 仍把编辑委派出去。

## 沿 escalation ladder 升级

验收失败后，执行 R1：在同一线程、同一 dial 上发一张返工工单。返工指出被违反的要求、可复现失败、期望行为和核验；工单里不含修法，仅有结构偏好也不能构成返工理由。返工也失败，且诊断把原因归为能力时，原尝试和返工合计为一次能力失败。

发生能力失败后，把工作移到下一个档位，并在新线程中携带下文的 handoff。除非没有其他选择，否则不要切换到同一档位中的另一个模型。除非没有其他选择，下一个 dial 的模型等级不能低于失败的 dial；模型不变时使用更高 effort。在此下限之上，根据失败暴露出的难点选择。

路径为 `mainstay` -> `crux` -> `rescue` -> 用户。`rescue` 只能经 `crux` 或用户声明到达；从 `crux` 开始的工作在一次 `crux` 能力失败后到达 `rescue`。R3 继续作为约束：同一模型最多提档一次。按 R4，工具反复失败、执行失控或触碰保留项等重大执行问题可以跳过返工，并计为一次能力失败。

## 保留或更换线程

同模型、同 effort 的 worker 返工可以通过 native 后续调用继续其线程，并沿用该线程的 `task_name`。每一次委派 effort 变更，无论升高或降低，都需要带显式设置的新 native 线程；模型变更和角色改派也需要新的匹配入口。带不同请求 effort 的已恢复线程不能满足本策略，改了提示词的 resume 也绝不能报告成新会话。这是明确的生命周期策略，不是对缓存行为或节省的普遍主张。

## 交接实际状态

替换写入者之前，结束或停止其冲突活动，并取得可用证据。检查范围内的实际变更，保留有用的部分结果和无关编辑。把这份紧凑 handoff 与角色数据包一起交给后继者：

~~~text
OBJECTIVE AND BINDING DECISIONS
<Original task, authorized scope, ownership, retained interfaces, and constraints.>

CURRENT STATE
<Actual changed/new files, useful partial changes, relevant task/source references,
and confirmation that the predecessor no longer writes this scope.>

ATTEMPT AND DIAGNOSIS
<Previous role/model/effort/thread, completed checks, failed acceptance or inability,
reproducible evidence, diagnosed cause, and any unresolved contract gap.>

REMAINING WORK
<Corrections and verification still needed without lowering acceptance conditions.>
~~~

记录前任/后继标识、观察到的 effort，以及新 spawn 对比后续调用的事件。比较真实标识和设置，而不是标签或散文。缺失或矛盾的转换证据使该转换保持未核验。
