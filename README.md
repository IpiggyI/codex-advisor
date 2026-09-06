# Codex Advisor

Codex Advisor is a Codex-only fork of
[Sol Advisor](https://github.com/DannyMac180/sol-advisor).
Your primary model and reasoning effort remain your choice.

Sol, Luna, and other non-Astra primary sessions do their own work and consult an
independent Astra Advisor at consequential decisions and before multi-step delivery.
Astra primary sessions can work solo. Selecting Astra or proposing Architect mode
does not authorize delegation-only work.

This release delivers independent installation and Advisor mode. Architect-mode
implementation and independent final review are planned in later tickets.

## Install from this checkout

Use a current Codex host with plugins and native custom agents, plus `jq`.
Use your actual checkout path:

~~~sh
codex plugin marketplace add /absolute/path/to/codex-advisor
codex plugin add codex-advisor@codex-advisor
plugin_dir="$(codex plugin list --json | jq -r '.installed[] | select(.pluginId == "codex-advisor@codex-advisor") | .source.path')"
test -n "$plugin_dir" && test "$plugin_dir" != null && test -d "$plugin_dir" && test -f "$plugin_dir/scripts/install-agents.sh" && sh "$plugin_dir/scripts/install-agents.sh"
~~~

The companion installer adds the fork's native roles under `$CODEX_HOME/agents`,
or `~/.codex/agents` when `CODEX_HOME` is unset. It preserves existing Sol Advisor
files, unrelated agents, and primary-session configuration. Modified or unsafe
destinations are refused. Repeating installation leaves exact files unchanged.

Start a fresh Codex task after installation. Confirm that it exposes
`codex-advisor:orchestration` and the native roles listed by the installer.
A listed plugin alone does not establish native-agent discovery.

## Use

~~~text
Use $codex-advisor:orchestration to implement and verify this feature.
~~~

In Advisor mode, the primary agent consults Astra before architecture decisions,
data migrations, API designs, and refactors touching at least three files; after
two distinct unsuccessful attempts at the same problem; and before declaring a
multi-step deliverable complete. It explains its decision and any disagreement
with the Advisor. Existing user authorization and project approval gates apply.

Astra consultation defaults to `high`. You can request another supported effort
in normal conversation. The workflow checks the actual model and effort; an
unavailable Astra or missing or conflicting evidence pauses the affected step.
Consultation does not establish independent final review of the actual changes.

## Check and update

Check without changing installed files:

~~~sh
sh "$plugin_dir/scripts/install-agents.sh" --check
~~~

After updating this checkout, repeat plugin installation and the companion installer,
then start a fresh task. The installer refuses changed role destinations; inspect
and reconcile them explicitly before retrying. It never deletes another installation.

For selective checks, disposable development installs, runtime evidence, permissions,
and verification, read [native operations](plugins/codex-advisor/skills/orchestration/references/operations.md).
Installation, discovery, and live model routing are separate checks.

## Attribution

The upstream author writes [**Attention Heads**](https://attentionheads.substack.com/?utm_source=github&utm_medium=readme&utm_campaign=sol-advisor)
and the **Agentic Engineering Field Notes** series on AI and agentic engineering.
[Subscribe](https://attentionheads.substack.com/subscribe?utm_source=github&utm_medium=readme&utm_campaign=sol-advisor).
The original MIT attribution remains in [LICENSE](LICENSE).
