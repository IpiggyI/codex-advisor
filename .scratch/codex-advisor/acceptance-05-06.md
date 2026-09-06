# Tickets 05 and 06 acceptance

Date: 2026-09-06. Implementation base: `cc08d60e344bc4a0a01129c3a908806636542931`.
Scope: direct Sol implementation and native parallel implementation scheduling.

## Deterministic verification

The new installation check first failed for the absent Sol template, then passed
after adding the template and installer role. The new runtime check first failed
for the absent `--sol-effort` option, then passed after its implementation.
The installer suite covers all four active roles, selective non-mutating checks,
exact bytes, refusal before partial installation, and preservation of unrelated
configuration. Runtime fixtures cover Sol effort values and invalid input, wrong
roles/models, missing and conflicting settings/permissions, and payload filtering.
Existing Luna max and independent-review effort checks remain passing.

The complete `sh plugins/codex-advisor/scripts/verify.sh` suite passed, as did
plugin validation, skill validation, and `git diff --check`. JSON, TOML, YAML,
skill frontmatter, and Shell syntax checks are the applicable static verification;
this repository has no typed application. No new dependency or scheduler service
was introduced. Native host capacity and lifecycle interfaces perform scheduling.

## Ticket 05 live verification

Codex CLI `0.153.4` ran in a disposable installed home at
`/tmp/codex-advisor-05-06.ieyyf36b`. Marketplace/plugin installation and companion
role installation ran before fresh tasks. Scenario prompts, JSONL events, final
responses, and stderr use the scenario name below. Exact native rollouts are under
`home/sessions`; `observed.jsonl` contains projected routing and timing evidence.

| Scenario | Observed result | Native threads |
|---|---|---|
| `sol-default` | Astra primary low selected Sol directly at high for deny-by-default authorization repair. Sol changed only `policy.py`; the architect inspected all contents, reran the check, and obtained fresh Astra high review. | Primary `01a074f5-3497-78c3-be44-a1282432a0a5`; Sol `01a074f6-1105-7623-8443-6a80da6f7f89`; reviewer `01a074f8-6f91-7182-8913-7e5c46c46ab2` |
| `sol-adjusted` | The same higher-risk workflow honored explicit Sol medium while the Astra primary remained low. Architect checks and fresh Astra high review completed. | Primary `01a074f5-417c-7b12-b7f3-1f79fe8ac3f7`; Sol `01a074f6-0027-7c10-b479-cf6c022f73ec`; reviewer `01a074f7-aec8-7a60-98d3-a7055e8bc230` |
| `sol-primary` | Direct Sol remained low, changed `calc.py` itself, passed the meaningful check, and obtained fresh Astra high readiness advice in Advisor mode. | Primary `01a074f5-72c5-7f52-bcbd-542d64063f1e`; Advisor `01a074f6-8764-7d12-ae68-304f96b5ba23` |

Actual patches, architect inspections and reruns, and reviewer reads/checks were
inspected independently of final prose. Inspector calls for the exact child IDs
passed with the requested role/model/effort and parent linkage. Implementers did
not delegate further. Review calls used `fork_turns: none` after architect checks.
Before/after scoped contents and inventory confirmed that `check.py` and `peer.txt`
were preserved and review caused no scoped mutation. The root verifier also read
all final implementations and reran their authoritative checks successfully.

The access-policy fixture checks 64 combinations (4 roles, 2 ownership states,
4 actions, 2 suspension states). Its printed label incorrectly says 128; the
observed coverage is 64, not that label. Primary effort freedom is demonstrated
at low, and delegated Sol adjustment at medium; other recognized efforts have
parser coverage only, not demonstrated host/account support.

A separate installed home at `/tmp/codex-advisor-05-06.3m5wiz2t` withheld only the
Sol role. In `sol-unavailable`, primary `01a074ff-1f9a-74a2-b8d4-9c1e0bc94e5b`
observed the selective check's exit 1 and missing-role error, invoked no substitute,
and explicitly left implementation and acceptance pending. Exact workspace bytes
remained unchanged. This covers missing-role refusal, not a provider outage.

## Ticket 06 live verification

The final scheduling contracts were installed into a second disposable home at
`/tmp/codex-advisor-05-06.1xmf5ytc`. Each scenario has its own workspace, prompt,
JSONL log, final response, and native rollouts. All primary sessions ran Astra low;
all ten implementation workers ran native Luna max with correct parent linkage.
Every worker received ownership and verification requirements and returned a report.
No implementation worker spawned additional implementation work.

