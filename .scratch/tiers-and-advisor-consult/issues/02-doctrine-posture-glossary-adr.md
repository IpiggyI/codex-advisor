# 02: Doctrine, canonical posture text, glossary, and ADR-0006

**What to build:** A primary that loads the skill reads the new tier mechanism (admission, escalation, failure counting), the consultation posture and adoption rules, and the acceptance dial rule. The canonical posture text exists once, in a new reference that later tickets copy byte for byte. The glossary and ADR-0006 match. The Chinese twins of every touched Markdown file are updated in the same change.

**Blocked by:** 01 (the consultation wording and ADR-0006's mechanism section need its mechanism decision; ADR-0006's host facts come from its probes).

**Status:** resolved

## Required reading before starting

- `spec.md`: §Authority and conflicts, TR-1, TR-4 to TR-8, AC-1 to AC-7, DR-1, DR-3, DR-4, DR-5 (ticket 02 sections), DR-6, DR-7, AC-12 (for ADR-0006), X-4, X-5 (the stage-scope note), §Decision Boundaries, §Goal-Drift Checks, §Mechanism decision (filled by 01).
- `sources.md` §2.4 (all rows: Rejected rows must not reappear; Superseded rows show the wording to avoid).
- `acceptance.md` §01 (host facts for ADR-0006).
- Current files: `plugins/codex-advisor/skills/orchestration/SKILL.md`, `references/role-contracts.md`, `references/operations.md` (§Recover and hand off actual state, §Advice and independent acceptance), `CONTEXT.md`, `docs/adr/0003-*.md`, `0004-*.md`, `0005-*.md`, `plugins/codex-advisor/skills/orchestration/agents/openai.yaml`.
- rpiv-advisor at `d74b1c99`: `advisor/register.ts` (`DEFAULT_PROMPT_GUIDELINES`, the text AC-7 adapts) and `prompts/advisor-system.txt` (the plan / correction / stop contract).
- `AGENTS.md` §Chinese mirror of runtime docs.

## Owns

- `plugins/codex-advisor/skills/orchestration/SKILL.md`
- `plugins/codex-advisor/skills/orchestration/references/consult-posture.md` (new)
- `plugins/codex-advisor/skills/orchestration/references/role-contracts.md`
- `references/operations.md`, only §Recover and hand off actual state and §Advice and independent acceptance
- `plugins/codex-advisor/skills/orchestration/agents/openai.yaml`, only if its text names a retired concept
- `CONTEXT.md`
- `docs/adr/0006-*.md` (new)
- The `docs/zh/` twins of every Markdown file above

Not the routing profile: ticket 03 owns it so that the verifier's profile-to-template check stays consistent.

## Establishes and consumes

- **Establishes** DR-3: the canonical posture text. Tickets 04 (EN-5), 05 (AC-8), and 06 copy or read it and must not reword it.
- **Establishes** the doctrine text for TR-1, TR-4 to TR-8, AC-1 to AC-6, DR-1, DR-4, DR-6, DR-7.
- **Consumes** the ticket 01 mechanism decision.

## Acceptance

- [x] `SKILL.md` covers:
  - [x] Admission: `mainstay` by default; `crux` at first round when a key difficulty or interacting constraints are identified; no quota; `rescue` never at first round without a user declaration.
  - [x] Escalation: next tier, no same-tier model switch, a model-level floor, and a higher effort when the model stays the same.
  - [x] Failure counting and the path to the user, R3 kept, per TR-8.
  - [x] The consultation per AC-3, with posture and adoption rules pointing to `consult-posture.md`.
  - [x] Acceptance per AC-1 and AC-2, including the low-confidence rule.
  - [x] No first-round pool, senior gate, decision packet, "Proactive advice is allowed", model name, or effort value.
  - [x] Complete-attempt, fresh-thread, Architect mode, and acceptance-ownership text unchanged in meaning.
- [x] `consult-posture.md` has three delimited blocks: the full variant, the reduced variant, and the adoption rules. The text follows AC-5 to AC-7, with imperative triggers, no "commit" step, the durable-before-call rule, the restate-in-next-reply rule, and the reconcile call; AC-6 is complete. It states the AC-5 identity rule and the `gpt-5.6-terra` example without hard-coding a family list.
- [x] `role-contracts.md` keeps the explorer and worker packets, keeps the acceptance packet with the AC-2 dial rule and the low-confidence rule, removes the decision packet, and says the consultation takes no packet.
- [x] `operations.md` §Recover and hand off actual state and §Advice and independent acceptance describe TR-7/TR-8 and AC-1/AC-2; no senior gate or decision packet remains in these sections.
- [x] `CONTEXT.md` changes per DR-6.
- [x] ADR-0006 records this spec's decisions, lists every superseded sentence of ADR-0003, ADR-0004, and ADR-0005 by quoting it, records the ticket 01 mechanism decision and host facts with invalidation checks, records AC-12's `/hooks` review as the one user step ADR-0004's installation-only rule cannot remove, and moves the grok lane to `0.4.0`.
- [x] Twins are re-translated. Identifiers, entry names, dial notation, and the posture block delimiters stay character-exact.

## Verification

- `python3 tests/test_zh_mirror.py` passes.
- `sh plugins/codex-advisor/scripts/verify.sh` passes. It reads only the routing profile among the docs, which this ticket does not touch, so a failure here means an unexpected coupling. Report it rather than working around it.
- Text search, limited to the files this ticket owns (D45): `SKILL.md`, `consult-posture.md`, `role-contracts.md`, the two owned sections of `operations.md`, `openai.yaml` if touched, and their twins, plus `CONTEXT.md` except its `_Avoid_` lines, which DR-6 requires to name the retired terms. ADR-0006 is excluded because it quotes the superseded text. The routing profile, the rest of `operations.md`, templates, scripts, README, and `plugin.json` still hold old terms that tickets 03 and 06 change; they are not searched here.
  - None of these in that scope: `first-round pool`, `senior gate`, `decision packet`, `DECISION packet`, `Proactive advice is allowed`, or `light`/`standard`/`senior` used as tier names.
  - Not in `SKILL.md` or its twin: any `gpt-` string, or any dial notation of the form `name[effort…]`.

  Record the commands and their output.
- `git diff --check`.

## Stop conditions

S8. Also stop if the ticket 01 decision is still pending.

## Not in this ticket

The routing profile, the templates, the installer, the inspector, the consultation component, the hooks, README, and the version manual.

## Comments

Resolved on 2026-09-26. The checked items record this ticket's acceptance
checkpoint; later tickets extend the intermediate state where specified.
See `../acceptance.md` section 02 for commands, evidence, authorized
exceptions and the current result. Final delivery review is recorded separately.
