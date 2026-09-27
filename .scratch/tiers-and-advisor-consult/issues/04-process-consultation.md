# 04：过程咨询

**要构建的内容：** 一个零参数的咨询，主代理、任何 worker 以及任何 explorer 都可以通过工单 01 所选的机制调用：
- 它自动携带调用者当前的有效上下文，包括未完成的轮次以及压缩之后的视图。
- 它以该调用者的 AC-4 拨档运行 advisor，并且没有工具。
- 它恰好返回 plan、correction 或 stop 之一，并带有实际的模型与推理等级。
- 它向调用者标出模型或推理等级不匹配。

在同一工单中，每一个 explorer 与 worker 入口都获得它的姿态小节（EN-5），以便没有入口让被委派者去调用一个尚不存在的咨询。

**Blocked by:** 01（机制决定）, 02（规范姿态文本与咨询原则）, 03（路由配置与已安装的入口）。

**Status:** resolved

## 开始前必读

- `spec.md`：AC-3、AC-4、AC-5、AC-10（咨询部分）、AC-11、EN-1（最后一条：额外入口，如果机制需要它们）、EN-5、EN-6、DR-5（工单 04 小节）、X-2、X-4、§Mechanism decision、§Decision Boundaries、§Open Decisions（O3）、§Testing Decisions 第 1 项（姿态检查）、第 4 项与第 6 项、§Goal-Drift Checks（前三项以及姿态小节那一项）。
- `sources.md` §2.4 行 D17、D18、D19、D20、D28、D33、D34、D41、D43、D44。
- `plugins/codex-advisor/skills/orchestration/references/consult-posture.md`（来自工单 02；姿态小节的唯一来源，复制时不改写）。
- 当前的 explorer 与 worker 模板、它们的 `docs/zh/agents/` 对照，以及 `verify.sh` 安装组（来自工单 03）。
- `acceptance.md` §01 P4（所选配置的证据）以及 §03（已安装的入口）。
- `plugins/codex-advisor/skills/orchestration/references/routing-profile.md`（按交付时那样的 AC-4 映射）。
- 处于 `d74b1c99` 的 rpiv-advisor：`advisor/execute.ts`、`advisor/context.ts`、`advisor/inventory.ts`、`prompts/advisor-system.txt`，以及测试 `advisor.execute.test.ts`、`advisor.strip.test.ts`、`advisor.errorresult.test.ts`（要镜像的行为用例）。

## 拥有

- 咨询组件，位于机制所要求的位置，在 `plugins/codex-advisor/` 之下。
- 它所需要的 `plugin.json` 字段，例如一个 MCP 服务器条目。不是 `version`，也不是描述。
- 为它新增的一个 `verify.sh` 组（不加限定的运行包含它）。
- `references/operations.md` 中新的 §Process consultation 及其对照。
- 任何额外的原生入口，按 EN-1 的最后一条，连同它们的对照、路由配置行、退役与清单处理，以及检查。
- 每一个 explorer 与 worker 模板（`plugins/codex-advisor/agents/ca-explorer-*.toml`、`ca-worker-*.toml`）及其对照的姿态小节。那些模板中的其他任何东西都不在内。
- 在 `verify.sh` 安装组中：姿态检查，以及把同一角色指令相同检查收窄到姿态小节之外的文本。

## 所确立与所消费

- **所确立** AC-3、AC-4、EN-5，以及 AC-10 的咨询部分。
- **所消费** 工单 01 的机制、工单 02 的姿态文本、工单 03 的路由配置与模板，以及 AC-11。

工单 05 的完成前钩子需要知道一次咨询发生过。在 §Process consultation 小节中写明，一次咨询在一个会话之内如何可被观察（例如，会话记录中的工具调用名称，或按会话的状态）。工单 05 依赖该描述。

## 验收

