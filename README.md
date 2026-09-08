# Codex Advisor

Codex Advisor is a Codex-only fork of
[Sol Advisor](https://github.com/DannyMac180/sol-advisor).
Your primary model and reasoning effort remain your choice.

Sol, Luna, and other non-Astra primary sessions do their own work and consult an
independent Astra Advisor at consequential decisions and before multi-step delivery.
Astra primary sessions can work solo. Selecting Astra or proposing Architect mode
does not authorize delegation-only work.

This release delivers independent installation, Advisor mode, and explicitly
authorized Astra Architect work with Luna or Astra implementation, explicitly selected
Sol implementation, and independent Astra review when required. A Luna Explorer provides read-only source investigation
for any primary model, with reasoning effort selected by the primary for each call.

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

Request Architect mode in normal conversation, for example:

~~~text
Use $codex-advisor:orchestration in Architect mode for this task.
~~~

The primary session must already use Astra. Authorization covers the task and its
follow-ups; an unrelated task needs new authorization unless you explicitly chose
Architect mode for the whole session. The plugin preserves your primary effort.
The architect specifies work and delegates every implementation edit, including
one-line changes and corrections. Bounded, fully specified work with little
implementation judgment and clear acceptance checks goes to Luna at `max`. Work
requiring substantial judgment, cross-module understanding, or higher risk goes
directly to Astra at `medium`. Sol is available only when you explicitly select it,
defaulting to `high`. Astra and Sol allow explicit supported effort adjustments;
implementation effort does not automatically follow the primary. A Luna attempt is
not required before Astra. The architect inspects all actual changes and reruns key
checks before acceptance. Missing or incorrect routing evidence keeps acceptance pending.

After failed Luna acceptance, the architect diagnoses the cause and chooses
specification clarification, a Luna correction, or Astra reassignment. There is no
fixed retry count or automatic Sol fallback. Specification gaps must be resolved
before dependent implementation.

Independent tasks with disjoint ownership run concurrently within the host's
available capacity. Dependencies, conflicting ownership, and capacity limits cause
sequencing. The architect obtains every worker's report and checks the combined
result; incomplete work remains pending even when another worker succeeds.

High-risk work and explicit review requests receive a fresh Astra Independent
reviewer after the architect's own checks. Ordinary work does not automatically
add this reviewer, including work implemented by Astra. Default review effort is the
higher of `high` and the resolved primary effort; an explicit supported adjustment
must stay at or above the primary.
Missing, conflicting, or unavailable review evidence pauses completion. Reviewers
provide findings; Implementers make corrections and the architect owns acceptance.
Read-only behavior under broader host permissions is reported separately from
enforced isolation.

### Explore with Luna

The installed `codex_advisor_luna_explorer` is available to every primary model,
including all non-Astra models, without loading the skill or entering Architect
mode. Outside the skill, your primary can choose it from available roles. When
`codex-advisor:orchestration` applies and the primary decides to delegate exploration,
it selects the Luna Explorer by default. The skill's trigger scope is unchanged;
installation does not create a global default exploration route.

The Explorer uses `gpt-5.6-luna`. The primary explicitly chooses a supported effort
for every call, with no `max` minimum, and checks actual routing evidence. The
Luna Implementer's `max` requirement is unchanged. The Explorer returns source
references, evidence-based explanations, and gaps without implementing or reviewing
changes. If it is unavailable or findings are insufficient, the primary may
investigate directly; a more expensive delegated substitute requires your explicit
authorization. A requested read-only sandbox is not proof of enforced isolation.

## Check and update

Check without changing installed files:

~~~sh
sh "$plugin_dir/scripts/install-agents.sh" --check
~~~

After updating this checkout, repeat plugin installation and the companion installer,
then start a fresh task. The installer refuses changed role destinations; inspect
and reconcile them explicitly before retrying, including the updated Sol description.
It never deletes another installation.

For selective checks, disposable development installs, runtime evidence, permissions,
and verification, read [native operations](plugins/codex-advisor/skills/orchestration/references/operations.md).
Installation, discovery, and live model routing are separate checks.

## Attribution

The upstream author writes [**Attention Heads**](https://attentionheads.substack.com/?utm_source=github&utm_medium=readme&utm_campaign=sol-advisor)
and the **Agentic Engineering Field Notes** series on AI and agentic engineering.
[Subscribe](https://attentionheads.substack.com/subscribe?utm_source=github&utm_medium=readme&utm_campaign=sol-advisor).
The original MIT attribution remains in [LICENSE](LICENSE).
