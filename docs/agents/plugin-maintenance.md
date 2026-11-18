# Plugin maintenance

`plugins/codex-advisor/` ships what runtime callers and delegates read: the
[orchestration skill](../../plugins/codex-advisor/skills/orchestration/SKILL.md),
its references, the entry templates, and the runtime scripts. The maintainer
verification scripts and their fixtures live in the repository's `tests/` and
do not ship with the plugin. This page holds the procedures and internals for
changing the plugin. Run every command from the repository root.

## Development installation

For development, install the marketplace/plugin in a temporary `CODEX_HOME`,
install entries into its `agents` directory, and start a fresh host task. An empty
temporary `--target-dir` checks installation without touching active settings.
Copy only required connection/authentication settings, keep credentials out of
reports, and remove temporary credential copies after testing.

A managed plugin cache is installed output. Reinstallation replaces local edits
with files from the configured marketplace source. Deliver fixes through that
source, or through an explicitly selected local marketplace. Verify a fresh install
and a reinstall against the intended source; a cache copy alone does not establish
that an update persists.

## Companion installer

The installer is manifest-driven: the manifest is the set of templates shipped
beside it. A missing or differing manifest destination is written and reported as
installed; an identical one is reported as unchanged. The installer deletes nothing.
Nothing else is read or written, including upstream Sol Advisor files, unrelated
agents, and the primary configuration. Writes are atomic per file. `--check` writes
nothing and fails on drift (a differing or missing manifest file), listing each.
Symlinked destinations or ancestors, non-regular destinations, non-directory
ancestors, dot segments, and the filesystem root are refused before any write.
Relative targets resolve against the current directory.

On Windows, pass the target as a POSIX path, for example
`sh "$plugin_dir/scripts/install-agents.sh" --target-dir /c/Users/<user>/.codex/agents`.
Git `sh` treats a drive-letter path such as `C:\Users\<user>\.codex` as relative,
so a Windows-form `CODEX_HOME` makes the installer write to and check a new
directory under the current one, and both runs report success. A PowerShell
started from WSL also inherits WSL's `CODEX_HOME`, so the default target is
wrong there as well.

[ADR-0008](../adr/0008-installer-deletes-no-old-filenames.md) records why the
installer deletes no old filenames and when to revisit that.

## Host upgrade checks

After each host upgrade and before each plugin release, run all three local maintainer
checks from the repository root:

```sh
python3 tests/consultation_schema_check.py
python3 tests/consultation_corpus_replay.py
python3 tests/consultation_native_corpus.py
```

The schema check generates the installed host's experimental JSON protocol schema
in a temporary directory and compares every `ResponseItem` variant with
`consult_context.py`'s `ITEM_POLICY`. A nonempty `missingTypes` list means the
policy table needs an explicit decision for those host types. Schema generation
or an unreadable union also fails the check.

The corpus check runs production `reconstruct()` at sequential `function_call` and
`custom_tool_call` boundaries in every rollout under `~/.codex/sessions` and existing
`/mnt/c/Users/*/.codex/sessions` directories. Repeat `--root PATH` to replace the
default roots. Each boundary uses the latest preceding turn context as MCP
metadata and a truncated copy in a temporary home. An id-less boundary receives
a temporary selection id; it is excluded from reconstructed history. Prior
records remain unchanged. Legacy files without a session header and boundaries
before any turn context or task-start event are skipped and counted.
Positions with an earlier declared call still awaiting its result are skipped as
`parallelSkipped`, included in `boundariesSkipped`. The batch-start position is
replayed. Pairing follows `ITEM_POLICY`, including capability and hosted calls;
compaction replaces the tracked history. Invalid pairing
structures remain subject to production validation.

Corpus output is JSON containing counts and failure locations, stages, types,
codes, and messages, without history text. Failures with code `rollback` are
deliberate design rejections: their diagnostics appear in `designRejections`,
with counts by code in `counts.designRejections`, and do not change the exit
status. Every other failure appears in `failures` and produces a nonzero exit
status, identifying a reconstruction limit to investigate before release. Do not
relax validation merely to pass the corpus. The report includes both the
boundary index and the failing record index, starting at zero. A skipped boundary
is unverified. Neither check sends a remote request or changes real rollouts;
temporary schemas and rollout copies are removed automatically. These maintainer
checks are explicit commands and are not run by `tests/verify.sh`.

