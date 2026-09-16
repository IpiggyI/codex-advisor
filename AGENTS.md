## Agent skills

### Issue tracker

Issues live as markdown files under `.scratch/<feature>/`. See `docs/agents/issue-tracker.md`.

### Triage labels

Canonical roles map 1:1 to `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `CONTEXT.md` plus `docs/adr/` at the repo root. See `docs/agents/domain.md`.

### Chinese mirror of runtime docs

Every `plugins/codex-advisor/**/*.md` has a Chinese twin at the same relative path under `docs/zh/` (`docs/zh/skills/orchestration/…`). A change to a runtime `.md` updates its twin in the same commit. `python3 tests/test_zh_mirror.py` checks the one-to-one existence (not content). The mirror is repo-only and does not ship.

### Version manual

From plugin version `0.1.0` onward, each `plugin.json` version has `docs/releases/<version>.html`: that version's description plus the delta from the previous version. See `docs/agents/version-manual.md`.

### Plugin release & local update

Installed marketplaces on WSL and Windows point at GitHub (`IpiggyI/codex-advisor`), not this working tree. Push to `origin` first, then on each side: `codex plugin marketplace upgrade codex-advisor`, reinstall `codex-advisor@codex-advisor`, and run the companion installer. An unpushed commit never reaches the plugin.
