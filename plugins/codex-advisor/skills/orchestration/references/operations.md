# Native operations

## Install and discover

The plugin supplies `codex-advisor:orchestration`; the companion installer supplies
thirteen tier-named native entries. Resolve scripts from the installed skill:

~~~sh
skill_dir=<directory-containing-SKILL.md>
installer="$skill_dir/../../scripts/install-agents.sh"
runtime_inspector="$skill_dir/../../scripts/inspect-agent-runtime.sh"
sh "$installer" --check-role advisor-mainstay
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
| Explorer, `mainstay`, default candidate | `ca_explorer_mainstay_m` | `explorer-mainstay-m` | caller |
| Explorer, `mainstay`, stronger alternative | `ca_explorer_mainstay_h` | `explorer-mainstay-h` | caller |
| Explorer, `crux`, default candidate | `ca_explorer_crux_m` | `explorer-crux-m` | `max` |
| Explorer, `crux`, stronger alternative | `ca_explorer_crux_h` | `explorer-crux-h` | `xhigh` |
| Explorer, `rescue` | `ca_explorer_rescue` | `explorer-rescue` | caller |
| Worker, `mainstay`, default candidate | `ca_worker_mainstay_m` | `worker-mainstay-m` | `max` |
| Worker, `mainstay`, stronger alternative | `ca_worker_mainstay_h` | `worker-mainstay-h` | `high` |
| Worker, `crux`, default candidate | `ca_worker_crux_m` | `worker-crux-m` | caller |
| Worker, `crux`, stronger alternative | `ca_worker_crux_h` | `worker-crux-h` | caller |
| Worker, `rescue` | `ca_worker_rescue` | `worker-rescue` | caller |
| Advisor, `mainstay` | `ca_advisor_mainstay` | `advisor-mainstay` | caller |
| Advisor, `crux` | `ca_advisor_crux` | `advisor-crux` | `high` |
| Advisor, `rescue` | `ca_advisor_rescue` | `advisor-rescue` | `xhigh` |

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
agent_type: ca_worker_crux_m
fork_turns: none
reasoning_effort: <listed-effort>
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
sh "$runtime_inspector" --agent ca_worker_crux_m --effort <listed-effort> <native-thread-id>
sh "$runtime_inspector" --sessions-dir /absolute/path/to/sessions --agent ca_explorer_rescue --effort <listed-effort> <native-thread-id>
sh "$runtime_inspector" --agent ca_advisor_crux <native-thread-id>
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
escalation eligibility, fresh invocation, quality, or enforced isolation. Check
those against task evidence and native events. Never infer actual settings from
role self-reports or dump prompts and credentials to establish them. Missing entries,
unsupported settings, contradictions, or absent evidence leave affected work
explicitly pending without a silent substitute. Direct independent investigation
may continue.

The generic interface is `--agent NAME [--effort EFFORT] THREAD_ID`. Earlier
review-selection and per-role options fail with a diagnostic that names `--agent`.
Choose the acceptance entry through the routing profile.

## Recover and hand off actual state

Count a complete worker attempt only after implementation, ordinary debugging,
and verification result in failed acceptance or concrete inability to complete.
An intermediate failing test or tool error is not such an attempt. Diagnose
environment, missing facts, contract, reasoning, and executor suitability before
choosing repair, clarification, or a ladder step. Do not infer weak capability
from an environment or contract problem; a contract gap is a corrected contract
on the same thread, not a ladder step.

The skill's escalation ladder governs a failed acceptance. R1 is a rework ticket
in the same thread at the same dial. When rework also fails and the diagnosis
attributes the cause to capability, the attempt and rework together count as one
capability failure. Move the work to the next tier in a fresh thread with the
handoff below. Do not switch models inside the failed tier unless no other choice
exists. The next dial's model level cannot be lower than the failed dial's unless
no other choice exists; if the model stays the same, use a higher effort. R3 keeps
the same-model raise to at most once. Under R4, a major execution problem may skip
rework and counts as one capability failure.

The path is `mainstay` -> `crux` -> `rescue` -> the user. `rescue` is reached only
through `crux` or a user declaration. Work that starts in `crux` reaches `rescue`
after one `crux` capability failure. Environment problems and contract gaps do not
move work along this path.

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

The advisor used by process consultation has no escalation path of its own. A failed
consultation returns an explicit failure and cannot count as advice or acceptance.
A low-confidence independent-acceptance verdict leaves acceptance pending and goes
to the user; it does not trigger an automatic review at another dial.

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

Process consultation takes no packet. Invoke it with zero arguments at the triggers
in the full or reduced posture selected by exact caller/advisor model identity.
Use the consultation mapping in the routing profile and the canonical posture and
adoption rules in [consult-posture.md](consult-posture.md). Consultation returns a
plan, correction, stop signal, or explicit failure. It grants no authorization and
never substitutes for independent acceptance.

