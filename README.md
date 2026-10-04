# Codex Advisor

Codex Advisor is a Codex-only fork of
[Sol Advisor](https://github.com/DannyMac180/sol-advisor).
Any primary can implement directly, delegate work, or combine both.
Your primary model and reasoning effort remain your choice.

Version 0.3.2 supplies seventeen native entries across `mainstay`, `crux`, and
`rescue`, a single routing profile, zero-argument process consultation, and
hooks for posture injection and automatic dispatch verification.
See the [Chinese version manual](docs/releases/0.3.2.html) for a complete guide.

## Install

Use Codex with plugins, native custom agents, MCP, and hooks; Python 3.11 or
later; a POSIX shell; and `jq`. On Windows, the hooks and the MCP server start
through `sh`, so Git for Windows' `bin` directory, for example
`C:\Program Files\Git\bin`, must be on PATH; see
[Windows launch](docs/agents/plugin-maintenance.md#windows-launch). Consultation
on Windows also needs the native `codex.exe`; see
[plugin maintenance](docs/agents/plugin-maintenance.md#process-consultation-component).
The consultation protocol is qualified on Codex 0.160.0; hook metadata is qualified
on Codex 0.157.0. Host
schema or cache-layout changes need renewed qualification rather than an assumed
compatibility guarantee.

For a provider configured with `env_key = "S2A_API_KEY"`, start Codex with that
variable available. The plugin explicitly forwards it to the consultation MCP
process. Other credential environment names need their own `env_vars` declaration
in the plugin source and an update; ordinary MCP startup does not inherit them.
See [authentication and diagnostics](docs/agents/plugin-maintenance.md#process-consultation-component).

~~~sh
codex plugin marketplace add https://github.com/IpiggyI/codex-advisor.git
codex plugin add codex-advisor@codex-advisor
plugin_dir="$(codex plugin list --json | jq -r '.installed[] | select(.pluginId == "codex-advisor@codex-advisor") | .source.path')"
test -n "$plugin_dir" && test "$plugin_dir" != null && test -d "$plugin_dir" && test -f "$plugin_dir/scripts/install-agents.sh" && sh "$plugin_dir/scripts/install-agents.sh"
sh "$plugin_dir/scripts/install-agents.sh" --check
~~~

The companion installer writes seventeen entries under `$CODEX_HOME/agents`, or
`~/.codex/agents` when unset. It overwrites this plugin's differing files and
deletes nothing. It leaves unrelated agents and primary configuration alone.
Installed entries are not hand-edited.

Start a fresh interactive task and review the plugin's two hooks in `/hooks`.
Installing or enabling a plugin does not trust hooks. Until you trust them, the
host skips them and shows a startup warning. Confirm that the task exposes
`codex-advisor:orchestration`, the native entries, and the `codex_advisor` MCP
server's `process_consultation` tool. These are separate discovery checks.

For development, substitute the checkout's absolute path for the marketplace
URL and use a temporary `CODEX_HOME`; do not point the real installation at
unreleased working-tree changes.

## Use

~~~text
Use $codex-advisor:orchestration to implement and verify this feature.
~~~

The primary owns goals, decomposition, scheduling, and acceptance within your
scope, reserved decisions, and resource limits. Workers receive an objective,
ownership, retained interfaces, constraints, and meaningful verification. They
own implementation and local debugging, preserve concurrent edits, and do not
further delegate implementation. Explorers return read-only evidence and gaps.

| Role | `mainstay` | `crux` | `rescue` |
|---|---|---|---|
| Explorer | `ca_explorer_mainstay_m` / `ca_explorer_mainstay_h` | `ca_explorer_crux_m` / `ca_explorer_crux_h` | `ca_explorer_rescue` |
| Worker | `ca_worker_mainstay_m` / `ca_worker_mainstay_h` | `ca_worker_crux_m` / `ca_worker_crux_h` | `ca_worker_rescue_m` / `ca_worker_rescue_h` |
| Advisor | `ca_advisor_mainstay_m` / `ca_advisor_mainstay_h` | `ca_advisor_crux_m` / `ca_advisor_crux_h` | `ca_advisor_rescue_m` / `ca_advisor_rescue_h` |

Model segments, models, allowed efforts, defaults, and candidate order live only in the
[routing profile](plugins/codex-advisor/skills/orchestration/references/routing-profile.md).
Model segments run from `starter` through `midrange` and `premium` to `flagship`;
they rank models independently of the three task tiers.
Each entry pins its model. A single-effort entry pins effort; otherwise the
caller must pass `reasoning_effort`. Use a fresh thread with `fork_turns: none`.

Request delegation-only implementation explicitly:

~~~text
Use $codex-advisor:orchestration in Architect mode for this task.
~~~

Architect mode covers the authorized task and follow-ups. Every implementation
edit and correction is delegated; the primary retains design, scheduling, and
acceptance. A ticket, selected model, or unaccepted proposal does not activate it.

## Admission and recovery

Work normally starts in `mainstay`. It may start in `crux` when a key difficulty
is identified or interacting constraints need joint handling. `rescue` requires
a capability failure in `crux` or your explicit declaration. See
[allocation](plugins/codex-advisor/skills/orchestration/SKILL.md#allocate-by-role-and-capability-tier).

After failed acceptance, the primary issues rework in the same thread at the
same dial. Only a capability failure moves work along the path `mainstay` to
`crux` to `rescue` to the user; environment problems and contract gaps do not.
[Recovery](plugins/codex-advisor/skills/orchestration/references/recovery.md#climb-the-escalation-ladder)
holds the counting rules, the ladder, and the handoff.

## Process consultation and posture

Call `process_consultation` with `{}`. The primary, workers, and explorers use
the same interface. It reconstructs the caller's effective context from the host
record, and a fresh advisor without tools returns a `plan`, `correction`, or
`stop`. A failed consultation returns an explicit failure, never fabricated
advice, and the work stays pending. See
[consultation](plugins/codex-advisor/skills/orchestration/SKILL.md#consult-at-decision-points).

Exact caller/advisor model identity selects the full or reduced posture. The
posture says when to consult; the adoption rules say how to adopt, deviate from,
or reject advice. Advice grants no authorization. See the
[canonical posture](plugins/codex-advisor/skills/orchestration/references/consult-posture.md).

## Hooks and acceptance

`SessionStart` injects the primary's selected posture and adoption rules, also
on resume. Delegates carry their posture in their entry instructions. On a
matching `ca_*` dispatch, `PostToolUse` adds one confirmation line:

~~~text
Codex Advisor: {role} identity, model, and effort match the host record at {model}[{effort}]; working directory and permissions were not checked.
~~~

Missing caller effort, a mismatch, or missing evidence leaves work pending and
informs the spawning session. For a `ca_*` dispatch, no message means the hook
did not run, for example because it is untrusted in `/hooks`, so the dispatch is
unchecked. The inspector remains the check for working directory and observed
permissions. No primary or worker finish hook blocks completion, and these hooks
keep no state. See the
[dispatch check](plugins/codex-advisor/skills/orchestration/references/operations.md#read-the-dispatch-check).

Independent acceptance remains separate from consultation. After primary checks,
high-risk work or an explicit review request requires a packet-based read-only
review in a fresh Advisor thread. The
[acceptance mapping](plugins/codex-advisor/skills/orchestration/references/routing-profile.md#acceptance-mapping)
selects the Advisor; see
[independent acceptance](plugins/codex-advisor/skills/orchestration/references/independent-acceptance.md).

The primary inspects all changes and owns verification, whether it executes
checks or assigns a checker. Read-only role instructions do not prove enforced
isolation; the host may apply broader permissions. See
[acceptance](plugins/codex-advisor/skills/orchestration/SKILL.md#accept-the-actual-deliverable).

## Check and update

After the release is pushed, run on each installation:

~~~sh
codex plugin marketplace upgrade codex-advisor
codex plugin remove codex-advisor@codex-advisor
codex plugin add codex-advisor@codex-advisor
plugin_dir="$(codex plugin list --json | jq -r '.installed[] | select(.pluginId == "codex-advisor@codex-advisor") | .source.path')"
sh "$plugin_dir/scripts/install-agents.sh"
sh "$plugin_dir/scripts/install-agents.sh" --check
~~~

Open a fresh interactive task and review `/hooks` again when hook definitions
change. Trust belongs to the current hook hash; an update cannot grant it.
WSL and Windows are separate installations. Use the matching native Codex and
home for each; Windows shell examples require Git Bash and its dependencies.

`--check` reports differing or missing templates without writing. For a
targeted metadata investigation:

~~~sh
sh "$plugin_dir/scripts/inspect-agent-runtime.sh" --agent ca_worker_mainstay_m <thread-id>
~~~

Caller-effort entries also require `--effort <the effort you passed>`.
[Native operations](plugins/codex-advisor/skills/orchestration/references/operations.md#validate-routing-evidence)
says when to run the inspector. Maintainers find verification groups, live route
checks, native scenarios, and installer and hook internals in
[plugin maintenance](docs/agents/plugin-maintenance.md). Route checks establish
observed dispatch, not quality, cost, or stability.

## Attribution

The upstream author writes [**Attention Heads**](https://attentionheads.substack.com/?utm_source=github&utm_medium=readme&utm_campaign=sol-advisor)
and the **Agentic Engineering Field Notes** series on AI and agentic engineering.
[Subscribe](https://attentionheads.substack.com/subscribe?utm_source=github&utm_medium=readme&utm_campaign=sol-advisor).
The original MIT attribution remains in [LICENSE](LICENSE).
