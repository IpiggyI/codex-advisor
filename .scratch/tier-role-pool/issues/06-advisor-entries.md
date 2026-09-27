# 06：带有两种请求形态的 Advisor 档位入口

**要构建的内容：** 主代理可以安装并派发 `ca_advisor_light`、`ca_advisor_standard` 与 `ca_advisor_senior`，用于决策数据包或验收数据包，用检查器验证该调用，并且不再找到 reviewer 入口。路由配置与随附模板现在互相做机械检查。

**Blocked by:** 05.

**Status:** resolved

- [x] 三份模板 `ca-advisor-light`（Astra，固定 `low`）、`ca-advisor-standard`（Astra，固定 `medium`）、`ca-advisor-senior`（Astra，调用者的推理等级）；`sandbox_mode = "read-only"`。
- [x] `developer_instructions` 按 R05 携带两种返回形态：决策数据包为 RECOMMENDATION / EVIDENCE / ASSUMPTIONS / TRADEOFFS / GAPS，验收数据包为 READINESS / FINDINGS / VERIFICATION / GAPS，按收到的数据包选择；只读；每个请求一个新线程；不推断设置。三份正文逐字节相同。
- [x] 旧的 `codex-advisor-astra-advisor` 与 `codex-advisor-astra-reviewer` 模板被删除，它们的文件名被加入退役列表；退役列表现在恰好持有八个 0.1.0 文件名。
- [x] 三份中文 TOML 对照具有相等的配置键与中文散文键。
- [x] 验证器的静态检查增加：路由配置表中的每一个入口名称都有一份具有该 `name` 的随附模板，每一份随附模板都在表中被点名，并且每一对在 `model` 上一致。
- [x] 安装到一个持有八个旧文件的临时目标后，恰好留下十一份新文件加上任何无关文件，并且对该目标的 `--check` 通过。
- [x] 没有模板、参考或对照点名 reviewer 入口。
- [x] 两个验证器组、镜像测试以及手册测试都通过。

## 验收

由主代理于 2026-09-17 验收。通道：`generalPurpose`，固定为 `cursor-grok-4.6-xhigh`（已请求，未经确认）。第 1 级：主代理重跑了完整的 `verify.sh`、`tests/test_zh_mirror.py`（26/26）、`tests/test_version_manual.py`；代理目录恰好持有十一份 `ca-*` 模板，以及带有八个 0.1.0 名称的 `retire.txt`。第 2 级：主代理阅读了 `ca-advisor-light.toml`——固定 `low`，只读，指令携带两种数据包形态及其 RETURN 块，且没有调用者职责。通道记录的反证：一份模板中错误的 `model` 会使配置到模板检查在点名该入口时失败。通道关于 `rg reviewer` 的 GAP 被原样接受：留存的命中是已退役的选项名 `--reviewer-effort`（检查器必须继续拒绝它）、句子 "no separate reviewer entry exists"，以及关于一次新评审的散文；没有一处点名 reviewer 入口。
