# 07：README、审计清单、0.2.0 版本说明书以及版本提升

**要构建的内容：** 从 0.1.0 更新的用户在 README 中读到八个旧入口名称为何失败以及由什么替换它们，用新安装器安装并检查，并找到一份描述整个版本以及相对 0.1.0 的增量的 0.2.0 版本说明书。插件报告版本 0.2.0，并且每一项检查都通过。

**Blocked by:** 06.

**Status:** resolved

- [x] README 被重写：从检出安装、使用、按角色与档位列出的十一个入口且没有拨档值（指向路由配置）、Architect 模式未改变、恢复与建议小节与阶梯和门禁一致、带有覆盖与退役语义的检查和更新，以及一个点名八个已退役入口及其替换者的升级小节。
- [x] README 使用 Worker，从不使用 Implementer；已退役的入口名称不出现在升级小节之外。
- [x] `docs/releases/0.2.0.html`：风格与 0.1.0 手册一致的自包含中文 HTML，包含 `本版说明`（安装、使用、入口与档位、为 0.2.0 冻结的路由配置表、池、门禁、阶梯、Advisor 形态、安装器与检查器用法、检查、已知限制）以及 `相对上一版`（相对 0.1.0 的每一项变更及其理由与 ADR-0004 引用）。
- [x] 插件清单版本 `0.2.0`；`description`、`shortDescription`、`longDescription` 与 `keywords` 描述按档位命名的入口以及路由配置，而没有按模型命名的入口。市场清单没有版本字段，并且未改变。
- [x] 审计清单记录决定：R01 为 update（LF 属性，工单 01），R02 为 update（对照已纠正，工单 03），R05 为 simplify（工单 04 到 06），R08 为 update（路由配置中的拨档记法）。其余保持待定。
- [x] 文本检查：插件目录、镜像或 README 之下不出现 `Implementer`、`implementer` 或任何已退役的入口名称，退役列表以及 README 升级小节除外。
- [x] 完整验证通过：两个验证器组、镜像测试、手册测试、`git diff --check`。
- [x] 推送到 `origin`、`codex plugin marketplace upgrade`、两侧的插件重新安装，以及在两侧运行安装器，都是用户门控的步骤；本工单列出这些命令并且不运行它们。

## 验收

由主代理于 2026-09-17 验收。通道：`generalPurpose`，固定为 `cursor-grok-4.6-xhigh`（已请求，未经确认）。第 1 级：主代理重跑了 `verify.sh`、`tests/test_zh_mirror.py`（26/26）、`tests/test_version_manual.py`（针对 0.2.0 为 3/3）、`git diff --check`；`plugin.json` 报告 0.2.0，其描述或关键词中没有模型名称。第 2 级：主代理通读了 README（160 行；没有拨档值的入口表、R1–R4、senior 门禁、Advisor 数据包、带有八个已退役名称的升级表）以及手册的小节标题（`本版说明` 在部分标签处，`相对上一版` 作为一个标题，495 行）。审计清单决定 R01/R02/R05/R08 由主代理记录。发布步骤（推送、市场升级、重新安装、两侧的安装器）仍然由用户门控，并且没有被运行。

## 发布命令（用户门控；主代理未运行）

从本次检出，在 0.2.0 提交存在之后：

```sh
git push origin main
```

然后在每一侧（WSL，以及从 Windows 驱动器经由 `cmd.exe` 的 Windows）：

```sh
codex plugin marketplace upgrade codex-advisor
codex plugin remove codex-advisor@codex-advisor
codex plugin add codex-advisor@codex-advisor
plugin_dir="$(codex plugin list --json | jq -r '.installed[] | select(.pluginId == "codex-advisor@codex-advisor") | .source.path')"
sh "$plugin_dir/scripts/install-agents.sh"
sh "$plugin_dir/scripts/install-agents.sh" --check
```

之后开始一个新的 Codex 任务；十一个 `ca_*` 入口替换八个 0.1.0 名称，安装器会删除那些旧名称。
