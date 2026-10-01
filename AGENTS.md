## Agent skills

### Issue tracker

Issues live as markdown files under `.scratch/<feature>/`. See `docs/agents/issue-tracker.md`.

### Triage labels

Canonical roles map 1:1 to `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `CONTEXT.md` plus `docs/adr/` at the repo root. See `docs/agents/domain.md`.

### Chinese mirror of runtime docs

Every `plugins/codex-advisor/**/*.md` and every native entry `plugins/codex-advisor/agents/*.toml` has a Chinese twin at the same relative path under `docs/zh/` (`docs/zh/skills/orchestration/…`, `docs/zh/agents/…`). A change to a runtime file updates its twin in the same commit. `python3 tests/test_zh_mirror.py` checks the one-to-one existence for both types and, for a TOML twin, that `name`, `model`, `model_reasoning_effort`, and `sandbox_mode` equal the template while the two prose keys are Chinese. The mirror is repo-only and does not ship.

### Version manual

From plugin version `0.1.0` onward, each `plugin.json` version has `docs/releases/<version>.html`: that version's description plus the delta from the previous version. See `docs/agents/version-manual.md`.

### Plugin maintenance

`plugins/codex-advisor/` holds only what runtime callers and delegates read. The procedure for changing the plugin lives in `docs/agents/plugin-maintenance.md`.

### Plugin release & local update

Installed marketplaces on WSL and Windows point at GitHub (`IpiggyI/codex-advisor`), not this working tree. Push to `origin` first, then on each side: `codex plugin marketplace upgrade codex-advisor`, reinstall `codex-advisor@codex-advisor`, and run the companion installer; then ask the user to review `/hooks` in a fresh task on each side when a hook definition is new or changed. An unpushed commit never reaches the plugin.

### Wording of shipped text

Text that ships under `plugins/codex-advisor/**`, together with its `docs/zh/**` twins, states settled results: the rules and facts its reader acts on. This covers prose, skill and entry descriptions, manifest and hook descriptions, code comments and user-facing messages. Write "The models show no clear difference in speed.", not a remark on what the text lists. A "because" clause that explains why a rule holds stays. How the text came to be goes to a coordination artifact:
- what the text lists or omits, why a file exists, and which rule replaced which → an ADR;
- retired names → `_Avoid_` in `CONTEXT.md`;
- dated observations and unverified status → the issue file or ADR.

`python3 tests/test_shipped_wording.py` fails on known phrasings of this kind; a pass does not prove the rule as a whole.

### Canonical notation for the user's declarations

The user often declares models and dials in loose notation: `6-sol`, `sol`, `GPT-6.1 Sol`, `astra[low, medium]`, `[low* medium]`. Every artifact writes them in canonical form, with no note on the original spelling:
- models as the full id an entry template's `model` carries (`gpt-6-luna`, `gpt-6.1-sol`, `gpt-6-astra`);
- dials as `model[a*, b]` (the routing profile's notation line); a multi-effort dial without `*` gets it on the first listed effort.

Verbatim quotes of the user in specs and discussion records stay as written. Ask only when a loose name fits more than one model.

The same test checks shipped text and `README.md`: the routing profile's anchor list equals the template models in both twins, every dial uses a template model and canonical brackets, and no known loose model name appears.
