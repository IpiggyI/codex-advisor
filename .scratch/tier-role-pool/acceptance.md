# Acceptance record: tier-named native entries (0.2.0)

Recorded 2026-09-17 by the primary. Host: `codex-cli 0.154.0` on WSL; provider `official` from the user's `config.toml`; parent model `gpt-6-astra` at `low` (the user's default). Working tree at tickets 01–06 accepted, before ticket 07.

## Live route check (eleven entries)

Method: a temporary `CODEX_HOME` received copies of `auth.json` and `config.toml` and the eleven templates through `install-agents.sh --target-dir`; a scratch workspace held a two-line `README.md`; one `codex exec --sandbox read-only` run per entry asked the parent to spawn exactly one subagent of that entry with `fork_turns none` (passing `reasoning_effort` only for the six caller-selected entries) and to report the file's first line; the child rollout was located by `agent_role` and read with `inspect-agent-runtime.sh --sessions-dir … --agent <name> [--effort <e>]`. The temporary home, the credential copies, the workspace, and the logs were deleted afterwards.

| Entry | Effort passed | Observed model | Observed effort | Sandbox / permission | Child thread | Inspector |
|---|---|---|---|---|---|---|
| `ca_explorer_light` | high | gpt-5.6-luna | high | read-only / managed | 01a0ab15-d019-7ad0-9413-12de29c51eaf | exit 0 |
| `ca_explorer_standard_m` | (pinned) | gpt-5.6-luna | max | read-only / managed | 01a0ab16-e0ff-7ce3-95b3-c88115e40773 | exit 0 |
| `ca_explorer_standard_h` | medium | gpt-5.6-terra | medium | read-only / managed | 01a0ab17-8ab8-7380-a40c-1c8c99b10fac | exit 0 |
| `ca_explorer_senior` | medium | gpt-5.6-sol | medium | read-only / managed | 01a0ab17-e0ad-7341-b4d8-bbf7bdf93451 | exit 0 |
| `ca_worker_light` | (pinned) | gpt-5.6-luna | max | read-only / managed | 01a0ab18-330e-7f13-9944-44efbf6cdb48 | exit 0 |
| `ca_worker_standard_m` | high | gpt-5.6-sol | high | read-only / managed | 01a0ab18-a2fe-71a2-bf3d-613185fb2c94 | exit 0 |
| `ca_worker_standard_h` | (pinned) | gpt-6-astra | low | read-only / managed | 01a0ab18-fc17-7b23-b70c-a1c415dcb248 | exit 0 |
| `ca_worker_senior` | medium | gpt-6-astra | medium | read-only / managed | 01a0ab19-4e18-7772-b6d1-f69ae563aa80 | exit 0 |
| `ca_advisor_light` | (pinned) | gpt-6-astra | low | read-only / managed | 01a0ab19-a580-79e2-91a4-73030ed6b232 | exit 0 |
| `ca_advisor_standard` | (pinned) | gpt-6-astra | medium | read-only / managed | 01a0ab1a-09f9-7ad3-9334-ab193ffb2a84 | exit 0 |
| `ca_advisor_senior` | high | gpt-6-astra | high | read-only / managed | 01a0ab1a-7676-7cb1-9401-6819e8dd3564 | exit 0 |

Every run exited 0 and the parent's reply carried the child's answer (the fixture's first line). Every child rollout's `parent_thread_id` was the run's parent session and `cwd` was the scratch workspace. Parent token usage per run ranged from about 1,000 to about 20,000.

What this establishes: each entry is discoverable by name after installation, spawns with the template's `model`, and runs at the pinned effort or the passed effort. `gpt-5.6-terra` and Luna at `max` are callable on this account; Luna `xhigh` was not exercised.

What this does not establish: enforced isolation (the observed `read-only` sandbox came from the parent's `--sandbox read-only`; `permission_profile_type` was `managed`), quality, cost, or stability; the `[agents]` defaults path (none set in the copied `config.toml`); behaviour under an interactive session rather than `codex exec`.

## Deterministic checks at acceptance of ticket 06

- `sh plugins/codex-advisor/scripts/verify.sh`: installation and runtime groups pass (manifest-driven installer with overwrite, retire, drift and residue checks; profile-to-template names and models; same-role identical instructions; pinned set; table-driven inspector cases; payload filtering).
- `python3 tests/test_zh_mirror.py`: 26/26 (four Markdown twins, eleven TOML twins by existence, eleven by key equality and Chinese prose).
- `python3 tests/test_version_manual.py`: 3/3 for the current `0.1.0` (ticket 07 bumps and adds the 0.2.0 manual).

## Code review (two axes, codex lane report mode, `gpt-6-astra[low]`, 2026-09-17)

Both lanes returned `complete` receipts (sessions `01a0ab26-3e55-7fe1-aae1-43e6fbdc6f9b` standards, `01a0ab26-3e55-7980-b81a-1bee98ce9e34` spec; `dirty_baseline: true`, so the read-only tool set was the only guard). Dispositions:

- Standards, hard: a symlink at a retired filename was deleted instead of refused (installer preflight exempted symlinks) → rework on the scripts lane; preflight now refuses any non-regular entry at a retired name and the removal loop deletes regular files only; verifier case added.
- Standards, hard: the 0.2.0 manual omitted `codex plugin marketplace upgrade` and the per-side reinstall order required by `AGENTS.md` → rework on the docs lane; the manual now lists the full sequence.
- Standards, judgement: duplicated existence-check block in `tests/test_zh_mirror.py` → noted, not changed.
- Standards, contract gap: the glossary's Routing profile `_Avoid_` forbade any dial value in a TOML description while the spec requires a pinned entry to name its fixed effort → glossary wording narrowed by the primary.
- Spec, missing: ticket 07 did not list the release commands → added to the ticket by the primary.
- Spec, missing: README repeated an effort value in the inspector example → rework; the example now uses the pinned `ca_worker_light`.
- Spec, wrong: the verifier hardcoded the pinned set and the entry count → rework; both are now derived from the routing profile only (negative proof: an unpinned template given an effort fails naming the entry).
- Spec, scope creep: none found.

After the reworks: `verify.sh` both groups, `tests/test_zh_mirror.py` 26/26, `tests/test_version_manual.py` 3/3, `git diff --check` clean.
