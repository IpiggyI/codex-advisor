# Native operations

## Install and discover

The plugin supplies `codex-advisor:orchestration`; the companion installer supplies
eight model-pinned native entries. Resolve scripts from the installed skill:

~~~sh
skill_dir=<directory-containing-SKILL.md>
installer="$skill_dir/../../scripts/install-agents.sh"
runtime_inspector="$skill_dir/../../scripts/inspect-agent-runtime.sh"
sh "$installer" --check-role advisor
~~~

Run a non-mutating selective check before the first use of each required role.
Cache success for the current task only; recheck after installation/configuration
changes. Use `--check` for all roles, or repeat selectors from the table below.
Selective checks ignore unrelated installed roles. A failure leaves the affected
call pending until the installation is reconciled; independent work may continue.

For development, install the marketplace/plugin in a temporary `CODEX_HOME`,
install roles into its `agents` directory, and start a fresh host task. An empty
temporary `--target-dir` checks installation without touching active settings.
Copy only required connection/authentication settings, keep credentials out of
reports, and remove temporary credential copies after testing.

The installer preflights destinations before writing. Exact files remain unchanged;
modified, conflicting, nonregular, and symlinked files or ancestors are refused.
Dot segments and the filesystem root are refused. Relative targets resolve against
the current directory. Neither check mode creates directories or changes files.
Updated templates count as conflicting installed copies: inspect and explicitly
reconcile them before retrying. No automatic overwrite, migration, deletion of
another installation, or primary-configuration rewrite occurs.

## Select a native entry

Use the skill's allocation policy within user resources. Any primary can select
these entries; installation names distinguish models and responsibilities, not
extra tiers. Explorer and judgment entries are also callable without loading
the skill; installation alone does not create a global routing default.

| Responsibility | Native entry | Install selector | Inspector option | Allowed effort |
|---|---|---|---|---|
| light worker | `codex_advisor_luna_implementer` | `luna` | `--luna` | `max` |
| standard worker | `codex_advisor_sol_implementer` | `sol` | `--sol-effort` | `high`, `xhigh` initially |
| senior worker | `codex_advisor_astra_implementer` | `astra` | `--astra-effort` | `medium`, `high`; eligible `xhigh` |
| light or preferred substantial exploration | `codex_advisor_luna_explorer` | `explorer` | `--explorer-effort` | `high` for light; `max` otherwise |
| direct substantial exploration | `codex_advisor_sol_explorer` | `sol-explorer` | `--sol-explorer-effort` | `medium`, `high` |
| direct substantial exploration | `codex_advisor_astra_explorer` | `astra-explorer` | `--astra-explorer-effort` | `medium`, `high` |
| senior decision advice | `codex_advisor_astra_advisor` | `advisor` | `--advisor-effort` | `medium`, `high`; eligible `xhigh` |
| senior independent acceptance | `codex_advisor_astra_reviewer` | `reviewer` | `--reviewer-effort` | `medium`, `high`; eligible `xhigh` |

Luna entries pin `gpt-5.6-luna`, Sol entries pin `gpt-5.6-sol`, and Astra
entries pin `gpt-6-astra`. Only Luna worker fixes `model_reasoning_effort=max`;
all other templates omit it so caller selection is effective. Keep primary settings
unchanged and respect explicit model exclusions. Luna exploration is preferred
in most substantial investigations, not a mandatory predecessor to Sol or Astra.

## Invoke and validate

Use the native spawn interface with an explicit effort and fresh context:

~~~text
agent_type: codex_advisor_sol_implementer
fork_turns: none
reasoning_effort: xhigh
message: <five-part worker packet from role-contracts.md>
~~~

Replace entry, effort, and packet for the selected role. Always pass effort, even
when it matches a likely default; otherwise host inheritance may select it.
Use `fork_turns: none` for an explicit packet without copied conversation.
Initial Sol worker `xhigh` needs no failure or separate user selection. Astra
`xhigh` requires relevant complete failure under the skill's role-specific policy.
Never edit role files or primary settings to adjust effort.

Require an accepted native call and actual routing evidence. Recognized inspector
inputs do not prove host/account support. Public spawn/details metadata is authoritative;
use the narrow inspector for omitted fields without overriding contradictions:

~~~sh
sh "$runtime_inspector" --sol-effort xhigh <native-thread-id>
sh "$runtime_inspector" --sessions-dir /absolute/path/to/sessions --sol-explorer-effort medium <native-thread-id>
sh "$runtime_inspector" --reviewer-effort medium <native-thread-id>
~~~

Pass the actual selected effort (no effort argument after `--luna`). Validate
role, model, effort, thread, parent association, working directory, and observed
permissions. Compare parent ID and working directory with the expected task.
The inspector reads exactly one UUID-matched rollout and emits allowlisted metadata
only, rejecting absent, ambiguous, malformed, or conflicting evidence. Generic
inspection without a role option does not certify a role contract.

The inspector does not certify user authorization, complete failed attempts,
`xhigh` eligibility, fresh invocation, quality, or enforced isolation. Check those
against task evidence and native events. Never infer actual settings from role
self-reports or dump prompts and credentials to establish them. Missing roles,
unsupported settings, contradictions, or absent evidence leave affected work
explicitly pending without a silent substitute. Direct independent investigation
may continue.

Primary-derived reviewer selection is retired. `--review-primary-effort` and
`--select-review-effort` fail with a diagnostic; use explicit `--reviewer-effort`
without a primary floor. A primary at `max` can receive review at `medium`.

## Recover and hand off actual state

