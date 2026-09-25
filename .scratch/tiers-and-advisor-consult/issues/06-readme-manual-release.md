# 06: README, plugin manifest, 0.3.0 version manual, and release preparation

**What to build:** A user updating from 0.2.0 reads in the README what replaces the eleven old entries and how consultation and hooks work. The plugin reports `0.3.0`. A `0.3.0` version manual describes the whole version and the delta from 0.2.0, in the visual system of the shipped 0.2.0 manual, verified by viewing both pages. The release commands are listed for the user, not run.

**Blocked by:** 02, 03, 04, 05 (the README and the manual describe what each of them delivers; 05 lands last).

**Status:** resolved

## Required reading before starting

- `spec.md`: DR-8 to DR-11, AC-12, X-1, X-5, §Authority and conflicts (text versus baseline), §Visual Acceptance, §Stop and Return (S7), §Goal-Drift Checks (version manual item).
- `docs/agents/version-manual.md` (the required phrases, what `本版说明` must cover, no Markdown twin).
- The visual baseline, `docs/releases/0.2.0.html`. Open it in a browser and read its source before writing. Commit `f812f9b`, SHA-256 `d89f0f18ccfc0cb42156a5548bc531527372603ea12efb13d759e86589b6d4ea`; confirm the hash before starting and record it.
- Not a baseline: `.scratch/manual-redesign/0.2.0-magazine.html`.
- `README.md` (current), `plugins/codex-advisor/.codex-plugin/plugin.json`, `docs/adr/0006-*.md` (for the `相对上一版` references), `acceptance.md` §01 to §05 (known limits and what the live checks established).
- `.scratch/tier-role-pool/issues/07-readme-manual-release.md` §Release commands (the command shape to update).

## Owns

- `README.md`
- `plugins/codex-advisor/.codex-plugin/plugin.json`: `version`, `description`, `interface.shortDescription`, `interface.longDescription`, `keywords`
- `docs/releases/0.3.0.html` (new)
- `.scratch/tiers-and-advisor-consult/visual/` (screenshots)
- `acceptance.md` §06

## Acceptance

- [x] README covers:
  - [x] install, including the `/hooks` review of the plugin's hooks, and that untrusted hooks are skipped with a startup warning (AC-12);
  - [x] use;
  - [x] the thirteen entries by role and tier, without dial values, pointing to the routing profile;
  - [x] admission and escalation;
  - [x] consultation and posture;
  - [x] hooks;
  - [x] acceptance;
  - [x] check and update, including a new `/hooks` review after any update that changes a hook;
  - [x] an upgrade section that names the eleven retired 0.2.0 entries and their replacements.
- [x] `plugin.json` `version` is `0.3.0`. The descriptions and keywords describe the new tiers, consultation, and hooks, with no model names. The marketplace manifest is unchanged.
- [x] `docs/releases/0.3.0.html` is Chinese and self-contained, and contains `本版说明` and `相对上一版` character-exact.
  - [x] `本版说明` covers everything DR-10 lists and freezes the routing-profile table for 0.3.0.
  - [x] `相对上一版` lists every change from 0.2.0 with its reason and an ADR-0006 reference, including the eleven retired names.
- [x] **Visual.** Render scenes V1 to V5 for the baseline and for 0.3.0 with identical settings. Save them as `visual/<scene>-baseline.png` and `visual/<scene>-0.3.0.png`, open and look at every pair, and record per-scene observations with pass or fail in `acceptance.md` §06. Each scene passes the "must match" list in spec §Visual Acceptance, and every difference falls in the allowed list. The baseline file's SHA-256 is unchanged at the end.
- [x] **X-5 text check.** No 0.2.0 entry name, no light/standard/senior used as tiers, and no "first-round pool", "senior gate", or "decision packet" appears outside the allowed places. Record the command and its output.
- [x] Release commands are listed in `acceptance.md` §06, updated from the 0.2.0 shape for 0.3.0: push to `origin`, then on WSL and Windows run the marketplace upgrade, the plugin remove and add, the installer, the installer check, and the `/hooks` review in a fresh interactive session (AC-12). They are marked user-gated and not run.

## Verification

- `python3 tests/test_version_manual.py` (for `0.3.0`)
- `python3 tests/test_zh_mirror.py`
- `sh plugins/codex-advisor/scripts/verify.sh`
- `git diff --check`
- `sha256sum docs/releases/0.2.0.html`
- The visual table in `acceptance.md` §06

Functional checks do not substitute for the visual comparison.

## Stop conditions

S7 (content that the baseline's components cannot express) and S8. X-1: no push, upgrade, reinstall, or real-home installer run without the user's explicit authorization.

## Not in this ticket

The final acceptance sweep (spec §Requirement Ownership, after this ticket).

## Comments

Resolved on 2026-09-26 after primary verification and fresh independent senior
acceptance. See `../acceptance.md` section 06 and Final acceptance for
evidence and limitations. D47 cancels finish blocking, D48 permits only a local
commit, and D49 waives only repetition of the final-definition manual trust test.
No push or real installation update was performed.
