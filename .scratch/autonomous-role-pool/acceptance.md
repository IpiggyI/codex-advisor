# Autonomous role pool acceptance

Date: 2026-09-12. Implementation base and approved review baseline:
`f170eef80734e9140231defcd87a91281549ba3d`.
Scope: tickets 01–04, with dependencies 01 → 03 → 04 and independent ticket 02.

## Tested source and host

Codex CLI `0.154.0` ran four disposable installations under
`/tmp/codex-advisor-autonomy.k0ekgvjh`. Each used the public marketplace/plugin
installation and companion role installer before starting a fresh task.
The tested plugin source digest covers every regular file under
`plugins/codex-advisor/`, sorted by its repository-relative path. SHA-256 receives
each UTF-8 path, NUL, file bytes, and NUL in that order. The digest is
`a8faf34269afc646cfd763aacc922fbc6889fcae00871b3dd9e5c214153560de`.

The installed policies, role templates, installer, and runtime inspector matched
the final source modulo trailing blank lines normalized after installation. The
deterministic verifier's shared invalid-effort helper was refactored after live
checks and its affected runtime group passed again. Historical acceptance
records were preserved. No active installation, primary configuration, release,
provider bridge, scheduler, or profile schema was changed.

Each scenario directory contains its prompt, events, final response, workspace,
and native rollouts under `home/sessions`. The local `audit.py` independently
checks completed native calls, explicit spawn settings, parent association,
working directory, thread reuse, and actual final bytes. Its allowlisted projection
is `observed.json`; raw transcripts and credentials are not committed.

| Scenario | Primary model / effort | Parent UUID |
|---|---|---|
| workers | Sol / medium | `01a0940e-a9b7-7300-aa89-47cc898affb0` |
| explorers | Sol / medium | `01a0940e-a9b7-73b3-bb4d-04c9d74ff651` |
| advice | Sol / max | `01a0940e-a9b7-7b00-9c76-4e3241f7cd5f` |
| branches | Sol / medium | `01a09416-8d9c-75d0-8d0d-c13c97f48764` |

Parent settings came from their own turn metadata, independently of child reports.
Every child used explicit effort and `fork_turns: none`; runtime inspection
matched role/model/effort, UUID, expected parent, workspace, and permissions.
All observed children had `workspace-write` / `managed` permissions.
No child delegated implementation further.

## Deterministic checks

The changed public checks first failed against the old behavior: Sol accepted
unlisted low effort; the two new Explorer templates were absent; Luna Explorer
accepted low; and primary-derived reviewer selection still succeeded.
After the corresponding changes, focused installation/runtime checks passed.
The full `sh plugins/codex-advisor/scripts/verify.sh` suite then passed once on
the combined implementation. Shell syntax, TOML/JSON/YAML parsing, skill frontmatter,
documentation links, and `git diff --check` passed.

Coverage includes all eight installed identities, full/selective/repeated checks,
refusal before partial writes, preservation of unrelated configuration, exact
native allocation validation, obsolete reviewer-selector refusal, missing parent
or cwd evidence, malformed/ambiguous/conflicting records, and payload filtering.
Fixtures certify parser and refusal behavior, not successful advisory judgment or
failure eligibility. No typed application or typechecker is shipped.

## Tickets 01 and 03: work, recovery, and sessions

The primary created and checked `direct.txt`, selected Luna autonomously for a
bounded light outcome, dispatched standard workers for disjoint files, inspected
actual outputs, and reran a combined exact-byte check with a negative control.
The ordinary multi-step workflow completed without an Advisor or reviewer.
Task specifications did not activate Architect mode.

| Worker | Observed effort | Native UUID | Observed outcome |
|---|---|---|---|
| Luna light | max | `01a0940f-5f43-76b2-9ff7-05b565e12b87` | `light.txt = LIGHT\n` |
| Sol standard | high | `01a0940f-affc-75b3-b208-a70783a1e65a` | `standard-high.txt = STANDARD-HIGH\n` |
| Sol standard | xhigh | `01a0940f-e043-76d1-8b2a-141348128c42` | First attempt; `standard-xhigh.txt = STANDARD-XHIGH\n` |
| Astra senior | medium | `01a09410-df2c-7f82-958f-70155aa93b4b` | Missing-gate inability; same-thread correction after environment repair |
| Astra senior | high | `01a09412-d28c-7f92-a1ba-3e7ab3fdfee3` | New writer extends actual artifact after prior writer finishes |
| Astra senior | medium | `01a09413-9f83-7743-b26c-c24cc06ef6f7` | New thread on effort decrease; useful prior changes preserved |
| Astra senior | xhigh | `01a09414-8b65-7ed2-9f7f-95f816c8b6a7` | Eligible controlled same-work handoff; final verification line added |