Count a complete worker attempt only after implementation, ordinary debugging,
and verification result in failed acceptance or concrete inability to complete.
An intermediate failing test or tool error is not such an attempt. Diagnose
environment, missing facts, contract, reasoning, and executor suitability before
choosing repair, clarification, rework, effort adjustment, or takeover. Do not
infer weak capability from an environment or contract problem.

Same-model, same-effort worker correction may use native follow-up/resume.
Any effort change in either direction, model change, or role reassignment uses
a new native thread with explicit settings and the matching entry point.
Exploration and advice calls start fresh; independent acceptance always starts
fresh, including after corrections at unchanged effort. A resumed thread with
different requested effort does not satisfy this policy.

Before replacing a writer, finish or stop its conflicting activity and obtain
available evidence. Inspect actual scoped changes and preserve useful partial
results and unrelated edits. Give the successor this compact handoff alongside
the role contract:

~~~text
OBJECTIVE AND BINDING DECISIONS
<Original task, authorized scope, ownership, retained interfaces, and constraints.>

CURRENT STATE
<Actual changed/new files, useful partial changes, relevant task/source references,
and confirmation that the predecessor no longer writes this scope.>

ATTEMPT AND DIAGNOSIS
<Previous role/model/effort/thread, completed checks, failed acceptance or inability,
reproducible evidence, diagnosed cause, and any unresolved contract gap.>

REMAINING WORK
<Corrections and verification still needed without lowering acceptance conditions.>
~~~

Relevant complete worker failure can qualify Astra worker `xhigh` for the same
work, including takeover. Worker failure never by itself qualifies Advisor `xhigh`.
A complete advisory failure means failure to answer its question or a materially
invalidated conclusion, not disagreement. Diagnose and carry that evidence for
an eligible higher-effort advisory attempt on the same question.

Record predecessor/successor IDs, observed efforts, and new-spawn versus follow-up
events. Compare real IDs, not labels or prose. Missing or contradictory transition
evidence leaves the transition unverified. Fresh sessions are an explicit policy,
not a claim that all hosts invalidate caches or that savings are guaranteed.

## Schedule and check combined work

Record dependencies, owned files/modules, generated outputs, verification side
effects, acceptance checks, and scoped starting state. Identify concurrent or user
edits to preserve. Establish available slots from host limits and active agents;
do not create nested workers to evade them. If capacity is unknown, use one worker
until established; if none is available, retain work as pending and report the wait.

Dispatch independent delegated tasks with disjoint ownership within capacity.
Sequence dependent tasks after inspecting prerequisite results and rerunning key
checks. Sequence shared ownership after the earlier writer finishes, updating the
next packet with actual state. Release finished agents through the host lifecycle
when needed after retaining their reports and evidence.

Collect changes, checks, judgment calls, and gaps from every worker. Failed,
blocked, absent, or incomplete work and its dependents stay pending; independent
work may continue. Inspect the complete combined diff, including new files and
worker-authored tests. Rerun meaningful checks and reconcile evidence before
acceptance. Claim parallel execution only when native events or activity show
overlapping worker lifetimes; requests alone establish intent.

## Advice and independent acceptance

Use the decision packet for proactive advice and mandatory judgment at uncovered
key decisions, invalidated key premises, or unclear failure cause after diagnosis.
Reuse applicable advice while premises hold. Check sources and explain material
disagreement; advice grants no authorization, veto, or changed user requirement.

After primary diff inspection and checks, ordinary work may complete without
delivery advice. High-risk work or an explicit independent-review request requires
the separate reviewer entry and review packet. Risk follows consequences,
reversibility, and difficulty checking correctness, not step/file count or model.

Capture scoped state, spawn a fresh reviewer, validate settings and tool activity,
and check its actual complete-diff inspection and findings. Advice, exploration,
and worker self-review cannot substitute. Resolve material findings, inspect and
reverify corrections, then obtain fresh independent acceptance of the revised
deliverable even at unchanged effort. Ordinary mode allows primary corrections;
Architect mode delegates them. Missing required review or unresolved material
findings leaves completion pending.

## Observe permissions

Explorer, Advisor, and Independent reviewer request read-only access. The host
may reapply broader parent permissions. Record actual sandbox policy and permission
profile; inspect tool activity and exact before/after scoped files and artifacts.

- Claim enforced isolation only when the host enforces it and observations agree.
- Under broader permissions, proceed only if hard isolation is not required,
  the packet prohibits edits, and scoped state confirms no mutation. Report
  behavioral read-only operation under the observed permissions.
- Missing/conflicting permissions, unavailable required isolation, or observed
  mutation prevents affected acceptance and must be reported.

Unchanged scoped files do not establish absence of writes outside that scope.

## Verify changes

From the repository root, use focused checks while editing, then the full suite:

~~~sh
sh plugins/codex-advisor/scripts/verify.sh --installation
sh plugins/codex-advisor/scripts/verify.sh --runtime
sh plugins/codex-advisor/scripts/verify.sh
git diff --check
~~~

The public scripts check safe installation, role allocations, bounded diagnostics,
and evidence consistency. Shell syntax and JSON/TOML parsing are the applicable
static checks; this project has no typed application. Fixtures establish parser
and refusal behavior, not model behavior.

Use tiny disposable native scenarios for advertised routes and critical branches:
ordinary direct/delegated/mixed completion, explicit Architect delegation,
tiered exploration, complete versus intermediate failure, repair/clarification,
same-allocation rework, effort changes both ways, and independent acceptance.
Use short advisory questions for reused/invalidated advice, disagreement, and
eligible advisory escalation. Reuse actual calls and metadata across checks.
Record expected/observed behavior, native settings, IDs, sources, permissions,
tested revision/host, and unexercised paths in the feature acceptance record.
These smoke checks do not establish general quality, cost, or stability gains.
