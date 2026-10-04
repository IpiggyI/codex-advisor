# Native operations

Read this before each new native spawn, including the Advisor dispatch for
independent acceptance, and before sending work to an existing thread.

## Check the entry

The plugin supplies `codex-advisor:orchestration`; the companion installer supplies
seventeen tier-named native entries. Resolve scripts from the installed skill:

~~~sh
skill_dir=<directory-containing-SKILL.md>
installer="$skill_dir/../../scripts/install-agents.sh"
runtime_inspector="$skill_dir/../../scripts/inspect-agent-runtime.sh"
sh "$installer" --check-role advisor-mainstay-m
~~~

Run a non-mutating selective check before the first use of each required entry.
Cache success for the current task only; recheck after installation/configuration
changes. Use `--check` for all entries, or repeat `--check-role` with a selector:
the entry name without `ca_`, with hyphens for underscores, so `ca_worker_crux_m`
becomes `worker-crux-m`. Selective checks ignore unrelated installed files. A failure
leaves the affected call pending until the installation is reconciled; independent
work may continue.

Explorer and Advisor entries are also callable without loading the skill;
installation alone does not create a global routing default.

## Dispatch

Use the native spawn interface with fresh context; an Explorer call always starts
a new thread. Pass `reasoning_effort` when the entry leaves effort to the caller;
a pinned entry takes none. On every fresh spawn, set `task_name` to a short name
that distinguishes this thread from its siblings. The first line of `message` is
that same name, verbatim plain text with no Markdown marker, then a blank line,
then the route declaration below, another blank line, and the role packet:

~~~text
agent_type: ca_worker_crux_m
fork_turns: none
task_name: wire_http_checks
message: <short name, blank line, Route line, blank line, five-part worker packet>
~~~

Replace entry, effort, short name, and packet for the selected role. Use
`fork_turns: none` for an explicit packet without copied conversation; per-spawn
`model` and `reasoning_effort` are honoured only with it. For a caller-selected
entry, always pass an effort listed in the routing profile, even the default;
otherwise host inheritance may select it. The template's `model` and
`model_reasoning_effort` take precedence over spawn values, so a pinned entry
cannot reach another effort. Never edit entry files or primary settings to adjust
effort. Installed entries are written only by the installer; do not hand-edit them.

## Declare every route

Use this single-line form, with the chosen role, tier, model, and one effort from
the routing profile:

~~~text
Route: role=<role> tier=<tier> dial=<model>[<effort>] basis=<kind> ref=<evidence reference>
~~~

For `mainstay`, omit `basis` and `ref`. Other tiers require a nonempty reference
and a basis from this table:

| Role | `crux` basis | `rescue` basis |
|---|---|---|
| Worker or Explorer | `key-difficulty`, `failure`, `user-declaration` | `failure`, `user-declaration` |
| Advisor | `acceptance-mapping`, `user-declaration` | `acceptance-mapping`, `user-declaration` |

Reference the identified constraints for `key-difficulty`, the failed attempt
and diagnosis for `failure`, the user's declaration for `user-declaration`, and
the accepted scope and profile mapping for `acceptance-mapping`. A model-only
declaration does not authorize `rescue`. Independent acceptance follows its
mapping even when it is the Advisor's first call.

`followup_task` and `send_message` to a worker start `message` with the route
line, a blank line, then the packet or correction. Check the
[reuse window](recovery.md#keep-or-replace-the-thread) before either call; new
tickets also state the shared area and concrete need for existing context.
Use the target's UUID, canonical task path, or relative task path. The hook
requires one matching target in the caller's host session; an unresolved or
ambiguous target is denied. Explorer calls and independent acceptance use fresh
threads. Messages to a resolved primary or non-plugin entry need no route.

The `PreToolUse` hook rejects missing or malformed declarations, entry/tier/dial
conflicts, unlisted efforts, invalid basis kinds, and worker reuse outside the
window or without valid host evidence. A passed check emits a route confirmation.
It checks the basis format, not its truth, task fit, user authorization, or whether
the selected tier is the lowest compatible one; the caller checks those against
the task record. The hook reads the target's actual dial and activity from its
transcript and writes no state.

## Read the dispatch check

The `PostToolUse` hook compares each `ca_*` dispatch with its shipped template's
model and pinned effort, or with the caller effort passed explicitly; a pinned
effort takes precedence over a spawn argument. It also checks the child's role,
parent, session, and task path against the host record. A match adds one
confirmation line to the spawning session: identity, model, and effort match the
host record, and working directory and permissions were not checked. Missing
caller effort, a mismatch, or missing or conflicting evidence adds a message that
the affected work remains pending. A dispatch to any other entry gets no message.
For a `ca_*` dispatch, no message means the hook did not run, for example because
it is not trusted; that dispatch is unchecked, not verified.

The route confirmation and the observed-dial confirmation establish different
facts. An inspector pass cannot establish that the pre-call route check ran.
Without its confirmation, manually check the declaration and eligibility and
report the automatic gate as unverified. New or changed hooks require the user's
trust review in `/hooks`. A skipped or failed hook cannot enforce the gate.

## Validate routing evidence

Require an accepted native call and actual routing evidence. Recognized inspector
inputs do not prove host/account support. Validate role, model, effort, thread,
parent association, working directory, and observed permissions for every dispatch;
compare parent ID and working directory with the expected task. Public spawn/details
metadata is authoritative; use the narrow inspector for omitted fields without
overriding contradictions. Run the inspector yourself when a `ca_*` dispatch shows
no hook message, and when native metadata omits the working directory or
permissions, which the hook never checks:

~~~sh
sh "$runtime_inspector" --agent ca_worker_crux_h --effort <listed-effort> <native-thread-id>
sh "$runtime_inspector" --sessions-dir /absolute/path/to/sessions --agent ca_explorer_rescue --effort <listed-effort> <native-thread-id>
sh "$runtime_inspector" --agent ca_advisor_crux_h <native-thread-id>
~~~

The generic interface is `--agent NAME [--effort EFFORT] THREAD_ID`. `--agent`
names the entry. The inspector reads the expected model and any pinned effort from
the shipped template of that name, resolved beside the script. For a caller-selected
entry, `--effort` is required and is the expected effort. For a pinned entry, omit
`--effort` or pass a value equal to the pin; a different value is rejected. The
inspector does not judge whether an effort is allowed; the routing profile does.
It reads exactly one UUID-matched rollout and emits allowlisted metadata only,
rejecting absent, ambiguous, malformed, or conflicting evidence. Generic inspection
without `--agent` does not certify a role contract.

The inspector does not certify user authorization, complete failed attempts,
escalation eligibility, fresh invocation, quality, or enforced isolation. Check
those against task evidence and native events. Never infer actual settings from
role self-reports or dump prompts and credentials to establish them. Missing entries,
unsupported settings, contradictions, or absent evidence leave affected work
explicitly pending without a silent substitute. Direct independent investigation
may continue.

## Schedule within capacity

Record the scoped starting state and the acceptance checks each dispatch rests on,
and identify concurrent or user edits to preserve. Establish available slots from
host limits and active agents. If capacity is unknown, use one worker until
established; if none is available, retain work as pending and report the wait.
A delegated check run uses a Worker entry; the read-only Explorer and Advisor
entries take only checks that write nothing. Release finished agents through the
host lifecycle when needed after retaining their reports and evidence. Claim
parallel execution only when native events or activity show overlapping worker
lifetimes; requests alone establish intent.

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
