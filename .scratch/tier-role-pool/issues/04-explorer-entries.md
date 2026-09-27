# 04：Explorer 档位入口

**要构建的内容：** 主代理可以安装并派发 `ca_explorer_light`、`ca_explorer_standard_m`、`ca_explorer_standard_h` 与 `ca_explorer_senior`，每一个都固定到它的模型，用通用检查器验证该调用，并阅读每一份模板的中文对照。三个旧的 Explorer 入口由安装器退役。

**Blocked by:** 01, 02, 03.

**Status:** resolved

- [x] 四份模板 `ca-explorer-light`、`ca-explorer-standard-m`、`ca-explorer-standard-h`、`ca-explorer-senior`，其 `name` 字段为 `ca_explorer_light`、`ca_explorer_standard_m`、`ca_explorer_standard_h`、`ca_explorer_senior`；模型为 Luna、Luna、Terra、Sol；`sandbox_mode = "read-only"`；只有 `ca-explorer-standard-m` 固定 `model_reasoning_effort = "max"`。
- [x] 每一份 `description` 都点名角色、档位、模型，以及固定的推理等级或调用者传入它；它不列出允许的推理等级。
- [x] `developer_instructions` 遵循审计发现 R05：权限、期望的数据包、返回形态（FINDINGS / EXPLANATION / GAPS）、新线程与不再委派的规则、不推断运行时设置；没有调用者职责。四份正文逐字节相同。
- [x] 三份旧的 Explorer 模板（`codex-advisor-luna-explorer`、`codex-advisor-sol-explorer`、`codex-advisor-astra-explorer`）从随附模板中删除，它们的文件名被加入安装器的退役列表。插件前缀变量变为 `ca-`；验证器的前缀断言变为 `ca-` 与 `ca_`。
- [x] 四份中文对照是镜像的 `agents/` 目录下、文件名相同的可解析 TOML；`name`、`model`、`model_reasoning_effort`（存在性与值）以及 `sandbox_mode` 等于模板；`description` 与 `developer_instructions` 是中文。
- [x] 镜像测试覆盖 TOML 文件：对 `.md` 与 `.toml` 双向检查存在性，并且对每一份 TOML 对照检查四个配置键的键相等，外加两个散文键中的中文文本。`model` 与模板不同的对照使测试失败。
- [x] 验证器的静态检查增加：同一角色的全部模板（按名称的第二段）携带逐字节相同的 `developer_instructions`；模板恰好在路由配置把它标为单一推理等级的那个集合中时，才固定 `model_reasoning_effort`。
- [x] 安装到一个持有八个旧文件的临时目标后，四份新的 Explorer 文件被安装，三份旧的 Explorer 文件被移除，另外五个旧文件未被触碰（它们在工单 05 与工单 06 中退役）。
- [x] 两个验证器组、镜像测试以及手册测试都通过。运行时组现在自动覆盖四份新模板。
- [x] 实况路由检查不是本工单验证的一部分；主代理在工单 06 之后对全部十一个入口跑一遍，并把它记录在该功能的验收记录中。

## 验收

由主代理于 2026-09-16 验收。通道：`generalPurpose`，固定为 `cursor-grok-4.6-xhigh`（已请求，未经确认）。第 1 级：主代理重跑了完整的 `verify.sh` 与 `tests/test_zh_mirror.py`（12/12）；代理目录持有四份 `ca-explorer-*` 模板、五份剩余的旧模板，以及带有三个旧 Explorer 名称的 `retire.txt`。第 2 级：主代理阅读了 `ca-explorer-light.toml` 与 `ca-explorer-standard-m.toml` 及其对照——标头如所规定，固定入口的注释说推理等级已固定，指令为 12 行且没有调用者职责，对照保持标识符与 RETURN 标签逐字符精确。结转的工单 02 诊断已修复。主代理更新了 `AGENTS.md` / `CLAUDE.md` 的镜像规则，以覆盖 TOML 对照。
