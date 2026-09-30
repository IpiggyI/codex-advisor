---
status: accepted
---

# GPT-6.1 Sol across the routing profile

## Decision

`gpt-6.1-sol` replaces `gpt-6-sol` in every Explorer and Worker cell, joins the
`rescue` Worker cell, and becomes the first candidate in every Advisor cell. The
entries that change against `0.3.0`:

| Entry | `0.3.0` | `0.3.1` |
|---|---|---|
| `ca_explorer_mainstay_h` | gpt-6-sol[medium*, high] | gpt-6.1-sol[medium*, high] |
| `ca_explorer_crux_h` | gpt-6-sol[xhigh] | gpt-6.1-sol[xhigh] |
| `ca_worker_mainstay_h` | gpt-6-sol[high] | gpt-6.1-sol[medium*, high] |
| `ca_worker_crux_m` | gpt-6-sol[xhigh*, max] | gpt-6.1-sol[xhigh] |
| `ca_worker_rescue_m` | none | gpt-6.1-sol[max] |
| `ca_worker_rescue_h` | named `ca_worker_rescue` | same dial |
| `ca_advisor_mainstay_m` | none | gpt-6.1-sol[medium*, high] |
| `ca_advisor_mainstay_h` | named `ca_advisor_mainstay` | same dial |
| `ca_advisor_crux_m` | none | gpt-6.1-sol[high*, xhigh] |
| `ca_advisor_crux_h` | named `ca_advisor_crux` | same dial |
| `ca_advisor_rescue_m` | none | gpt-6.1-sol[xhigh*, max] |
| `ca_advisor_rescue_h` | named `ca_advisor_rescue` | same dial |

Renamed entries keep their dials and instructions and take the `_h` suffix that
ADR-0004 gives a cell with two models. The plugin ships seventeen native
entries. For "not weaker", the model order is
`gpt-6-luna < gpt-6-sol < gpt-6.1-sol < gpt-6-astra`; `gpt-6-sol` stays in it
for primaries that run on it.

An Explorer or Worker consults at the lowest dial in its tier's Advisor cell that
is not weaker than its own dial, or at that cell's strongest dial when none is.
Luna and `gpt-6.1-sol` entries therefore consult `gpt-6.1-sol`, and Astra
entries consult `gpt-6-astra`. The five `gpt-6.1-sol` Explorer and Worker
entries match their advisor's model and carry the reduced posture.

A primary consults at the lowest Advisor dial not weaker than its own, or at
`gpt-6-astra[xhigh]` when none is. A primary whose exact model id is absent from
the profile consults at `gpt-6.1-sol[xhigh]`. The routing profile declares that
dial, and the consultation component reads it from there.

Independent acceptance of delegated work uses the Advisor cell of the highest
tier involved, at the lowest dial in that cell not weaker than the strongest dial
that built the work. Primary-authored work uses the lowest Advisor dial not
weaker than the primary; when two entries allow that dial, the entry in the lower
tier answers. When no dial qualifies, `ca_advisor_rescue_h` answers. When the
primary's exact model id is absent from the profile, `ca_advisor_crux_m` answers
at `xhigh`.

`SessionStart` selects the primary's posture by applying the consultation mapping
at every effort, because the event carries no effort. When the selected advisor
model depends on effort, the posture stays pending. `ca_advisor_rescue_m` allows
`max` so that a `gpt-6.1-sol` primary reaches `gpt-6.1-sol` at every effort and
receives the reduced posture.

The release is `0.3.1`; `0.4.0` stays reserved for the grok lane.

## Basis

The user's Codex bill for 2026-09-30 showed three process consultations costing
$2.00 of $2.46 (81%). All three ran on `gpt-6-astra`, replayed the caller's full
context (192,272 input tokens together), and read no cached input. The bill's unit
costs are $10 input and $50 output per million tokens for `gpt-6-astra`, and $2
input, $0.10 cached input, and $10 output for `gpt-6.1-sol`. At the `gpt-6.1-sol`
rates, the same consultations cost about $0.40. Before this decision every Advisor
dial was `gpt-6-astra`, and a `gpt-6.1-sol` primary, absent from the profile,
consulted at `gpt-6-astra[xhigh]`.

The user made three decisions on 2026-09-30:

1. `gpt-6.1-sol` joins the Advisor row, ranks no higher than `gpt-6-astra`, and
   the `rescue` Advisor cell also allows `max`.
2. Every Explorer and Worker `gpt-6-sol` dial moves to `gpt-6.1-sol` with the
   dials above, and the `rescue` Worker cell gains `gpt-6.1-sol[max]`. The new
   `gpt-6.1-sol` delegates at `high` in `mainstay` and at `xhigh` in `crux`
   outranked the single `gpt-6.1-sol` dial of their Advisor cell, so the user
   widened `ca_advisor_mainstay_m` and `ca_advisor_crux_m` instead of sending
   those consultations to `gpt-6-astra`.
