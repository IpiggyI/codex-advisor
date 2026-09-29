# 指令审计第三轮：待确认清单

Status: ready-for-human

记录日期：2026-09-29。

本清单接管[第一轮清单](confirmation-checklist.md)和[第二轮清单](0.3.0-confirmation-checklist.md)中的全部未决项，并以最新基线重新核对。两份旧清单保留已记录的裁定和当时的证据。

用户已于 2026-09-29 裁定全部条目，见各项的"裁定"字段。以下行为仍需在执行它的那次请求中另行授权：
- 修改已安装副本；
- 修改用户配置目录或权限；
- 提交、推送、发布或部署。

## 基线

- 提交：`8f843b2d2909aa2800887f19f37abf7ce434536d`，插件版本 `0.3.0`。
- 工作区中未提交的改动也计入基线。这些改动按 ADR-0007 修改了技能的 `description` 和咨询段。行号按下表中的文件内容计算；哈希变化说明行号可能已经移动。

| 文件 | 状态 | `git hash-object` |
|---|---|---|
| `plugins/codex-advisor/skills/orchestration/SKILL.md` | 已修改 | `07ca4fd28736d001385362e5027dd5e6a87d3ae2` |
| `docs/zh/skills/orchestration/SKILL.md` | 已修改 | `eaae35d9612857b610ef2ac7b39b1b43ebb5b952` |
| `docs/adr/0007-load-orchestration-on-events.md` | 未跟踪 | `596d568813084ed69e9a1adb1f68830049504d09` |

- 本轮不把这些进行中的改动当作缺陷，只核对它们对旧发现的影响。
- 部署状态，2026-09-29 核实：
  - `git ls-remote` 显示 `origin/main` 是 `09c21c8`，即插件 `0.2.0`。`0.3.0` 从未推送。
  - WSL 与 Windows 的插件缓存都只有 `0.2.0`。
  - 两端的 `agents` 目录各有十一个 `0.2.0` 入口文件，没有 `0.1.x` 文件。
  - 本机 Codex CLI 是 `0.157.1`。README 写的认证版本是 `0.157.0`。本轮没有重新认证。
  - GitHub 仓库 `IpiggyI/codex-advisor` 是公开仓库，派生仓库数和星标数都是 0。

## 两部分的划分

- 第二部分只审查随插件发布的内容，即 `plugins/codex-advisor/` 下的全部文件。市场清单 `.agents/plugins/marketplace.json` 的 `source.path` 指向这个目录。
- 第一部分审查其余内容：仓库根目录文件、`docs/`、`tests/`，以及本机部署。
- 第二部分的条目只写插件文件。一项插件改动在仓库侧引起的改动集中写在第一部分，包括中文孪生、README、CONTEXT.md、ADR、版本说明书、测试和部署。

## 审计口径与范围

