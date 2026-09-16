# 07: README, audit checklist, 0.2.0 version manual, and version bump

**What to build:** A user updating from 0.1.0 reads in the README why the eight old entry names fail and what replaces them, installs and checks with the new installer, and finds a 0.2.0 version manual that describes the whole version and the delta from 0.1.0. The plugin reports version 0.2.0 and every check passes.

**Blocked by:** 06.

**Status:** resolved

- [x] README rewritten: install from checkout, use, the eleven entries by role and tier with no dial values (pointing at the routing profile), Architect mode unchanged, recover and advice sections consistent with the ladder and gate, check and update with the overwrite and retire semantics, and an upgrade section that names the eight retired entries and their replacements.
- [x] README uses Worker, never Implementer; no retired entry name appears outside the upgrade section.
- [x] `docs/releases/0.2.0.html`: self-contained Chinese HTML in the style of the 0.1.0 manual, containing `本版说明` (install, use, entries and tiers, routing profile table frozen for 0.2.0, pool, gate, ladder, Advisor shapes, installer and inspector usage, checks, known limits) and `相对上一版` (each change from 0.1.0 with its reason and ADR-0004 reference).
- [x] Plugin manifest version `0.2.0`; `description`, `shortDescription`, `longDescription`, and `keywords` describe tier-named entries and the routing profile without model-named entries. The marketplace manifest has no version field and is unchanged.
- [x] The audit checklist records decisions: R01 update (LF attributes, ticket 01), R02 update (twin corrected, ticket 03), R05 simplify (tickets 04 to 06), R08 update (dial notation in the routing profile). Others stay pending.
- [x] Text check: no occurrence of `Implementer`, `implementer`, or any retired entry name under the plugin directory, the mirror, or README, except the retire list and the README upgrade section.
- [x] Full verification passes: both verifier groups, the mirror test, the manual test, `git diff --check`.
- [x] Push to `origin`, `codex plugin marketplace upgrade`, plugin reinstall on both sides, and running the installer on both sides are user-gated steps; the ticket lists the commands and does not run them.

## Acceptance

Accepted 2026-09-17 by the primary. Lane: `generalPurpose` pinned `cursor-grok-4.6-xhigh` (requested, not confirmed). Tier 1: `verify.sh`, `tests/test_zh_mirror.py` (26/26), `tests/test_version_manual.py` (3/3 for 0.2.0), `git diff --check` rerun by the primary; `plugin.json` reports 0.2.0 with no model name in its descriptions or keywords. Tier 2: the primary read the README in full (160 lines; entry table without dial values, R1–R4, senior gate, Advisor packets, upgrade table with the eight retired names) and the manual's section headings (`本版说明` at the part label, `相对上一版` as a heading, 495 lines). Audit-checklist decisions R01/R02/R05/R08 were recorded by the primary. Release steps (push, marketplace upgrade, reinstall, installer on both sides) remain user-gated and were not run.

## Release commands (user-gated; not run by the primary)

From this checkout, after the 0.2.0 commit exists:

```sh
git push origin main
```

Then on each side (WSL, and Windows from a Windows drive via `cmd.exe`):

```sh
codex plugin marketplace upgrade codex-advisor
codex plugin remove codex-advisor@codex-advisor
codex plugin add codex-advisor@codex-advisor
plugin_dir="$(codex plugin list --json | jq -r '.installed[] | select(.pluginId == "codex-advisor@codex-advisor") | .source.path')"
sh "$plugin_dir/scripts/install-agents.sh"
sh "$plugin_dir/scripts/install-agents.sh" --check
```

Start a fresh Codex task afterwards; the eleven `ca_*` entries replace the eight 0.1.0 names, which the installer deletes.