- [x] 咨询接受零个参数。调用者不能传入一份摘要来代替自动上下文。
- [x] 上下文（D43）：夹具测试表明下面这些全都到达 advisor 调用：
  - [x] 一个未完成轮次的工具调用与结果；
  - [x] 一份压缩摘要以及其后的消息；
  - [x] 一条来自会话最早的未压缩轮次的约束，该会话长于机制所使用的任何窗口。

  实况的随机数、压缩以及最早上下文检查通过（`acceptance.md` §04）。
- [x] advisor 调用没有工具（D44）。测试断言该组件发送的工具集为空。实况证据是 advisor 请求的实际工具集，按发送时或按宿主所记录的那样，展示为空；一次被拒绝的尝试或 advisor 自己的陈述不是证据。
- [x] 拨档：对 `mainstay`、`crux` 与 `rescue` 调用者，以及对位于 `gpt-6-astra[xhigh]`、`gpt-6-sol[high]` 与 `gpt-5.6-terra`（夹具）上的主代理，advisor 拨档等于 AC-4。结果报告实际的模型与推理等级；实际与期望之间的不匹配作为失败呈现给调用者，而不是作为建议。
- [x] 输出：恰好是 plan、correction 或 stop 之一。执行器错误、中止或空输出返回一次明确的失败。是否重试是实现者的选择，但任何重试都以一次为界；没有重试循环。
- [x] 该组件不读取、不复制、也不发送凭据（D41）。所保留的唯一状态是按会话的，按 AC-11。
- [x] 可以从主代理、从被派发的 worker、从被派发的 explorer 实况调用，每一次都带有线程标识以及观察到的 advisor 模型与推理等级（`acceptance.md` §04）。
- [x] `operations.md` 中的 §Process consultation（及其对照）说明：
  - [x] 如何调用它、它返回什么，以及拨档与不匹配如何工作；
  - [x] 在一个会话之内，三种结果各自如何可被观察并被区分：一次咨询已开始，一次咨询已成功（在期望拨档上的一份有效 plan、correction 或 stop），以及一次咨询已失败（错误、中止、空，或不匹配）；
  - [x] 失败如何展示给调用者。

  工单 05 依赖这一点。无论用户如何决定 O3，这一区分都是必需的。
- [x] **姿态小节（EN-5）。**
  - [x] 每一个 explorer 与 worker 模板都有一个带定界的姿态小节，逐字节等于 `consult-posture.md` 中 AC-5 所指定的变体：`gpt-6-luna` 与 `gpt-6-sol` 入口为完整变体，`gpt-6-astra` 入口为精简变体。
  - [x] Advisor 模板没有姿态小节。
  - [x] 在该小节之外，同一角色的指令保持逐字节相同。
  - [x] 该小节陈述规则的结果，并且从不要求被委派者推断它自己的模型。
  - [x] 对照翻译该小节，并保持它的定界符逐字符精确。
- [x] **`verify.sh` 安装组中的姿态检查。**
  - [x] 小节相等。变体通过把每个入口的模型标识与路由配置中该档位的 advisor 模型标识相比较来计算，从不通过一份家族名称列表。
  - [x] advisor 模板中没有该小节。
  - [x] 该小节之外的同一角色同一性。
  - [x] 为每一种情形记录一条反证：被改动一个字符的小节、被给予精简变体的 `gpt-6-luna` 入口，以及被给予一个小节的 advisor 模板，各自使该组失败。

## 验证

- `sh plugins/codex-advisor/scripts/verify.sh`（全部组）
- `python3 tests/test_zh_mirror.py`
- `git diff --check`
- `acceptance.md` §04 中的实况表

## 停止条件

S3 与 S4（如果实况行为与工单 01 矛盾）、S8、S9。

## 不在本工单内

钩子、姿态注入、完成前强制、README、手册以及版本提升。

## 评论

于 2026-09-26 解决。已勾选的条目记录本工单的验收
检查点；后续工单在有规定的地方延伸中间状态。
见 `../acceptance.md` 第 04 节，其中有命令、证据、已授权的
例外以及当前结果。最终交付评审另行记录。
