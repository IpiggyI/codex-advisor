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
