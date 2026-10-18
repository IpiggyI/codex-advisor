# 03：保留 web_search_call、策略表外条目和未知内容块

**要构建：** `web_search_call`、策略表之外的历史条目类型和未知内容块都原样注入顾问线程，并在请求比较中必须按序出现。保护手段是实际请求比较和工单 02 的通用工具隔离检查。用户于 2026-10-18 选定此方案（`spec.md` 第 5 节决定 1 及追加的内容块决定）。ADR-0006 中“未认定形态明确失败”的规则和 `plugin-maintenance.md` 的组件契约同步改写。

**Blocked by:** 01

**Status:** resolved

- [x] `diagnosis.md` 列出的 10 月 15 日 2 个失败边界重放后通过，`web_search_call` 保留在注入列表的原位置。
- [x] 一个虚构的未知条目类型和一个未知内容块都被注入，并进入期望列表；请求中缺失或改写它们时，咨询以上下文丢失失败。
- [x] 本机固定端点链路中，含 `web_search_call` 的历史完成注入和请求比较；若宿主拒绝或改写该条目，记录实际结果，不放宽比较。
- [x] ADR-0006 和 `plugin-maintenance.md` 的对应规则与新行为一致；不涉及 `plugins/codex-advisor/**` 下的 Markdown 时无需改中文镜像，涉及时同步。

## Comments

2026-10-18：工单 01 至 04 作为一份合同交给 codex 执行器，提交档位 `gpt-6-astra[low]`（crux，依据为策略表需同时约束输入、注入、比较和工具隔离；提交值，未观测实际运行值），会话 `01a14e5c-b7af-7b80-9b9c-fb737e2f8102`。首轮回执 `verification_failed`：本机宿主丢弃虚构类型，这是合同中测试设计的缺口。主会话审查另发现两处缺陷：`web_search_call` 要求可选字段，导致 384 个真实条目中 348 个被拒；非 Lite 空工具证明被放宽。第一次返工修复这三项；第二次返工恢复对所有类型生效的传输层规范化（`id`、内部元数据、空值）。终轮回执 `complete`，四项检查退出码均为 0。

主会话验收：10 月 18 日 8 个、10 月 15 日 2 个原始失败边界用新重建函数重放，全部通过；本机 729 个会话中 384 个 `web_search_call` 全部保留，10 对工具搜索条目和 2 个 `additional_tools` 全部按能力声明排除且校验通过。本机宿主 `0.163.0` 在固定端点链路中原样转发注入的 `web_search_call` 和 `image_generation_call`，虚构类型按预期以上下文丢失失败。主工作区整批检查：`tests/verify.sh` 中咨询、安装、运行时和钩子各组通过，`verify-routing.py` 的复用时间窗测试首轮失败 1 项，随后在原始 `HEAD` 和主工作区各重跑通过，原因未复现，记为未解释的偶发失败；该测试不导入本次改动的模块；`verify-consultation-env.py` 5 项、`test_shipped_wording.py`、`test_zh_mirror.py`、`test_version_manual.py` 均通过。ADR-0006 已由主会话补充历史策略一节。未提交，未安装；真实 Responses API 行为由工单 07 验证。

2026-10-18 更正：真实咨询证明，用户配置的服务端点拒绝含 `web_search_call` 的无工具请求（400，`unsupported_parameter`，`param: input`）。保留 `web_search_call` 的做法只在本机回环端点上成立。用户决定把内置工具记录改为排除，由工单 09 实现。本工单其余结论（策略表外类型和未知内容块原样保留）不变。
