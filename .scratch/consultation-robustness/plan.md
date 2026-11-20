# 流程咨询健壮性改进计划

日期：2026-11-20。依据：`.scratch/consultation-exec-yield/diagnosis.md`（含 GPT 车道意见）。

## 用户决定

2026-11-20 用户原话：“删除，批准，做，是”。对应：

1. 删除 `consult_context.py` 中“咨询边界之后不得出现 `response_item`”的检查。
2. 批准超时诊断所需的真实认证调用。用户没有给出数量；本计划自定预算为最多 10 次真实顾问调用，超出前重新征求同意。
3. 做失败即拒检查的分类审计。
4. 恢复已停用的 Windows 线程 `01a1f678-71ae-7ce1-aade-ec2b7a3575b1`（清除其失败计数）。

完整上下文、顾问无工具、明确失败、三次停用四项规则保持不变。提交、推送和两侧重装需要用户另行授权。

## 工单

| 工单 | 内容 | 执行者 | 依赖 |
|---|---|---|---|
| 01 | 删除边界检查；增加基于合成会话记录的回归用例（边界后有后台输出和后续工作，重建结果与边界时刻相同）；语料回放增加不截断的读取方式；同步 `docs/agents/plugin-maintenance.md`；版本 `0.3.11` 与版本手册 | worker，codex 车道，独立工作树 | 无 |
| 01a | ADR-0006 边界校验条文更新 | 主会话（决策记录） | 01 验收 |
| 02 | 超时诊断：固定合成上下文、同一顾问档位，按阶段记录耗时和重试，对照 WebSocket 与 HTTP 传输 | 主会话 | 无 |
| 03 | 分类审计：逐条列出 `consult_context.py`、`consult_native.py`、`process-consultation.py`、`consult_limits.py` 中的失败即拒检查，标明保护的是咨询结果正确性还是某个假设，给出处理建议 | 主会话 | 无；结论中涉及放宽的项交用户决定 |
| 04 | 清除 Windows 线程失败计数 | 主会话 | 无 |

并行：01 在独立工作树中运行，不与主工作树中用户未提交的改动混合；02、03、04 不写交付文件，可与 01 同时进行。01 的检查清单由运行器执行一次；`sh tests/verify.sh`、`python3 tests/test_shipped_wording.py`、`python3 tests/test_version_manual.py`、`git diff --check` 和本机语料回放作为批量检查，在 01 和 01a 落入主工作树后由主会话运行一次。

## 工单状态

| 工单 | 状态 | 证据 |
|---|---|---|
| 01 | 已验收 | codex 车道 `gpt-6.2-sol[medium]`（提交值，未观测），会话 `01a1f699-345d-7991-a2f7-fb446b2a9181`，回执 `complete`，6 项检查退出 0。主会话复核：在原代码上回归用例以 `History changed beyond the unfinished consultation boundary.` 报错，修复后通过；语料变更测试在原代码上失败。差异已从工作树应用到主工作树。 |
| 01a | 已完成 | ADR-0006 新增“Consultation boundary”一节。6 个真实失败案例在当前代码上读取完整文件与边界时刻读取，重建结果完全相同。 |
| 02 | 已完成 | `timeout.md`；真实调用 8 次，预算剩 2 次。 |
| 03 | 已完成 | `audit.md`；候选改动待用户决定。 |
| 04 | 已完成 | Windows 计数表删除该线程 1 行（原值 3），其余 42 行未动；操作前备份了数据库。 |

## 批量检查记录

2026-11-20，主工作树，WSL，Codex CLI `0.170.0`：

| 检查 | 结果 |
|---|---|
| `sh tests/verify.sh` | 通过，`VERIFY PASSED`，2 分 21 秒 |
| `python3 tests/test_shipped_wording.py` | 66/66 通过 |
| `python3 tests/test_version_manual.py` | 3/3 通过 |
| `python3 tests/test_zh_mirror.py` | 41/41 通过 |
| `git diff --check` | 通过 |
| `python3 tests/consultation_schema_check.py` | 18 类，`missingTypes` 为空 |
| `python3 tests/consultation_corpus_replay.py` | 874 份记录；回放 33008 个位置，32913 通过，95 个回滚按设计拒绝，失败 0；跳过 8697 个位置（未验证）；12 分 18 秒 |
| `python3 tests/consultation_native_corpus.py` | 11 类 11 项通过，仅覆盖 Responses Lite 模式 |

未验证：Windows 上的同等检查。

## 发布

2026-11-20，用户授权“提交推送，重装，验收”。发布提交 `387e0ce` 已推送，两侧重装为 `0.3.11`，
两侧安装后以 `yield_time_ms: 1` 的真实咨询均成功。记录见 `.scratch/release-0.3.11/acceptance.md`。

待用户决定：`audit.md` 的四项候选改动，`timeout.md` 的三项时限候选。