The native corpus check selects the smallest eligible reconstructed caller history
for every preserved item type, measured as UTF-8 JSON bytes of base instructions
and items. For capability, control, and hosted types, it selects boundaries whose raw
effective history before the boundary contains the type. Production reconstruction
must exclude those items, and the actual native requests must contain neither
excluded items nor tools at request or item level. Both sample kinds use the
replay check's sequential boundary and compaction rules.
The source is the real caller rollout; it does not generate caller histories with
consultation-specific features. Repeat `--root PATH` to replace the default session
roots. Types without an eligible sample appear in `uncoveredTypes` and fail coverage.

Each selected history runs through production `consult_native.execute()`, including
its catalog, configuration, injection, isolation checks, and strict request
verification. At run time it reads the `ca_advisor_*` rows in the routing profile
and queries `codex debug models --bundled`. Each sample runs in every request mode
used by those advisor models, according to their `use_responses_lite` values. The
selected advisor uses that mode in the unmodified production catalog. Modes used
by no advisor model appear in `notCovered`; they are not executed and do not fail
the check. `requestModes` lists the active modes and their advisor models. The
tool does not force catalog flags. The provider is a credential-free
loopback endpoint in a temporary home, with a fixed structured response. No caller
provider configuration or credentials are copied. Homes, traces, and rollout
copies are removed after use. This check cannot prove remote API acceptance of
opaque or injected items.
Loopback checks cannot detect a backend that rejects hosted tool records. Before
release, any newly preserved hosted tool type requires one real authenticated
request to the configured backend, with tool isolation and a structured result
verified.

Output is JSON: selected file names and boundary indices, verdicts for each type
and mode, `sampleKind` (`preserved` or `excluded`), uncovered types, and failures
containing only stage, type, code, path, and message. It never emits history text.
Any failed mode, selection failure, or
uncovered type produces a nonzero exit status. Investigate failures without
relaxing comparison. The targeted native mutation test
`test_transport_normalization_mutation_fails_with_type_and_path` in
`tests/test_consultation_native_corpus.py` uses a synthetic history with a source
item id. It verifies that the normal comparison passes, then deliberately disables
source id removal and requires a context failure with a type and field path.

## Process consultation component

