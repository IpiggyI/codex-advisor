# 05: Worker tier entries

**What to build:** A primary can install and spawn `ca_worker_light`, `ca_worker_standard_m`, `ca_worker_standard_h`, and `ca_worker_senior`, each pinned to its model, with effort pinned where the tier allows one. The three old worker entries are retired and the word Implementer leaves the plugin and the mirror.

**Blocked by:** 04 (shared retire list, verifier data, and mirror directory).

**Status:** resolved

- [x] Four templates `ca-worker-light` (Luna, pins `max`), `ca-worker-standard-m` (Sol, caller effort), `ca-worker-standard-h` (Astra, pins `low`), `ca-worker-senior` (Astra, caller effort); no `sandbox_mode` key.
- [x] `description` names role, tier, model, and fixed or caller effort; `developer_instructions` per R05 with the return shape COMPLETION / CHANGES / VERIFICATION / JUDGMENT CALLS / GAPS, the you-are-not-alone preservation rule, no further delegation, fresh thread on effort or model change, no inference of settings; four bodies byte-identical.
- [x] The three old templates (`codex-advisor-luna-implementer`, `codex-advisor-sol-implementer`, `codex-advisor-astra-implementer`) are deleted and their filenames added to the retire list.
- [x] Four Chinese TOML twins with equal configuration keys and Chinese prose keys.
- [x] Implementer and implementer no longer appear anywhere under the plugin directory or the mirror except inside the installer's retire list. README is left to ticket 07.
- [x] Installing into a temporary target that holds the eight old files leaves eight new files (four Explorer, four worker) installed, six old files removed, and the two old Advisor and reviewer files untouched.
- [x] Both verifier groups, the mirror test, and the manual test pass.

## Acceptance

Accepted 2026-09-17 by the primary. Lane: `generalPurpose` pinned `cursor-grok-4.6-xhigh` (requested, not confirmed). Tier 1: full `verify.sh` and `tests/test_zh_mirror.py` (20/20) rerun by the primary; agents directory holds eight `ca-*` templates, the two old Advisor/reviewer templates, and `retire.txt` with six names. Tier 2: the primary read `ca-worker-standard-m.toml` and its twin header — no `sandbox_mode`, caller-selected effort, instructions carry the five-part packet vocabulary and the five-part RETURN with no caller duties; `rg -i implementer` matches only `retire.txt`.
