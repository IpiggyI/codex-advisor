# 验收记录：按档位命名的原生入口（0.2.0）

由主代理于 2026-09-17 记录。宿主：WSL 上的 `codex-cli 0.154.0`；提供方 `official` 来自用户的 `config.toml`；父模型 `gpt-6-astra`，推理等级为 `low`（用户的默认值）。工作区处于工单 01–06 已验收、工单 07 之前。

## 实况路由检查（十一个入口）

方法：一个临时 `CODEX_HOME` 接收了 `auth.json` 与 `config.toml` 的副本，并通过 `install-agents.sh --target-dir` 接收了十一个模板；一个临时工作区放有一份两行的 `README.md`；每个入口各运行一次 `codex exec --sandbox read-only`，要求父代理以 `fork_turns none` 恰好派发一个该入口的子代理（只对六个由调用者选择推理等级的入口传入 `reasoning_effort`），并报告该文件的第一行；子会话记录按 `agent_role` 定位，并用 `inspect-agent-runtime.sh --sessions-dir … --agent <name> [--effort <e>]` 读取。临时主目录、凭据副本、工作区以及日志随后被删除。

| 入口 | 传入的推理等级 | 观察到的模型 | 观察到的推理等级 | 沙箱 / 权限 | 子线程 | 检查器 |
|---|---|---|---|---|---|---|
| `ca_explorer_light` | high | gpt-5.6-luna | high | read-only / managed | 01a0ab15-d019-7ad0-9413-12de29c51eaf | 退出码 0 |
| `ca_explorer_standard_m` | （固定） | gpt-5.6-luna | max | read-only / managed | 01a0ab16-e0ff-7ce3-95b3-c88115e40773 | 退出码 0 |
| `ca_explorer_standard_h` | medium | gpt-5.6-terra | medium | read-only / managed | 01a0ab17-8ab8-7380-a40c-1c8c99b10fac | 退出码 0 |
| `ca_explorer_senior` | medium | gpt-5.6-sol | medium | read-only / managed | 01a0ab17-e0ad-7341-b4d8-bbf7bdf93451 | 退出码 0 |
| `ca_worker_light` | （固定） | gpt-5.6-luna | max | read-only / managed | 01a0ab18-330e-7f13-9944-44efbf6cdb48 | 退出码 0 |
| `ca_worker_standard_m` | high | gpt-5.6-sol | high | read-only / managed | 01a0ab18-a2fe-71a2-bf3d-613185fb2c94 | 退出码 0 |
| `ca_worker_standard_h` | （固定） | gpt-6-astra | low | read-only / managed | 01a0ab18-fc17-7b23-b70c-a1c415dcb248 | 退出码 0 |
| `ca_worker_senior` | medium | gpt-6-astra | medium | read-only / managed | 01a0ab19-4e18-7772-b6d1-f69ae563aa80 | 退出码 0 |
| `ca_advisor_light` | （固定） | gpt-6-astra | low | read-only / managed | 01a0ab19-a580-79e2-91a4-73030ed6b232 | 退出码 0 |
| `ca_advisor_standard` | （固定） | gpt-6-astra | medium | read-only / managed | 01a0ab1a-09f9-7ad3-9334-ab193ffb2a84 | 退出码 0 |
| `ca_advisor_senior` | high | gpt-6-astra | high | read-only / managed | 01a0ab1a-7676-7cb1-9401-6819e8dd3564 | 退出码 0 |

每一次运行都以退出码 0 结束，并且父代理的回复带有子代理的答案（夹具的第一行）。每一个子会话记录的 `parent_thread_id` 都是该次运行的父会话，`cwd` 都是该临时工作区。每次运行的父令牌用量大约从 1,000 到大约 20,000。

本检查所确立的内容：安装之后，每个入口都可以按名称被发现，以模板的 `model` 派发，并运行在被固定的推理等级或被传入的推理等级上。`gpt-5.6-terra` 以及推理等级为 `max` 的 Luna 在此账户上可以调用；Luna 的 `xhigh` 未被行使。

本检查所不确立的内容：强制隔离（观察到的 `read-only` 沙箱来自父代理的 `--sandbox read-only`；`permission_profile_type` 为 `managed`）、质量、成本或稳定性；`[agents]` 默认值路径（被复制的 `config.toml` 中没有设置）；在交互会话中、而不是在 `codex exec` 下的行为。

## 工单 06 验收时的确定性检查

- `sh plugins/codex-advisor/scripts/verify.sh`：安装组与运行时组通过（由清单驱动的安装器，带有覆盖、退役、漂移与残留检查；路由配置到模板的名称与模型；同一角色的指令相同；固定集合；由表驱动的检查器用例；载荷过滤）。
- `python3 tests/test_zh_mirror.py`：26/26（四份 Markdown 对照，十一份按存在性计的 TOML 对照，十一份按键相等与中文散文计的对照）。
- `python3 tests/test_version_manual.py`：针对当前 `0.1.0` 为 3/3（工单 07 会提升版本并加入 0.2.0 手册）。

## 代码评审（两个轴线，Codex 通道报告模式，`gpt-6-astra[low]`，2026-09-17）

两个通道都返回了 `complete` 回执（会话 `01a0ab26-3e55-7fe1-aae1-43e6fbdc6f9b` 为标准轴线，`01a0ab26-3e55-7980-b81a-1bee98ce9e34` 为规格轴线；`dirty_baseline: true`，因此只读工具集是唯一的防护）。处置如下：

- 标准，硬性：退役文件名处的符号链接被删除，而不是被拒绝（安装器预检豁免了符号链接）→ 在脚本通道上返工；预检现在拒绝退役名称处的任何非常规入口，删除循环只删除常规文件；已加入验证器用例。
- 标准，硬性：0.2.0 手册遗漏了 `codex plugin marketplace upgrade`，以及 `AGENTS.md` 所要求的每一侧重新安装顺序 → 在文档通道上返工；手册现在列出完整顺序。
- 标准，判断：`tests/test_zh_mirror.py` 中重复的存在性检查块 → 已注明，未更改。
- 标准，契约缺口：术语表中路由配置的 `_Avoid_` 禁止在 TOML 描述里出现任何拨档值，而规格要求固定入口写明其固定推理等级 → 主代理收窄了术语表措辞。
- 规格，缺失：工单 07 没有列出发布命令 → 主代理已把它们加入该工单。
- 规格，缺失：README 在检查器示例中重复了一个推理等级值 → 返工；该示例现在使用固定的 `ca_worker_light`。
- 规格，错误：验证器把固定集合和入口数量写死 → 返工；两者现在只从路由配置推导（反证：给一个未固定的模板加上推理等级，会在点名该入口时失败）。
- 规格，范围蔓延：未发现。

返工之后：`verify.sh` 的两个组、`tests/test_zh_mirror.py` 的 26/26、`tests/test_version_manual.py` 的 3/3，以及 `git diff --check` 均为干净。
