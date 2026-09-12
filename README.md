# Codex Advisor

Codex Advisor is a Codex-only fork of
[Sol Advisor](https://github.com/DannyMac180/sol-advisor).
Any primary model can implement directly, delegate work, or combine both.
Your primary model and reasoning effort remain your choice.

The primary chooses scoped worker and Explorer allocations, owns scheduling,
checks actual changes, and seeks Astra advice where judgment is needed.
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

The companion installer adds eight native entries under `$CODEX_HOME/agents`,
or `~/.codex/agents` when `CODEX_HOME` is unset. It preserves unrelated agents,
existing Sol Advisor files, and primary configuration. Modified or unsafe
destinations are refused before installation; exact files remain unchanged.

Start a fresh task after installation. Confirm that it exposes
`codex-advisor:orchestration` and the native entries listed by the installer.
Plugin installation and native-agent discovery are separate checks.

## Use

~~~text
Use $codex-advisor:orchestration to implement and verify this feature.
~~~

The primary adjusts decomposition and division of work within your goals, scope,
reserved decisions, acceptance conditions, and resource limits. It chooses allowed
delegated settings without a permission question for each routine call. Workers
receive outcomes, ownership, retained interfaces, constraints, and meaningful
verification; they own local implementation choices and debugging.

| Role | Tier | Model and reasoning effort |
|---|---|---|
| Explorer | light | Luna `high` |
| Explorer | standard / senior | Usually Luna `max`; direct Sol or Astra `medium` / `high` |
| worker (Implementer) | light | Luna `max` |
| worker (Implementer) | standard | Sol `high` / `xhigh`, including the first attempt |
| worker (Implementer) | senior | Astra `medium` / `high`; eligible `xhigh` after complete worker failure |
| Advisor, including independent acceptance | senior | Astra `medium` / `high`; eligible `xhigh` after complete advisory failure |

Luna is preferred for most substantial exploration, not required before direct
Sol or Astra selection. Explorers return source locations, supporting observations,
examined scope, and gaps. They do not implement or perform final acceptance.
Installed Explorers are available to any primary without Architect mode or the
skill; installation alone does not impose a global exploration default.

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
and executor suitability before choosing repair, clarification, rework, changed
effort, or takeover. Escalation is an option, not a fixed ladder.

Relevant complete worker failure can make Astra worker `xhigh` eligible for
the same work. It does not unlock Advisor `xhigh`: that requires a relevant
complete failure to answer the advisory question or a materially invalidated
conclusion. Disagreement alone is insufficient.

Every delegated effort change, up or down, requires a new native thread.
Model changes and role reassignments also start fresh. Same-model, same-effort
worker corrections may reuse the thread; independent acceptance always starts
fresh. Stop conflicting previous writers and hand off actual changes, decisions,
checks, failure evidence, and remaining work. This is an explicit session policy,
not a guarantee about cache behavior or savings.

## Advice and acceptance

The primary may seek advice proactively. Advice is required for key decisions
uncovered by an applicable plan, evidence invalidating a key plan assumption,
or failure causes still unclear after initial diagnosis. Applicable advice can
be reused while its premises hold. The primary checks sources and explains
material disagreement; advice grants no authorization or veto.

Ordinary direct, delegated, and mixed multi-step work can complete after primary
inspection and verification. High-risk work or an explicit independent-review
request requires a fresh Astra Independent reviewer after those checks.
Risk follows consequences, reversibility, and difficulty checking correctness;
step count, file count, and model identity alone do not trigger review.

Decision advice and independent acceptance use separate native entries and
contracts within the Advisor role. Initial effort is `medium` or `high`,
independently of primary effort. Material review findings require corrections,
primary re-verification, and a new review thread even at unchanged effort.
Unavailable required calls, unsupported settings, missing/conflicting evidence,
or unresolved material findings leave affected completion pending.

Read-only roles request isolation, but the host may apply broader permissions.
Observed read-only behavior under broader permissions is reported separately
from enforced isolation.

## Check and update

~~~sh
sh "$plugin_dir/scripts/install-agents.sh" --check
~~~

After updating the checkout, repeat plugin installation and the companion installer,
then start a fresh task. Updated role templates count as conflicting installed
copies: inspect and explicitly reconcile them before retrying. The installer
does not overwrite them or delete another installation.

See [native operations](plugins/codex-advisor/skills/orchestration/references/operations.md)
for selective checks, exact entry names, calls, runtime metadata, and disposable
verification. Simple route checks establish observed dispatch and session behavior;
quality, stability, and savings need later experience with real tasks.

## Attribution

The upstream author writes [**Attention Heads**](https://attentionheads.substack.com/?utm_source=github&utm_medium=readme&utm_campaign=sol-advisor)
and the **Agentic Engineering Field Notes** series on AI and agentic engineering.
[Subscribe](https://attentionheads.substack.com/subscribe?utm_source=github&utm_medium=readme&utm_campaign=sol-advisor).
The original MIT attribution remains in [LICENSE](LICENSE).
