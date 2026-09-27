# 05：Worker 档位入口

**要构建的内容：** 主代理可以安装并派发 `ca_worker_light`、`ca_worker_standard_m`、`ca_worker_standard_h` 与 `ca_worker_senior`，每一个都固定到它的模型，并在档位只允许一个推理等级的地方固定推理等级。三个旧的 worker 入口被退役，Implementer 这个词离开插件与镜像。

**Blocked by:** 04（共享退役列表、验证器数据以及镜像目录）。

**Status:** resolved

- [x] 四份模板 `ca-worker-light`（Luna，固定 `max`）、`ca-worker-standard-m`（Sol，调用者的推理等级）、`ca-worker-standard-h`（Astra，固定 `low`）、`ca-worker-senior`（Astra，调用者的推理等级）；没有 `sandbox_mode` 键。
- [x] `description` 点名角色、档位、模型，以及固定的或调用者的推理等级；`developer_instructions` 按 R05，返回形态为 COMPLETION / CHANGES / VERIFICATION / JUDGMENT CALLS / GAPS，有你并非独自一人的保留规则，不再进一步委派，推理等级或模型变更时使用新线程，不推断设置；四份正文逐字节相同。
- [x] 三份旧模板（`codex-advisor-luna-implementer`、`codex-advisor-sol-implementer`、`codex-advisor-astra-implementer`）被删除，它们的文件名被加入退役列表。
- [x] 四份中文 TOML 对照具有相等的配置键与中文散文键。
- [x] Implementer 与 implementer 不再出现在插件目录或镜像之下的任何地方，安装器退役列表内部除外。README 留给工单 07。
- [x] 安装到一个持有八个旧文件的临时目标后，八份新文件（四份 Explorer、四份 worker）被安装，六份旧文件被移除，两份旧的 Advisor 与 reviewer 文件未被触碰。
- [x] 两个验证器组、镜像测试以及手册测试都通过。

## 验收

由主代理于 2026-09-17 验收。通道：`generalPurpose`，固定为 `cursor-grok-4.6-xhigh`（已请求，未经确认）。第 1 级：主代理重跑了完整的 `verify.sh` 与 `tests/test_zh_mirror.py`（20/20）；代理目录持有八份 `ca-*` 模板、两份旧的 Advisor/reviewer 模板，以及带有六个名称的 `retire.txt`。第 2 级：主代理阅读了 `ca-worker-standard-m.toml` 及其对照的标头——没有 `sandbox_mode`，推理等级由调用者选择，指令携带五部分数据包词汇以及五部分 RETURN，且没有调用者职责；`rg -i implementer` 只匹配 `retire.txt`。
