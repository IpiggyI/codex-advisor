# Codex Advisor

Codex Advisor is a Codex-only fork of
[Sol Advisor](https://github.com/DannyMac180/sol-advisor).
Any primary can implement directly, delegate work, or combine both.
Your primary model and reasoning effort remain your choice.

Version 0.3.0 supplies thirteen native entries across `mainstay`, `crux`, and
`rescue`, a single routing profile, zero-argument process consultation, and
hooks for posture injection and automatic dispatch verification.
See the [Chinese version manual](docs/releases/0.3.0.html) for a complete guide.

## Install

Use Codex with plugins, native custom agents, MCP, and hooks; Python 3.11 or
later; a POSIX shell; and `jq`. The consultation protocol and hook metadata are
qualified on Codex 0.157.0. Host schema or cache-layout changes need renewed
qualification rather than an assumed compatibility guarantee.

~~~sh
codex plugin marketplace add https://github.com/IpiggyI/codex-advisor.git
codex plugin add codex-advisor@codex-advisor
plugin_dir="$(codex plugin list --json | jq -r '.installed[] | select(.pluginId == "codex-advisor@codex-advisor") | .source.path')"
test -n "$plugin_dir" && test "$plugin_dir" != null && test -d "$plugin_dir" && test -f "$plugin_dir/scripts/install-agents.sh" && sh "$plugin_dir/scripts/install-agents.sh"
sh "$plugin_dir/scripts/install-agents.sh" --check
~~~

The companion installer writes thirteen entries under `$CODEX_HOME/agents`, or
`~/.codex/agents` when unset. It overwrites this plugin's differing files and
removes nineteen retired filenames from 0.1.0 and 0.2.0. It leaves unrelated
agents and primary configuration alone. Installed entries are not hand-edited.

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
| Worker | `ca_worker_mainstay_m` / `ca_worker_mainstay_h` | `ca_worker_crux_m` / `ca_worker_crux_h` | `ca_worker_rescue` |
| Advisor | `ca_advisor_mainstay` | `ca_advisor_crux` | `ca_advisor_rescue` |

Models, allowed efforts, defaults, and candidate order live only in the
[routing profile](plugins/codex-advisor/skills/orchestration/references/routing-profile.md).
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
is identified or interacting constraints need joint handling. The narrower
alternative admission rule is recorded but disabled. `rescue` requires a
capability failure in `crux` or your explicit declaration.

After failed acceptance, issue same-thread, same-dial rework that states the
violated requirement, reproduction, expected behavior, and verification. A
complete attempt plus failed rework counts as one capability failure only when
the cause is capability. Environment problems, missing facts, contract gaps,
and intermediate test failures do not advance the ladder.

The path is `mainstay` to `crux` to `rescue` to the user. Do not switch models
inside a failed tier or lower the model level unless no other choice exists.
If the model stays the same, raise effort; one model can be raised at most once.
A major execution problem may skip rework and count as one capability failure.
Every model, effort, or role change starts a fresh matching thread.

## Process consultation and posture

Call `process_consultation` with `{}`. The primary, workers, and explorers use
the same interface. It reconstructs the caller's full effective context,
including the unfinished turn, from the host record. Compaction replaces old
history with its replacement history; no caller summary or recent-turn window
is substituted. A fresh native advisor has no tools and returns a `plan`,
`correction`, or `stop`, with validated actual model and effort. Unsupported
context or execution failure returns explicit failure, never fabricated advice.

Exact caller/advisor model identity selects the canonical posture. Different
models use the full posture: consult before substantive work, when stuck,
before changing approach, and before declaring done; reconcile conflicting
evidence and advice. Same-model callers use the reduced posture: on a multi-step
task, consult before committing to an approach and before declaring done.
Save deliverables before the final consultation. Restate the key guidance in
the next visible reply before continuing. See the
[canonical posture](plugins/codex-advisor/skills/orchestration/references/consult-posture.md)
for all conditions and short-task exceptions.

Adopt advice by default. Explain deviations supported by failed execution or
primary-source evidence. Reject conflicts with user constraints or authorization
directly. Before rejecting a different-model advisor for a reasoning flaw, make
one reconciliation call; same-model callers may reject with a stated reason.
Advice grants no authorization, veto, or new requirement. Only successful
consultation counts; failure leaves work pending until success or user release.

## Hooks and acceptance

`SessionStart` injects the primary's selected posture and adoption rules, also
on resume. Delegates carry their posture in their entry instructions.
`PostToolUse` automatically checks each native dispatch against its template and
explicit caller effort. Matching dispatches are silent; mismatches or missing
proof leave work pending and inform the spawning session. A manual inspector
is not needed for that comparison. No primary or worker finish hook blocks
completion, and these hooks keep no state or observation log.

Independent acceptance remains separate from consultation. After primary checks,
high-risk work or an explicit review request requires a packet-based read-only
review in a fresh Advisor thread. Work from one tier uses that tier's Advisor;
mixed-tier work uses the highest tier involved. Primary-authored work uses the
lowest Advisor dial not weaker than the primary, or the strongest if none
qualifies or the exact primary model is unknown. Low confidence remains pending
and goes to the user; it does not trigger an automatic review at another dial.

The primary inspects all changes and owns verification, whether it executes
checks or assigns a checker. Reuse valid evidence. After material corrections,
reverify and obtain a fresh required review. Read-only role instructions do not
prove enforced isolation; the host may apply broader permissions.

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

`--check` reports differing or missing templates and retained retired names
without writing. For a targeted metadata investigation:

~~~sh
sh "$plugin_dir/scripts/inspect-agent-runtime.sh" --agent ca_worker_mainstay_m <thread-id>
~~~

Caller-effort entries also require `--effort <the effort you passed>`. See
[native operations](plugins/codex-advisor/skills/orchestration/references/operations.md)
for verification groups, metadata, lifecycle limits, and temporary checks.
Route checks establish observed dispatch, not quality, cost, or stability.

## Upgrade from 0.2.0

The installer removes all eleven names below. Select replacements by the new
role/tier contract and routing profile; this is not a promise of identical dials.
The eight 0.1.0 filenames remain retired as well.

| Retired entry | Replacement |
|---|---|
| `ca_explorer_light` | `ca_explorer_mainstay_m` |
| `ca_explorer_standard_m` | `ca_explorer_crux_m` |
| `ca_explorer_standard_h` | `ca_explorer_mainstay_h` or `ca_explorer_crux_h` |
| `ca_explorer_senior` | `ca_explorer_rescue` |
| `ca_worker_light` | `ca_worker_mainstay_m` |
| `ca_worker_standard_m` | `ca_worker_mainstay_h` or `ca_worker_crux_m` |
| `ca_worker_standard_h` | `ca_worker_crux_h` |
| `ca_worker_senior` | `ca_worker_rescue` |
| `ca_advisor_light` | `ca_advisor_mainstay` |
| `ca_advisor_standard` | `ca_advisor_mainstay` or `ca_advisor_crux` |
| `ca_advisor_senior` | `ca_advisor_rescue` |

The old decision packet is replaced by zero-argument consultation. Independent
acceptance keeps its packet but follows the new allocation rule. The former
light/standard first-round pool and senior gate are replaced by model-based
tiers and the capability-failure ladder described above.

## Attribution

The upstream author writes [**Attention Heads**](https://attentionheads.substack.com/?utm_source=github&utm_medium=readme&utm_campaign=sol-advisor)
and the **Agentic Engineering Field Notes** series on AI and agentic engineering.
[Subscribe](https://attentionheads.substack.com/subscribe?utm_source=github&utm_medium=readme&utm_campaign=sol-advisor).
The original MIT attribution remains in [LICENSE](LICENSE).
