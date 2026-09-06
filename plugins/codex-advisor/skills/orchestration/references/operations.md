# Native operations

## Install and discover

The plugin supplies `codex-advisor:orchestration`. Its companion installer supplies
`codex_advisor_astra_advisor`, `codex_advisor_luna_implementer`, and
`codex_advisor_astra_reviewer`.
Resolve scripts from the installed skill directory:

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
Use `--check` for all shipped roles or repeat `--check-role advisor`,
`--check-role luna`, and `--check-role reviewer` for the required calls.
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
contradictory model/effort/permission evidence, and mismatched requested-role settings.
It does not emit prompts, credentials, or unrelated session messages.
Its form without a role option reports generic native-child metadata without
certifying a contract. Parser success alone does not prove that advice was returned
or that the primary agent checked it. The child inspector is not a primary-session
resolver. If public metadata omits primary settings, read only the current thread's
resolved `model` and `effort` from its applicable `turn_context`; do not dump session
contents or infer current settings from another thread or an earlier turn.

Compare local and public evidence when both exist. Any contradiction, unavailable
Astra, failed call, or unresolved required evidence pauses the affected step.
Report what is missing; do not accept a substitute or a model's self-description.
Match the evidence to the returned native thread ID and its actual parent. Confirm
the fresh-context invocation from the spawn arguments, not from the agent's prose.

## Invoke and accept Luna implementation

Check `--check-role luna` before the first implementation call. Use native spawn:

~~~text
agent_type: codex_advisor_luna_implementer
fork_turns: none
reasoning_effort: max
message: <complete implementation specification from role-contracts.md>
~~~

The role pins `gpt-5.6-luna` and `max`; this mandatory delegated setting may override
a spawn value. It does not modify the primary session. Confirm the actual settings
through public metadata, supplemented by the narrow inspector:

~~~sh
sh "$runtime_inspector" --luna <native-thread-id>
~~~

Missing, conflicting, or mismatched evidence pauses acceptance without certifying
implementation. Inspect all actual changes and rerun the specification's key checks.
Use a new or resumed Implementer for corrections; the architect remains responsible
for the verification after each correction. A worker's report is a claim to check.

## Select and invoke independent Astra review

After the architect inspects the complete changes and reruns key verification,
check `--check-role reviewer`. Resolve the current primary's actual Astra model and
effort from host evidence. Missing or conflicting evidence pauses required review.

Use the inspector to select effort before calling the reviewer:

~~~sh
primary_effort=<resolved-primary-effort>
review_effort=$(sh "$runtime_inspector" --select-review-effort --review-primary-effort "$primary_effort")
~~~

Stop if selection fails. The established order is `low`, `medium`, `high`, `xhigh`,
`max`. Defaults are `high` for the first three, `xhigh` for primary `xhigh`, and
`max` for primary `max`. For an explicit adjustment, add `--reviewer-effort` with
the requested value to selection and later validation. The selector permits an
explicit value at or above the primary, including `low` or `medium` when that
floor permits it. It rejects unknown orderings, including `ultra`, instead of
guessing from a display label. This pauses review, not use of that primary effort.
The recognized order is not proof of host/account support: confirm native-call
support and actual settings. Never silently replace an unsupported setting.

Capture the exact scoped file and artifact state, then use native spawn:

~~~text
agent_type: codex_advisor_astra_reviewer
fork_turns: none
reasoning_effort: <selected review_effort>
message: <complete review packet from role-contracts.md>
~~~

The role pins Astra and leaves effort to the invocation, so role configuration
cannot silently replace the selected effort with a fixed lower default. Use a new
thread for each independent review. Confirm the returned thread, parent linkage,
fresh invocation, model, and effort through public metadata and the inspector:

~~~sh
sh "$runtime_inspector" --review-primary-effort "$primary_effort" <native-thread-id>
~~~

If selection used an explicit `--reviewer-effort`, repeat it here. The inspector
requires the distinct reviewer role, `gpt-6-astra`, the selected effort, and
observable permissions. Supplied primary effort remains a caller claim until
matched to the current primary's actual evidence. Compare public and local metadata;
any contradiction, unavailable call, or missing evidence pauses required review.

Compare the exact before/after scoped state and reviewer tool activity. A mutation
or an unmet isolation requirement keeps review pending; report it explicitly. Check
the review's actual diff inspection and verification evidence before accepting its
judgment. Consultation and upstream Sol review cannot substitute for this contract.

## Observe permissions

The Advisor and Independent reviewer request a read-only sandbox. The host can
reapply broader parent permissions. Capture the actual sandbox policy and permission
profile, and inspect tool activity and exact before/after scoped file and artifact state.

- If the host enforces read-only access and the observed behavior supports that
  boundary, report it as enforced isolation.
- Under broader permissions, proceed only when hard isolation is not required,
  the prompt prohibits edits, and before/after state confirms no scoped mutation.
  Report behavioral read-only operation under those broader permissions.
- Missing or conflicting permission evidence, required but unavailable isolation,
  or an observed mutation pauses the consultation or review. Do not hide a mutation
  or claim enforced isolation from the TOML request alone.

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
For Architect work, cover authorization lifetimes, Luna edits and corrections,
worker-evidence rejection, ordinary completion, required review, effort floors and
overrides, required-review failure, and the observed judgment permission boundary.
Record actual model, effort, permission evidence, primary response, and unrun cases
in the ticket acceptance record. Fixtures validate parsing and refusals; only live
calls can validate host routing and model-dependent workflow behavior.
