---
status: accepted
---

# GPT-6.2 across the routing profile

## Decision

`gpt-6.2-sol` replaces `gpt-6.1-sol` and `gpt-6.2-astra` replaces `gpt-6-astra`
in every native entry and in every routing-profile cell. Entry names, efforts,
defaults, and candidate order stay as they were in `0.3.9`; `gpt-6-luna` stays,
because the catalog has no 6.2 Luna.

| Model in `0.3.9` | Model in `0.3.10` | Segment |
|---|---|---|
| `gpt-6-luna` | `gpt-6-luna` | `starter` |
| `gpt-6.1-sol` | `gpt-6.2-sol` | `premium` |
| `gpt-6-astra` | `gpt-6.2-astra` | `flagship` |

The fallback for a primary whose model id is absent from the profile becomes
`gpt-6.2-sol[xhigh]`, and the strongest Advisor dial becomes
`gpt-6.2-astra[xhigh]`.

The segment table keeps `gpt-6.1-sol` in `premium` and `gpt-6-astra` in
`flagship`. No entry uses them; they rank a primary that still runs on one of
them, so that primary consults and is accepted at the dial its segment and effort
select instead of at the unknown-model fallback. A `gpt-6-astra` primary at
`xhigh` therefore consults `gpt-6.2-astra[xhigh]`, not `gpt-6.2-sol[xhigh]`. Both
legacy primaries receive the full posture, because the posture is reduced only on
an exact match between the primary's model and its advisor's model.

Both declared assumptions in the routing profile hold for 6.2: a higher segment
gains more than an effort increase, and `xhigh` is a distinct capability jump.

The release is `0.3.10`; `0.4.0` stays reserved for the grok lane.

## Basis

On 2026-11-17 the user stated that GPT moved to the 6.2 series
(`gpt-6.2-astra`, `gpt-6.2-sol`) and chose, in this order: a direct model swap with
every dial unchanged; the existing segments and assumptions for the 6.2 models;
and keeping the replaced ids in the segment table for primaries.

On 2026-11-17, `codex debug models` (refreshed catalog) from Codex CLI `0.169.0`
on WSL listed `gpt-6.2-sol` and `gpt-6.2-astra` with efforts `low` through
`ultra`, and no 6.2 Luna. The bundled catalog of that same binary did not list
either 6.2 model. Process consultation reads only the bundled catalog
(`consult_native.py`, `catalog()`) and fails with `catalog` when the exact advisor
model is absent. After upgrading WSL to Codex CLI `0.169.1`,
`codex debug models --bundled` listed both 6.2 models, each with
`use_responses_lite` true. Consultation on a 6.2 dial therefore requires Codex CLI
`0.169.1` or later on each side.

ADR-0011 records segment placements as user-declared routing values, not
measurements. No comparison has measured `gpt-6.2-sol` against `gpt-6.1-sol` or
`gpt-6.2-astra` against `gpt-6-astra`; placing each pair in one segment is the
user's declaration.

ADR-0008 stands: entry filenames do not change, so the installer overwrites each
template in place and no hand cleanup is needed.

## Alternatives not adopted

- Re-tune dials together with the swap: the user kept every dial.
- Drop `gpt-6.1-sol` and `gpt-6-astra` from the segment table: a primary on
  either would take `gpt-6.2-sol[xhigh]`, so an Astra primary would get a weaker
  advisor.
- Read the refreshed catalog instead of the bundled one: the bundled catalog is
  the offline, version-pinned source that the tool-isolation evidence was taken
  from; upgrading the CLI keeps that source.

## Revisit when

- A consultation or acceptance on a 6.2 dial fails because the account cannot
  serve that model at the routed effort, once.
- Evidence ranks a 6.2 model outside the segment of the model it replaced.
- A 6.2 Luna, or another model the profile does not list, becomes available to a
  primary.

## What this supersedes

From ADR-0011:

> The routing profile assigns `gpt-6-luna` to `starter`, `gpt-6.1-sol` to
> `premium`, and `gpt-6-astra` to `flagship`.

The profile now assigns `gpt-6-luna` to `starter`, `gpt-6.2-sol` and
`gpt-6.1-sol` to `premium`, and `gpt-6.2-astra` and `gpt-6-astra` to `flagship`.

ADR-0009's dial structure, consultation mapping, and acceptance mapping stand
with the model ids replaced as above.