- 口径：用户的两份提示词《Agent 文档与指令体检提示词》和《会话残留清理与去冗提示词》，于 2026-09-29 从 `D:\Document\Prompts\` 读取。
- 用户本轮提出的新要求：
  1. 清单分为仓库自身内容和插件发布内容两部分，插件部分不混入仓库内容。
  2. 新议题：`SKILL.md` 和 `operations.md` 单个文件过重，并且持续膨胀。为渐进式加载，对它们精简和拆分。
  3. 新议题：插件对旧版入口的清理可以移除，改为一次性操作，因为目前只在本机部署。
  4. 清单调整完成后，先与 GPT-6-Astra 沟通一致，再开始修改。本次 Astra 的推理等级用 `xhigh`。
- 已覆盖：
  - 插件的技能正文、四个参考文件、`agents/openai.yaml`、十三个入口模板、`retire.txt`、`plugin.json`、`.mcp.json`、`hooks/hooks.json`；
  - 脚本，只用于核实文档中的说法；
  - README、AGENTS.md、CLAUDE.md、CONTEXT.md、`docs/agents/`、`docs/adr/`、中文镜像；
  - 版本说明书中与退役相关的段落。
- 未覆盖：
  - `.scratch/` 下的任务记录。它们是历史记录，按记载时点判断。
  - 业务代码审查。
  - 全局 `~/.codex/AGENTS.md`，见[两部分之外的遗留项](#两部分之外的遗留项r09r11)。
- 在上述基线上运行过的检查：
  - `python3 tests/test_zh_mirror.py`：31/31 通过。
  - `python3 tests/test_version_manual.py`：3/3 通过。
  - `sh plugins/codex-advisor/scripts/verify.sh`：通过。共 61 项测试，其中 8 项需要 Windows，已跳过。
  - `git diff --check`：没有问题。
  - 仓库和插件中 25 个 Markdown 文件的相对链接与锚点：0 个问题。锚点按近似规则生成。
- 没有测量延迟、上下文用量、成本或质量。文中标为"估计"的行数都是推算，不是测量结果。

## 如何记录裁定

用户审阅某一项之前，保持复选框未勾选。审阅后勾选，并把"裁定"字段改为 `keep`、`simplify`、`remove`、`update`、`defer` 或 `reject` 之一，再写明商定的范围。多步骤的项，每个步骤各有一个复选框，可以单独批准。勾选只表示裁定已记录，不表示已实施或已验证。

修改开始前有两道门：
1. GPT-6-Astra（`gpt-6-astra`，推理等级 `xhigh`）评审本清单，双方意见一致。
2. 用户逐项确认。

涉及安全、权限边界或减少验证的建议，另列在各部分末尾的保障变更登记中，需要在那里单独裁定。

## 需要先裁定的问题

以下问题影响多个条目。

- **Q1 版本号：** 本清单的改动进入尚未发布的 `0.3.0`，还是另起 `0.3.1`？
  - 事实：`0.3.0` 从未推送，部署版本是 `0.2.0`。[版本说明书规则](../../docs/agents/version-manual.md)写道 "A version manual is not overwritten when a later version ships"。`0.3.0` 尚未发布，所以改写 `docs/releases/0.3.0.html` 不违反这条规则。
  - 建议：并入 `0.3.0`。用户实际会从 `0.2.0` 直接升级，`0.3.0` 说明书中"相对上一版"的比较对象仍然正确。另起 `0.3.1` 会产生一份相对于无人安装过的版本的差异说明。
  - `plugin.json` 的版本号属于插件，版本说明书属于仓库，两者都跟随 Q1。
  - 裁定：并入 `0.3.0`，用户于 2026-09-29 裁定。
- **Q2 一次性清理的方式：** 取决于 Q1，见 [A01](#a01本机旧版入口的一次性清理及仓库侧改动)。
  - 裁定：手动删除，用户于 2026-09-29 裁定。
- **Q3 "5.x 版本的内容清理"的范围：**
  - 本清单的理解：`retire.txt` 列出的全部十九个旧文件名，即 `0.1.x` 的八个和 `0.2.0` 的十一个；以及安装器、测试和文档中对应的退役逻辑。
  - 这些入口属于 GPT-5.x 模型时期，但其中一部分使用 `gpt-6-astra`，所以"5.x"只是大致对应。
  - 检查器对已退役参数的专门报错（B02d）属于同类兼容逻辑。是否一并移除，由用户决定。
  - 裁定：范围是 B02a–B02d，包括 B02d，用户于 2026-09-29 裁定。删除专门报错之后，`scripts/inspect-agent-runtime.sh` 第 110 行仍以 "unknown argument." 拒绝旧参数，只失去指向 `--agent` 的提示。
- **选项型裁定：** B03 选 (a) 还是 (b)；B06 删除定义还是补上后果；B07 选 (a) 还是 (b)。
  - 裁定：B03 选 (b)；B06 删除定义；B07 选 (a)。用户于 2026-09-29 裁定。

## 旧编号对照

| 旧编号 | 状态 | 本清单中的位置 |
|---|---|---|
| R01、R02、R05、R07、R08 | 第一轮已裁定 | 不再列出 |
| R03 | 未决 | 并入 B03c，低优先级 |
| R04 | 第二轮已并入 R13 | 见 B01 |
| R06 | 未决 | 规则部分并入 A03a；升级说明部分并入 A01c |
| R09–R11 | 未决 | 不属于两部分，见两部分之外的遗留项 |
| R12 | 未决 | A07 |
| R13 | 未决 | 插件部分为 B01；仓库落点为 A02 |
| R14 | 未决 | B04；中文孪生见 A04 |
| R15 | 未决 | 插件部分并入 B01b；README 部分为 A03a |
| R16 | 未决 | 插件部分为 B05；README 部分为 A03b |
| R17 | 未决；后半项已被工作区中的 ADR-0007 改动覆盖 | 插件部分为 B03；README 部分为 A03c |
| R18 | 未决 | 插件部分为 B06；CONTEXT.md 部分见 A04 |
| R19 | 未决 | A06 |
| R20 | 未决 | A08 |
| 新增 | — | B01、B02（用户议题）；B07；A01、A02、A05 |

---

# 第一部分：本仓库自身内容

本部分涉及 `plugins/codex-advisor/` 以外的仓库文件和本机部署。

## A01：本机旧版入口的一次性清理及仓库侧改动

- [x] A01a：一次性清理两端的十一个 `0.2.0` 入口文件。
- [x] A01b：新增 ADR，记录"安装器不再删除旧文件名"及其前提。
- [x] A01c：删除 README、CONTEXT.md 和版本说明书中关于退役文件名的描述。

**裁定：** 按建议执行，用户于 2026-09-29 裁定。A01a 为 `remove`：手动删除两端各十一个 `0.2.0` 入口文件，时机和记录位置按建议；执行删除的那次请求仍需用户明确授权。A01b 为 `update`：新增 ADR。A01c 为 `remove`，版本说明书按 Q1 改 `docs/releases/0.3.0.html`。

**分类：** 部署操作和文档删除，对应插件侧的 B02。A01a 是用户配置目录中的破坏性操作。

**位置与原文：**

- 两端的入口目录：WSL 为 `~/.codex/agents/`；Windows 为 `C:\Users\<用户>\.codex\agents\`，本次从 `/mnt/c/Users/*/.codex/agents/` 观察。两端的文件名相同：
  - `ca-explorer-light.toml`、`ca-explorer-standard-m.toml`、`ca-explorer-standard-h.toml`、`ca-explorer-senior.toml`；
  - `ca-worker-light.toml`、`ca-worker-standard-m.toml`、`ca-worker-standard-h.toml`、`ca-worker-senior.toml`；
  - `ca-advisor-light.toml`、`ca-advisor-standard.toml`、`ca-advisor-senior.toml`。
- [README](../../README.md)：
  - 第 29–30 行："removes nineteen retired filenames from 0.1.0 and 0.2.0"；
  - 第 163 行："`--check` reports differing or missing templates and retained retired names"；
  - 第 175–198 行整节「Upgrade from 0.2.0」。
- [CONTEXT.md](../../CONTEXT.md) 第 33 行，安装器的定义中有 "deleting retired entry names"。
- [ADR-0004](../../docs/adr/0004-tier-named-entries-first-round-pool.md) 第 15 行："it overwrites the eleven shipped entries when they differ, deletes the eight retired filenames when present, touches nothing else, and fails its check mode on drift or residue."
- [ADR-0006](../../docs/adr/0006-mainstay-crux-rescue-and-process-consultation.md) 第 17–18 行把 `0.2.0` 的十一个入口加入退役集合。
- `docs/releases/0.3.0.html` 第 322 行、第 332 行，以及第 460 行起的「退役入口与替代入口」表。

**已核实的情况：**

- 两端当前运行 `0.2.0` 插件，它使用这十一个入口。在新版本的入口装好之前删除它们，正在使用的 `0.2.0` 插件就会失去入口。
- `0.1.x` 的八个文件名在两端都不存在，不需要清理。
- "目前只在本机部署"是用户的陈述，我们没有独立证实。仓库是公开的，派生仓库数和星标数为 0。这不能证明没有其他安装。

**建议：**

- A01a 的时机：在每一端，先升级插件并运行新安装器，确认十三个新入口已经写入。然后删除上面十一个文件，再列出目录核对。
- A01a 的方式（Q2）：
  - 如果 Q1 选择并入 `0.3.0`，就不存在一个能自动清理的中间版本，手动删除是唯一的路径。建议采用这条路径。
  - 另一条路径：先按当前代码发布 `0.3.0`，由它的退役逻辑自动清理一次，再在下一版移除退役逻辑。代价是多一次发布和部署，而且发布的是本清单还要修改的版本。
- A01a 的记录位置：该次发布的任务记录，即 `.scratch/<feature>/`。写明执行的命令，以及删除前后的目录列表。不写入 README 或 AGENTS.md，因为这个操作只执行一次。
- A01b 新 ADR 的要点：
  - 决定：安装器覆盖本插件自己的文件，不再删除任何旧文件名；`--check` 只报告缺失和不一致。
  - 前提：插件只部署在本机的 WSL 与 Windows 两端。这是用户于 2026-09-29 的陈述。
  - 失效条件：本版本发布之前，有其他机器或其他用户安装过 `0.1.x` 或 `0.2.0`。
  - 取代的内容：ADR-0004 第 15 行中关于删除退役文件名和报告残留的两个分句，以及 ADR-0006 第 17–18 行关于退役集合的句子。按 ADR-0006「What this supersedes」的写法逐句引用。
- A01c：
  - 删除 README 第 29–30 行的退役分句、第 163 行的 "and retained retired names"，以及第 175–198 行整节；
  - 改写 CONTEXT.md 第 33 行，去掉 "deleting retired entry names"；
  - 按 Q1 更新版本说明书中的对应段落。

**影响：** 仓库不再为只存在于本机的旧文件维护迁移说明。如果存在其他安装者，他们会失去迁移表和自动清理。

**验证（未运行）：**
- 删除后，两端的 `agents` 目录只剩十三个新入口和无关文件。
- 新安装器的 `--check` 通过。
- README、CONTEXT.md 和说明书中不再出现退役文件名。
- 新 ADR 的链接可以到达。

## A02：插件维护内容的落点

- [x] A02a：新建 `docs/agents/plugin-maintenance.md`，接收 B01a 迁出的内容。
- [x] A02b：在 AGENTS.md 中加一行指向和放置规则。
- [x] A02c：按 B01 的新文件结构增加、改写或删除中文孪生，并逐句核对语义。
- [x] A02d：README 中指向参考文件的链接随新结构更新。

**裁定：** `update`：A02a–A02d 按建议执行，用户于 2026-09-29 裁定。

**分类：** 迁移，并防止维护内容再次混入插件。对应插件侧的 B01。

**已核实的情况：**

- AGENTS.md 第 17 行的镜像规则只覆盖 `plugins/codex-advisor/**/*.md` 和入口 TOML。`docs/agents/` 下的新文件不需要中文孪生。
- ADR-0006「Consultation mechanism and host facts」已经记录了咨询机制和宿主事实。
- README 第 62、112、171 行链接到插件的参考文件。第 171–172 行说 `operations.md` 中有 "verification groups, metadata, lifecycle limits, and temporary checks"。验证分组迁出之后，这句话就不再成立。
- `tests/test_zh_mirror.py` 只检查孪生文件是否存在，以及 TOML 的四个键。它发现不了语义漂移；第一轮的 R02 就是这样一次漂移。

**建议：**

- A02a：维护文档接收以下内容：
  - 开发安装，`operations.md` 第 22–26 行；
  - 安装器的内部行为和安全规则，第 28–39 行；
  - 咨询组件的内部细节，第 252–325 行中调用方规则以外的部分；
  - 钩子的信任说明、`SessionStart` 的选择逻辑和内部细节，第 327–341、349–358 行；
  - 验证分组、路由变更的实机检查和原生场景清单，第 375–433 行；
  - `routing-profile.md` 第 58–64 行「Adjust a value」。

  与 ADR-0006 重复的宿主事实改为链接，不复制。
- A02a 补充：安装器的写入边界和钩子的信任边界中面向用户的部分，README 第 28–31 行和第 33–35 行已经覆盖，不需要新增；维护文档收录其余细节。钩子信任步骤见 A05。
- A02b：在 AGENTS.md 中加一行，实际措辞用英文，意思是："`plugins/codex-advisor/` 只放运行时调用方和被委派方需要读的内容；修改插件的程序写在 `docs/agents/plugin-maintenance.md`。"
  - 这一行针对膨胀的来源：维护者内容混入运行时文件。
  - 本清单不建议设行数上限。体检口径按实际阅读路径判断，不按字数判断。
- A02c：B01 新增的参考文件需要孪生，否则镜像测试失败。改写或删除的段落同步修改孪生。实施时逐句对照英文和中文的规范性句子。
- A02d：README 第 171–172 行改为指向维护文档。另外两个链接按 B01 之后的文件名核对。

**影响：** 维护者内容有一个固定的去处。今后修改维护程序时，不需要改动运行时文件。

**验证（未运行）：** 链接检查、镜像测试，以及逐句对照的记录。

## A03：README 在规则层面重复插件内容

- [x] A03a：README 第 76–143 行，每个概念只保留一段简短说明，并链接到技能。来源是 R15 和 R06 的规则部分。
- [x] A03b：删除会话残留。来源是 R16 的 README 部分。
- [x] A03c：按 B03 的裁定改写钩子的说法。来源是 R17 的 README 部分。
- [x] A03d：把 Windows 上的咨询前提写进安装前提。

**裁定：** 按建议执行，用户于 2026-09-29 裁定。A03a 为 `simplify`，A03b 为 `remove`，A03c 为 `update`（跟随 B03 选 (b)），A03d 为 `update`。

**分类：** 精简和纠正。

**已核实的情况：**

- README 第 76–143 行复述了准入、升级阶梯、咨询姿态、采纳规则、钩子和验收映射。插件规则每改一次，README 都要跟着改。验收映射在 README 第 134–138 行，与插件内的三处副本重复，插件侧见 B01b。
- A03b：
  - 第 79–80 行："The narrower alternative admission rule is recorded but disabled." 读者无法据此行动。这条规则记录在 ADR-0006 第 12–13 行。
  - 第 129–130 行："these hooks keep no state or observation log"。其中 "observation log" 指一个已经取消的提案。
- A03c：第 127–129 行："Matching dispatches are silent; ... A manual inspector is not needed for that comparison." 问题见 B03。
- A03d：咨询在 Windows 上需要原生的 `codex.exe`，写在 `operations.md` 第 314–318 行。README 第 15–18 行的安装前提没有这一条。B01a 把这一段迁出插件之后，用户能看到它的位置只剩 README。

**建议：**
- 按上面四个步骤修改。
- CONTEXT.md 作为术语表，保留它的定义，不在本项范围内。
- 自上一轮以来的变化：README 这几处原文没有变化。第二轮 R06 中的「Upgrade from 0.2.0」一节改由 A01c 删除。

**影响：** README 的读者看不到规则细节，但可以通过链接查阅。版本说明书仍然是每个版本的完整指南。

## A04：第二部分其余各项的仓库侧连带改动

- [x] 按第二部分的裁定，同步下列仓库文件。

**裁定：** `update`：跟随第二部分各项的裁定，用户于 2026-09-29 确认。B06 选删除定义，所以 CONTEXT.md 第 65 行的对应句子随之删除；版本说明书按 Q1 改 `docs/releases/0.3.0.html`；B07 选 (a)，维护文档中的验证命令随之修改。

| 插件项 | 中文孪生 | 其他仓库文件 |
|---|---|---|
| B01 | 见 A02c | README 链接见 A02d；README 规则层重复见 A03a |
| B02 | 无。脚本和 `retire.txt` 没有孪生；`operations.md` 的孪生随 B01 处理 | 见 A01 |
| B03 | `operations.md` 的孪生 | README 见 A03c |
| B04 | 十三个 TOML 孪生中的描述和注释 | 无 |
| B05 | `SKILL.md` 和 `operations.md` 的孪生 | README 见 A03b |
| B06 | `SKILL.md` 孪生 | CONTEXT.md 第 65 行："An advisory attempt must answer its specified question with a supportable conclusion." 随 B06 删除或补上后果 |
| B07 | 无 | 选 (a) 时，验证脚本移到 `tests/`，维护文档中的命令随之修改 |
| 全部 | — | 按 Q1 更新 `docs/releases/0.3.0.html`，或新建 `docs/releases/0.3.1.html` |

## A05：发布流程缺少钩子复核步骤

- [x] 审阅 A05 并记录裁定。

**裁定：** `update`：按建议在发布步骤的末尾加上 `/hooks` 复核，用户于 2026-09-29 裁定。

**分类：** 补充遗漏的用户步骤。这一项增加保障。

**位置与原始指令：** AGENTS.md 第 25 行（CLAUDE.md 相同）："Push to `origin` first, then on each side: `codex plugin marketplace upgrade codex-advisor`, reinstall `codex-advisor@codex-advisor`, and run the companion installer."

**已核实的情况：**
- 从 `0.3.0` 起，插件带有 `SessionStart` 和 `PostToolUse` 两个钩子。用户在 `/hooks` 中信任它们之前，宿主会跳过它们。更新改变钩子定义之后，需要再次信任。依据：README 第 33–35 行和第 158–159 行；ADR-0006 第 98–103 行。
- 两端现在都是 `0.2.0`，没有钩子：`09c21c8` 的插件目录和两端的 `0.2.0` 缓存中都没有 `hooks/` 目录，`plugin.json` 也没有钩子字段。下一次部署是两端第一次安装钩子。

**建议：** 在这一步的末尾加上："then ask the user to review `/hooks` in a fresh task on each side when a hook definition is new or changed." 这是用户步骤，代理不能代做。

**影响：** 如果按现有流程完成部署，两个钩子可能都处于未信任状态，并且没有任何提示，见 B03。

## A06：AGENTS.md 和 CLAUDE.md 是两份需要分别维护的副本

- [x] 审阅 A06 并记录裁定。

**裁定：** `simplify`：`CLAUDE.md` 改为一行 `@AGENTS.md`，用户于 2026-09-29 裁定。低优先级。

**分类：** 去掉重复维护。原 R19。

**已核实的情况：**
- 两个文件逐字节相同，各 25 行，都是普通文件，不是链接。
- Claude Code 官方文档 [How Claude remembers your project](https://code.claude.com/docs/en/memory)，2026-09-29 读取：
  - 存在 `CLAUDE.md` 时，默认只读 `CLAUDE.md`，不读 `AGENTS.md`。没有 `CLAUDE.md` 时，v2.1.277 及以上版本直接读 `AGENTS.md`。
  - 有些会话不能直接读 `AGENTS.md`，例如升级后的第一次会话，或者禁用了内置的 `agents-md` 插件。文档建议在这些情况下使用一个含 `@AGENTS.md` 导入的 `CLAUDE.md`。
  - 在 Windows 上，创建符号链接需要管理员权限或开发者模式；否则 Git 会把它检出为纯文本文件。
- 本机 Claude Code 版本是 `2.1.283`。
- 自上一轮以来的变化：文件没有变化。导入语法现在已按官方文档核实。

**建议：** 把 `CLAUDE.md` 的内容改为一行 `@AGENTS.md`。

**影响：** 两个宿主加载同一份仓库规则，少一处可能不同步的副本。

**验证（未运行）：** 修改后，在一个新的 Claude Code 会话中用 `/memory` 或 `/context` 确认 `AGENTS.md` 经导入加载。

## A07：领域文档中不适用的模板内容

- [x] 审阅 A07 并记录裁定。

**裁定：** `simplify`：按建议执行，用户于 2026-09-29 裁定。替换技能名之前、删除「Wayfinding operations」一节之前，先在目标宿主中核实。低优先级。

**分类：** 精简。原 R12，有一处新增。

**位置与原文：**

- [domain.md](../../docs/agents/domain.md)：
  - 第 11 行提到 `/grill-with-docs` 和 `/improve-codebase-architecture`。本会话可用的相关技能是 `domain-modeling` 和 `grilling`，没有这两个名字。某个宿主里没有，不能证明所有宿主里都没有。
  - 第 13–39 行是多上下文目录的示例。仓库选择的是单上下文，见 AGENTS.md 第 13 行。
  - 第 51 行的示例："Contradicts ADR-0007 (event-sourced orders)"。这是新增的问题：仓库现在有真实的 ADR-0007，即 `0007-load-orchestration-on-events.md`，示例的编号会误导读者。
- [issue-tracker.md](../../docs/agents/issue-tracker.md) 第 21–30 行「Wayfinding operations」服务 `/wayfinder`。本会话没有这个技能，证据边界同上。
- [triage-labels.md](../../docs/agents/triage-labels.md) 第 5–11 行，两列标签完全相同。

**建议：**
- 保留 `CONTEXT.md`、相关 ADR 和冲突披露规则。
- 删除多上下文示例。
- 把示例中的 ADR 编号改为不会与真实 ADR 重名的写法，或者去掉编号。
- 改为指向仍在维护的技能名；替换之前，在目标宿主中核实。
- 分诊表去掉重复的一列，保留每个状态的含义。
- 确认目标宿主没有 `/wayfinder` 之后，删除「Wayfinding operations」一节。

**影响：** 减少模板阅读，以及对不存在入口的搜索。

## A08：ADR-0006 保存了它自己说应放在别处的探查细节

- [x] 审阅 A08 并记录裁定。

**裁定：** `simplify`：按建议执行，用户于 2026-09-29 裁定。低优先级。

**分类：** 迁移。原 R20。

**位置与原文：**
- [ADR-0006](../../docs/adr/0006-mainstay-crux-rescue-and-process-consultation.md) 第 105–120 行记录了线程标识、对话框按钮文字和 `/hooks` 计数，随后写道："The detailed sequence belongs in the P7 trust record."
- 第 75–79 行："These facts were established on 2026-09-26 with Codex CLI `0.157.0`:" 这句话和它引出的表格之间，插入了一段维护来源说明。

**已核实的情况：** 提交 `8f843b2` 把第 77–79 行和第 120 行的链接锚点改成了中文任务记录的锚点，链接检查通过。问题本身没有变化。

**建议：** ADR 中只保留信任边界的结论和失效检查，详细过程改为链接到 P7 记录。把维护来源说明移到表格之后。

**影响：** 只涉及面向维护者的记录，不影响运行时。

## 两部分之外的遗留项：R09–R11

- [x] 审阅这三项的去向并记录裁定。

R09–R11 针对全局 `~/.codex/AGENTS.md`，它不是本仓库的产出。ADR-0007 说用户级指令 "maintained in the user's prompts repository"。本机的 `~/.codex/AGENTS.md` 与 `D:\Document\Prompts\AGENTS.md` 内容不同，本轮没有确认它的来源仓库。

建议：在本清单中关闭这三项，转入维护全局指令的那个仓库自己的审计。三项在那里仍然是未决状态。

**裁定：** `defer`：在本清单中关闭，转入维护全局指令的仓库自己的审计，用户于 2026-09-29 裁定。

## 第一部分的保障变更登记

| 项 | 建议的改动 | 涉及的保护 | 保留的保障或替代保障 |
|---|---|---|---|
| A01a | 一次性删除两端各十一个旧入口文件 | 用户配置目录中的文件；没有备份时不可恢复 | 执行前列出目标，并在执行它的那次请求中获得用户的明确授权；可以先复制到临时目录；删除后列出目录核对 |
| A01a | 删除的时机 | 正在使用的 `0.2.0` 插件 | 只在该端装好新入口之后删除 |
| A01c | 删除 README 的升级说明和退役描述 | 其他安装者得到迁移指引 | 前提是只在本机部署，并记入 A01b 的 ADR；仓库公开、派生仓库数为 0 是剩余风险 |
| A02b | 维护验证说明迁出插件 | 维护者在发布前验证插件改动 | AGENTS.md 指向维护文档。在本仓库中工作时，Codex 加载 AGENTS.md，Claude Code 加载 CLAUDE.md，见 A06 |
| A03c | 改写 README 的钩子说法 | 派发核验 | 同 B03 |
| A06 | `CLAUDE.md` 改为导入 | Claude Code 会话加载仓库规则 | 修改后在新会话中用 `/memory` 或 `/context` 确认 |

A05 增加一项保障，不在此表中。第一部分没有建议放宽权限或取消必需的验证。

2026-09-29：用户按建议裁定了本表各项。A01a 的删除仍需在执行它的那次请求中获得用户的明确授权。

---

# 第二部分：随插件发布的内容

本部分只涉及 `plugins/codex-advisor/` 下的文件。每一项在仓库侧引起的改动，集中写在第一部分 A01–A04。

## 机器解析的文本：任何修改都必须遵守的硬约束

以下内容于 2026-09-29 重新核对，自第二轮以来没有变化。

- `scripts/consult_context.py` 的 `route()`，第 176–203 行：
  - 在 `routing-profile.md` 全文中收集 `` `ca_name` gpt-…[efforts] `` 形式的匹配，存入一个字典。正文中后出现的同形写法会悄悄覆盖表格中的值。
  - 把调用方所在档位 `Advisor` 单元格中列出的第一个推理等级当作咨询的推理等级。
  - 依赖 `routing-profile.md` 第 48–50 行 "compare model first: … . Compare effort second: … ." 的原样结构和换行位置。改写之后，所有咨询都会失败，并报 "Routing profile ordering is unavailable."。
- `scripts/advisor-hooks.py` 的 `posture()`，第 44–62 行：
  - 要求所有 `` `ca_advisor_…` model[ `` 匹配中只出现一个模型；
  - 按 `consult-posture.md` 中的 `<!-- consult-posture:…:start -->` 和 `<!-- consult-posture:…:end -->` 标记取块。
- `scripts/verify.sh` 的 `parse_profile()`：
  - 在所有表格行中，每个 `ca_` 名称只出现一次；
  - 模板有固定推理等级的字段，当且仅当单元格里只有一个不带星号的推理等级。
- `scripts/verify-hooks.py` 在一个反例夹具中精确替换子串 `` `ca_advisor_rescue` gpt-6-astra ``。
- `consult-posture.md` 的姿态块逐字节复制到各入口，也由 `SessionStart` 钩子注入。`verify.sh` 检查英文副本和中文副本。

因此，任何一项都不移动、不重命名 `routing-profile.md` 和 `consult-posture.md`，不改写上述句式，也不在路由配置的正文中重复拨档写法。

## B01：按加载事件精简并拆分技能正文与 `operations.md`

- [x] B01a：把只服务维护者的内容移出插件。落点见 A02。
- [x] B01b：每条运行时规则只留一处。
- [x] B01c：按加载事件重组文件。`SKILL.md` 保留公共路径，条件分支放进按事件读取的参考文件。
- [x] B01d：把 `SKILL.md` 第 27–30 行的"委派前全部阅读"改为事件和文件的对照。

**裁定：** 按建议执行，用户于 2026-09-29 裁定。B01a、B01c、B01d 为 `update`，B01b 为 `simplify`。B01c 的可选项不做，权限观察和检查器核对留在 `operations.md`。咨询失败时调用方的规则同时写进 `process-consultation.py` 的工具描述。

**分类：** 精简、迁移和拆分。这是用户本轮的新议题，合并了第二轮 R13（其中含第一轮 R04）和 R15 的插件部分。B01a、B01b、B01c 涉及保障。

**位置与原始指令：**

- `SKILL.md` 第 27–30 行："Before a delegated call, read the relevant packet in role-contracts.md, the installation, invocation, evidence, and permission procedures in operations.md, and the dial table in routing-profile.md."
- `SKILL.md` 第 3 行的 `description`，即工作区中按 ADR-0007 修改的版本，列出了技能的加载事件：
  - 被要求委派，或即将委派；
  - 即将验收、返工或升级一个委派结果；
  - 用户授权 Architect 模式；
  - 交付需要独立验收；
  - 主代理、worker 或 Explorer 缺少适用的姿态块或采纳块。

**已核实的情况：**

- 增长趋势，单位为行：

| 节点 | `SKILL.md` | `operations.md` | `role-contracts.md` | `routing-profile.md` | `consult-posture.md` |
|---|---|---|---|---|---|
| `0.1.0`（`f37830f`） | 141 | 234 | 145 | — | — |
| `0.2.0`（`09c21c8`） | 154 | 266 | 157 | 42 | — |
| ADR-0005（`f812f9b`） | 170 | 300 | 163 | 42 | — |
| `0.3.0`（`5c2728d`） | 182 | 433 | 129 | 64 | 62 |
| 工作区 | 184 | 433 | 129 | 64 | 62 |

  五个文件合计 6,970 词，由 `wc -w` 统计。
- 委派调用前的阅读量：
  - 按整文件计：`SKILL.md` 184 行、`operations.md` 433 行、`role-contracts.md` 129 行、`routing-profile.md` 64 行，共 810 行。
  - 只读第 27–30 行点名的章节，约 390 行。
  - 第 27–30 行没有给出章节锚点。模型实际读整个文件还是只读章节，没有观测。
- `operations.md` 各段的读者。该文件自 `5c2728d` 以来没有变化，行号与第二轮相同：

| 内容 | `operations.md` 行号 | 读者 | 已有位置或重复处 |
|---|---|---|---|
| 派发前的 `--check-role`、派发参数、`task_name` 规则、证据核对、权限观察 | 15–20、73–122、360–373 | 运行时调用方 | 只在此处 |
| 开发安装、安装器内部行为与安全规则 | 22–39 | 维护者；安装插件的用户 | README 第 28–31 行覆盖面向用户的部分 |
| 入口表和 `Effort` 列 | 41–69 | 调用方 | `routing-profile.md` 第 13–25 行 |
| 恢复、升级阶梯、线程生命周期 | 128–158、181–184 | 调用方 | `SKILL.md` 第 73–114 行，几乎逐句相同 |
| 交接模板、转移证据 | 160–179、186–189 | 调用方 | 只在此处 |
| 调度与合并检查 | 191–222 | 调用方 | `SKILL.md` 第 63–71、153–160 行 |
| 咨询与验收 | 224–250 | 调用方 | `SKILL.md` 第 116–184 行；`role-contracts.md` 第 76–88 行 |
| 咨询组件：调用、隔离、结果、Windows、重新认证 | 252–325 | 维护者；结果含义面向调用方 | ADR-0006「Consultation mechanism and host facts」 |
| 钩子：信任、`SessionStart`、`PostToolUse`、内部细节 | 327–358 | 用户；维护者；调用方只需要消息的含义 | ADR-0006 第 38–43、98–103 行 |
| 验证分组、路由变更的实机检查、原生场景清单 | 375–433 | 修改本插件的维护者 | 只在此处 |

- 规则的重复：
  - 验收映射写在 `SKILL.md` 第 171–177 行、`operations.md` 第 235–241 行、`role-contracts.md` 第 79–84 行和 `routing-profile.md` 第 38–46 行。而 `SKILL.md` 第 30–32 行写道："Every model name, effort option, default, candidate order, consultation mapping, and acceptance mapping lives in the routing profile." 这是原 R15 的插件部分。
  - 入口表的入口名、`_m`/`_h` 顺序和 `Effort` 列与路由配置重复。"安装选择器"一列可以由安装器用法说明中的规则推出：`install-agents.sh` 第 18–19 行，"filename stem minus the plugin prefix"。
  - `routing-profile.md` 第 24–25 行写了一条派发规则：把 `fork_turns` 设为 none。这条规则属于派发步骤。
- 自上一轮以来的变化：ADR-0007 把咨询从加载事件中移除。因此没有任何运行时指令指向 `operations.md` 第 252–325 行「Process consultation」：技能不因咨询而加载，第 27–30 行也没有点名这一节。模型是否会因为读整个文件而读到这一节，没有观测。可以确定的是，调用方咨询时一定能看到两样东西：
  - 工具描述中的 "an explicit failure leaves the work pending"，见 `scripts/process-consultation.py` 第 15–17 行；
  - 注入的姿态块和采纳块。

**建议：**

原则：
- `SKILL.md` 放每个加载事件都要用的公共路径。
- 每个条件分支只放在一个以事件命名的参考文件中。
- 数值留在 `routing-profile.md`，姿态留在 `consult-posture.md`。
- 维护者内容移出插件。
- 每个分支在 `SKILL.md` 中保留一行不变量。这样，即使模型没有跟随指针读取分支文件，关键护栏仍在上下文中。示例：验收失败后，先在同一线程、同一拨档返工；推理等级、模型或角色的任何变化都使用新线程。

B01a，迁出：`operations.md` 第 22–26、28–39、252–325（调用方规则除外）、327–341、349–358、375–433 行，以及 `routing-profile.md` 第 58–64 行。去处见第一部分 A02a。

B01b，去重：
- 删除上面列出的重复规则。
- 验收映射只留在 `routing-profile.md`；其他位置写"按路由配置的验收映射选择拨档"。
- 入口表换成一句选择器规则。
- `routing-profile.md` 第 24–25 行的派发规则移到派发参考中。

B01c，文件结构。行数为估计：

| 文件 | 何时读 | 内容 | 主要来源 | 估计行数 |
|---|---|---|---|---|
| `SKILL.md` | 技能加载时 | 授权与 Architect 模式；角色与档位选择；委派契约要点；调度原则；普通验收，即主代理检查；咨询段；事件与文件的对照；每个分支的一行不变量 | `SKILL.md` 第 8–71、116–164 行，精简 | 80–100 |
| `references/operations.md`，保留文件名，内容改为派发操作 | 每次委派调用前，包括为独立验收派发 Advisor | 派发前的 `--check-role`；派发参数和 `task_name`；不要手改入口文件；钩子消息的含义；检查器和证据；容量未知与并行声明；只读入口只接不写入的检查；权限观察 | `operations.md` 第 5–20、43–48、73–122、193–197、209–211、220–222、343–348、360–373 行 | 90–110 |
| `references/recovery.md`，新文件 | 验收失败后，改派之前 | 完整尝试、诊断、升级阶梯、线程生命周期、交接模板、转移证据 | `SKILL.md` 第 73–114 行；`operations.md` 第 160–189 行 | 60–70 |
| `references/independent-acceptance.md`，新文件 | 需要独立验收时 | 触发条件与风险定义；Advisor 验收数据包；对评审的核对；修正后重新评审 | `SKILL.md` 第 166–184 行；`operations.md` 第 240–250 行；`role-contracts.md` 第 76–129 行 | 70–90 |
| `references/role-contracts.md` | 委派调用前 | Explorer 和 Worker 数据包 | 第 1–74 行 | 约 75 |
| `references/routing-profile.md` | 选择拨档时 | 数值；解析结构不变 | 删去第 24–25 行和第 58–64 行 | 约 55 |
| `references/consult-posture.md` | 姿态块缺失或不适用时 | 不变 | — | 62 |

各加载事件的阅读量对照。建议后的数字都是估计：

| 加载事件 | 现在：整文件 / 点名章节 | 建议后 | 该事件跳过的参考文件 |
|---|---|---|---|
| 委派调用 | 810 / 约 390 | 约 220–340 | `recovery.md`、`independent-acceptance.md`、`consult-posture.md` |
| 验收委派结果（普通） | 184 | 80–100，只读 `SKILL.md` | 全部参考文件 |
| 返工或升级 | 184 加上 `operations.md` 中的交接模板，最多 617 | 约 140–170；改派时再读派发所需的三个文件 | `independent-acceptance.md`、`consult-posture.md` |
| 独立验收 | 约 330 / 最多 810 | 约 285–355 | `recovery.md`、`role-contracts.md` |
| 姿态块缺失 | 310 | 约 200–220 | 其余参考文件 |

薄壳检查：上表最后一列表明，每个参考文件至少被一个加载事件跳过。如果实施后发现某个文件在每个事件中都要读，就把它并回 `SKILL.md`。

B01d：把 `SKILL.md` 第 27–30 行改为事件对照，实际措辞用英文：
- 委派调用前：读 `operations.md`、相应的数据包和路由表；
- 验收失败后：读 `recovery.md`；
- 需要独立验收时：读 `independent-acceptance.md` 和验收映射；
- 姿态块缺失时：读 `consult-posture.md` 和咨询映射。

**不能丢的内容：** 以下内容只存在于 `operations.md`，必须迁移，不能消失。

- 风险定义，第 240–241 行："Risk follows consequences, reversibility, and difficulty checking correctness, not step/file count or model." 这是"高风险"唯一的正面定义。移到 `independent-acceptance.md`。
- 交接模板，第 165–179 行。移到 `recovery.md`。
- 转移证据，第 186–189 行。移到 `recovery.md`。
- 容量未知时的规则，第 196–197 行："If capacity is unknown, use one worker until established"。留在 `operations.md`。
- 声称并行执行所需的证据，第 220–222 行。留在 `operations.md`。
- `task_name` 与消息首行的规则，第 75–77 行。留在 `operations.md`。
- 只读入口只执行不写入的检查，第 210–211 行。留在 `operations.md`。
- 第 91–92 行："Never edit entry files or primary settings to adjust effort." 留在 `operations.md`。
- 第 46–48 行：Explorer 和 Advisor 入口不加载技能也可以调用；仅仅安装不会产生全局路由默认值。留在 `operations.md`。
- 咨询失败时调用方的规则，第 305–307 行："The caller states the failure in its next visible reply; it must not present the failure as advice or declare consultation complete."
  - 在 `SKILL.md` 的咨询段保留一句。
  - 技能没有加载时，调用方只能看到工具描述中的 "an explicit failure leaves the work pending"。是否把这句规则扩写进工具描述，由用户决定。这是 `process-consultation.py` 的代码改动。
  - 裁定：写进工具描述，用户于 2026-09-29 裁定。
- 安装器的安全规则（第 32–39 行）和信任边界（第 331–333 行）：迁出插件，只迁移，不删除。去处见第一部分 A02a。

**刻意保留：**
- `SKILL.md` 第 39 行 "There is no usage quota"。它对应一个真实的用户故事，防止主代理限量使用 `crux`。
- `consult-posture.md` 第 6 行的 `gpt-5.6-terra` 示例，以及 "Do not infer posture from a model family"。

**影响：**
- 每个加载事件只读它需要的分支。每条规则只有一个修改点。
- 插件中的技能 Markdown 从 872 行降到约 520 行，这是估计；约 200 行维护内容移到仓库。
- 风险：模型可能不跟随指针读取分支文件。一行不变量和下面的行为场景用来发现并缓解这个风险。
- 新增两个参考文件，仓库侧相应增加两份中文孪生，见 A02c。

**验证（未运行）：**
- 结构：镜像测试、完整的 `verify.sh`、`git diff --check` 和链接检查。
- 覆盖：实施时做一张对照表。旧文件中的每一句规范性句子，都对应一个新位置，或者写明删除理由。
- 行为：结果取决于模型，需要在临时 `CODEX_HOME` 中运行。
  1. 派发。任务：一个需要由调用方选择推理等级的 `worker` 的小任务。通过标准：首次使用前运行 `--check-role`；使用 `fork_turns: none`；`task_name` 等于消息首行；传入路由配置中列出的推理等级。
  2. 失败恢复。任务：一个预设为验收失败的小任务。通过标准：先在同一线程、同一拨档返工；再次失败并诊断为能力问题时，在新线程中升到下一档，并使用交接模板。
  3. 独立验收。任务：用户明确要求独立评审的一个小交付。通过标准：主代理完成检查之后，在新线程中使用 Advisor 入口，按验收映射选择拨档，并发送验收数据包。

## B02：移除旧版入口的退役机制

- [x] B02a：删除 `agents/retire.txt`，以及安装器中读取、检查和删除退役文件名的代码与用法说明。
- [x] B02b：删除 `verify.sh` 中针对退役的夹具和断言。
- [x] B02c：删除 `operations.md` 中关于退役的描述，与 B01a 一并处理。
- [x] B02d：可选，见 Q3。删除检查器对已退役参数的专门报错，以及相应的测试和文档。

**裁定：** `remove`：B02a–B02d 按建议执行，范围由 Q3 确定，用户于 2026-09-29 裁定。顺序按「顺序约束」：B02 与其他改动在同一版本发布，A01a 在两端装好新入口之后执行。

**分类：** 删除，并改变功能和测试覆盖。涉及保障。这是用户本轮的新议题。

**位置与原文：**

- `agents/retire.txt` 第 1–20 行，共十九个文件名。
- `scripts/install-agents.sh`：
  - 第 12–13 行的用法说明："remove retired names"；
  - 第 16–21 行中 `--check` 和 `--check-role` 关于退役文件的说明；
  - 第 28 行；
  - 第 52–63 行读取退役清单，其中第 52 行的注释是 "Later tickets edit retire.txt."；
  - 第 131–139 行，`--check` 报告残留；
  - 第 152–156 行的预检；
  - 第 178–186 行的删除。
- `scripts/verify.sh`：
  - 第 235–259 行的残留夹具；
  - 第 298–367 行的退役集合、`0.1.0` 遗留目录和符号链接夹具，其中第 304 行读取仓库中的 `docs/adr/0004-…md`；
  - 第 383–384 行的通过信息。
- `skills/orchestration/references/operations.md` 第 28–35、387–392、422 行。
- B02d：`scripts/inspect-agent-runtime.sh` 第 28、104–108 行；`scripts/verify.sh` 第 478–486 行；`operations.md` 第 124–125 行，与 B05 重叠。

**已核实的情况：**
- 十九个名字中，八个是 `0.1.x` 的 `codex-advisor-*` 入口，十一个是 `0.2.0` 的 `light`、`standard`、`senior` 入口。从 `f37830f` 和 `09c21c8` 的模板读取，它们使用 `gpt-5.6-luna`、`gpt-5.6-sol`、`gpt-5.6-terra` 和 `gpt-6-astra`。
- 部署状态见基线。实际需要清理的只有本机两端各十一个 `0.2.0` 文件。一次性操作写在第一部分 A01。
- 移除之后，安装器保留三项行为：覆盖本插件自己的文件；`--check` 报告缺失和不一致；拒绝不安全的目标路径。

**建议：**
- 按四个步骤删除。
- 安装器的用法说明改为 "overwrite this plugin's own files and leave everything else untouched"。

**刻意保留：**
- `consult-posture.md` 第 6 行、`verify-hooks.py` 第 103 行、`verify-consultation.py` 第 418 行的 `gpt-5.6-terra`，是"未知模型"的示例或夹具，不是清理逻辑。
- `verify-consultation.py` 第 114 行的 `…/codex-advisor/0.2.0` 是缓存布局的夹具路径。

**顺序约束：** B02 可以与其他改动在同一版本中发布。但第一部分的 A01a 必须在两端装好新入口之后执行。

**影响：**
- 删除约 20 行清单、约 40 行安装器代码、约 90 行测试和相应文档。这些数字是估计。
- 安装器的写入面变窄：它不再删除任何文件。
- 失去的覆盖：其他安装上的旧入口不再被自动删除；`--check` 不再报告残留。

**验证（未运行）：**
- 删除退役断言后，`verify.sh --installation` 通过。
- 夹具中的无关文件保持不变。
- 在干净的目标目录上，`--check` 通过。
- 安装器的用法说明不再提到退役。

## B03：钩子被跳过和派发检查通过，表现完全相同

- [x] B03a：二选一。(a) 只改文档；(b) 检查通过时输出一行确认。
- [x] B03b：写明检查器的其他检查项何时仍需手动执行。
- [x] B03c：低优先级。把 "actual" 限定为实际观察到的证据层。

**裁定：** `update`，用户于 2026-09-29 裁定。B03a 采用 (b)，包括 `scripts/verify-hooks.py` 的测试改动；B03b、B03c 按建议执行。

**分类：** 纠正一项验证声明。方案 (b) 是功能变更。合并了原 R17 的插件部分和原 R03 的剩余部分。

**自上一轮以来的变化：**
- 工作区中的 ADR-0007 改动已经处理了第二轮 R17 的后半项。技能的 `description` 把"缺少适用的姿态块或采纳块"列为加载事件；`SKILL.md` 第 131–138 行在块缺失时读取 `consult-posture.md`。
- 这项处理是否生效，取决于模型能否察觉块的缺失，没有验证。
- 剩余的问题是 `PostToolUse` 的静默。

**位置与原始指令：**
- `operations.md` 第 345–348 行："Matching dispatches are silent. … No manual inspector run is needed for this comparison."
- 第 331–333 行："the host skips untrusted hooks and prints a startup warning pointing to `/hooks`. The plugin does not modify trust state or add its own untrusted-hook detector."
- 第 110–111 行仍然要求调用方 "Validate role, model, effort, thread, parent association, working directory, and observed permissions."
- B03c：`SKILL.md` 第 122 行 "with its actual model and effort"；`operations.md` 第 350 行 "reads its actual turn model and effort"。

**已核实的情况：**
- 派发检查通过时没有输出；钩子因为未被信任而被跳过时，同样没有输出。调用方无法区分这两种情况。启动警告是否会进入模型上下文，没有验证。
- 钩子核对派发的身份关联（角色、父线程、会话、任务路径）以及模型和推理等级，见 `scripts/advisor-hooks.py` 第 82–117 行。工作目录和权限不在钩子的范围内，仍要用原生元数据或检查器核对；文档没有说明何时需要这样做。
- 信任按每个钩子的哈希分别授予，见 ADR-0006 第 98–103 行。`SessionStart` 在运行，不能证明 `PostToolUse` 已被信任。
- B03c：钩子读取子会话头中的回合设置；咨询组件读取宿主的推理请求追踪。两者都是宿主的记录，不是服务端执行的独立证据。

**建议：**
- (a) 只改文档：把"无需手动运行检查器"改为以钩子已被信任为前提；写明工作目录和权限何时仍要用检查器核对。局限：缺口被写明了，但仍然存在。
- (b) 改代码：检查通过时，钩子输出一行简短的确认。这样，没有输出就说明钩子没有运行。代价是每次派发增加少量上下文。建议采用 (b)。
- (b) 还要修改 `scripts/verify-hooks.py`。它的第 146、150、164、205 行断言检查通过时钩子没有输出（`run(...) is None`），`verify.sh` 第 604 行运行这个测试。这些断言改为断言输出确认行；新断言在钩子被禁用时必须失败，写法同第 45–54 行的 `pending()`。B07 选 (a) 时，这个测试随 B07 移出插件。
- B03c：把这两处 "actual" 改为点名证据层，例如 "host-recorded"。不要求为此做服务端调查。

**影响与失去的覆盖：** 按现有文字，主代理可能把一次未经检查的派发报告为已核实。(b) 恢复这项保证；(a) 只缩小缺口。

**验证（未运行）：**
- 在临时 `CODEX_HOME` 中保持 `PostToolUse` 未被信任，用错误的推理等级派发一个由调用方选择推理等级的入口。通过标准：主代理没有把这次派发报告为已核实。
- 选择 (b) 时，再验证：钩子被信任之后，一次正确的派发会出现确认行。
- 选择 (b) 时，完整的 `verify.sh` 通过，其中包括 `verify-hooks.py` 对确认行的新断言和它们的禁用反例。

## B04：入口的模型和推理等级写在多处

- [x] 审阅 B04 并记录裁定。

**裁定：** `simplify`：按建议执行，用户于 2026-09-29 裁定。描述中的模型名和 "effort fixed at …" 只在宿主的显示得到确认之后删除；否则保留，只删注释、改正路由配置第 4–6 行的声明。关于描述的部分会部分推翻 `0.2.0` 的一项决定。

**分类：** 精简。原 R14。删除注释一项涉及保障。

**自上一轮以来的变化：** 模板没有变化。本机 CLI 从 `0.157.0` 变为 `0.157.1`。宿主是否在角色列表中显示模型和推理等级，仍然没有验证。

**位置与原始指令：** 十三个[入口模板](../../plugins/codex-advisor/agents/)。以 `ca-advisor-crux.toml` 为例：
- 第 2 行："Advisor, crux tier: gpt-6-astra, effort fixed at high."
- 第 4 行：`model_reasoning_effort = "high"`
- 第 7 行："# Effort is pinned on this entry; a caller override is not required."

七个由调用方选择推理等级的入口，描述写 "the caller passes reasoning_effort"，注释写 "# The caller selects effort; a role-level setting would override that choice."。

[routing-profile.md](../../plugins/codex-advisor/skills/orchestration/references/routing-profile.md) 第 4–6 行写道："This file is the only place where effort options, defaults, and candidate order are written; `SKILL.md` and entry descriptions do not repeat them."

**已核实的情况：**
- 六个固定推理等级的入口，在描述和字段中各写一次值，注释又重复说一次"已固定"。七个由调用方选择的入口，在描述和注释中有两处表述。
- `verify.sh` 核对字段与路由配置是否一致，但不检查描述和注释。这两份副本改错了也不会被发现。
- 对入口描述而言，路由配置第 4–6 行的声明不成立。ADR-0006 第 15–16 行规定路由配置是 "the sole source for model, effort, default, candidate, consultation, and acceptance dials"。所以偏离现行决定的是入口描述，不是路由配置。
- TOML 注释不会进入模型上下文，只对维护者可见。注释所说的规则，`verify.sh` 已经在强制检查。
- 宿主探查（第二轮，从 Codex CLI `0.157.0` 程序文件中的字符串推断，不是直接观察）：宿主会在角色列表中，把固定的模型和推理等级附加到每个角色的描述之后。
- [`0.2.0` 规格](../tier-role-pool/spec.md)有三处相关内容：
  - 用户故事 15（第 41 行）要求描述写出模型和推理等级是否固定，"以便我可以不加载技能就从代理列表中选择它"；
  - 第 84 行又说 TOML 描述不重复推理等级或默认值；
  - 第 143 行把"宿主是否向主代理展示自定义代理的描述"留作未验证。

**建议：**
- 删除十三个模板中的注释行。
- 描述保留角色、档位、候选位置、用途和 `fork_turns none`。
- 由调用方选择推理等级的入口，描述保留 "the caller passes reasoning_effort"。原因有两个：宿主不会显示"必须传入推理等级"之类的提示；漏传时，`PostToolUse` 钩子会报 "A caller-effort entry was spawned without reasoning_effort."，并把这次派发标为待定。
- 如果宿主的显示得到确认，就从描述中删去模型名和 "effort fixed at …"。
- 改正路由配置第 4–6 行，使声明与实际一致。

**影响：** 固定的值只保留在字段和路由配置的表格两处，两处都有 `verify.sh` 检查。没有检查的副本不再存在。如果宿主的显示得到确认，用户故事 15 的需求就由宿主满足。

**验证（未运行）：** 在 `0.157.1` 的临时 `CODEX_HOME` 中，查看派发工具的角色列表。通过标准：一个固定入口显示了模型和推理等级。可以从请求追踪中查看，也可以让主代理原样引用角色列表。如果不显示，描述保留模型名和固定的推理等级，只删注释、改正声明。

## B05：运行时文本中的会话残留

- [x] 审阅 B05 并记录裁定。

**裁定：** `remove`：删除上述四处，保留刻意保留的句子，用户于 2026-09-29 裁定。

**分类：** 删除或改写。原 R16 的插件部分。

**自上一轮以来的变化：** 以下原文都没有变化。

**位置、原文与来源：**
- `SKILL.md` 第 11–12 行："A midrange primary is a preference, not a plugin requirement."
  - 来源是 `autonomous-role-pool` 规格中关于主代理模型的用户故事，当时针对上游固定使用 Sol 做主代理的设计。
  - 前一句 "Preserve the user's primary model and reasoning effort" 已经表达了这条规则。
- `SKILL.md` 第 40–41 行："The narrower admission rule recorded for possible future use is not enabled."
  - 运行时文档从未定义这条规则，读者无法据此行动。
  - 这条规则记录在 ADR-0006 第 12–13 行和相应规格中。
- `operations.md` 第 124–125 行："Earlier review-selection and per-role options fail with a diagnostic that names `--agent`."
  - 这是 `0.1.0` 的迁移说明，脚本自身的报错已经覆盖。与 B02d 重叠。
- `operations.md` 第 356–357 行："There is no primary `Stop` or worker `SubagentStop` hook."
  - 它提到的是一个已经取消的提案，见 ADR-0006 第 38–43 行。
  - 保留其中可执行的部分：调用方自己遵循姿态，没有任何机制会自动阻止完成。

**刻意保留：** 同 B01 的"刻意保留"。

**建议：** 删除上述四处，保留刻意保留的句子。

**验证：** 这些只是文字修改，运行镜像测试和链接检查即可。被删除的句子没有任何规则依赖它们，所以不提议做行为测试。

## B06：顾问失败的定义没有后果

- [x] 审阅 B06 并记录裁定。

**裁定：** `remove`：删除 `SKILL.md` 第 142–145 行的定义，用户于 2026-09-29 裁定。

**分类：** 删除，或者补上后果；后者是行为变更。原 R18 的插件部分。

**位置与原始指令：** `SKILL.md` 第 142–145 行："A complete advisory attempt fails when it does not answer its specified question or source and verification evidence materially invalidate its conclusion. Mere disagreement, intermediate tool errors, and worker failure alone are not complete advisory failures."

**已核实的情况：**
- 在 ADR-0003 之下，这个定义用来判断 `Advisor` 能否使用 `xhigh`。ADR-0006 第 150 行已经取代了那条规则。现在没有任何运行时文本说明，一次完整的顾问尝试失败之后该怎么做。
- 自上一轮以来的变化：无。补充一点：`SKILL.md` 第 126–129 行用几乎相同的措辞定义了"完整的咨询尝试"。那个定义在别处有后果：没有返回允许的结果时，返回明确的失败，工作保持待定，见 `operations.md` 第 305–307 行和工具描述；结论被证据推翻时，适用采纳块中的偏离规则。两个几乎相同的定义服务两种用途，容易混淆。

**建议：** 二选一。
- 删除第 142–145 行的定义。行为不变。建议采用。
- 写明失败后的处理，例如：验收保持待定，由同一入口在新线程中重新评审，或者交给用户决定。这会改变验收行为。

## B07：维护者验证脚本随插件发布，并依赖不随插件发布的仓库文件

- [x] 审阅 B07 并记录裁定。

**裁定：** `update`：采用 (a)，把 `verify.sh`、`verify-hooks.py`、`verify-consultation.py` 和 `scripts/fixtures/` 移到仓库的 `tests/`，用户于 2026-09-29 裁定。低优先级。

**分类：** 测试位置变更，属于功能变更，单独列出。新发现。

**位置：**
- `scripts/verify.sh` 第 22 行读取 `.agents/plugins/marketplace.json`，第 129–130 行读取 `docs/zh/…`，第 304 行读取 `docs/adr/0004-…md`。
- `scripts/verify-hooks.py`、`scripts/verify-consultation.py` 和 `scripts/fixtures/` 只服务验证。

**已核实的情况：**
- 运行时只用到 `install-agents.sh`、`inspect-agent-runtime.sh`、`advisor-hooks.py`、`process-consultation.py`、`consult_context.py`、`consult_native.py` 和 `run-python.sh`。依据：`hooks/hooks.json` 和 `.mcp.json` 的引用，以及脚本的导入关系。
- 把 `plugins/codex-advisor/` 复制到仓库之外，运行 `sh codex-advisor/scripts/verify.sh --installation`，失败并报 `FileNotFoundError: [Errno 2] No such file or directory: '/tmp/.agents/plugins/marketplace.json'`。已安装的插件缓存就是这种布局。
- 文档中的验证命令都以仓库根目录为起点，例如 `operations.md` 第 323–325 行和第 380–411 行。

**建议：** 二选一。
- (a) 把 `verify.sh`、`verify-hooks.py`、`verify-consultation.py` 和 `scripts/fixtures/` 移到仓库的 `tests/`，并调整它们推算插件目录的方式。插件只保留运行时脚本。建议采用。
- (b) 脚本留在插件中，把三处仓库文件检查移到 `tests/`，使 `verify.sh` 在插件目录内可以独立运行。

**影响：** 发布内容与维护工具分开，运行时行为不变。B02 会先去掉第 304 行这一处依赖。

**验证（未运行）：** 移动之后，在仓库中运行完整验证；在仓库外的插件副本中，确认运行时脚本仍然可用。

## 第二部分的保障变更登记

| 项 | 建议的改动 | 涉及的保护 | 保留的保障或替代保障 |
|---|---|---|---|
| B01a | 迁出安装器内部说明、MCP 隔离细节、信任边界说明和验证分组 | 用户与维护者了解写入边界和信任边界；维护者在发布前验证 | 只迁移，不删除。运行时保留 "Never edit entry files or primary settings to adjust effort." |
| B01b | 删除 `operations.md` 中重复的验收和恢复规则 | 高风险工作的独立验收 | 先把风险定义移入 `independent-acceptance.md`；`SKILL.md` 保留一行不变量 |
| B01c | 把失败恢复和独立验收的规则移入按事件读取的参考文件 | 这些规则在需要时被读到 | `SKILL.md` 中每个分支保留一行不变量；行为场景 2 和 3 |
| B01c 可选项，默认不做 | 把权限观察和检查器核对改为按条件读取 | 每次派发的隔离证据和路由证据 | 默认把它们留在每次派发都要读的 `operations.md` 中。改为按条件读取会减少验证，需要用户明确选择 |
| B02 | 安装器不再删除旧文件名；`--check` 不再报告残留 | 其他安装上的旧入口被自动清理和发现 | 写入面变窄；本机的一次性清理见 A01；前提和失效条件记入 A01b 的 ADR |
| B03 | 修改"无需手动运行检查器"的说法，或增加一行确认 | 派发的模型和推理等级核验 | (b) 恢复这项保证；(a) 只写明缺口。(a) 的较窄触发条件会减少对工作目录和权限的逐次核对 |
| B04 | 删除 TOML 中关于推理等级的注释 | 防止维护者误加或误删固定的推理等级 | `verify.sh` 断言：当且仅当路由配置单元格中只有一个不带星号的推理等级时，模板才有该字段 |
| B06 | 删除顾问失败的定义，或补上后果 | 验收的正确性 | 删除不改变任何行为；补上后果会改变验收行为 |
| B07 | 维护者验证脚本移出插件 | 维护者的验证 | 脚本移到仓库的 `tests/`，命令路径随之更新；运行时脚本不受影响 |

以下选择需要明确裁定：B01c 的可选项；B02 的整体移除；B03 选 (a) 并采用较窄的触发条件；B06 补上后果。所有建议都不会放宽权限、取消必需的独立验收、削弱安装器对不一致文件的检测，也不会改变钩子信任。B02 去掉的是残留检测，不是不一致检测。

2026-09-29：B03 选了 (b)，B06 选了删除定义，这两项不再需要在这里裁定。用户按建议裁定了其余两项：B01c 的可选项不做；B02 整体移除。

---

## 建议的执行顺序

1. 先裁定 Q1–Q3 和各选项型问题。
2. 纠正错误或不安全的说法：B03；B04 中路由配置第 4–6 行的声明。
3. 删除没有规则依赖的文字：B05、B06。
4. 调整结构：先建落点 A02a，再依次执行 B01a、B01b、B01c、B01d；同时处理 A02b、A02c、A02d 和 A03。
5. B02 与 A01b、A01c 随同一版本发布。
6. 确认宿主的显示之后，完成 B04 的其余部分；然后处理 B07。
7. 仓库维护：A05、A06、A07、A08。
8. 发布：
   1. 按 Q1 处理版本号和版本说明书，并在同一提交中更新中文孪生；
   2. 推送；
   3. 在两端依次升级插件、重新安装、运行安装器；
   4. 执行 A01a；
   5. 请用户在 `/hooks` 中信任钩子。

## 与 GPT-6-Astra 的评审

- 评审对象：本文件，按文件哈希固定版本。
- 评审方：`gpt-6-astra`，推理等级 `xhigh`，由作者会话通过 codex 车道直接派发，只读。评审意见由作者会话转交用户。
- 目标：双方对每一项的事实、建议和保障登记达成一致。无法一致的地方写明分歧，交给用户裁定。
- 达成一致之后，由用户逐项确认。确认之前，不修改任何被审查的文件。

**评审记录（2026-09-29）：**
- 第一轮评审的对象是本文件的 sha256 `78aa5cfbb3eeece1ce82f232f82d6e57cd84c362fd2ec8ef3f4871b80fcbfa31`。Astra 提出三个确认问题，没有待确认事项和独立建议。用户全部采纳，作者已改入本文件：
  1. B03(b) 补上 `scripts/verify-hooks.py` 的测试改动和对应的验证。
  2. B03 按 `scripts/advisor-hooks.py` 更正钩子的核对范围，涉及"已核实的情况"、方案 (a) 和保障登记表中的 B03 行。
  3. 本节更正评审方式。
- 复审的对象是 sha256 `78bc6a885d747aee4f2884cb686b93759f9ed20e27b75ceaa798540a2c3aa44a`。Astra 确认三个问题都已解决，没有发现新问题，结论是"与作者一致"。
- 两轮评审在同一个 Codex 会话 `01a0ebca-7d36-7071-ba86-accf1df01b3d` 中进行。会话日志记录的实际配置是 `gpt-6-astra`、`xhigh` 和只读沙箱。两份回执在 `.fable-advisor/receipts/`，该目录没有被 git 跟踪。
- 复审之后，本文件增加了这段记录和用户的裁定，各项建议的内容没有变化。
- 状态：两道门都已通过：与 Astra 沟通一致；用户已于 2026-09-29 裁定全部条目。

## Comments

### 2026-09-29 实施记录

**方式：** 编排姿态。作者会话 `claude`（`claude-opus-5-5`）按裁定写合同，由 Claude 车道的 worker 实现，作者逐个验收。两个 CLI 车道在 implement 模式下要求干净的工作区，而工作区有未提交的基线改动，所以本轮没有用它们实现。跨厂商的检查放在最后的验收评审中。

子代理的会话记录显示，每个合同实际运行的模型和推理等级都与请求一致，见下表。

| 合同 | 裁定项 | 实际运行的设置 |
|---|---|---|
| D | B01、B02c、B03 的文字部分、B04 的路由配置声明、B05、B06、A02a | `claude-opus-5-5`，`xhigh`；`worker-xh`，同模型派发 |
| P | B02a、B02b、B02d、B03a (b)、B01 的工具描述、B04 的注释 | `claude-opus-5-5`，`high`；`worker-h` |
| R1 | A01b、A01c 的 CONTEXT.md 部分、A02b、A04 的 CONTEXT.md 行、A05、A06、A07、A08 | `claude-opus-5-5`，`high`；`worker-h` |
| Z | A02c、A04 的孪生 | `claude-opus-5-5`，`high`；`worker-h` |
| R2 | A01c 的 README 部分、A02d、A03 | `claude-opus-5-5`，`high`；`worker-h` |
| B07 | B07 (a) | `claude-sonnet-5`，`high`；`worker-h` |
| M | A01c 和 A04 的版本说明书部分 | `claude-opus-5-5`，`high`；`worker-h` |

**实施中的发现：**
- P 的确认行最初写 "dispatch check passed"，超出了钩子实际核对的范围。返工后，这一行点名身份、模型和推理等级，并写明没有核对工作目录和权限。
- A07 的两个条件步骤没有执行。`/grill-with-docs`、`/improve-codebase-architecture` 和 `/wayfinder` 在本机的 Claude Code 和 Codex 中都存在，只允许显式调用。A07 中"本会话没有这些技能"的说法，只对模型可见的技能列表成立。
- 实际行数超过 B01c 的估计。`SKILL.md` 是 140 行，估计是 80–100 行。派发 Explorer 或 Worker 之前读 391 行，独立验收读 393 行；估计分别是 220–340 行和 285–355 行。插件中的技能 Markdown 从 872 行降到 599 行。
- 逐句覆盖记录保存在 [round-3-b01-coverage.tsv](round-3-b01-coverage.tsv)，共 413 条，每条都有去向或删除理由。

**验收：**
- 作者按合同逐个验收：读验证输出，对照工作区抽查。
- Astra 按用户的 `实现评审提示词.md` 做了交付前评审，共两轮，在 Codex 会话 `01a0ec0b-6ab2-7e12-a2c7-495697f7df03` 中进行。会话日志记录的实际配置是 `gpt-6-astra`、`xhigh` 和只读沙箱。
- 第一轮提出三个确认问题，作者核实后发出返工单：
  1. 说明书第 450 行把"缺少确认行"等同于钩子被跳过。
  2. 独立验收的 Advisor 派发被要求读取 Explorer 或 Worker 数据包，涉及 `SKILL.md`、中文孪生和说明书第 345 行。
  3. 维护文档开头仍称验证脚本随插件发布。
- 复审确认三处都已解决，结论是"与作者一致"。复审还指出覆盖记录中三条命令的迁移标注有误，作者已更正。回执在 `.fable-advisor/receipts/`。
- 返工之后的检查：`sh tests/verify.sh` 退出码 0；镜像测试 33/33；版本说明书测试 3/3；`git diff --check` 没有问题；32 个 Markdown 文件中的 69 个相对链接和锚点，0 个问题。

**待办，都需要用户授权或操作：**
1. 提交。ADR-0008 链接到未跟踪的 ADR-0007 和本清单，它们要一起提交。
2. 推送，然后在两端升级插件、重新安装、运行安装器。
3. A01a：在两端装好新入口之后，删除各十一个 `0.2.0` 入口文件。执行时需要用户当次授权。
4. A05：两端在新任务中通过 `/hooks` 信任两个钩子。
5. B04 的宿主显示探查。需要在临时 `CODEX_HOME` 中登录，涉及复制认证文件。
6. B01 的三个行为场景和 B03 的真实宿主信任场景。结果取决于模型和宿主，需要临时 `CODEX_HOME`。
7. A06：在新的 Claude Code 会话中，用 `/memory` 或 `/context` 确认 `AGENTS.md` 经导入加载。

**超出裁定范围、没有处理的观察：**
- `docs/agents/domain.md` 第 8–9 行仍提到多上下文仓库的 `CONTEXT-MAP.md`。
- 中文孪生中"拨档"与 "dial"、"Architect 模式"与 "Architect mode" 的用词不统一。这早于本轮。
- 英文 `SKILL.md` 咨询段中 "advisor" 的大小写与别处不一致。`recovery.md` 没有给 R2 标号。两处都早于本轮。
- 说明书侧栏的"中文孪生与检查"与正文标题"中文镜像与检查"不一致。这早于本轮。

### 2026-09-29 发布与部署记录

用户于 2026-09-29 授权推送并部署。

**推送：** `git push origin main`。`origin/main` 从 `09c21c8` 更新到 `4b3c85e`。

**部署：** 两端都按 README「Check and update」执行以下命令：

```sh
codex plugin marketplace upgrade codex-advisor
codex plugin remove codex-advisor@codex-advisor
codex plugin add codex-advisor@codex-advisor
plugin_dir="$(codex plugin list --json | jq -r '.installed[] | select(.pluginId == "codex-advisor@codex-advisor") | .source.path')"
sh "$plugin_dir/scripts/install-agents.sh"
sh "$plugin_dir/scripts/install-agents.sh" --check
```

- WSL：Codex CLI `0.157.1`，`CODEX_HOME=/home/hyy/.codex`。
- Windows：从 WSL 调用 Git Bash（`/mnt/c/Program Files/Git/bin/bash.exe -l -s`），Codex CLI `0.158.0`。
  - `WSLENV` 会把 WSL 的 `CODEX_HOME` 原样传给 Windows 进程。Git Bash 把它解析为不存在的 `C:/Program Files/Git/home/hyy/.codex`，Codex 因此报错 "failed to resolve CODEX_HOME"。
  - 注册表中没有用户级或系统级的 `CODEX_HOME`。所以命令开头先执行 `unset CODEX_HOME`，Codex 使用默认的 `C:\Users\Shy\.codex`。
- 结果：
  - 两端的插件都是 `0.3.0`，市场克隆都指向 `4b3c85e`。
  - 缓存中只有 `0.3.0`，只带七个运行时脚本，含 `hooks/hooks.json` 和两个新参考文件。
  - 十三个入口都是 `INSTALL PASSED` 和 `CHECK PASSED`，并与仓库模板逐字节一致。
- 剩余风险：Windows 的 Codex CLI 是 `0.158.0`，README 写的认证版本是 `0.157.0`。本轮没有重新认证。

**A01a：** 用户于 2026-09-29 授权"直接删除"，没有做备份。
- 删除前，两端的 `agents` 目录各有 24 个文件：十三个新入口，以及下面十一个 `0.2.0` 入口。
- 十一个旧文件中，八个与 `09c21c8` 的模板逐字节一致。三个 Advisor 入口与 `f812f9b` 的模板逐字节一致，说明它们曾从本地检出安装。所以删除的内容都能从 git 历史取回。
- 命令：对两端的下列文件名逐个执行 `rm -- <agents 目录>/<文件名>`，共删除 22 个文件。
  - `ca-advisor-light.toml`、`ca-advisor-senior.toml`、`ca-advisor-standard.toml`；
  - `ca-explorer-light.toml`、`ca-explorer-senior.toml`、`ca-explorer-standard-h.toml`、`ca-explorer-standard-m.toml`；
  - `ca-worker-light.toml`、`ca-worker-senior.toml`、`ca-worker-standard-h.toml`、`ca-worker-standard-m.toml`。
- 删除后，两端的 `agents` 目录各只剩十三个新入口，没有其他文件。再次运行 `--check`，两端都是 `CHECK PASSED`。

**待办的状态：** 上面「待办」中的第 1–3 项已经完成：提交 `4b3c85e`、推送并部署、A01a。仍然待办：
1. A05：两端在新任务中通过 `/hooks` 信任两个钩子。
2. A06：在新的 Claude Code 会话中确认 `AGENTS.md` 经导入加载。
3. B04 的宿主显示探查。
4. B01 的三个行为场景和 B03 的真实宿主信任场景。

**A05 和 A06，2026-09-29：**
- A05 已完成。用户报告两端的钩子都已信任。两端的 `config.toml` 都有 `hooks.state."codex-advisor@codex-advisor:hooks/hooks.json:session_start:0:0"` 和 `…:post_tool_use:0:0` 两条 `trusted_hash`，两端的哈希相同。`0.2.0` 没有钩子，所以这些条目是为 `0.3.0` 的钩子建立的。
- A06 已完成。在本仓库中运行 Claude Code `2.1.283` 的无头会话，禁用读文件和执行命令的工具，要求它原样引用「Plugin maintenance」一节。它逐字给出了这一节的正文，而这段文字只存在于 `AGENTS.md`；`CLAUDE.md` 只有 `@AGENTS.md`。所以导入已生效。调试日志不记录加载了哪些指令文件，不能作为佐证。
- 仍然待办：B04 的宿主显示探查；B01 的三个行为场景；B03 的真实宿主场景。钩子已信任，现在可以观察一次正确派发是否出现确认行。
