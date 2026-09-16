# Version manual

From plugin version `0.1.0` onward, every `plugins/codex-advisor/.codex-plugin/plugin.json` version has a matching `docs/releases/<version>.html`. That page is the version manual: a frozen description of that version, plus the delta from the previous version. Versions before `0.1.0` are not backfilled.

`README.md`, `SKILL.md`, and `docs/zh/` describe current behavior and are overwritten in place. A version manual is not overwritten when a later version ships.

There is no Markdown twin. Do not keep `docs/releases/<version>.md` beside the page.

## When this fires

Write or update a version manual when any of these happens:

- `plugin.json` `version` changes
- a plugin release is prepared
- the user asks for this version's 说明书

## File

Path: `docs/releases/<version>.html`, where `<version>` is the exact `plugin.json` `version` string.

The file is Chinese. It lives under `docs/`, not under `plugins/codex-advisor/` and not under `.scratch/`. It does not ship with the plugin and does not take a `docs/zh/` twin.

The page must contain both of these phrases, character-exact:

```text
本版说明
相对上一版
```

`本版说明` is complete for that version: install, use, roles, modes, recovery, checks, and known limits. A reader who has only this page can operate that version.

`相对上一版` is only the delta from the immediately previous plugin version. For `0.1.0` it states that this is the first frozen manual and names the upstream baseline (Sol Advisor) instead of a previous `codex-advisor` version.

## Checks

`python3 tests/test_version_manual.py` fails when the current `plugin.json` version has no matching HTML file, when either required phrase is missing, or when a Markdown twin exists.

Do not ship or bump `version` while that check fails.
