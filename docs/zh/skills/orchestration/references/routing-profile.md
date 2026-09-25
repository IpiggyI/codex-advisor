# 路由配置

声明于 2026-09-26。下列拨档锚定于 GPT-6 Luna、GPT-6 Sol 和 GPT-6 Astra。
本文件是写入 effort 选项、默认值和候选顺序的唯一位置；`SKILL.md` 和入口描述
不重复这些值。

记法为 `model[a*, b]`。列出的每个 effort 都可用，`*` 标记默认值。一个单元格
列出两个候选项时，`›` 按使用顺序分隔候选项。单个不带星号的 effort 固定在
入口中；有多个 effort 的入口把 effort 留给调用方选择。

| 角色 | `mainstay` | `crux` | `rescue` |
|---|---|---|---|
| Explorer | `ca_explorer_mainstay_m` gpt-6-luna[high*, xhigh] › `ca_explorer_mainstay_h` gpt-6-sol[medium*, high] | `ca_explorer_crux_m` gpt-6-luna[max] › `ca_explorer_crux_h` gpt-6-sol[xhigh] | `ca_explorer_rescue` gpt-6-astra[medium*, high] |
| Worker | `ca_worker_mainstay_m` gpt-6-luna[max] › `ca_worker_mainstay_h` gpt-6-sol[high] | `ca_worker_crux_m` gpt-6-sol[xhigh*, max] › `ca_worker_crux_h` gpt-6-astra[low*, medium] | `ca_worker_rescue` gpt-6-astra[high*, xhigh] |
| Advisor | `ca_advisor_mainstay` gpt-6-astra[low*, medium] | `ca_advisor_crux` gpt-6-astra[high] | `ca_advisor_rescue` gpt-6-astra[xhigh] |

## 固定 effort 与调用方选择的 effort

六个入口因所在单元格只有一个 effort 而固定 `model_reasoning_effort`：
`ca_explorer_crux_m`、`ca_explorer_crux_h`、`ca_worker_mainstay_m`、
`ca_worker_mainstay_h`、`ca_advisor_crux` 和 `ca_advisor_rescue`。其余七个
入口省略该字段；调用方从该入口列出的 effort 中选择一个传入，并把 `fork_turns`
设为 none。每个入口都固定自己的模型。

## 咨询映射

`mainstay` 入口以 gpt-6-astra[low] 咨询。`crux` 入口以
gpt-6-astra[high] 咨询。`rescue` 入口以 gpt-6-astra[xhigh] 咨询。
Advisor 没有自己的咨询升级路径。

primary 使用不弱于其拨档的最低 Advisor 拨档进行咨询。如果没有不弱于它的
Advisor 拨档，则使用 gpt-6-astra[xhigh]。如果本配置没有 primary 的精确模型
标识，也使用 gpt-6-astra[xhigh]。

## 验收映射

一个档位完成的工作使用该档位的 Advisor 入口：`ca_advisor_mainstay`、
`ca_advisor_crux` 或 `ca_advisor_rescue`。多个档位共同完成的工作使用其中最高
档位。primary 自行完成的工作使用不弱于 primary 拨档的最低 Advisor 拨档。
如果没有合格拨档，或本配置没有 primary 的精确模型标识，则使用固定 effort 的
`ca_advisor_rescue`。低置信度裁定使验收保持待定并交给用户；它不会触发另一个
Advisor 拨档。

判断“不弱于”时，先比较模型：
gpt-6-luna < gpt-6-sol < gpt-6-astra。再比较 effort：
low < medium < high < xhigh < max。

## 声明的假设

本配置假设更换模型带来的能力增益大于提高 effort，并假设 `xhigh` 是一次独立的
能力跃升。下一次模型换代会使这两个假设失效，并要求重新评估。

## 调整数值

先重新检查声明的假设和账户可调用的拨档。然后同时修改受影响模板的 `model` 或
`model_reasoning_effort` 与本表，运行 `sh plugins/codex-advisor/scripts/verify.sh`，
并对每个受影响入口重跑实时路由检查。除非角色或档位契约也发生变化，模型换代
只修改本配置和模板。