After primary diff inspection and checks, ordinary work may complete without
independent acceptance. High-risk work or an explicit independent-review request
requires the acceptance packet on an Advisor entry in a fresh thread. Work produced
in one tier uses that tier's Advisor entry; work produced by several tiers uses the
highest tier involved. Primary-authored work uses the lowest advisor dial not weaker
than the primary's dial; if none qualifies, use the strongest advisor dial. A primary
whose exact model id is absent from the routing profile also uses the strongest
advisor dial. Risk follows consequences, reversibility, and difficulty checking
correctness, not step/file count or model.

Capture scoped state, spawn a fresh Advisor thread, validate settings and tool
activity, and check its actual complete-diff inspection and findings. Consultation,
exploration, a worker's self-review, and a delegated check run cannot substitute.
Resolve material findings, inspect and reverify corrections, then obtain fresh
independent acceptance of the revised deliverable even at an unchanged dial.
Ordinary mode allows primary corrections; Architect mode delegates them. Missing
required review, a low-confidence verdict, or unresolved material findings leaves
completion pending and goes to the user.

## Process consultation

Call the `codex_advisor` MCP server's `process_consultation` tool with `{}`. The
primary, workers, and explorers use the same call. There is no summary, prompt,
path, or dial argument. The installed `.mcp.json` starts Python 3 from the plugin
root through `scripts/run-python.sh`. The launcher requires a POSIX shell and
selects a working Python 3.11 or later from `python3`, `python`, or `py -3`, with
UTF-8 protocol output and bytecode writes disabled. An unusable interpreter is
rejected before starting the component. The component requires the qualified versioned Codex plugin-cache layout;
an unknown layout fails explicitly. Codex supplies caller thread, session, turn,
and item identity in MCP metadata. The component reads exactly one matching
rollout snapshot and stops before the unfinished consultation item, including
when that item is the host's code-mode wrapper.

The snapshot retains all effective raw messages, roles, images, opaque reasoning,
and paired tool calls/results, including truncated output as the caller sees it.
Compaction replaces earlier history with `replacement_history`; no turn window,
summary fallback, or recovery of removed history is used. Unsupported rollback,
content, incomplete pairings, missing replacement history, or inconsistent
identity returns failure. The caller's tool inventory is not forwarded.

The routing profile selects the caller tier's consultation dial. For a primary,
it selects the lowest advisor dial not weaker than the actual caller dial, or
the strongest advisor dial if none qualifies or the model is unknown. The
component uses native Codex authentication and never reads, copies, or transmits
credentials. It creates a fresh ephemeral App Server thread with source base
instructions, injects the effective raw history and consultant guidance, and
requests exactly one structured `plan`, `correction`, or `stop`.

Before passing any caller context, a native discovery process enumerates every
configured MCP server name through all inventory pages and then terminates with
its child processes. Discovery can start configured servers but receives no
caller context; tool/resource descriptions are discarded. A second native process
disables every discovered name, verifies that MCP capabilities and hooks are empty,
and disables built-in tools through a temporary model catalog and feature settings.
Every actual inference request must prove the expected model and effort, an empty
`additional_tools.tools` or explicit top-level `tools=[]`, and no nonempty tool
inventory at either location. Every request must also retain the complete caller
history in order; silent automatic compaction is a context failure. Missing trace evidence, a
nonempty tool inventory, or any dial mismatch fails the consultation.

Within the caller's existing session record, the tool-call event is **started**.
A returned MCP `structuredContent.status` of `succeeded`, with `isError=false`,
means the output has exactly one valid `kind` and nonempty `advice`, and every
observed request matched `expected` and `actual` model/effort. A valid `stop` is
success: the caller must halt and escalate as advised. The result includes
`callerThreadId` and `advisorThreadId`. A returned `status=failed`, with
`isError=true`, carries `code`, `message`, `expected`, and `actual` where observed;
it contains no advice. The text content repeats that same structured object so
the caller and session hooks can read the identical outcome. A call without a
terminal result has started but has not succeeded. Only a successful result
satisfies the caller's consultation requirement.

Errors, aborts, cancellation, context overflow, empty or malformed output, and
mismatches leave the work pending. The caller states the failure in its next
visible reply; it must not present the failure as advice or declare consultation
complete. No automatic retry is made. MCP cancellation terminates the native
process tree and returns failure. The native execution deadline is 180 seconds.
Catalogs, request traces, captured outputs, logs, and SQLite state stay in one
temporary directory and are deleted when the call finishes or is cancelled.
The component writes no session markers, repository files, or credential files.

On Windows, consultation requires a native `codex.exe` on PATH or a unique native
executable in the official npm package layout beside the discovered Codex shim.
It does not execute `.cmd` wrappers with configuration arguments. Windows Job
Objects contain the native process tree; unavailable or failed containment and
cleanup APIs return an explicit failure.

