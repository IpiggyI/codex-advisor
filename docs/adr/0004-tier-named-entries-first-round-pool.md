---
status: accepted
---

# Tier-named native entries, first-round pool with a gated senior tier, and a self-updating installer

## Decision

Native entries are named by role and capability tier, not by model: `ca_explorer_light`, `ca_explorer_standard_m`, `ca_explorer_standard_h`, `ca_explorer_senior`, `ca_worker_light`, `ca_worker_standard_m`, `ca_worker_standard_h`, `ca_worker_senior`, `ca_advisor_light`, `ca_advisor_standard`, `ca_advisor_senior`. A tier that lists two models gets two entries; `_m` is the default candidate and `_h` the stronger alternative (`_l` is reserved for a cheaper one). Every entry pins its model. An entry pins its reasoning effort only when its cell allows a single effort; otherwise the caller passes the effort per spawn. The eight model-named entries of 0.1.0 are retired.

Dial values live in one routing profile shipped as a reference inside the skill, in the notation `model[a*, b, c]` (all listed efforts are first-round options, `*` is the default, listed model order is candidate order). The skill text carries mechanism only: light and standard form the first-round pool, chosen by judgment dependence with no precondition between them and the cheapest adequate dial at its default; senior is reached only through the senior gate (two capability-attributed complete failed attempts inside the pool, or a user declaration; for the Advisor, a low-confidence verdict or a user declaration); after a failed acceptance the escalation ladder applies: R1 rework ticket in the same thread at the same dial; R2 raise in a fresh thread with the current-state handoff when rework fails and the cause is capability, either a higher effort of the same model or another model; R3 the same model is raised at most once; R4 a major execution problem may skip the rework ticket and change model, counted as one failure.

Independent acceptance is the Advisor's second request shape and runs on the Advisor entries in a fresh thread; the separate reviewer entry is retired. Decision advice defaults to the standard tier, acceptance to the light tier.

The companion installer owns this plugin's installed files: it overwrites the eleven shipped entries when they differ, deletes the eight retired filenames when present, touches nothing else, and fails its check mode on drift or residue. It keeps refusing symlinked, non-regular, root, and dot-segment destinations. Distributed text files are pinned to LF through repository attributes. The inspector takes an entry name and reads the expected model and any pinned effort from the shipped TOML; it no longer judges whether an effort is allowed.

Every shipped TOML has a parseable Chinese twin whose configuration keys equal the template. The term Implementer is retired in favor of Worker. Version `0.2.0`, with a version manual.

## What this supersedes

- ADR-0003: the sentence that no fixed ladder is imposed is replaced by the escalation ladder and the senior gate; the wording that decision advice and independent acceptance retain distinct native entries is replaced by one Advisor entry per tier with two request shapes; the routing table in the skill is replaced by the routing profile reference. The complete-attempt definition, the fresh-thread policy for every effort or model change, Architect mode, the required-advice triggers, and the acceptance rules stand.
- The fork specification's user story 39 and its installer decision (never overwrite a modified destination): the installer now overwrites this plugin's own files and deletes its retired names. Non-destructive behaviour toward everything else stands.
- ADR-0001 and ADR-0002 are already historical; their entry names appear here only in the retire list.

## Basis

The user declared the table on 2026-09-16 (three grilling rounds) after watching the sibling plugin's main agent route first-round work to the most expensive models when doctrine left the tier choice to judgment, and after observing that model-named entries make every model generation change ripple through entry names, skill text, inspector options, and installer selectors.

Host facts checked on 2026-09-16 against the official Codex subagents documentation and the spawn tool text in a local rollout: a custom agent file's `model` and `model_reasoning_effort` take precedence over spawn values; a file that sets only `model` keeps the effort resolved from the spawn value, the agents default, then the parent; per-spawn `model` and `reasoning_effort` are honoured only with `fork_turns` set to none. This is why pinning the model in every file and the effort only in single-effort cells removes the omission footgun without removing first-round choice.

The two machines each carry the eight 0.1.0 entries under `$CODEX_HOME/agents`; the installer of 0.1.0 would leave them in place after the rename because a new name is not a conflict. The sibling plugin's ADR 0018 chose unconditional overwrite plus a retire list for its own user-level files and named this plugin's refusal policy as the alternative it rejected; this fork now adopts the same policy for the same reason: live copies are written only by the installer, so old versus new is not a judgment the installer needs to make.

## Alternatives not adopted

- One entry per dial with both model and effort pinned (seventeen files): rejected as too many files for the value; only the standard tier has two models, so eleven entries suffice when the caller passes effort where a cell allows several.
- Rank suffixes `_l`, `_m`, `_h` as the only distinguisher across all tiers: adopted only inside a tier with several models; single-model tiers carry no suffix.
- Keeping the routing table in the skill text: every value change would edit doctrine.
- A user-level routing profile installed to a live path, as the sibling plugin does: this fork already ships its table inside the plugin, and a plugin-internal reference reaches both machines through the plugin update with no extra installer target. The sibling plugin may pilot the same shape later; that is its own decision.
- Keeping a separate reviewer entry: a fourth role name for one request shape of the Advisor.
- Keeping the refuse-to-overwrite installer plus a retire list: still forces a hand deletion after every template edit.
- Deleting retired files only after reading their `name` field: adds a branch for a case that does not exist, since only this installer ever wrote those filenames.
- `1.0.0` for the breaking rename: the routing table is expected to change again; `0.x` minor carries the break, and the README upgrade notes name the retired entries.

## Revisit when

- The host adds an agents-level way to express a tier's allowed efforts: the caller-passed effort could then be constrained mechanically and the routing profile would shrink.
- The Codex CLI moves past 0.154.0 and changes the custom-agent precedence or the `fork_turns` condition: re-read the documentation and re-run the live route check.
- The primary agent still takes the most expensive dial inside the pool: consider making `*` a hard default in the entries.
- The installer overwrites a hand-edited installed entry that the user wanted kept, once or more: reconsider a dry-run option.
- `gpt-6-sol` or another generation ships: change the model identifier in the affected TOML and the routing profile only; no new ADR.
- The grok lane (0.3.0) is designed: mechanism recorded here as a Node runner wrapping the `grok` CLI with a spec and receipt flow through the shell, ported from the sibling plugin's runner; naming, tests, and doctrine wording get their own spec and decision record.

## Notes

- Task artifacts: `.scratch/tier-role-pool/`. Baseline commit `f37830f`.
- The sibling plugin's routing profile lists different codex-lane dials in four cells (Explorer light, Explorer standard, Explorer senior, worker light). The user chose this fork's table as authoritative; updating the sibling's canonical profile is a follow-up in that repository.
