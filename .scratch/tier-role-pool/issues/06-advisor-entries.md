# 06: Advisor tier entries with both request shapes

**What to build:** A primary can install and spawn `ca_advisor_light`, `ca_advisor_standard`, and `ca_advisor_senior` for either a decision packet or an acceptance packet, verify the call with the inspector, and no longer finds a reviewer entry. The routing profile and the shipped templates are now mechanically checked against each other.

**Blocked by:** 05.

**Status:** resolved

- [x] Three templates `ca-advisor-light` (Astra, pins `low`), `ca-advisor-standard` (Astra, pins `medium`), `ca-advisor-senior` (Astra, caller effort); `sandbox_mode = "read-only"`.
- [x] `developer_instructions` per R05 carry both return shapes: RECOMMENDATION / EVIDENCE / ASSUMPTIONS / TRADEOFFS / GAPS for a decision packet and READINESS / FINDINGS / VERIFICATION / GAPS for an acceptance packet, chosen by the packet received; read-only; a fresh thread per request; no inference of settings. Three bodies byte-identical.
- [x] The old `codex-advisor-astra-advisor` and `codex-advisor-astra-reviewer` templates are deleted and their filenames added to the retire list; the retire list now holds exactly the eight 0.1.0 filenames.
- [x] Three Chinese TOML twins with equal configuration keys and Chinese prose keys.
- [x] The verifier's static checks gain: every entry name in the routing profile's table has a shipped template with that `name`, every shipped template is named in the table, and each pair agrees on `model`.
- [x] Installing into a temporary target that holds the eight old files leaves exactly the eleven new files plus any unrelated files, and `--check` on that target passes.
- [x] No template, reference, or twin names a reviewer entry.
- [x] Both verifier groups, the mirror test, and the manual test pass.

## Acceptance

Accepted 2026-09-17 by the primary. Lane: `generalPurpose` pinned `cursor-grok-4.6-xhigh` (requested, not confirmed). Tier 1: full `verify.sh`, `tests/test_zh_mirror.py` (26/26), `tests/test_version_manual.py` rerun by the primary; agents directory holds exactly the eleven `ca-*` templates and `retire.txt` with the eight 0.1.0 names. Tier 2: the primary read `ca-advisor-light.toml` — pinned `low`, read-only, instructions carry both packet shapes with their RETURN blocks and no caller duties. Negative proof recorded by the lane: a wrong `model` in one template fails the profile-to-template check naming the entry. The lane's GAP on `rg reviewer` is accepted as-is: the surviving hits are the retired option name `--reviewer-effort` (which the inspector must keep rejecting), the sentence "no separate reviewer entry exists", and prose about a fresh review; none names a reviewer entry.
