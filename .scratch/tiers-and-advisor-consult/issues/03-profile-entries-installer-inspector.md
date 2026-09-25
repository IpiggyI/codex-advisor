# 03: Routing profile, thirteen native entries, installer, inspector, and route check

**What to build:** A primary picks work by role and tier from the new table, and each of the thirteen tier-named entries dispatches at its dial.
- The routing profile holds the TR-3 table, the AC-4 and AC-2 mappings, the dial ordering, and the TR-9 assumptions.
- The thirteen entries replace the eleven 0.2.0 entries, and installing removes the old names.
- The inspector and the verifier cover the new set, and a live route check proves every entry dispatches at its dial.

The entries' posture sections are added by ticket 04, together with the consultation they tell delegates to call.

**Blocked by:** 01 (dial availability and precedence on this Codex version), 02 (the doctrine the entries and the routing profile point to, including the acceptance-only Advisor).

**Status:** resolved

## Required reading before starting

- `spec.md`: TR-2, TR-3, TR-9, AC-2, AC-4, EN-1 to EN-4, EN-6, DR-2, DR-5 (ticket 03 sections), X-2, X-4, X-5, §Testing Decisions items 1, 2, 5, 6, §Goal-Drift Checks.
- `sources.md` §2.4 rows D3, D4, D16, D16a, D19.
- `acceptance.md` §01 (dial availability and precedence on this Codex version).
- `plugins/codex-advisor/skills/orchestration/references/role-contracts.md` as ticket 02 left it (the acceptance-only Advisor packet the advisor entries answer).
- Current `references/routing-profile.md`, `agents/*.toml`, `agents/retire.txt`, `scripts/install-agents.sh`, `scripts/inspect-agent-runtime.sh`, `scripts/verify.sh`, `tests/test_zh_mirror.py`, `docs/zh/agents/*.toml`.
- `docs/adr/0004-*.md` (naming, pinning, installer policy).
- `.scratch/tier-role-pool/acceptance.md` §Live route check (method and record shape).

## Owns

- `plugins/codex-advisor/skills/orchestration/references/routing-profile.md` and its twin
- `plugins/codex-advisor/agents/*.toml`: add thirteen, delete the eleven 0.2.0 templates
- `agents/retire.txt`
- `scripts/install-agents.sh`
- `scripts/inspect-agent-runtime.sh` (only if needed)
- `scripts/verify.sh`: installation and runtime groups
- `tests/test_zh_mirror.py` (only if needed)
- `docs/zh/agents/*.toml`
- `references/operations.md` §Install and discover, §Select a native entry, §Invoke and validate, and the group list in §Verify changes, plus their twin sections

## Establishes and consumes

- **Establishes** DR-2, EN-1 to EN-4, EN-6 for the templates, and the TR-3 table as shipped.
- **Consumes** the ticket 01 dial facts and the ticket 02 doctrine.
- **Leaves for ticket 04:** the posture sections (EN-5) and the verifier's posture checks. Until then, the existing same-role identical-instructions check stays as it is.

## Acceptance

- [x] The routing profile's table equals spec TR-3 cell by cell, with entry names, `›` candidate order, and worker `crux` `astra[low*, medium]`. It contains the AC-4 consultation mapping, the AC-2 acceptance mapping (including the Derived rules), the "not weaker" ordering, the TR-9 assumptions with "next model generation change" as their invalidation trigger, and the adjustment method. No `gpt-5.6-*` model and no Terra appear.
- [x] Thirteen templates exist exactly as EN-1 lists them: name, filename, model, pinned effort present only where listed, sandbox. The eleven 0.2.0 templates are gone.
- [x] Advisor templates answer only the REVIEW packet.
- [x] Explorer and worker templates have no posture section yet, and same-role instructions are byte-identical.
- [x] `retire.txt` lists the eight 0.1.0 and eleven 0.2.0 filenames.
- [x] Installer selectors are the thirteen tier-based short names. The overwrite, retire, check, and refusal behaviour is unchanged.
- [x] `verify.sh` installation group adds these checks:
  - [x] profile-to-template equality for names, models, and pins;
  - [x] a retire list containing the eleven 0.2.0 names.
- [x] Each new check fails when fed a deliberately wrong fixture: record the negative proof, for example a template whose model differs from the profile, or a retire list missing one 0.2.0 name.
- [x] Runtime group cases are driven by the thirteen templates.
- [x] Every template has a parseable Chinese twin with equal configuration keys.
- [x] The `operations.md` sections list the thirteen entries, the selectors, and the invocation examples, with no dial values beyond each entry's own pinned effort.
- [x] **Live route check** (`acceptance.md` §03), in a temporary `CODEX_HOME` with the templates installed through `install-agents.sh --target-dir`. One spawn per entry, passing an effort only for caller-effort entries, and one inspector run per child. The table has: entry, effort passed, observed model, observed effort, sandbox and permission, child thread, inspector exit. Also record that installing over a directory seeded with the eleven 0.2.0 files removes them.

## Verification

- `sh plugins/codex-advisor/scripts/verify.sh` (all groups)
- `python3 tests/test_zh_mirror.py`
- `git diff --check`
- A text search over `plugins/codex-advisor/` (except `agents/retire.txt` and `.codex-plugin/plugin.json`, which ticket 06 owns) and `docs/zh/`, showing no 0.2.0 entry name and no `light`/`standard`/`senior` used as a tier name. README, ADRs, earlier version manuals, and `.scratch/` are outside this stage check; X-5 covers them at final acceptance (D45). Report a hit in a file a later ticket owns; do not fix it here.

## Stop conditions

S1, S2 (if the route check contradicts ticket 01), S8.

## Not in this ticket

The consultation component, hooks, README, `plugin.json`, and the version manual.

## Comments

Resolved on 2026-09-26. The checked items record this ticket's acceptance
checkpoint; later tickets extend the intermediate state where specified.
See `../acceptance.md` section 03 for commands, evidence, authorized
exceptions and the current result. Final delivery review is recorded separately.
