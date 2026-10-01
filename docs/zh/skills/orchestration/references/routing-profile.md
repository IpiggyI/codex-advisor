# 路由配置

声明于 2026-09-30。下列拨档锚定于 `gpt-6-luna`、`gpt-6.1-sol` 和 `gpt-6-astra`。
本文件是每个模型、允许的 effort、默认值和候选顺序的来源。每个入口模板把自己的
模型和任何固定 effort 复制到其字段中。模板描述写出模型；单元格有两个候选时，
描述写出候选位置；effort 固定时，描述写出该 effort。skill 正文不重复其中任何一项。

记法为 `model[a*, b]`。列出的每个 effort 都可用，`*` 标记默认值。一个单元格
列出两个候选项时，`›` 按使用顺序分隔候选项。单个不带星号的 effort 固定在
入口中；有多个 effort 的入口把 effort 留给调用方选择。

| 角色 | `mainstay` | `crux` | `rescue` |
|---|---|---|---|
| Explorer | `ca_explorer_mainstay_m` gpt-6-luna[high*, xhigh] › `ca_explorer_mainstay_h` gpt-6.1-sol[medium*, high] | `ca_explorer_crux_m` gpt-6-luna[max] › `ca_explorer_crux_h` gpt-6.1-sol[xhigh] | `ca_explorer_rescue` gpt-6-astra[medium*, high] |
| Worker | `ca_worker_mainstay_m` gpt-6-luna[max] › `ca_worker_mainstay_h` gpt-6.1-sol[medium*, high] | `ca_worker_crux_m` gpt-6.1-sol[xhigh] › `ca_worker_crux_h` gpt-6-astra[low*, medium] | `ca_worker_rescue_m` gpt-6.1-sol[max] › `ca_worker_rescue_h` gpt-6-astra[high*, xhigh] |
| Advisor | `ca_advisor_mainstay_m` gpt-6.1-sol[medium*, high] › `ca_advisor_mainstay_h` gpt-6-astra[low*, medium] | `ca_advisor_crux_m` gpt-6.1-sol[high*, xhigh] › `ca_advisor_crux_h` gpt-6-astra[high] | `ca_advisor_rescue_m` gpt-6.1-sol[xhigh*, max] › `ca_advisor_rescue_h` gpt-6-astra[xhigh] |

## 固定 effort 与调用方选择的 effort

七个入口因所在单元格只有一个 effort 而固定 `model_reasoning_effort`：
`ca_explorer_crux_m`、`ca_explorer_crux_h`、`ca_worker_mainstay_m`、
`ca_worker_crux_m`、`ca_worker_rescue_m`、`ca_advisor_crux_h` 和
`ca_advisor_rescue_h`。其余十个入口省略该字段，把 effort 留给调用方。每个入口都
固定自己的模型。

## 咨询映射

Explorer 或 Worker 入口在本档位的 Advisor 单元格里，使用不弱于自身拨档的
最低拨档进行咨询；如果没有这样的拨档，则使用该单元格最强的拨档。Advisor 没有
自己的咨询升级路径。

primary 在所有档位的 Advisor 拨档中，使用不弱于其拨档的最低拨档进行咨询。如果
没有不弱于它的 Advisor 拨档，则使用 gpt-6-astra[xhigh]。如果本配置没有 primary
的精确模型标识，则使用 gpt-6.1-sol[xhigh]。

## 验收映射

委派完成的工作使用参与档位中最高档位的 Advisor 单元格，并在该单元格里选用
不弱于参与工作的最强拨档的最低拨档。primary 自行完成的工作使用不弱于 primary
拨档的最低 Advisor 拨档；两个入口都允许该拨档时，使用较低档位的入口。如果没有
合格拨档，则使用固定 effort 的 `ca_advisor_rescue_h`。如果本配置没有 primary 的
精确模型标识，则使用 `ca_advisor_crux_m`，effort 为 `xhigh`。低置信度裁定使验收
保持待定并交给用户；它不会触发另一个 Advisor 拨档。

判断“不弱于”时，先比较模型：
gpt-6-luna < gpt-6-sol < gpt-6.1-sol < gpt-6-astra。再比较 effort：
low < medium < high < xhigh < max。

## 声明的假设

本配置假设更换模型带来的能力增益大于提高 effort，并假设 `xhigh` 是一次独立的
能力跃升。下一次模型换代会使这两个假设失效，并要求重新评估。