[ADR-0006](../adr/0006-mainstay-crux-rescue-and-process-consultation.md#consultation-mechanism-and-host-facts)
records the selected mechanism, each host fact it rests on with its evidence
boundary and invalidation check, and what production must validate and reject.
This section adds the component contract beyond those facts. The caller-facing
rules are in the skill's consultation section.

The installed `.mcp.json` starts Python 3 from the plugin root through
`scripts/run-python.sh`. The launcher requires a POSIX shell and selects a working
Python 3.11 or later from `python3`, `python`, or `py -3`, with UTF-8 protocol
output and bytecode writes disabled. An unusable interpreter is rejected before
starting the component. The component requires the qualified versioned Codex
plugin-cache layout; an unknown layout fails explicitly.

The component checks `$CODEX_HOME/codex-advisor/consultation-off` on every call,
using the caller's `CODEX_HOME` derived from the versioned plugin cache layout.
WSL and Windows each have their own `CODEX_HOME` and marker. While the marker
exists, the component returns a failed `switched_off` result with
`consultationDisabled=true`, the stop-calling guidance, and the marker path to
delete. It reads no rollout, starts no native process, and neither reads nor writes
failure counts; the result has no `failureCount`. Deleting the marker enables the
next call in the same MCP process. A thread that receives the switched-off result
stops calling for the rest of that thread, so only new threads resume after deletion.

With no marker, the component selects one rollout snapshot using the caller identity
in the MCP metadata. When multiple file names contain the thread ID, it decodes each
snapshot and requires exactly one with the matching thread and session header and
the consultation item under the matching turn context. Selection precedes full
history validation: an invalid matching snapshot cannot be discarded to resolve
ambiguity. Undecodable candidates fail explicitly. If this search finds zero or
multiple matching snapshots, it fails with `candidateCount` and `matchingCount`;
modification times do not select a snapshot. The selected bytes undergo the same
complete validation as a single-file snapshot, without rereading or merging files. Reconstruction stops
before the unfinished consultation item, including when that item is the host's
code-mode wrapper. The caller's tool inventory is not
forwarded. The server applies the routing profile's consultation mapping to the
caller's host-recorded dial. The component uses native Codex authentication. It
does not parse credential values or copy credential files.

The history policy table declares `preserve`, `capability`, `control`, `hosted`, or `reject` for each
known item and content block. It drives validation, injection, expected history,
and type-specific comparison normalization. Call/result pairs share one declaration.
`additional_tools` and the complete `tool_search_call`/`tool_search_output` pair
are capability declarations and enter neither injected nor expected history.
`configuration_update` and `compaction_trigger` are caller control items and also
enter neither injected nor expected history. `web_search_call`,
`image_generation_call`, and `local_shell_call` are hosted tool records: they are
validated, then enter neither injected nor expected history. `local_shell_call`
pairs with `function_call_output` through the same nonempty `call_id`; its result
is excluded with the call. A missing identity or a pair with only one excluded
member fails as `pairing`. Ordinary function call results remain preserved.
A `function_call_output` without a `call_id` is preserved as a standalone result
when it has a nonempty string `name` and an absent, null, or string `namespace`.
An empty `call_id` or an unmatched nonempty `call_id` still fails as `pairing`.
Standalone results do not complete pending calls; their names, namespaces, output,
and order must survive request comparison.
`context_compaction` and `other` are preserved.
Incomplete pairs fail. Undeclared item types and undeclared
content blocks are preserved verbatim; missing or changed payloads fail comparison.
Comparison removes item-level `id`, `internal_chat_message_metadata_passthrough`,
and null-valued fields from every type as transport normalization. Only declared
types receive type-specific normalization, including empty tool text blocks and
Lite image detail omission.
Every request must omit tools or carry an empty tool list, both at request level
and in every input item, regardless of its type. Non-Lite requests must prove an
empty tool set with `request.tools == []` or an `additional_tools` item whose
`tools == []`; only Responses Lite may omit both inventories. Declared shapes
require only protocol-required fields, plus pairing and opaque-content invariants;
optional fields may be absent.
History failures report `stage` (`record`, `item`, `content`, or `request`), `type`,
`recordIndex` and/or `historyIndex`, and `hostVersion` from `session_meta.cli_version`
when available. Comparison failures also report the first differing field `path`,
without field values or compared text. Unknown rollout records, retained events,
rollback, invalid declared shapes, and incomplete tool pairs still fail explicitly.

Native MCP startup filters the host environment. The plugin's `.mcp.json`
explicitly forwards `S2A_API_KEY` through `env_vars` for providers whose `env_key`
uses that name. The host process must already have the variable. Other provider
environment names require an explicit declaration in the source manifest and a
plugin update; they are not discovered from provider configuration or inherited
automatically. Do not store credential values in the manifest, add wildcard
inheritance, or patch the managed plugin cache. Native file/keyring authentication
continues to use the configured Codex home.

The routing profile maps host modes to comparison efforts. The current `ultra`
mode compares as `xhigh`. Qualified `retained_context` events are model-invisible
host bookkeeping: verified answers remain in their original tool results, and
compaction supplies the model-visible replacement history. Unknown event variants
still fail explicitly.

Replacement history may contain a `compaction` item with nonempty opaque
`encrypted_content`. The component preserves that item and its position when
injecting history. Request verification requires the encrypted content to match
exactly; missing, changed, or reordered compaction items fail as context loss.

Before passing any caller context, a native discovery process enumerates every
configured MCP server name through all inventory pages and then terminates with
its child processes. Discovery can start configured servers but receives no
caller context; tool/resource descriptions are discarded. A second native process
disables every discovered name, verifies that MCP capabilities and hooks are empty,
and disables built-in tools through the temporary model catalog and settings.
Every actual inference request must prove the expected model and effort and no
nonempty or malformed tool inventory at either location. Each `additional_tools`
item must contain `tools=[]`; a present top-level `tools` must equal `[]`.
When the selected native catalog enables `use_responses_lite`, omission of both
inventories also proves an empty tool set. Other catalog modes require at least
one explicit empty inventory. The temporary catalog sizes the tool-output byte
limit from the actual caller history so injection cannot shorten an existing result.
Every request must also retain the caller's base instructions, complete history,
consultation guidance, and final consultation request in order. Base instructions
must be in the top-level instruction field or the leading developer message;
silent automatic compaction is a context failure. Comparison permits removal of empty
text blocks from tool results and transport-only item fields. When the selected
native catalog enables `use_responses_lite`, comparison also permits omission of
the supported image `detail` hints (`auto`, `high`, and `original`) from messages
and tool results. Image URLs, bytes, text, and ordering must still match exactly;
other detail changes and omission without that catalog setting fail. Missing trace
evidence, a nonempty tool inventory, or any dial mismatch fails the consultation.

The advisor is asked for exactly one structured `plan`, `correction`, or `stop`.
Within the caller's existing session record, the tool-call event is **started**.
A returned MCP `structuredContent.status` of `succeeded`, with `isError=false`,
means the output has exactly one valid `kind` and nonempty `advice`, and every
observed request matched `expected` and `actual` model/effort. The result includes
`callerThreadId` and `advisorThreadId`. A returned `status=failed`, with
`isError=true`, carries `code`, `message`, `expected`, and `actual` where observed;
it contains no advice. Optional `details` locate the failing record or history
item and retain qualified native error codes and HTTP status without copying
history or arbitrary native error text. A qualified missing-environment error
also reports `reason=missing_environment_variable`, the bounded variable name in
`environmentVariable`, and an instruction to forward it through MCP `env_vars`.
No variable value is returned. Text content leads with readable advice or the
failure reason; `structuredContent` carries the machine-readable outcome.

Native failures include bounded `details.nativeExecution` diagnostics: the failing
phase, elapsed milliseconds, phase durations, the last recognized native event and
its time, the first text or reasoning delta time when observed, and the retry count.
A retry can include only a qualified native error code and HTTP status. Event names
outside the fixed diagnostic list appear as `other`; event bodies, output text,
request payloads, credentials, and arbitrary error messages are never retained.
`firstOutputMs` measures the first native text or reasoning delta observed by the
plugin, not the provider's first response. When cleanup and request verification
follow an execution failure, `totalElapsedMs` and the final phase durations cover
that work while `phase` and `elapsedMs` retain the original failure location.
These diagnostics survive temporary trace cleanup in the returned failure result.

Calls with a qualified host thread identity and no marker report `failureCount` and
`consultationDisabled`. The third cumulative failed call disables further
consultation for that thread. Successful calls do not reset the count. A disabled
thread receives `code=disabled` before reconstruction or native execution; the
caller stops consultation and continues authorized work with consultation marked
unavailable. User approvals and independent acceptance still apply.

Counts are stored atomically by thread ID in
`$CODEX_HOME/codex-advisor/consultation-failures.sqlite3`. The file contains only
thread IDs and bounded counts. Resuming a thread or restarting its MCP process keeps
the limit; another thread, including a child thread, has an independent count.
Existing counts of four remain readable and disabled without rewriting the database.
The initial schema is built in a private sibling file and published through an
atomic hard link, so concurrent readers cannot observe a partly initialized database.
An existing database is never replaced or repaired. Unsupported atomic publication
returns `failure_state`; the private initialization file is removed after the attempt.
The MCP tool declares `readOnlyHint=false` because failed calls update this state.
Calls whose cache layout or host identity cannot be qualified disable consultation
without assigning a counter to an unverified thread. Unavailable or malformed
counter storage disables consultation with
`code=failure_state` instead of starting an unbounded attempt.

Errors, aborts, cancellation, context overflow, empty or malformed output, and
mismatches all end in that failure result. Native `willRetry=true` notifications
wait for the same turn's terminal result within the existing deadline. The
component starts no additional consultation attempt. Failed inference also checks
available request traces to report observed model and effort. MCP
cancellation terminates the native process tree and returns failure. Cancellation
and deadlines remain effective while writing to a blocked native input pipe and
while consuming buffered completion events. Completed MCP requests release their
registry entries, and only active duplicate request IDs are refused. The native
execution deadline is 180 seconds. Catalogs, request traces, captured outputs,
logs, and native SQLite state stay in one temporary directory and are deleted when
the call finishes or is cancelled. Only the bounded failure counters persist. The
component writes no repository files, caller history, or credential files.

On Windows, consultation requires a native `codex.exe` on PATH or a unique native
executable in the official npm package layout beside `codex.cmd` on PATH. If the
first native executable's bundled catalog lacks the exact advisor model, the
component checks the bundled catalog of the distinct npm executable. The
component uses the selected executable for discovery and inference. It uses
`codex.cmd` only to locate the package. Windows Job Objects contain the native
process tree. An unavailable or failed containment or cleanup API returns an
explicit failure.

On Linux, a dedicated child subreaper owns each native process and reaps descendants
even when they leave the original process group. Shutdown terminates the native
process before closing a blocked input pipe. The supervisor allows ten seconds
for descendant cleanup; its caller allows twelve seconds for supervisor exit and
reports an explicit failure if cleanup cannot be established. Other POSIX platforms
use process-group cleanup; descendants that detach from the group are not contained.

The two-stage isolation adds one native initialization per call. Normal caller
startup must already have initialized its Codex home; consultation does not
bootstrap a fresh home. Requalify after host rollout, metadata, catalog, trace,
or cache-layout changes. Run `sh tests/verify.sh
--consultation` for deterministic MCP-boundary checks with a substitute native
executable. These checks do not establish live routing or installed-host behavior.
Run `python3 tests/verify-consultation-host.py` with the native Codex executable
available for real request construction against an unauthenticated loopback
endpoint. It covers long function/custom-tool results, empty text blocks, image
detail normalization in user messages and both tool-result types, and
recovery after a completed message precedes a stream failure, in a temporary home
without contacting a model provider. It also checks that a missing provider
environment variable produces a specific diagnostic before any HTTP request.

Run `python3 tests/verify-consultation-env.py` for changes to `.mcp.json` or native
launch. It installs a disposable local marketplace/plugin and starts its MCP
server through the real native host, using inert marker values. The check proves
that undeclared provider variables are filtered, the shipped declaration forwards
the required variable, and an unrelated variable stays excluded. It also exercises
the complete host-to-MCP-to-native consultation chain, using the host's own metadata
and rollout, and checks that the returned advice and temporary-state cleanup survive
the return path. Directly starting the Python MCP script does not exercise this host
environment boundary. These loopback checks establish no authenticated consultation
in an existing desktop session.

## Hooks

The plugin loads `hooks/hooks.json` from the default plugin location. After first
installation, the user reviews and trusts its hooks in `/hooks`, and reviews them
again after an update changes a hook definition. Installation does not grant trust;
the host skips untrusted hooks and prints a startup warning pointing to `/hooks`.
The plugin does not read or modify trust state. The `PreToolUse` route confirmation
and `PostToolUse` observed-dial confirmation identify separate checks; absence of
the corresponding line leaves that check unverified. An inspector pass establishes
no pre-call gate execution. A hook error, timeout, or untrusted definition cannot
enforce route admission; the caller must check eligibility manually and report
the automatic gate as unverified.
ADR-0006 records the trust boundary and the probe that exercised it.

`SessionStart` injects the exact selected canonical posture block and adoption
block, including on resume and compaction. It compares the session's exact model
id with the advisor model that the routing profile's consultation mapping
selects for it. The event carries no effort, so the hook applies the mapping at
every effort; if the selected advisor model depends on effort, missing selection
evidence leaves the work pending.
Native delegate identity excludes a second posture injection; entries carry their
own posture. Missing session identity also leaves the work pending.

`PreToolUse` matches `collaborationspawn_agent`, `collaborationfollowup_task`, and
`collaborationsend_message`. It reads the route declaration from the visible assistant
message immediately before the current call in the host transcript. The event's
session, turn, call ID, tool, and arguments must match that transcript, and the
declaration names the exact tool and target. An intervening message, tool call,
turn boundary, or compaction requires a fresh declaration. Completed calls cannot
reuse declarations. The native message remains opaque: the host forwards that
field in `agent_message.encrypted_content`, so the hook never parses its body.
It reads allowed dials from the routing profile and expected settings from the entry template, and
returns `permissionDecision: deny` on an invalid route. Admission basis kinds are
role-specific; Advisor acceptance mapping is an allowed basis in higher tiers.
It checks structure and compatibility, not whether the cited evidence is true or
the user authorized the work. Non-plugin spawns and resolved non-plugin targets
pass through. Unknown or ambiguous message targets are denied.

For continuation, the target is resolved from the caller's host session by UUID
or absolute/relative task path. The hook reads its role and all recorded turn dials,
requires a Worker, and compares the latest `response_item`, `event_msg`, or
`turn_context` timestamp with UTC now. An age from zero through 1800 seconds is
allowed; missing, invalid, naive, future, and expired times are denied. File mtime
and session creation time do not establish recent activity. New-ticket context
reuse and the lowest compatible tier remain caller judgments. The runtime rules
and route form are in [operations.md](../../plugins/codex-advisor/skills/orchestration/references/operations.md#declare-every-route).

`PostToolUse` joins the native response's task path and the parent transcript
identity to one child session header, then reads that child's host-recorded turn
model and effort. It waits at most two seconds for child evidence to appear. A
later unobserved write is never treated as a successful verification. On a match
it prints one confirmation line that names the entry and its host-recorded dial
and states that working directory and permissions were not checked; a dispatch to
a non-`ca_*` entry gets no output. The caller-facing meaning of its messages is in
[operations.md](../../plugins/codex-advisor/skills/orchestration/references/operations.md#read-the-dispatch-check).

These hooks write no files or persistent state, including Python bytecode. They
do not read configuration or credentials. The host-provided transcript directory
must use the qualified `sessions` layout; changed host event or transcript schemas
need renewed qualification. Consultation result validation is provided by the
consultation component.

## Windows launch

The hooks and the MCP server start `sh` with `scripts/run-python.sh`. On Windows
both commands look up `sh` on PATH, so Git for Windows' `bin` directory, which
holds `sh.exe`, must be on PATH; its `cmd` directory holds no `sh`.

On Windows, Codex runs a hook's `commandWindows` in place of `command`, through
PowerShell. Each `commandWindows` is its `command` with `$PLUGIN_ROOT` written
as `$env:PLUGIN_ROOT`; the hooks group checks this equality. When `CODEX_HOME`
is set, the host passes `PLUGIN_ROOT` in the `\\?\` form, which `sh` cannot open,
and the hooks fail. Without PowerShell, the host runs hook commands through
`cmd.exe`, which does not expand `$env:PLUGIN_ROOT`, and the hooks fail too.
[ADR-0010](../adr/0010-windows-launch-through-git-sh.md) records the host facts
behind these rules and when to re-check them.

## Verify a change

Select checks by the behavior the change touches. While editing one area, run its
focused group:

~~~sh
sh tests/verify.sh --installation
sh tests/verify.sh --runtime
sh tests/verify.sh --consultation
sh tests/verify.sh --hooks
~~~

The installation group covers the installer, the seventeen entry templates, the
manifest, and the routing profile's names/models/pins against those templates. It
also checks canonical posture equality, advisor exclusion, and same-role identity
outside the posture section, with negative fixtures. It includes a negative fixture
for a model mismatch and checks that other files in the target stay untouched.
The runtime group drives the inspector from all seventeen templates and covers its
options, template-derived expectations, rejection paths, and emitted metadata.
The consultation group exercises the MCP boundary with a substitute native
executable: complete context, routing, actual request validation, isolation,
outcomes, explicit failures, cancellation, and temporary-state cleanup. Separate
lifecycle checks cover request-ID reuse, malformed cancellation, native input
backpressure, buffered completion, and process startup failure. Linux checks also
cover detached descendants before and after their native parent exits. The hooks
group runs shipped commands with pinned JSON events, checking canonical injection,
delegate exclusion, all entry dials with the confirmation line on a match, delayed
child evidence, and explicit pending outcomes. Every surfacing case, confirmation
lines included, also rejects a disabled hook as a negative proof. It does not
establish installed-host trust or live dispatch behavior. A template change reaches
installation and runtime groups, so it takes the unqualified run. Documentation
changes have no group here: check structure, links, and whether the text still
matches actual behavior.

The hooks group also runs `verify-routing.py`: all entry dials, role-specific
bases, spawn and both continuation entrances, declaration binding and stale-declaration
refusal, target resolution, actual dial conflicts, and exact reuse-window boundaries.
Run `python3 tests/verify-routing-host.py --allow-hook-trust-bypass` after the user
authorizes the disposable-home hook trust bypass. It installs the current hooks
from a temporary local marketplace and drives the native host against a loopback
response service; only the unrelated MCP manifest is omitted. It verifies all
three native entrances, rejected calls, the child roles and dials, and unchanged
packet hashes in the children's encrypted content blocks. The provider returns
fixed responses and does not decrypt packets. These checks establish neither
user-reviewed hook trust nor authenticated model behavior. Qualification evidence
and untested boundaries live in the
[message-format issue](../../.scratch/native-route-message-format/issues/01-spawn-message-header-rejection.md).
Requalify after changes to the host's pre-call transcript flush, turn/call identity,
native tool schema, or agent-message transport.

Run the unqualified verifier once on the final state. It contains all four groups,
so it replaces the focused runs instead of following them:

~~~sh
sh tests/verify.sh
python3 tests/test_shipped_wording.py
git diff --check
~~~

The public scripts check safe installation, role allocations, bounded diagnostics,
and evidence consistency. Shell syntax and JSON/TOML parsing are the applicable
static checks; this project has no typed application. Fixtures establish parser
and refusal behavior, not model behavior.

## Check a route change live

For a route change, use a temporary `CODEX_HOME`, install through the public
installer, and spawn every affected entry once. Pass an effort only when the entry
leaves it to the caller, then run the inspector for that child. Record the entry,
effort passed, observed model and effort, sandbox and permission, child thread,
and inspector exit. These live checks establish dispatch and wiring; they do not
establish general quality, cost, or stability.

## Choose native scenarios

Select tiny disposable native scenarios from ordinary direct/delegated/mixed
completion, explicit Architect delegation, tiered exploration, complete versus
intermediate failure, repair/clarification, same-allocation rework, effort changes
both ways, process consultation, and independent acceptance. Exercise the scenarios
the change can break and record the rest as not exercised. Reuse actual calls and
metadata across checks; after a correction, repeat the affected checks rather than
the whole set. Record expected and observed behavior, native settings, IDs, sources,
permissions, tested revision and host, and unexercised paths in the feature
acceptance record.

## Adjust a routing value

Re-check the
[declared assumptions](../../plugins/codex-advisor/skills/orchestration/references/routing-profile.md#declared-assumptions)
and the account's callable dials. Then change the affected template's `model` or
`model_reasoning_effort` and the routing profile's table together, run
`sh tests/verify.sh`, and repeat the live route check for
every affected entry. Model-generation changes stay confined to the profile and
templates unless the role or tier contract also changes. Each model in the
segment table must reach one Advisor model at every effort, and each entry one Advisor
model at every effort it allows: `SessionStart` sees no effort, and an entry
carries a single posture.

A segment-only change updates the segment table without changing entry models
or efforts. Re-check the affected consultation mappings and canonical postures;
if a selected Advisor dial changes, repeat the affected live route checks.