| Scenario | Observation | Primary thread |
|---|---|---|
| `parallel` | Two disjoint modules ran concurrently; both individual checks and the combined check passed after architect inspection. A user-requested fresh Astra high review then passed. | `01a074f7-808d-72c1-bc0a-fc1910807827` |
| `dependent` | A completed, then the architect inspected and reran A's check before dispatching B with the verified prerequisite. The combined check passed. | `01a074f8-2042-74c2-a815-3fa9c547a12a` |
| `conflict` | Two separate assignments owning `calc.py` ran sequentially despite available capacity. B preserved A's verified change. The combined check passed. | `01a074f9-797c-7190-bc56-0aee60428bcd` |
| `capacity` | Invocation with `-c agents.max_threads=1` exposed two total agents, leaving one worker slot. The parent obtained and checked the first report, released that worker, and dispatched the next. Both checks and the combined check passed. | `01a074f7-b43d-7281-b89e-13e4cb3a3c1d` |
| `incomplete` | Independent workers overlapped. Left completed; right reported partial because the immutable authoritative check required unavailable external certification. Parent inspection and reruns confirmed the gap and left whole-task acceptance pending. | `01a074f9-a537-7ab3-86aa-b4bf55ec101c` |

Native session start and task-complete timestamps establish actual scheduling:

| Scenario | First worker interval (UTC) | Second worker interval (UTC) |
|---|---|---|
| `parallel` | 04:27:00.291 to 04:29:30.176 | 04:27:53.777 to 04:29:42.802 |
| `dependent` | 04:27:37.380 to 04:30:09.496 | 04:30:43.721 to 04:32:03.633 |
| `conflict` | 04:29:09.470 to 04:30:25.221 | 04:31:03.145 to 04:32:31.721 |
| `capacity` | 04:27:09.822 to 04:30:05.048 | 04:30:34.121 to 04:31:59.639 |
| `incomplete` | 04:29:25.701 to 04:31:23.388 | 04:29:56.944 to 04:31:35.385 |

The parallel reviewer `01a074fb-68a8-71f0-9bb3-dc454c425bb1` started at
04:30:28.547, after both worker reports and architect checks. It used a fresh
context, read the actual files, and reran checks. The parent compared scoped state
after review and accepted the combined result. Protected files and user edits
remained unchanged in all five scenarios. The root verifier inspected every final
module and reran all combined checks: four passed, and `incomplete` exited 1 for
the expected external-certification gap. This expected refusal verifies the
workflow; the disposable task itself remains unaccepted.

During the dependent scenario, the parent initially imposed an incorrect exact
blank-line expectation on B's valid Python file. That verification command failed;
the parent corrected the expectation, reran it, and verified the protected state.
No implementation change was made for that verification-only mismatch.

## Evidence limits

These runs establish observed native workflow behavior on the stated host version,
not deterministic enforcement for every prompt. Recheck model/effort precedence,
role discovery, and capacity behavior after host or configuration changes. The
official custom-agent documentation endpoint returned HTTP 403; claims about this
host are based on exercised calls. Fixtures prove parser/refusal behavior, not
provider availability or live support for every accepted effort token.

Judgment agents received managed workspace-write permissions. Before/after scoped
state and tool activity establish behavioral read-only review, not enforced
isolation. Provider outages, host-capacity races, and enforced read-only isolation
were not exercised. Temporary paths are local evidence, not release assets.
Temporary authentication copies were removed from all three test homes after the
runs. The user's active installation, configuration, and credentials were unchanged.

## Code review

The code-review skill used independent read-only Standards and Spec agents against
`git diff --cached cc08d60e344bc4a0a01129c3a908806636542931`, adapting its usual HEAD
comparison to implement's review-before-commit order. Static review found no
implementation or standards issues. The Spec reviewer independently confirmed
ticket 05's live patches, routing, checks, review timing, and primary freedom. Its
ticket 06 follow-up independently confirmed all ten Luna runtimes, actual overlap
and sequencing, parent inspections and checks, incomplete-result handling, and
the combined independent review. Both axes finished with zero implementation
findings; no requested live acceptance scenario remains unrun.
