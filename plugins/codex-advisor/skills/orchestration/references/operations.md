# Native operations

## Install and discover

The plugin supplies `codex-advisor:orchestration`; the companion installer supplies
eleven tier-named native entries. Resolve scripts from the installed skill:

~~~sh
skill_dir=<directory-containing-SKILL.md>
installer="$skill_dir/../../scripts/install-agents.sh"
runtime_inspector="$skill_dir/../../scripts/inspect-agent-runtime.sh"
sh "$installer" --check-role advisor-standard
~~~

Run a non-mutating selective check before the first use of each required entry.
Cache success for the current task only; recheck after installation/configuration
changes. Use `--check` for all entries, or repeat `--check-role` with selectors
from the table below. Selective checks ignore unrelated installed files. A failure
leaves the affected call pending until the installation is reconciled; independent
work may continue.

For development, install the marketplace/plugin in a temporary `CODEX_HOME`,
install entries into its `agents` directory, and start a fresh host task. An empty
temporary `--target-dir` checks installation without touching active settings.
Copy only required connection/authentication settings, keep credentials out of
reports, and remove temporary credential copies after testing.

The installer is manifest-driven: the manifest is the set of templates shipped
beside it, and the retire list names the entry files of earlier versions. A missing
or differing manifest destination is written and reported as installed; an identical
one is reported as unchanged; a present retire file is deleted by filename and
reported as removed. Nothing else is read or written, including upstream Sol
Advisor files, unrelated agents, and the primary configuration. Writes are atomic
per file. `--check` writes nothing and fails on drift (a differing or missing
manifest file) or residue (a present retire file), listing each. Symlinked
destinations or ancestors, non-regular destinations, non-directory ancestors,
dot segments, and the filesystem root are refused before any write. Relative
targets resolve against the current directory. Installed entries are written
only by the installer; do not hand-edit them.

## Select a native entry

Use the skill's allocation mechanism and the dials in
[routing-profile.md](routing-profile.md) within user resources. Any primary can
select these entries. The name states role and tier; inside a tier with two models,
`_m` is the default candidate and `_h` the stronger alternative. Explorer and
Advisor entries are also callable without loading the skill; installation alone
does not create a global routing default.

| Responsibility | Native entry | Install selector | Effort |
|---|---|---|---|
| Explorer, light | `ca_explorer_light` | `explorer-light` | caller |
| Explorer, standard, default candidate | `ca_explorer_standard_m` | `explorer-standard-m` | `max` |
| Explorer, standard, stronger alternative | `ca_explorer_standard_h` | `explorer-standard-h` | caller |
| Explorer, senior | `ca_explorer_senior` | `explorer-senior` | caller |
| Worker, light | `ca_worker_light` | `worker-light` | `max` |
| Worker, standard, default candidate | `ca_worker_standard_m` | `worker-standard-m` | caller |
| Worker, standard, stronger alternative | `ca_worker_standard_h` | `worker-standard-h` | `low` |
| Worker, senior | `ca_worker_senior` | `worker-senior` | caller |
| Advisor, light (acceptance default) | `ca_advisor_light` | `advisor-light` | `low` |
| Advisor, standard (decision default) | `ca_advisor_standard` | `advisor-standard` | `medium` |
| Advisor, senior | `ca_advisor_senior` | `advisor-senior` | caller |

Every entry pins its model; a value in the Effort column is pinned in the template,
"caller" means the caller passes it. The template's `model` and `model_reasoning_effort`
take precedence over spawn values, so a pinned entry cannot reach another effort.
Keep primary settings unchanged and respect explicit model exclusions.

## Invoke and validate

Use the native spawn interface with fresh context. Pass `reasoning_effort` when
the entry leaves effort to the caller; a pinned entry takes none. On every fresh
spawn, set `task_name` to a short name that distinguishes this thread from its
siblings. The first line of `message` is that same name, verbatim plain text with
no Markdown marker, then a blank line, then the role packet:

~~~text
agent_type: ca_worker_standard_m
fork_turns: none
reasoning_effort: xhigh
task_name: wire_http_checks
message: <short name, blank line, five-part worker packet from role-contracts.md>
~~~

Replace entry, effort, short name, and packet for the selected role. Use
`fork_turns: none` for an explicit packet without copied conversation; per-spawn
`model` and `reasoning_effort` are honoured only with it. For a caller-selected
entry, always pass an effort listed in the routing profile, even the default;
otherwise host inheritance may select it. Never edit entry files or primary
settings to adjust effort. Follow-up on the same thread keeps that name; a new
thread gets its own.

