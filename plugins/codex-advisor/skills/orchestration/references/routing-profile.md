# Routing profile

Declared 2026-09-30. The dials below are anchored to `gpt-6-luna`,
`gpt-6.1-sol`, and `gpt-6-astra`. This file is the source of every model, allowed effort,
default, and candidate order. Each entry template copies its own model and any
pinned effort into its fields. Its description names the model, the candidate
position where a cell has two, and the effort where it is pinned. The skill text
repeats none of them.

Notation: `model[a*, b]`. Every listed effort is allowed and `*` marks the
default. Where a cell lists two candidates, `›` separates them in usage order.
A single bare effort is pinned in the entry; an entry with several efforts
leaves effort to the caller.

| Role | `mainstay` | `crux` | `rescue` |
|---|---|---|---|
| Explorer | `ca_explorer_mainstay_m` gpt-6-luna[high*, xhigh] › `ca_explorer_mainstay_h` gpt-6.1-sol[medium*, high] | `ca_explorer_crux_m` gpt-6-luna[max] › `ca_explorer_crux_h` gpt-6.1-sol[xhigh] | `ca_explorer_rescue` gpt-6-astra[medium*, high] |
| Worker | `ca_worker_mainstay_m` gpt-6-luna[max] › `ca_worker_mainstay_h` gpt-6.1-sol[medium*, high] | `ca_worker_crux_m` gpt-6.1-sol[xhigh] › `ca_worker_crux_h` gpt-6-astra[low*, medium] | `ca_worker_rescue_m` gpt-6.1-sol[max] › `ca_worker_rescue_h` gpt-6-astra[high*, xhigh] |
| Advisor | `ca_advisor_mainstay_m` gpt-6.1-sol[medium*, high] › `ca_advisor_mainstay_h` gpt-6-astra[low*, medium] | `ca_advisor_crux_m` gpt-6.1-sol[high*, xhigh] › `ca_advisor_crux_h` gpt-6-astra[high] | `ca_advisor_rescue_m` gpt-6.1-sol[xhigh*, max] › `ca_advisor_rescue_h` gpt-6-astra[xhigh] |

## Pinned and caller-selected effort

Seven entries pin `model_reasoning_effort` because their cell has one effort:
`ca_explorer_crux_m`, `ca_explorer_crux_h`, `ca_worker_mainstay_m`,
`ca_worker_crux_m`, `ca_worker_rescue_m`, `ca_advisor_crux_h`, and
`ca_advisor_rescue_h`. The other ten omit it and leave effort to the caller.
Every entry pins its model.

## Consultation mapping

An Explorer or Worker entry consults at the lowest dial in its tier's Advisor
cell that is not weaker than its own dial; if none is, it uses that cell's
strongest dial. The Advisor has no consultation ladder of its own.

A primary consults at the lowest Advisor dial in any tier that is not weaker
than the primary's dial. If no Advisor dial is not weaker, use
gpt-6-astra[xhigh]. A primary whose exact model id is absent from this profile
uses gpt-6.1-sol[xhigh].

## Acceptance mapping

Delegated work uses the Advisor cell of the highest tier that built it, at the
lowest dial in that cell not weaker than the strongest dial that built it.
Primary-authored work uses the lowest Advisor dial that is not weaker than the
primary's dial; when two entries allow that dial, use the one in the lower
tier. If none qualifies, use `ca_advisor_rescue_h` at its pinned effort. If
the primary's exact model id is absent from this profile, use
`ca_advisor_crux_m` at `xhigh`. A low-confidence verdict leaves acceptance
pending and goes to the user; it does not trigger another Advisor dial.

For "not weaker", compare model first:
gpt-6-luna < gpt-6-sol < gpt-6.1-sol < gpt-6-astra. Compare effort second:
low < medium < high < xhigh < max.

## Declared assumptions

This profile assumes that a model change gains more capability than an effort
increase, and that `xhigh` is a distinct capability jump. The next model
generation change invalidates both assumptions and requires re-evaluation.