The controlled gate belonged exclusively to the primary. Its absence produced a
completed concrete inability report, with no invented pass or unauthorized gate
creation. The primary diagnosed the environment, supplied `OPEN\n`, and resumed
the same medium worker. Native metadata contains two completed turns at unchanged
medium in that thread.

An explicit Architect-mode phase then began under the Sol primary. All subsequent
implementation edits were delegated. The real transition was medium
`01a09410-df2c-7f82-958f-70155aa93b4b` → high
`01a09412-d28c-7f92-a1ba-3e7ab3fdfee3` → medium
`01a09413-9f83-7743-b26c-c24cc06ef6f7`.
Each successor received current bytes, scope, binding decisions, completed checks,
the diagnosed failure, and remaining work after the earlier writer finished.
The final exact content was `READY\nHIGH\nMEDIUM\nVERIFIED\n`.

The xhigh call carried relevant complete worker failure and its repaired environment
cause; it was selected for the smoke route, not because the failure demonstrated
weak reasoning. An unavailable Ruby command during the medium extension was
handled with shell byte checks in that same attempt, without escalation.
Git history was absent in these disposable workspaces; complete contents, inventories,
hashes, and exact-byte checks supplied the actual-state evidence.

Existing scheduling evidence in [acceptance-05-06.md](../codex-advisor/acceptance-05-06.md)
covers capacity, dependencies, conflicting ownership, and incomplete sibling output
under the preserved native scheduling boundary. Current independent worker dispatch,
sequential gated ownership, and combined checks supplement it. Historical effort
and mode policies from that record are superseded, not reused as current acceptance.

## Ticket 02: exploration

Every Explorer inspected the same 105-byte `source.py`. Line 2 multiplies the
amount by `1.2`; lines 4–5 add the fee afterward. All six cited the actual source
and returned `total(10, 3) = 15`. Calling the multiplier tax was labeled as an
interpretation of the question. The source scope and negative-search limits were
explicit; no broader absence claim was needed.

| Explorer | Effort | Native UUID |
|---|---|---|
| Sol, directly selected before any Luna | medium | `01a0940f-3056-7133-bef9-76897d394daf` |
| Luna light | high | `01a09411-3bff-7773-a3c0-24690232fdf1` |
| Luna preferred substantial | max | `01a09411-5513-7d31-a6e2-2b6a07d10969` |
| Sol | high | `01a09411-6d1a-7853-9530-976d4c974e5b` |
| Astra | medium | `01a09411-84ed-78d3-9f8b-c9a87bb6e116` |
| Astra | high | `01a09413-3a2f-7f52-859f-0d7f2c785ea9` |

Each Explorer used one source-read command, `nl -ba source.py`. The source
SHA-256 stayed
`61468bd3f109c5b3c6db68082cc61ce2dbe3df6e0428fe3bc85bb8340d3a670f`;
the final inventory contained only that file. The primary and root verifier checked
citations, bytes, and the result independently.

## Ticket 04: advice and independent acceptance

