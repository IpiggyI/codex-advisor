# 06：README、插件清单、0.3.0 版本说明书以及发布准备

**要构建的内容：** 从 0.2.0 更新的用户在 README 中读到什么替换十一个旧入口，以及咨询与钩子如何工作。插件报告 `0.3.0`。一份 `0.3.0` 版本说明书描述整个版本以及相对 0.2.0 的增量，采用已交付的 0.2.0 手册的视觉体系，并通过同时查看两个页面来验证。发布命令为用户列出，而不被运行。

**Blocked by:** 02, 03, 04, 05（README 与手册描述它们各自交付的内容；05 最后落地）。

**Status:** resolved

## 开始前必读

- `spec.md`：DR-8 到 DR-11、AC-12、X-1、X-5、§Authority and conflicts（文本相对基线）、§Visual Acceptance、§Stop and Return（S7）、§Goal-Drift Checks（版本说明书那一项）。
- `docs/agents/version-manual.md`（所要求的短语、`本版说明` 必须覆盖什么、没有 Markdown 对照）。
- 视觉基线 `docs/releases/0.2.0.html`。在书写之前于浏览器中打开它并阅读它的源码。提交 `f812f9b`，SHA-256 `d89f0f18ccfc0cb42156a5548bc531527372603ea12efb13d759e86589b6d4ea`；开始之前确认该散列并记录它。
- 不是基线：`.scratch/manual-redesign/0.2.0-magazine.html`。
- `README.md`（当前）、`plugins/codex-advisor/.codex-plugin/plugin.json`、`docs/adr/0006-*.md`（供 `相对上一版` 的引用）、`acceptance.md` §01 到 §05（已知限制以及实况检查所确立的内容）。
- `.scratch/tier-role-pool/issues/07-readme-manual-release.md` §Release commands（要更新的命令形态）。

## 拥有

- `README.md`
- `plugins/codex-advisor/.codex-plugin/plugin.json`：`version`、`description`、`interface.shortDescription`、`interface.longDescription`、`keywords`
- `docs/releases/0.3.0.html`（新）
- `.scratch/tiers-and-advisor-consult/visual/`（截图）
- `acceptance.md` §06

## 验收

- [x] README 覆盖：
  - [x] 安装，包括对该插件钩子的 `/hooks` 评审，以及未受信任的钩子被跳过并带有一条启动警告（AC-12）；
  - [x] 使用；
  - [x] 按角色与档位列出的十三个入口，没有拨档值，指向路由配置；
  - [x] 准入与升级；
  - [x] 咨询与姿态；
  - [x] 钩子；
  - [x] 验收；
  - [x] 检查与更新，包括任何改变钩子的更新之后一次新的 `/hooks` 评审；
  - [x] 一个升级小节，点名十一个已退役的 0.2.0 入口及其替换者。
- [x] `plugin.json` 的 `version` 是 `0.3.0`。描述与关键词描述新档位、咨询以及钩子，没有模型名称。市场清单未改变。
- [x] `docs/releases/0.3.0.html` 是中文且自包含，并逐字符精确地包含 `本版说明` 与 `相对上一版`。
  - [x] `本版说明` 覆盖 DR-10 所列出的一切，并为 0.3.0 冻结路由配置表。
  - [x] `相对上一版` 列出相对 0.2.0 的每一项变更及其理由与一处 ADR-0006 引用，包括十一个已退役的名称。
- [x] **视觉。** 用相同的设置为基础线与 0.3.0 渲染场景 V1 到 V5。把它们保存为 `visual/<scene>-baseline.png` 与 `visual/<scene>-0.3.0.png`，打开并查看每一对，并在 `acceptance.md` §06 中记录逐场景的观察以及通过或失败。每一个场景都通过规格 §Visual Acceptance 中的 "must match" 列表，并且每一处差异都落在允许列表中。基线文件的 SHA-256 在结束时未改变。
- [x] **X-5 文本检查。** 在允许的地方之外，不出现 0.2.0 入口名称，不出现作为档位使用的 light/standard/senior，也不出现 "first-round pool"、"senior gate" 或 "decision packet"。记录该命令及其输出。
- [x] 发布命令列在 `acceptance.md` §06 中，从 0.2.0 的形态为 0.3.0 更新：推送到 `origin`，然后在 WSL 与 Windows 上运行市场升级、插件移除与添加、安装器、安装器检查，以及在一个新的交互会话中的 `/hooks` 评审（AC-12）。它们被标为用户门控并且不被运行。

## 验证

- `python3 tests/test_version_manual.py`（针对 `0.3.0`）
- `python3 tests/test_zh_mirror.py`
- `sh plugins/codex-advisor/scripts/verify.sh`
- `git diff --check`
- `sha256sum docs/releases/0.2.0.html`
- `acceptance.md` §06 中的视觉表

功能检查不能代替视觉比较。

## 停止条件

S7（基线的组件所不能表达的内容）与 S8。X-1：没有用户的明确授权，就不推送、不升级、不重新安装，也不在真实主目录上运行安装器。

## 不在本工单内

最终验收清扫（规格 §Requirement Ownership，在本工单之后）。

## 评论

于 2026-09-26 在主代理验证以及新的独立 senior 验收之后解决。见 `../acceptance.md` 第 06 节与 Final acceptance，其中有证据与限制。D47 取消完成阻断，D48 只允许一次本地提交，D49 只免除最终定义手册信任测试的重复。没有执行推送或真实的安装更新。
