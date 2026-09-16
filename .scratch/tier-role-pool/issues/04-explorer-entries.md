# 04: Explorer tier entries

**What to build:** A primary can install and spawn `ca_explorer_light`, `ca_explorer_standard_m`, `ca_explorer_standard_h`, and `ca_explorer_senior`, each pinned to its model, verify the call with the generic inspector, and read a Chinese twin of each template. The three old Explorer entries are retired by the installer.

**Blocked by:** 01, 02, 03.

**Status:** resolved

- [x] Four templates `ca-explorer-light`, `ca-explorer-standard-m`, `ca-explorer-standard-h`, `ca-explorer-senior` with `name` fields `ca_explorer_light`, `ca_explorer_standard_m`, `ca_explorer_standard_h`, `ca_explorer_senior`; models Luna, Luna, Terra, Sol; `sandbox_mode = "read-only"`; only `ca-explorer-standard-m` pins `model_reasoning_effort = "max"`.
- [x] Each `description` names role, tier, model, and either the fixed effort or that the caller passes it; it lists no allowed efforts.
- [x] `developer_instructions` follow audit finding R05: permissions, expected packet, return shape (FINDINGS / EXPLANATION / GAPS), fresh-thread and no-delegation rules, no inference of runtime settings; no caller duties. The four bodies are byte-identical.
- [x] The three old Explorer templates (`codex-advisor-luna-explorer`, `codex-advisor-sol-explorer`, `codex-advisor-astra-explorer`) are deleted from the shipped templates and their filenames added to the installer's retire list. The plugin prefix variable becomes `ca-`; the verifier's prefix assertions become `ca-` and `ca_`.
- [x] Four Chinese twins as parseable TOML under the mirror's `agents/` directory with the same filenames; `name`, `model`, `model_reasoning_effort` (presence and value), and `sandbox_mode` equal the template; `description` and `developer_instructions` are Chinese.
- [x] The mirror test covers TOML files: existence both ways for `.md` and `.toml`, and for each TOML twin key equality of the four configuration keys plus Chinese text in the two prose keys. A twin whose `model` differs fails the test.
- [x] The verifier's static checks gain: all templates of one role (by the second name segment) carry byte-identical `developer_instructions`; a template pins `model_reasoning_effort` exactly when it is in the set the routing profile marks as single-effort.
- [x] Installing into a temporary target that holds the eight old files leaves the four new Explorer files installed, the three old Explorer files removed, and the five other old files untouched (they retire in tickets 05 and 06).
- [x] Both verifier groups, the mirror test, and the manual test pass. The runtime group now covers the four new templates automatically.
- [x] A live route check is not part of this ticket's verification; the primary runs one pass over all eleven entries after ticket 06 and records it in the feature's acceptance record.

## Acceptance

Accepted 2026-09-16 by the primary. Lane: `generalPurpose` pinned `cursor-grok-4.6-xhigh` (requested, not confirmed). Tier 1: full `verify.sh` and `tests/test_zh_mirror.py` (12/12) rerun by the primary; the agents directory holds the four `ca-explorer-*` templates, the five remaining old templates, and `retire.txt` with the three old Explorer names. Tier 2: the primary read `ca-explorer-light.toml` and `ca-explorer-standard-m.toml` with their twins — headers as specified, the pinned entry's comment says the effort is pinned, instructions are 12 lines with no caller duties, twins keep identifiers and RETURN labels character-exact. Carried-over ticket 02 diagnostic fixed. `AGENTS.md` / `CLAUDE.md` mirror rule updated by the primary to cover TOML twins.
