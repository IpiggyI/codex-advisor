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
[ADR-0008](../adr/0008-installer-deletes-no-old-filenames.md) records why the
installer deletes no old filenames and when to revisit that.

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

The component reads exactly one rollout snapshot matching the caller identity in
the MCP metadata and stops before the unfinished consultation item, including when
that item is the host's code-mode wrapper. The caller's tool inventory is not
forwarded. The server applies the routing profile's consultation mapping to the
caller's host-recorded dial. The component uses native Codex authentication and
never reads, copies, or transmits credentials.

Before passing any caller context, a native discovery process enumerates every
configured MCP server name through all inventory pages and then terminates with
its child processes. Discovery can start configured servers but receives no
caller context; tool/resource descriptions are discarded. A second native process
disables every discovered name, verifies that MCP capabilities and hooks are empty,
and disables built-in tools through the temporary model catalog and settings.
Every actual inference request must prove the expected model and effort, an empty
`additional_tools.tools` or explicit top-level `tools=[]`, and no nonempty tool
inventory at either location. Every request must also retain the complete caller
history in order; silent automatic compaction is a context failure. Missing trace
evidence, a nonempty tool inventory, or any dial mismatch fails the consultation.

The advisor is asked for exactly one structured `plan`, `correction`, or `stop`.
Within the caller's existing session record, the tool-call event is **started**.
A returned MCP `structuredContent.status` of `succeeded`, with `isError=false`,
means the output has exactly one valid `kind` and nonempty `advice`, and every
observed request matched `expected` and `actual` model/effort. The result includes
`callerThreadId` and `advisorThreadId`. A returned `status=failed`, with
`isError=true`, carries `code`, `message`, `expected`, and `actual` where observed;
it contains no advice. The text content repeats that same structured object so
the caller and session hooks can read the identical outcome.

Errors, aborts, cancellation, context overflow, empty or malformed output, and
mismatches all end in that failure result. No automatic retry is made. MCP
cancellation terminates the native process tree and returns failure. The native
execution deadline is 180 seconds. Catalogs, request traces, captured outputs,
logs, and SQLite state stay in one temporary directory and are deleted when the
call finishes or is cancelled. The component writes no session markers, repository
files, or credential files.

On Windows, consultation requires a native `codex.exe` on PATH or a unique native
executable in the official npm package layout beside the discovered Codex shim.
It does not execute `.cmd` wrappers with configuration arguments. Windows Job
Objects contain the native process tree; unavailable or failed containment and
cleanup APIs return an explicit failure.

The two-stage isolation adds one native initialization per call. Normal caller
startup must already have initialized its Codex home; consultation does not
bootstrap a fresh home. Requalify after host rollout, metadata, catalog, trace,
or cache-layout changes. Run `sh tests/verify.sh
--consultation` for deterministic MCP-boundary checks with a substitute native
executable. These checks do not establish live routing or installed-host behavior.

## Hooks

The plugin loads `hooks/hooks.json` from the default plugin location. After first
installation, the user reviews and trusts its hooks in `/hooks`, and reviews them
again after an update changes a hook definition. Installation does not grant trust;
the host skips untrusted hooks and prints a startup warning pointing to `/hooks`.
The plugin does not read or modify trust state. The `PostToolUse` confirmation line
makes a skipped hook visible for each dispatch, as the absence of any message.
ADR-0006 records the trust boundary and the probe that exercised it.

`SessionStart` injects the exact selected canonical posture block and adoption
block, including on resume and compaction. It compares the session's exact model
id with the advisor model that the routing profile's consultation mapping
selects for it. The event carries no effort, so the hook applies the mapping at
every effort; if the selected advisor model depends on effort, missing selection
evidence leaves the work pending.
Native delegate identity excludes a second posture injection; entries carry their
own posture. Missing session identity also leaves the work pending.

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
outcomes, explicit failures, cancellation, and temporary-state cleanup. The hooks
group runs shipped commands with pinned JSON events, checking canonical injection,
delegate exclusion, all entry dials with the confirmation line on a match, delayed
child evidence, and explicit pending outcomes. Every surfacing case, confirmation
lines included, also rejects a disabled hook as a negative proof. It does not
establish installed-host trust or live dispatch behavior. A template change reaches
installation and runtime groups, so it takes the unqualified run. Documentation
changes have no group here: check structure, links, and whether the text still
matches actual behavior.

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
ordering must reach one Advisor model at every effort, and each entry one Advisor
model at every effort it allows: `SessionStart` sees no effort, and an entry
carries a single posture.
