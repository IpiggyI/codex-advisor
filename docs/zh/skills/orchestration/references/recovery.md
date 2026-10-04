# 恢复与交接

验收失败后、发出返工或改派工作之前，阅读本文件。改派是一次新的派发：同时遵循 [operations.md](operations.md)。

## 计入一次 complete attempt

一次 complete worker attempt 包含实现、常规调试和核验，然后以验收失败或确实无法完成目标结束。中间失败的测试和单次工具错误不算 complete failed attempt。

## 先诊断再行动

在选择修复、澄清或升级之前，诊断环境问题、缺失事实、契约缺口、推理失败和执行者是否合适。先修复环境问题。契约缺口（预期行为不明、要求冲突、涉及保留接口）在同一拨盘上以修正后的契约解决，仅在下述窗口内复用线程。这不计为升级或能力失败。环境问题和契约缺口不会让工作沿下文的路径移动。普通工作允许主代理接管；架构师模式仍把编辑委派出去。

## 沿 escalation ladder 升级

验收失败后，执行 R1：在同一拨盘上发一张返工工单，仅在下述窗口内复用线程。返工指出被违反的要求、可复现失败、期望行为和核验；工单里不含修法，仅有结构偏好也不能构成返工理由。返工也失败，且诊断把原因归为能力时，原尝试和返工合计为一次能力失败。

发生能力失败后，把工作移到下一个档位，并在新线程中携带下文的交接记录。除非没有其他选择，否则不要切换到同一档位中的另一个模型。除非没有其他选择，下一个拨档的模型在[路由配置](routing-profile.md#模型定位)中的定位不能低于失败拨档的模型定位；模型不变时使用更高推理强度。在此下限之上，根据失败暴露出的难点选择。

路径为 `mainstay` -> `crux` -> `rescue` -> 用户。`rescue` 只能经 `crux` 或用户声明到达；从 `crux` 开始的工作在一次 `crux` 能力失败后到达 `rescue`。R3 继续作为约束：同一模型最多提档一次。按 R4，工具反复失败、执行失控或触碰保留项等重大执行问题可以跳过返工，并计为一次能力失败。

## 保留或更换线程

续用窗口从宿主记录的工作线程最近活动时刻起算，为 30 分钟。从该线程的会话记录读取时间戳；时间缺失、无效、晚于当前时间或超窗时，新开线程。恰好 30 分钟仍在窗口内。这是生命周期政策，不是实测缓存寿命。

返工、修正契约、中断后续跑和新工单都受此窗口约束。续用还要求角色、模型和推理强度相同。新工单另需同一区域且确实依赖共享上下文，并在任务数据包写明这两项。探索调用和独立验收始终新开线程。

窗口内使用原生续发并保留 `task_name`。超窗后，在同一档位、同一拨盘上新开线程，携带原契约、缺陷证据、上轮报告和核验回执。换线程保留能力失败历史，也不推进升级阶梯。推理强度、模型或角色变化时，使用新的匹配入口和显式设置。复用线程中改变提示词不算新会话。新开与复用线程都遵循 [operations.md](operations.md) 的路由检查。

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
