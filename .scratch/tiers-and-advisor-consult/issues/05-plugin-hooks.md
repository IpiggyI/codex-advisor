# 05：插件钩子：姿态注入与每次派发的验证

**要构建的内容：** 随插件交付的钩子，做两件事：
- 在每一次会话开始时注入主代理的姿态变体；
- 自动验证每一次原生派发的实际模型与推理等级，并把不匹配呈现给主代理。

没有钩子运行在主代理的 `Stop` 或 worker 的 `SubagentStop` 上，并且没有钩子在一个会话之外保留任何记录。用户于 2026-09-26 取消了 AC-9，并授权以这个保留的范围继续到工单 06。Worker 仍然遵循规范的咨询姿态。

**Blocked by:** 01（本 Codex 版本上的钩子能力，包括需要受信任且正在运行的钩子的那些 P5 行）, 02（规范姿态文本）, 03（路由配置与入口，供 AC-5 比较与 AC-10 期望）, 04（咨询结果校验）。

**Status:** resolved

## 开始前必读

- `spec.md`：AC-5、AC-8、AC-9、AC-10、AC-11、AC-12、EN-5（最后一条）、DR-5（工单 05 小节）、DR-9（钩子字段）、X-2、X-3、§Decision Boundaries、§Open Decisions（O3、O4）、§Stop and Return（S5、S6、S9）、§Testing Decisions 第 3 项与第 6 项、§Goal-Drift Checks。
- `sources.md` §2.4 行 D8、D20、D27、D29、D30、D31、D33、D42。这些行背后的原文（第 1 部分 U5、U6、U10）只用于追溯，不是必读。
- `acceptance.md` §01 P5（本 Codex 版本上的钩子能力）以及 §04（咨询的可观察性）。
- `plugins/codex-advisor/skills/orchestration/references/consult-posture.md`（被注入的文本，不作修改）。
- `plugins/codex-advisor/skills/orchestration/references/routing-profile.md`（每个调用者的 advisor 模型，供 AC-5 比较；供 AC-10 的期望拨档）。
- `references/operations.md` §Process consultation（来自工单 04）。
- Codex Hooks 文档 <https://learn.chatgpt.com/docs/hooks>，重新阅读并标明日期。

## 拥有

- `plugins/codex-advisor/` 之下的插件钩子文件与脚本。
- `plugin.json` 的 `hooks` 字段，如果不使用默认位置。
- 一个 `verify.sh` 钩子组，包含在不加限定的运行中。
- `references/operations.md` 中新的 §Hooks、§Verify changes 中的钩子组，以及它们的对照。

## 验收

- [x] **`SessionStart`。**
  - 它通过把会话的模型标识与 AC-4 指定给主代理的 advisor 模型标识相比较来选择变体，并恰好注入那个 `consult-posture.md` 块加上采纳规则，逐字节相等。
  - 测试：`gpt-6-astra` 得到精简变体；`gpt-6-sol` 得到完整变体；`gpt-5.6-terra` 得到完整变体；恢复会话的情形被覆盖。
  - 如果工单 01 发现它在子代理会话中触发，子代理不从它收到任何东西。
- [x] **不存在主代理 `Stop` 或 worker `SubagentStop` 钩子**（D30 以及 AC-9 的取消）。
- [x] **AC-10 路线。**
  - 实际模型与推理等级与期望相符的一次派发是沉默的。
  - 不匹配的模型、不匹配的推理等级，以及一个由调用者给出推理等级的入口在没有推理等级的情况下被派发，各自在同一会话中呈现给主代理，而无须一次手工的检查器运行。
- [x] **AC-11。**
  - 所写入的唯一状态位于一个按会话的临时位置，并在会话结束时删除，或者不能被任何以后的会话读取。
  - 没有任何东西被写入仓库或 `CODEX_HOME`，并且没有任何东西被聚合。
  - 记录钩子代码中的每一个文件写入点以及它写到哪里。
- [x] `verify.sh` 中的钩子组在钩子命令行边界上覆盖上面的每一种情形，并带有被固定的 JSON 夹具。每一个阻断或呈现的情形也有一条反证：钩子被禁用或它的条件被反转会使测试失败。
- [x] **AC-12。** 插件、安装器或文档中没有任何东西把钩子标为受信任、编辑信任状态，或传入 `--dangerously-bypass-hook-trust`。`operations.md` 的 §Hooks 小节陈述首次安装时、以及任何改变钩子的更新之后的 `/hooks` 评审。
- [x] 实况检查（`acceptance.md` §05），在一个临时 `CODEX_HOME` 中，插件与入口已安装。每一行都记录它的信任状态：通过 `/hooks` 受信任、被绕过（仅当 O4 允许它时），或未受信任。
  - [x] 安装之后未受信任：钩子被跳过，并且宿主的 `/hooks` 警告出现；
  - [x] 至少一次运行使用用户通过 `/hooks` 信任的钩子，表明注入在没有任何绕过的情况下工作；
  - [x] 主代理在新会话中以及在恢复的会话中看到它被注入的变体；
  - [x] 一个由调用者给出推理等级的入口在没有推理等级的情况下被派发，会被呈现；
  - [x] 这些会话结束之后，没有按会话的状态留下。

## 验证

- `sh plugins/codex-advisor/scripts/verify.sh`（全部组）
- `python3 tests/test_zh_mirror.py`
- `git diff --check`
- `acceptance.md` §05 中的实况表

## 停止条件

S5、S6、S8、S9。不要用主代理的 `Stop` 钩子或只用技能的文本去替换一项缺失的钩子能力。

## 不在本工单内

README、手册、版本提升，以及任何日志或统计。

## 评论

于 2026-09-26 在主代理验证以及新的独立 senior 验收之后解决。见 `../acceptance.md` 第 05 节与 Final acceptance，其中有证据与限制。D47 取消完成阻断，D48 只允许一次本地提交，D49 只免除最终定义手册信任测试的重复。没有执行推送或真实的安装更新。