Require an accepted native call and actual routing evidence. Recognized inspector
inputs do not prove host/account support. Public spawn/details metadata is authoritative;
use the narrow inspector for omitted fields without overriding contradictions:

~~~sh
sh "$runtime_inspector" --agent ca_worker_standard_m --effort xhigh <native-thread-id>
sh "$runtime_inspector" --sessions-dir /absolute/path/to/sessions --agent ca_explorer_senior --effort medium <native-thread-id>
sh "$runtime_inspector" --agent ca_advisor_light <native-thread-id>
~~~

`--agent` names the entry. The inspector reads the expected model and any pinned
effort from the shipped template of that name, resolved beside the script. For a
caller-selected entry, `--effort` is required and is the expected effort. For a
pinned entry, omit `--effort` or pass a value equal to the pin; a different value
is rejected. The inspector does not judge whether an effort is allowed; the routing
profile does. Validate role, model, effort, thread, parent association, working
directory, and observed permissions. Compare parent ID and working directory with
the expected task. The inspector reads exactly one UUID-matched rollout and emits
allowlisted metadata only, rejecting absent, ambiguous, malformed, or conflicting
evidence. Generic inspection without `--agent` does not certify a role contract.

The inspector does not certify user authorization, complete failed attempts,
senior-gate eligibility, fresh invocation, quality, or enforced isolation. Check
those against task evidence and native events. Never infer actual settings from
role self-reports or dump prompts and credentials to establish them. Missing entries,
unsupported settings, contradictions, or absent evidence leave affected work
explicitly pending without a silent substitute. Direct independent investigation
may continue.

Primary-derived reviewer selection is retired. `--review-primary-effort` and
`--select-review-effort` fail with a diagnostic; choose the acceptance dial without
a primary floor. A primary at `max` can receive acceptance at the light tier. The
eight per-role options of 0.1.0 (`--luna`, `--sol-effort`, `--astra-effort`,
`--explorer-effort`, `--sol-explorer-effort`, `--astra-explorer-effort`,
`--advisor-effort`, `--reviewer-effort`) are retired in favour of `--agent` and
fail with a diagnostic naming it.

## Recover and hand off actual state

Count a complete worker attempt only after implementation, ordinary debugging,
and verification result in failed acceptance or concrete inability to complete.
An intermediate failing test or tool error is not such an attempt. Diagnose
environment, missing facts, contract, reasoning, and executor suitability before
choosing repair, clarification, or a ladder step. Do not infer weak capability
from an environment or contract problem; a contract gap is a corrected contract
on the same thread, not a ladder step.

The skill's escalation ladder governs a failed acceptance: R1 a rework ticket in
the same thread at the same dial; R2 when rework also fails and the cause is
capability, a raise in a fresh thread with the handoff below, either a higher
effort of the same model or another model from the routing profile; R3 the same
model raised at most once; R4 a major execution problem may skip the rework ticket
and change model, counted as one failure. Two capability-attributed complete
failures inside the first-round pool are the senior gate and a required consultation;
the Advisor's verdict settles whether the senior entry is warranted.

Same-model, same-effort worker correction may use native follow-up/resume.
Any effort change in either direction, model change, or role reassignment uses
a new native thread with explicit settings and the matching entry. Exploration
and advice calls start fresh; independent acceptance always starts fresh, including
after corrections at an unchanged dial. A resumed thread with different requested
effort does not satisfy this policy.

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

Worker failure never by itself moves the Advisor to its senior entry. A complete
advisory failure means failure to answer its question or a materially invalidated
conclusion, not disagreement. Diagnose it and choose fact gathering, clarification,
or another dial for the same question in a fresh thread; only a verdict that reports
low confidence or a user declaration opens the Advisor's senior gate.

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
Sequence dependent tasks after inspecting prerequisite results and checking the
premise the dependent work rests on; do not accumulate unverified premises to
lower the number of runs. Sequence shared ownership after the earlier writer
finishes, updating the next packet with actual state. Release finished agents
through the host lifecycle when needed after retaining their reports and evidence.

