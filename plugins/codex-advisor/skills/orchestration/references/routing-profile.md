# Routing profile

Declared 2026-09-16. The dials below are anchored to GPT-5.6 Luna, GPT-5.6 Terra,
GPT-5.6 Sol, and GPT-6 Astra. Re-evaluate an entry when its model changes
generation. This file is the only place where effort options, defaults, and
candidate order are written; `SKILL.md` and the entry descriptions do not repeat them.

Notation: `model[a*, b, c]`. Every listed effort is a first-round option and `*`
marks the default. Where a cell lists two models, the listed order is the candidate
order and `›` separates them. A pinned effort is written bare: `model[max]` means
the entry fixes `model_reasoning_effort` and the caller passes none.

| Role | light | standard | senior |
|---|---|---|---|
| Explorer | `ca_explorer_light` gpt-5.6-luna[high*, xhigh] | `ca_explorer_standard_m` gpt-5.6-luna[max] › `ca_explorer_standard_h` gpt-5.6-terra[medium*, high] | `ca_explorer_senior` gpt-5.6-sol[medium*, high] |
| Worker | `ca_worker_light` gpt-5.6-luna[max] | `ca_worker_standard_m` gpt-5.6-sol[high*, xhigh] › `ca_worker_standard_h` gpt-6-astra[low] | `ca_worker_senior` gpt-6-astra[medium*, high] |
| Advisor | `ca_advisor_light` gpt-6-astra[low] | `ca_advisor_standard` gpt-6-astra[medium] | `ca_advisor_senior` gpt-6-astra[high*, xhigh] |

## Pinned and caller-selected effort

Five entries pin `model_reasoning_effort` in their template because their cell
has one effort: `ca_worker_light` (`max`), `ca_explorer_standard_m` (`max`),
`ca_worker_standard_h` (`low`), `ca_advisor_light` (`low`), and
`ca_advisor_standard` (`medium`). The other six omit it; the caller passes
`reasoning_effort` from the listed options with `fork_turns` set to none.
Every entry pins its model.

## Advisor defaults

The decision packet goes to `ca_advisor_standard`; the acceptance packet goes to
`ca_advisor_light`. `ca_advisor_senior` is reached only when a verdict reports
low confidence or the user declares it.

The first-round pool, the senior gate, and the escalation ladder are in
[SKILL.md](../SKILL.md).

## Adjust a value

Change the affected template's `model` or `model_reasoning_effort` and this table
together, run `sh plugins/codex-advisor/scripts/verify.sh`, and release. A model
generation change touches only those two places; the skill text and the scripts
stay unchanged.
