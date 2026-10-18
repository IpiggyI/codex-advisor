# 09：排除内置工具的调用记录

**要构建：** 含网页搜索、图片生成或本地命令调用的会话可以正常咨询。`web_search_call`、`image_generation_call`，以及 `local_shell_call` 与其 `function_call_output` 整对，都作为工具记录排除：不注入顾问线程，也不进入期望列表。依据是 2026-10-18 的真实请求：没有工具的顾问请求中含 `web_search_call` 时，服务端点返回 400（`Hosted tool 'web_search' requires authorization and metering that are not supported by rustponsesapi.`，`param: input`）。用户于同日决定排除（`spec.md` 用户决定第 7 条）。

**Blocked by:** 无（可以立即开始）。工单 07 等待本工单。

**Status:** resolved

- [x] 三种内置工具记录不进入注入列表和期望列表；`local_shell_call` 与其结果按对排除，只排除一半时以配对失败结束。
- [x] 10 月 15 日两个原始失败边界重建后不含 `web_search_call`，并用真实认证完成一次真实咨询，返回结构化结果。
- [x] 协议差异检查、语料重放、语料原生链路和 `tests/verify.sh` 全部通过。
- [x] 维护文档写明这一类排除，并在升级流程中写明：本机回环检查发现不了后端拒绝内置工具记录的情况，新保留的内置工具类型需要一次真实请求。

## Comments

2026-10-18：codex 执行器完成，提交档位 `gpt-6.1-sol[medium]`（提交值，未观测实际运行值），新会话 `01a14ecd-ad4b-79b0-b3e7-8deab6e0a13f`，回执 `complete`，四项检查退出码均为 0。主会话审查策略表差异：三种内置工具记录归入 `hosted` 类，验证后排除；`local_shell_call` 的结果按 `call_id` 随调用一起排除。

真实咨询（用户授权的 3 次中的第 1 次）：10 月 15 日会话第 1070 行边界，宿主 `0.162.1`，原始历史含 `web_search_call`，重建后注入 138 条且不含它；结果 `succeeded`、`plan`，预期与实际均为 `gpt-6.1-sol[high]`，顾问线程 `01a14ed4-d741-72e3-912b-c324fde0a680`。结果为 `evidence/real-consult-oct15.json`。修复前同类真实请求的 400 错误和诊断见 `evidence/real-consult.json` 与 `spec.md` 用户决定第 7 条。主工作区整批检查全部通过：`tests/verify.sh`，`verify-consultation-env.py` 6 项，`verify-consultation-host.py` 9 项，措辞与镜像检查，协议差异检查，语料重放（26,475 个边界，失败 0），语料原生链路（12 次运行全部通过，保留 8 种、排除 4 种类型）。本机语料没有 `image_generation_call` 和 `local_shell_call`，二者只有合成样本证据。