Form verification batches separately from ticket and dispatch boundaries. Combine
checks that share costly setup while the scope stays understandable and a failure
stays locatable. Name one executor per batch: the primary, or a delegate that
receives the complete batch requirements, the merged changes, and the evidence
already collected. A delegated check run uses a Worker entry; the read-only
Explorer and Advisor entries take only checks that write nothing.

Collect changes, checks, judgment calls, and gaps from every worker. Failed,
blocked, absent, or incomplete work and its dependents stay pending; independent
work may continue. Inspect the complete combined diff yourself, including new
files and worker-authored tests. Run each verification batch once through its
executor, then reconcile coverage, actual output, and the current combined state
before acceptance. Reuse a result while the relevant code, artifacts, checks,
inputs, and environment still support it; check again for a changed dependency,
an evidence gap, an unexplained failure, or an identified risk. Claim parallel
execution only when native events or activity show overlapping worker lifetimes;
requests alone establish intent.

## Advice and independent acceptance

Use the decision packet for proactive advice and mandatory judgment at uncovered
key decisions, invalidated key premises, or unclear failure cause after diagnosis,
and at the senior gate after two complete failures. Send it to the Advisor entry
the routing profile names as the decision default. Reuse applicable advice while
premises hold. Check sources and explain material disagreement; advice grants no
authorization, veto, or changed user requirement.

After primary diff inspection and checks, ordinary work may complete without
delivery advice. High-risk work or an explicit independent-review request requires
the acceptance packet on an Advisor entry in a fresh thread; the routing profile
names the acceptance default. Both packets are request shapes of the same Advisor
entries; no separate reviewer entry exists. Risk follows consequences, reversibility,
and difficulty checking correctness, not step/file count or model.

Capture scoped state, spawn a fresh Advisor thread, validate settings and tool
activity, and check its actual complete-diff inspection and findings. Advice,
exploration, a worker's self-review, and a delegated check run cannot substitute.
Resolve material findings, inspect and reverify corrections, then obtain fresh
independent acceptance of the revised deliverable even at an unchanged dial.
Ordinary mode allows primary corrections; Architect mode delegates them. Missing
required review or unresolved material findings leaves completion pending.

## Observe permissions

Explorer and Advisor entries request read-only access. The host may reapply
broader parent permissions. Record actual sandbox policy and permission profile;
inspect tool activity and exact before/after scoped files and artifacts.

- Claim enforced isolation only when the host enforces it and observations agree.
- Under broader permissions, proceed only if hard isolation is not required,
  the packet prohibits edits, and scoped state confirms no mutation. Report
  behavioral read-only operation under the observed permissions.
- Missing/conflicting permissions, unavailable required isolation, or observed
  mutation prevents affected acceptance and must be reported.

Unchanged scoped files do not establish absence of writes outside that scope.

## Verify changes

From the repository root, select checks by the behavior the change touches. While
editing one area, run its focused group:

~~~sh
sh plugins/codex-advisor/scripts/verify.sh --installation
sh plugins/codex-advisor/scripts/verify.sh --runtime
~~~

The installation group covers the installer, the entry templates, the manifest,
and the routing profile's dials against those templates. The runtime group covers
the inspector: its options, the expectations it reads from a template, and the
metadata it emits. A template change reaches both groups, so it takes the
unqualified run. Documentation changes have no group here: check structure,
links, and whether the text still matches actual behavior.

Run the unqualified verifier once on the final state. It contains both groups,
so it replaces the focused runs instead of following them:

~~~sh
sh plugins/codex-advisor/scripts/verify.sh
git diff --check
~~~

The public scripts check safe installation, role allocations, bounded diagnostics,
and evidence consistency. Shell syntax and JSON/TOML parsing are the applicable
static checks; this project has no typed application. Fixtures establish parser
and refusal behavior, not model behavior.

Tiny disposable native scenarios cover the advertised routes and critical branches:
ordinary direct/delegated/mixed completion, explicit Architect delegation,
tiered exploration, complete versus intermediate failure, repair/clarification,
same-allocation rework, effort changes both ways, and independent acceptance.
Use short advisory questions for reused/invalidated advice, disagreement, and
eligible advisory escalation. Select from this set the scenarios the change can
break and record the rest as not exercised. Reuse actual calls and metadata
across checks; after a correction, repeat the affected checks rather than the
whole set. Record expected/observed behavior, native settings, IDs, sources,
permissions, tested revision/host, and unexercised paths in the feature acceptance
record. These smoke checks do not establish general quality, cost, or stability gains.
