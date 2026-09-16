# Codex Advisor

Codex Advisor is a Codex-only fork of
[Sol Advisor](https://github.com/DannyMac180/sol-advisor).
Any primary can implement directly, delegate work, or combine both.
Your primary model and reasoning effort remain your choice.

The plugin ships eleven tier-named native entries and one routing profile.
The primary chooses Explorer, Worker, or Advisor at light, standard, or senior,
owns scheduling and checks, and seeks Advisor judgment where needed.
An explicit Architect-mode request makes all implementation delegated for its
authorized scope, regardless of primary model.

## Install from this checkout

Use a current Codex host with plugins and native custom agents, plus `jq`.
Use your actual checkout path:

~~~sh
codex plugin marketplace add /absolute/path/to/codex-advisor
codex plugin add codex-advisor@codex-advisor
plugin_dir="$(codex plugin list --json | jq -r '.installed[] | select(.pluginId == "codex-advisor@codex-advisor") | .source.path')"
test -n "$plugin_dir" && test "$plugin_dir" != null && test -d "$plugin_dir" && test -f "$plugin_dir/scripts/install-agents.sh" && sh "$plugin_dir/scripts/install-agents.sh"
~~~

The companion installer writes the eleven entries under `$CODEX_HOME/agents`,
or `~/.codex/agents` when `CODEX_HOME` is unset. It overwrites this plugin's
own files when they differ, removes the eight retired 0.1.0 names, and touches
nothing else.

Start a fresh task after installation. Confirm that it exposes
`codex-advisor:orchestration` and the native entries listed by the installer.
Plugin installation and native-agent discovery are separate checks.

## Use

~~~text
Use $codex-advisor:orchestration to implement and verify this feature.
~~~

The primary adjusts decomposition and division of work within your goals, scope,
reserved decisions, acceptance conditions, and resource limits. It chooses
delegated entries without a permission question for each routine call. Workers
receive outcomes, ownership, retained interfaces, constraints, and meaningful
verification; they own local implementation choices and debugging.

| Role | light | standard | senior |
|---|---|---|---|
| Explorer | `ca_explorer_light` | `ca_explorer_standard_m` › `ca_explorer_standard_h` | `ca_explorer_senior` |
| Worker | `ca_worker_light` | `ca_worker_standard_m` › `ca_worker_standard_h` | `ca_worker_senior` |
| Advisor | `ca_advisor_light` | `ca_advisor_standard` | `ca_advisor_senior` |

Efforts, defaults, and candidate order live in the routing profile reference
inside the skill. Light and standard are the first-round pool; senior is behind
the senior gate.

Explorers return source locations, supporting observations, examined scope,
and gaps. They do not implement or perform final acceptance. Installed Explorers
are available to any primary without Architect mode or the skill; installation
alone does not impose a global exploration default.

Request delegation-only work explicitly:

~~~text
Use $codex-advisor:orchestration in Architect mode for this task.
~~~

Any primary can use this mode. Authorization covers the task and follow-ups;
unrelated tasks need new authorization unless you explicitly grant session-wide
scope. Every implementation edit and correction is delegated. A selected model,
ticket, specification, or unaccepted proposal does not activate the mode.

The primary retains scheduling. Independent delegated tasks can run within
available capacity; dependencies and conflicting ownership are sequenced. Workers
preserve concurrent edits and do not delegate implementation further. The primary
inspects all actual changes, including new files and worker-authored tests, reruns
key checks, and verifies the combined result.

## Recover failed work

A complete worker attempt includes implementation, debugging, and verification,
then failed acceptance or concrete inability to finish. Intermediate test failures
and tool errors do not count. Diagnose environment, facts, contracts, reasoning,
and executor suitability before a ladder step. A contract gap is a corrected
contract on the same thread, not a capability failure.

R1 is a rework ticket in the same thread at the same dial. R2 is a raise in a
fresh thread when rework also fails and the cause is capability, either another
dial of the same model or another model. R3 raises the same model at most once.
R4 lets a major execution problem skip the rework ticket and change model,
counted as one failure.

The senior gate is two capability-attributed complete failures inside the
first-round pool, or a user declaration. Every delegated effort or model change
starts a fresh thread. Same-dial worker rework may reuse its thread.

## Advice and acceptance

Advisor entries answer a decision packet or an acceptance packet. Acceptance
always starts in a fresh thread. Decision defaults to the standard tier;
acceptance defaults to the light tier. Senior is reached only on a verdict that
reports little confidence, or a user declaration.

The primary may seek advice proactively. Advice is required for key decisions
uncovered by an applicable plan, evidence invalidating a key plan assumption,
or failure causes still unclear after initial diagnosis. Applicable advice can
be reused while its premises hold. The primary checks sources and explains
material disagreement; advice grants no authorization or veto.

Ordinary direct, delegated, and mixed multi-step work can complete after primary
inspection and verification. Work whose failure is costly, hard to reverse, or
hard to check, or an explicit independent-review request, requires a fresh
acceptance packet after those checks. Step count, file count, and model identity
alone do not trigger review.

Read-only roles request isolation, but the host may apply broader permissions.
Observed read-only behavior under broader permissions is reported separately
from enforced isolation.

## Check and update

~~~sh
sh "$plugin_dir/scripts/install-agents.sh" --check
~~~

`--check` reports drift (differing or missing manifest files) and residue
(present retire files) without writing. After updating the checkout, reinstall
the plugin, run the installer again, and start a fresh task.

~~~sh
sh "$plugin_dir/scripts/inspect-agent-runtime.sh" --agent ca_worker_light <thread-id>
~~~

An entry whose effort the caller selects takes `--effort <the effort you passed>`.

See [native operations](plugins/codex-advisor/skills/orchestration/references/operations.md)
for selective checks, exact entry names, calls, runtime metadata, and disposable
verification. Simple route checks establish observed dispatch and session behavior;
quality, stability, and savings need later experience with real tasks.

## Upgrade from 0.1.0

A spawn of a retired name returns "Agent type not found". The installer deletes
the old files. The inspector's per-role options are replaced by `--agent`.

| Retired entry | Replacement |
|---|---|
| `codex_advisor_luna_explorer` | `ca_explorer_light` or `ca_explorer_standard_m` |
| `codex_advisor_sol_explorer` | `ca_explorer_senior` |
| `codex_advisor_astra_explorer` | no direct replacement; use `ca_explorer_senior` |
| `codex_advisor_luna_implementer` | `ca_worker_light` |
| `codex_advisor_sol_implementer` | `ca_worker_standard_m` |
| `codex_advisor_astra_implementer` | `ca_worker_senior` (or `ca_worker_standard_h`) |
| `codex_advisor_astra_advisor` | `ca_advisor_standard` (decision) |
| `codex_advisor_astra_reviewer` | `ca_advisor_light` (acceptance) |

## Attribution

The upstream author writes [**Attention Heads**](https://attentionheads.substack.com/?utm_source=github&utm_medium=readme&utm_campaign=sol-advisor)
and the **Agentic Engineering Field Notes** series on AI and agentic engineering.
[Subscribe](https://attentionheads.substack.com/subscribe?utm_source=github&utm_medium=readme&utm_campaign=sol-advisor).
The original MIT attribution remains in [LICENSE](LICENSE).
