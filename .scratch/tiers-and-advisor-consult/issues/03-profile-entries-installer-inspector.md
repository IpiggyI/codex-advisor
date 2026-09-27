# 03：路由配置、十三个原生入口、安装器、检查器以及路由检查

**要构建的内容：** 主代理按新表以角色与档位挑选工作，十三个按档位命名的入口各自以它的拨档派发。
- 路由配置持有 TR-3 表、AC-4 与 AC-2 映射、拨档顺序，以及 TR-9 假设。
- 十三个入口替换十一个 0.2.0 入口，并且安装会移除旧名称。
- 检查器与验证器覆盖这组新入口，一次实况路由检查证明每一个入口都以它的拨档派发。

各入口的姿态小节由工单 04 加入，连同它们让被委派者去调用的咨询一起加入。

**Blocked by:** 01（本 Codex 版本上的拨档可用性与优先级）, 02（各入口与路由配置所指向的原则，包括仅做验收的 Advisor）。

**Status:** resolved

## 开始前必读

- `spec.md`：TR-2、TR-3、TR-9、AC-2、AC-4、EN-1 到 EN-4、EN-6、DR-2、DR-5（工单 03 的各小节）、X-2、X-4、X-5、§Testing Decisions 第 1、2、5、6 项、§Goal-Drift Checks。
- `sources.md` §2.4 行 D3、D4、D16、D16a、D19。
- `acceptance.md` §01（本 Codex 版本上的拨档可用性与优先级）。
- `plugins/codex-advisor/skills/orchestration/references/role-contracts.md`，按工单 02 留下它的样子（advisor 入口所回答的、仅验收的 Advisor 数据包）。
- 当前的 `references/routing-profile.md`、`agents/*.toml`、`agents/retire.txt`、`scripts/install-agents.sh`、`scripts/inspect-agent-runtime.sh`、`scripts/verify.sh`、`tests/test_zh_mirror.py`、`docs/zh/agents/*.toml`。
- `docs/adr/0004-*.md`（命名、固定、安装器策略）。
- `.scratch/tier-role-pool/acceptance.md` §Live route check（方法与记录形态）。

## 拥有

- `plugins/codex-advisor/skills/orchestration/references/routing-profile.md` 及其对照
- `plugins/codex-advisor/agents/*.toml`：增加十三份，删除十一份 0.2.0 模板
- `agents/retire.txt`
- `scripts/install-agents.sh`
- `scripts/inspect-agent-runtime.sh`（仅在需要时）
- `scripts/verify.sh`：安装组与运行时组
- `tests/test_zh_mirror.py`（仅在需要时）
- `docs/zh/agents/*.toml`
- `references/operations.md` 的 §Install and discover、§Select a native entry、§Invoke and validate，以及 §Verify changes 中的组列表，加上它们的对照小节

## 所确立与所消费

- **所确立** DR-2、模板的 EN-1 到 EN-4 与 EN-6，以及按交付时那样的 TR-3 表。
- **所消费** 工单 01 的拨档事实与工单 02 的原则。
- **留给工单 04：** 姿态小节（EN-5）以及验证器的姿态检查。在那之前，现有的同一角色指令相同检查保持原样。

## 验收

- [x] 路由配置的表逐单元格等于规格 TR-3，带有入口名称、`›` 候选顺序，以及 worker 的 `crux` `astra[low*, medium]`。它包含 AC-4 咨询映射、AC-2 验收映射（包括派生规则）、"not weaker" 顺序、以 "next model generation change" 为失效触发条件的 TR-9 假设，以及调整方法。不出现 `gpt-5.6-*` 模型，也不出现 Terra。
- [x] 十三份模板严格按 EN-1 所列出的那样存在：名称、文件名、模型、只在列出的地方出现被固定的推理等级、沙箱。十一份 0.2.0 模板已经不在。
- [x] Advisor 模板只回答 REVIEW 数据包。
- [x] Explorer 与 worker 模板还没有姿态小节，并且同一角色的指令逐字节相同。
- [x] `retire.txt` 列出八个 0.1.0 文件名与十一个 0.2.0 文件名。
- [x] 安装器选择器是十三个基于档位的短名称。覆盖、退役、检查以及拒绝行为未改变。
- [x] `verify.sh` 安装组增加这些检查：
  - [x] 名称、模型与固定值的配置到模板相等；
  - [x] 一份包含十一个 0.2.0 名称的退役列表。
- [x] 每一项新检查在被喂入故意错误的夹具时失败：记录反证，例如一份模型与配置不同的模板，或一份缺少一个 0.2.0 名称的退役列表。
- [x] 运行时组用例由十三份模板驱动。
- [x] 每一份模板都有一份可解析的中文对照，配置键相等。
- [x] `operations.md` 的这些小节列出十三个入口、选择器以及调用示例，除了每个入口自己的固定推理等级之外，没有拨档值。
- [x] **实况路由检查**（`acceptance.md` §03），在一个临时 `CODEX_HOME` 中，模板通过 `install-agents.sh --target-dir` 安装。每个入口一次派发，只对由调用者给出推理等级的入口传入推理等级，并且每个子代理一次检查器运行。表中有：入口、传入的推理等级、观察到的模型、观察到的推理等级、沙箱与权限、子线程、检查器退出。还要记录：在一个种入了十一份 0.2.0 文件的目录上安装会移除它们。

## 验证

- `sh plugins/codex-advisor/scripts/verify.sh`（全部组）
- `python3 tests/test_zh_mirror.py`
- `git diff --check`
- 对 `plugins/codex-advisor/`（`agents/retire.txt` 与 `.codex-plugin/plugin.json` 除外，它们由工单 06 拥有）以及 `docs/zh/` 做一次文本搜索，表明没有 0.2.0 入口名称，也没有作为档位名称使用的 `light`/`standard`/`senior`。README、ADR、较早的版本说明书以及 `.scratch/` 在这次阶段检查之外；X-5 在最终验收时覆盖它们（D45）。在一份后续工单所拥有的文件中报告命中；不要在这里修复它。

## 停止条件

S1、S2（如果路由检查与工单 01 矛盾）、S8。

## 不在本工单内

咨询组件、钩子、README、`plugin.json` 以及版本说明书。

## 评论

于 2026-09-26 解决。已勾选的条目记录本工单的验收
检查点；后续工单在有规定的地方延伸中间状态。
见 `../acceptance.md` 第 03 节，其中有命令、证据、已授权的
例外以及当前结果。最终交付评审另行记录。