| Request | Effort | Native UUID | Observed outcome |
|---|---|---|---|
| Proactive decision advice | medium | `01a0940f-fd5e-7081-bf8c-6b2181829661` | Correct original fee explanation; advice reused while hashes/inputs held |
| Invalidated premise | high | `01a09412-9a60-7000-b39e-b97d3875023a` | Correct revised fee explanation and result 15.6 |
| Injected failed advice | medium | `01a09414-093e-77d0-b113-7db6102d3b54` | Deliberately unsupported old conclusion, refuted by source/calculation |
| Same-question advisory recovery | xhigh | `01a09415-03de-7421-a388-c0951f0f5ae5` | Correct source-backed answer after relevant failed advice |
| Declared high-risk acceptance | medium | `01a09417-3c05-7cd2-bd38-6d657ba5eb96` | Ready after primary checks, despite primary max |
| Explicit revised-deliverable review | high | `01a09418-e36a-7ec1-9239-1e59c949693f` | New thread; ready after adding checked note |
| Injected failed review | medium | `01a0941a-6035-7722-9c63-cb55c55a3790` | Unsupported old acceptance condition refuted |
| Same-question review recovery | xhigh | `01a0941b-6760-79e0-8b2c-5225692d89de` | Fresh source-backed acceptance with advisory-failure evidence |
| Uncovered decision and unclear failure cause | medium | `01a09417-40bf-7b62-9f58-030de5380ec1` | Required advice dispatched; missing failure facts identified without inventing a cause |
| Incomplete artifact review | medium | `01a09419-1fe7-7fc1-9ecd-e55572372d8a` | Actual DRAFT/VERIFIED mismatch reported; acceptance blocked |
| Corrected artifact review | medium | `01a0941a-4dec-79b1-8fa7-dc58726cec8a` | New thread at unchanged effort after primary correction and passed check |

The ordinary checkpoint needed no delivery consultation. Changing the source to
`subtotal(amount + fee)` invalidated the earlier advice, leading to renewed
judgment. The primary distinguished a hypothetical policy disagreement from factual
evidence and did not turn advice into authorization.

The two injected advisory conclusions were explicitly labeled test-double responses
with no source support. The primary refuted them using the actual source and
calculation, diagnosed the false premise, and handed that same-question evidence
to fresh xhigh calls. These demonstrate controlled eligibility and dispatch,
not spontaneous failures or evidence that more effort improved judgment.

Independent acceptance used the distinct reviewer identity and actual complete
contents after primary checks. In the branches scenario, the primary's deliberate
`DRAFT\n` failed the exact `VERIFIED\n` condition; the first reviewer reproduced
the failure. The primary corrected the bytes and passed verification before a
different medium reviewer accepted. This establishes review freshness even without
an effort change. The root independently verified all final fixture contents.

Reviewer and Advisor activity consisted of source reads, inventories, hashes, and
checks avoiding bytecode writes; the two injected failures used no tools. Scoped
before/after checks showed no role-authored mutation. This establishes behavioral
read-only operation under broader permissions, not hard isolation.

## Controlled policy probes and limits

Short primary probes returned the expected responses for ineligible initial Astra
xhigh, intermediate debugging failures, unclear behavior requiring clarification,
known reasoning failures allowing cause-based rework/takeover, worker failure
being insufficient for Advisor xhigh, missing/conflicting required review leaving
acceptance pending, invalid effort-changing resume, and advice reuse despite a
failure count. These were supplied policy cases, not live provider failures.

All advertised model/effort allocations were exercised. No primary/transport Cartesian
matrix, real destructive migration, provider outage, hard read-only enforcement,
or general task-quality evaluation was run. Remaining limits are those deliberate
boundaries; simple route checks do not prove quality, long-run stability, or savings.

Initial hosts saw WebSocket disconnects and native HTTPS fallback. The final branch
host used the documented provider `supports_websockets=false` setting and omitted
inherited outer thread-ID variables. This was confined to disposable host setup;
actual UUIDs were obtained from native records rather than shell variables.
See the [official configuration reference](https://developers.openai.com/codex/config-reference/).
Temporary evidence paths may be removed by later system cleanup.
All four primary scenarios exited successfully. Temporary authentication and
connection-configuration copies were removed from their disposable homes afterward.

## Code review

The user approved the implementation base above. Review uses
`git diff --cached f170eef80734e9140231defcd87a91281549ba3d`, adapting the usual
HEAD comparison to the implement skill's review-before-commit order. Independent
Standards review identified one minor duplication in the new invalid-effort fixture
loops; a shared helper now retains the same role-specific invalid sets. The affected
runtime group passed after that refactor. Spec review found zero deviations and
independently checked initial Sol xhigh, direct Sol exploration, primary max with
reviewer medium, and fresh same-effort review after correction. Fresh final Standards
and Spec reviewers each reported zero findings on the revised staged result. They
checked the helper, completion bookkeeping, native evidence, and reproducible source
digest independently; neither changed files or repeated the model scenarios.