The two-stage isolation adds one native initialization per call. Normal caller
startup must already have initialized its Codex home; consultation does not
bootstrap a fresh home. Requalify after host rollout, metadata, catalog, trace,
or cache-layout changes. Run `sh plugins/codex-advisor/scripts/verify.sh
--consultation` for deterministic MCP-boundary checks with a substitute native
executable. These checks do not establish live routing or installed-host behavior.

## Hooks

The plugin loads `hooks/hooks.json` from the default plugin location. After first
installation, review and trust its hooks in `/hooks`. Review them again after an
update changes a hook definition. Installation does not grant trust; the host skips
untrusted hooks and prints a startup warning pointing to `/hooks`. The plugin does
not modify trust state or add its own untrusted-hook detector.

`SessionStart` injects the exact selected canonical posture block and adoption
block, including on resume and compaction. It compares the session's exact model
id with the advisor model read from the routing profile. The profile currently
assigns one model to every advisor dial, so selection needs no inferred effort.
If that ceases to hold, missing selection evidence leaves the work pending.
Native delegate identity excludes a second posture injection; entries carry their
own posture. Missing session identity also leaves the work pending.

`PostToolUse` on native spawn automatically compares each `ca_*` dispatch with its
shipped template model and pinned effort, or the explicitly passed caller effort.
A pinned effort takes precedence over a spawn argument. Matching dispatches are
silent. Missing caller effort, mismatches, or missing/conflicting evidence add a
message to the spawning session that the affected work remains pending. No manual
inspector run is needed for this comparison. The hook joins the native response's
task path and the parent transcript identity to one child session header, then reads
its actual turn model and effort. It waits at most two seconds for child evidence
to appear. A later unobserved write is never treated as a successful verification.

These hooks write no files or persistent state, including Python bytecode. They
do not read configuration or credentials. The host-provided transcript directory
must use the qualified `sessions` layout; changed host event or transcript schemas
need renewed qualification. There is no primary `Stop` or worker `SubagentStop`
hook. Callers follow their consultation posture without automatic finish blocking.
Consultation result validation is provided by the consultation component.

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
sh plugins/codex-advisor/scripts/verify.sh --consultation
sh plugins/codex-advisor/scripts/verify.sh --hooks
~~~

The installation group covers the installer, the thirteen entry templates, the
manifest, the routing profile's names/models/pins against those templates, and
the complete retire set. It also checks canonical posture equality, advisor
exclusion, and same-role identity outside the posture section, with negative
fixtures. It includes negative fixtures for a model mismatch and a missing retired
entry. The runtime group drives the inspector from all thirteen
templates and covers its options, template-derived expectations, rejection paths,
and emitted metadata. The consultation group exercises the MCP boundary with a
substitute native executable: complete context, routing, actual request validation,
isolation, outcomes, explicit failures, cancellation, and temporary-state cleanup.
The hooks group runs shipped commands with pinned JSON events, checking canonical
injection, delegate exclusion, all entry dials, delayed child evidence, and explicit
pending outcomes. Every surfacing case also rejects a disabled hook as a negative
proof. It does not establish installed-host trust or live dispatch behavior.
A template change reaches installation and runtime groups, so it takes the
unqualified run. Documentation changes have no group here: check structure,
links, and whether the text still matches actual behavior.

Run the unqualified verifier once on the final state. It contains all four groups,
so it replaces the focused runs instead of following them:

~~~sh
sh plugins/codex-advisor/scripts/verify.sh
git diff --check
~~~

The public scripts check safe installation, role allocations, bounded diagnostics,
and evidence consistency. Shell syntax and JSON/TOML parsing are the applicable
static checks; this project has no typed application. Fixtures establish parser
and refusal behavior, not model behavior.

For a route change, use a temporary `CODEX_HOME`, install through the public
installer, and spawn every affected entry once. Pass an effort only when the entry
leaves it to the caller, then run the inspector for that child. Record the entry,
effort passed, observed model and effort, sandbox and permission, child thread,
inspector exit, and removal of seeded retired files. These live checks establish
dispatch and wiring; they do not establish general quality, cost, or stability.

Select tiny disposable native scenarios from ordinary direct/delegated/mixed
completion, explicit Architect delegation, tiered exploration, complete versus
intermediate failure, repair/clarification, same-allocation rework, effort changes
both ways, process consultation, and independent acceptance. Exercise the scenarios
the change can break and record the rest as not exercised. Reuse actual calls and
metadata across checks; after a correction, repeat the affected checks rather than
the whole set. Record expected and observed behavior, native settings, IDs, sources,
permissions, tested revision and host, and unexercised paths in the feature
acceptance record.
