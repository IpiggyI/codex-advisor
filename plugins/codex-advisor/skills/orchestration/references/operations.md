# Native operations

## Install and discover

The plugin supplies `codex-advisor:orchestration`. Its companion installer supplies
`codex_advisor_astra_advisor`. Resolve scripts from the installed skill directory:

~~~sh
skill_dir=<directory-containing-SKILL.md>
installer="$skill_dir/../../scripts/install-agents.sh"
runtime_inspector="$skill_dir/../../scripts/inspect-agent-runtime.sh"
sh "$installer" --check-role advisor
~~~

Run this non-mutating selective check before the first consultation. It ignores
unrelated roles, including conflicting files from another installation. Cache success
only for the current task; recheck after installation or configuration changes.
A check failure pauses the consultation until the user reconciles the installation.

For a disposable development installation, create an empty temporary directory and
pass it as `--target-dir`. To validate host discovery, run marketplace and plugin
installation in a temporary `CODEX_HOME`, install roles into that home's `agents`
directory, and start a fresh task. Keep the user's active environment unchanged.
Use only the connection settings and authentication needed for a live test; keep
credentials out of reports and remove temporary credential copies after testing.

The installer performs preflight checks before writing files. Exact destinations
remain unchanged. Modified, conflicting, nonregular, and symlinked destinations or
ancestors are refused. Dot path segments and the filesystem root are refused.
Use `--check` for all shipped roles or repeat `--check-role advisor` as needed.
Neither check creates directories or changes files. The installer does not migrate,
delete, or rewrite an upstream installation or primary-session configuration.

## Invoke Astra with an adjustable effort

Use the native spawn tool with a fresh context:

~~~text
agent_type: codex_advisor_astra_advisor
fork_turns: none
reasoning_effort: high
message: <complete decision packet from role-contracts.md>
~~~

Always supply effort. Replace `high` with an explicit user-requested effort that
the current host supports for Astra. The role file pins `gpt-6-astra` and omits
`model_reasoning_effort`: native role settings take precedence over spawn values,
so putting a default effort in the file would defeat a permitted adjustment.
Do not change the role file, the primary model, or global configuration to adjust
a consultation. If the host cannot express or honor the request, pause that call.

The inspector recognizes `low`, `medium`, `high`, `xhigh`, `max`, and `ultra`
as evidence values. This is input validation, not proof that the current host or
account supports every value. Require an accepted native call and observed settings.

## Validate the actual call

Public spawn/details metadata is authoritative. Confirm the exact native role,
actual model `gpt-6-astra`, and requested effort. Use the narrow inspector for
fields omitted by public metadata, never to override conflicting public evidence:

~~~sh
sh "$runtime_inspector" --advisor-effort high <native-thread-id>
~~~

Pass the actual requested effort. For a disposable session root:

~~~sh
sh "$runtime_inspector" --sessions-dir /absolute/path/to/sessions --advisor-effort medium <native-thread-id>
~~~

The inspector reads exactly one matching rollout and emits only routing metadata.
It refuses invalid IDs, absent or ambiguous records, missing required settings,
contradictory model/effort/permission evidence, and mismatched Advisor settings.
It does not emit prompts, credentials, or unrelated session messages.
Its default form without `--advisor-effort` reports generic metadata without
certifying a consultation. Parser success alone does not prove that advice was
returned or that the primary agent checked it.

Compare local and public evidence when both exist. Any contradiction, unavailable
Astra, failed call, or unresolved required evidence pauses the affected step.
Report what is missing; do not accept a substitute or a model's self-description.

## Observe permissions

The Advisor requests a read-only sandbox. The host can reapply broader parent
permissions. Capture the actual sandbox policy and permission profile, and inspect
the relevant tool activity and exact before/after scoped file and artifact state.

- If the host enforces read-only access and the observed behavior supports that
  boundary, report it as enforced isolation.
- Under broader permissions, proceed only when hard isolation is not required,
  the prompt prohibits edits, and before/after state confirms no scoped mutation.
  Report behavioral read-only operation under those broader permissions.
- Missing or conflicting permission evidence, required but unavailable isolation,
  or an observed mutation pauses the consultation. Do not hide a mutation or claim
  enforced isolation from the TOML request alone.

Unchanged files establish only the observed scope. They do not prove that a
broader-permission host prevented all writes.

## Verify a release

From the repository root:

~~~sh
sh plugins/codex-advisor/scripts/verify.sh --installation
sh plugins/codex-advisor/scripts/verify.sh --runtime
sh plugins/codex-advisor/scripts/verify.sh
git diff --check
~~~

The focused groups cover installer behavior and runtime evidence respectively.
The full entry point also validates shell syntax. JSON and TOML parsing replace
typechecking for this shell-and-metadata project; no typed application is shipped.
Documentation consistency checks are not evidence of model behavior.

Use the ticket acceptance matrix in a disposable installed host for live discovery,
primary-effort freedom, ordinary Astra solo work, consultation triggers, explicit
Advisor effort adjustment, disagreement, and unavailable or unobservable consultation.
Record actual model, effort, permission evidence, primary response, and unrun cases
in the ticket acceptance record. Fixtures validate parsing and refusals; only live
calls can validate host routing and model-dependent workflow behavior.
