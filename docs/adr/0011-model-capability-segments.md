---
status: accepted
---

# Model capability segments

## Decision

Rank models by four segments: `starter`, `midrange`, `premium`, and
`flagship`, from low to high. Keep the task tiers `mainstay`, `crux`, and
`rescue`. A segment describes a model's capability position; a tier describes
a task allocation. Models in the same segment share a capability rank.

The routing profile assigns `gpt-6-luna` to `starter`, `gpt-6.1-sol` to
`premium`, and `gpt-6-astra` to `flagship`. No current model occupies
`midrange`. Native entries keep their models, efforts, defaults, and candidate
order.

Consultation reads model ranks from the segment table and compares segment
first, then reasoning effort. Recovery uses the same segment floor. Allocation
may use a later candidate when its higher segment is needed. Missing, duplicate,
or unknown model placements fail explicitly before inference.

## Basis

The user requested four stable capability positions on 2026-10-02, following
the fable-advisor routing profile and its ADR 0026, accepted on 2026-10-01.
This revises [ADR-0009](0009-gpt-6-1-sol-across-the-routing-profile.md)'s
model-order representation. It makes the gap between `gpt-6-luna` and `gpt-6.1-sol`
explicit even when both are candidates in `mainstay`.

The segment assignments are user-declared routing values, not measured model
quality. The assumption that a higher segment improves results more than an
effort increase, and that `xhigh` is a distinct capability jump, remains subject
to re-evaluation at the next model generation change. Re-evaluate the changed
model's segment and check affected consultation, acceptance, and recovery paths.

## Shipped wording

`AGENTS.md` already requires settled, result-oriented shipped text. The review
found declaration dates and remarks about template descriptions and skill-text
duplication in both routing-profile twins. Those belong in maintenance records.
The native-entry anchor models remain runtime information.

The preceding dial declaration was dated 2026-09-30. Entry templates carry their
own model and any fixed effort; their descriptions identify model, candidate
position, and fixed effort. The routing profile owns these values, and the
orchestration doctrine uses that source rather than repeating them.

No speed conclusion is added: this repository's current runtime text contains
none, and the review does not measure model speed. Existing evidence requirements
and conditional failure messages remain actionable runtime rules.
