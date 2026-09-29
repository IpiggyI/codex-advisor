# Routing profile

Declared 2026-09-26. The dials below are anchored to GPT-6 Luna, GPT-6 Sol,
and GPT-6 Astra. This file is the source of every model, allowed effort,
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
| Explorer | `ca_explorer_mainstay_m` gpt-6-luna[high*, xhigh] › `ca_explorer_mainstay_h` gpt-6-sol[medium*, high] | `ca_explorer_crux_m` gpt-6-luna[max] › `ca_explorer_crux_h` gpt-6-sol[xhigh] | `ca_explorer_rescue` gpt-6-astra[medium*, high] |
| Worker | `ca_worker_mainstay_m` gpt-6-luna[max] › `ca_worker_mainstay_h` gpt-6-sol[high] | `ca_worker_crux_m` gpt-6-sol[xhigh*, max] › `ca_worker_crux_h` gpt-6-astra[low*, medium] | `ca_worker_rescue` gpt-6-astra[high*, xhigh] |
| Advisor | `ca_advisor_mainstay` gpt-6-astra[low*, medium] | `ca_advisor_crux` gpt-6-astra[high] | `ca_advisor_rescue` gpt-6-astra[xhigh] |

## Pinned and caller-selected effort

Six entries pin `model_reasoning_effort` because their cell has one effort:
`ca_explorer_crux_m`, `ca_explorer_crux_h`, `ca_worker_mainstay_m`,
`ca_worker_mainstay_h`, `ca_advisor_crux`, and `ca_advisor_rescue`. The other
seven omit it and leave effort to the caller. Every entry pins its model.

## Consultation mapping

A `mainstay` entry consults at gpt-6-astra[low]. A `crux` entry consults at
gpt-6-astra[high]. A `rescue` entry consults at gpt-6-astra[xhigh]. The Advisor
has no consultation ladder of its own.

A primary consults at the lowest Advisor dial that is not weaker than the
primary's dial. If no Advisor dial is not weaker, use gpt-6-astra[xhigh]. A
primary whose exact model id is absent from this profile also uses
gpt-6-astra[xhigh].

## Acceptance mapping

Work from one tier uses that tier's Advisor entry: `ca_advisor_mainstay`,
`ca_advisor_crux`, or `ca_advisor_rescue`. Work built by several tiers uses the
highest tier involved. Primary-authored work uses the lowest Advisor dial that
is not weaker than the primary's dial. If none qualifies, or the primary's exact
model id is absent from this profile, use `ca_advisor_rescue` at its pinned
effort. A low-confidence verdict leaves acceptance pending and goes to the user;
it does not trigger another Advisor dial.

For "not weaker", compare model first:
gpt-6-luna < gpt-6-sol < gpt-6-astra. Compare effort second:
low < medium < high < xhigh < max.

## Declared assumptions

This profile assumes that a model change gains more capability than an effort
increase, and that `xhigh` is a distinct capability jump. The next model
generation change invalidates both assumptions and requires re-evaluation.