3. A primary on a model absent from the profile consults, and its own work is
   accepted, at `gpt-6.1-sol[xhigh]` instead of `gpt-6-astra[xhigh]`.

That `gpt-6-sol` ranks below `gpt-6.1-sol` is our inference from the version
number; no comparison has measured it.

The lowest-not-weaker rule keeps each Advisor at least as strong as the delegate
it advises or accepts, so Astra-built work still meets an Astra advisor. The
fallback for an unlisted model gives up that guarantee: a primary on an unlisted
model stronger than `gpt-6.1-sol` gets a weaker advisor. The user chose the lower
cost.

The `SessionStart` input carries `session_id`, `transcript_path`, `cwd`,
`hook_event_name`, `model`, `permission_mode`, and `source`, and no effort
([Codex hooks](https://learn.chatgpt.com/docs/hooks), read 2026-09-30). The event
pinned in `tests/fixtures/hooks.json` has no effort either. Without `max` in
`ca_advisor_rescue_m`, a `gpt-6.1-sol` primary at `max` would consult
`gpt-6-astra[xhigh]` while it consults `gpt-6.1-sol` at every lower effort, and
the hook could not tell which posture applies.

On 2026-09-30, `codex debug models --bundled` from Codex CLI `0.159.2` on this
machine's WSL and Windows sides listed `gpt-6.1-sol` with efforts `low` through
`max`. Process consultation requires the exact advisor model in that catalog.

ADR-0007 names a change to the `SessionStart` posture injection or to server-side
dial selection as a revisit trigger, and both change here. Its decision holds: under
the current profile the hook still injects a posture for every primary model, and
the server still selects the dial, so consultation stays out of the skill's load
events.

ADR-0008 stands: the installer deletes no old filenames. After the update, the
former `ca-advisor-mainstay.toml`, `ca-advisor-crux.toml`,
`ca-advisor-rescue.toml`, and `ca-worker-rescue.toml` stay in each side's
`agents` directory and can still be spawned under their former names. A dispatch
under a former name leaves the dispatch check pending, because no shipped
template carries that name. A former `ca_worker_rescue` also has its process
consultations rejected, because the profile no longer lists it. The four files
are removed by hand on each side after the new entries are installed there, the
same one-time step ADR-0008 records for the `0.2.0` entries.

## Alternatives not adopted

- Replace `gpt-6-astra` with `gpt-6.1-sol` in every Advisor cell: Astra-built
  `crux` and `rescue` work would be consulted on and accepted by a weaker model.
- Keep `ca_advisor_mainstay_m` at `medium` and `ca_advisor_crux_m` at `high`:
  `gpt-6.1-sol` delegates at `high` in `mainstay` and at `xhigh` in `crux` would
  consult `gpt-6-astra`, at its price and under the full posture.
- Keep `ca_advisor_rescue_m` at `xhigh` only and let the hook assume an effort:
  the posture of a `gpt-6.1-sol` primary at `max` would not match its advisor,
  and no event field supports the assumption.
- Keep `gpt-6-astra[xhigh]` for a primary on an unlisted model: every such
  consultation and acceptance would run at Astra prices.
- Adopt the sibling fable-advisor plugin's lane dispatch for Advisor calls: the
  user kept this change to the routing profile.
- Release as `0.4.0`: ADR-0006 reserves it for the grok lane.

## Revisit when

- A consultation or acceptance on a `gpt-6.1-sol` dial fails because the account
  cannot serve that model at the routed effort, once.
- Evidence ranks `gpt-6.1-sol` at or below `gpt-6-sol`, or at or above
  `gpt-6-astra`.
- The `SessionStart` event starts carrying the session's effort.
- A later bill for a `gpt-6.1-sol` primary still shows consultation cost above
  main-session cost.
- A primary runs on a model that the profile does not list and that ranks above
  `gpt-6.1-sol`.

## What this supersedes

The quotations below are every complete sentence in ADR-0005 and ADR-0006 whose
rule this decision replaces.

From ADR-0005:

> The three Advisor entries state that the field may name an executor other than the primary, and that the evidence and its coverage are judged, not who ran it.

Only the count is replaced: all six Advisor entries carry the statement.

From ADR-0006:

> It uses `gpt-6-luna`, `gpt-6-sol`, and `gpt-6-astra` across thirteen role-and-tier native entries.

> The acceptance dial follows the accepted work's tier; work from several tiers uses the highest tier involved.

> Primary-authored work uses the lowest advisor dial not weaker than the primary, or the strongest advisor dial when none qualifies or the primary's exact model id is absent from the profile.

For the second quotation, only the dial choice is replaced: the highest tier
involved still selects the Advisor cell, and the dial inside that cell now
follows the strongest dial that built the work. For the third, only the case of
an absent model id is replaced: it now uses `ca_advisor_crux_m` at `xhigh`.
