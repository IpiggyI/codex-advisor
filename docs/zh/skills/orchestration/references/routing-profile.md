# Routing profile

声明于 2026-09-16。下表的 dial 锚定于 GPT-5.6 Luna、GPT-5.6 Terra、GPT-5.6 Sol 和 GPT-6 Astra。某个入口的模型换代时，重新评估该入口。本文件是唯一写有 effort 选项、默认值和候选顺序的地方；`SKILL.md` 和入口描述不重复它们。

记法：`model[a*, b, c]`。列出的每个 effort 都是首轮可选项，`*` 标记默认值。一个单元格列出两个模型时，列出顺序就是候选顺序，用 `›` 分隔。钉死的 effort 直接写出：`model[max]` 表示该入口固定 `model_reasoning_effort`，调用方不传 effort。

| 角色 | light | standard | senior |
|---|---|---|---|
| Explorer | `ca_explorer_light` gpt-5.6-luna[high*, xhigh] | `ca_explorer_standard_m` gpt-5.6-luna[max] › `ca_explorer_standard_h` gpt-5.6-terra[medium*, high] | `ca_explorer_senior` gpt-5.6-sol[medium*, high] |
| Worker | `ca_worker_light` gpt-5.6-luna[max] | `ca_worker_standard_m` gpt-5.6-sol[high*, xhigh] › `ca_worker_standard_h` gpt-6-astra[low] | `ca_worker_senior` gpt-6-astra[medium*, high] |
| Advisor | `ca_advisor_light` gpt-6-astra[low] | `ca_advisor_standard` gpt-6-astra[medium] | `ca_advisor_senior` gpt-6-astra[high*, xhigh] |

## 钉死的 effort 与调用方选择的 effort

五个入口在模板中钉死 `model_reasoning_effort`，因为其单元格只有一个 effort：`ca_worker_light`（`max`）、`ca_explorer_standard_m`（`max`）、`ca_worker_standard_h`（`low`）、`ca_advisor_light`（`low`）和 `ca_advisor_standard`（`medium`）。其余六个入口省略该字段；调用方从列出的选项中传入 `reasoning_effort`，并把 `fork_turns` 设为 none。每个入口都钉死其模型。

## Advisor 默认值

决策数据包发给 `ca_advisor_standard`；验收数据包发给 `ca_advisor_light`。只有裁定报告低置信度或用户声明时，才使用 `ca_advisor_senior`。

first-round pool、senior gate 和 escalation ladder 写在 [SKILL.md](../SKILL.md) 中。

## 调整一个值

同时修改受影响模板的 `model` 或 `model_reasoning_effort` 和本表，运行 `sh plugins/codex-advisor/scripts/verify.sh`，然后发布。模型换代只触及这两处；skill 正文和脚本保持不变。
