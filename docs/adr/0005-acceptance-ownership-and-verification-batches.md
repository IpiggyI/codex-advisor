---
status: accepted
---

# Acceptance ownership, named check executors, verification batches, and check selection

## Decision

Acceptance stays with the primary and separates the duties it cannot hand over from the work it can.

The primary itself inspects the actual complete diff, including new, untracked, corrected, and worker-authored files, confirms that a test can fail for the intended requirement, and confirms that the evidence describes the current deliverable.

Running the checks is assignable. Each verification batch names one executor: the primary, or a delegate that receives the complete batch requirements, the merged changes, and the evidence already collected. The record carries executor, scope, command, exit status, output location, and unverified items. A delegated run never moves the acceptance decision. A delegated check run uses a Worker entry, because the Explorer and Advisor entries pin `sandbox_mode = "read-only"` and a check that writes fails there; the tier follows the existing cheapest-adequate rule and the routing profile.

A result is reused while the relevant code, artifacts, checks, inputs, and environment still support it. A changed executor or a new session is not by itself a reason to run a check again. A changed dependency, an evidence gap, an unexplained failure, or an identified risk is, and rework covers the failed scenario and the scope it affects.

Verification batches are chosen separately from ticket and dispatch boundaries. Checks that share costly setup are combined while the scope stays understandable and a failure stays locatable. A dependency point keeps a real check on the premise the dependent work rests on; unverified premises are not accumulated to lower the number of runs.

A worker runs the verification its packet specifies and whatever its own debugging needs. Acceptance checks that span other work packages or the whole delivery stay in the primary's plan. Ordinary debugging is not deferred into acceptance.

Checks are selected by the behavior a change touches. The installation group covers the installer, the entry templates, the manifest, and the routing profile's dials against those templates; the runtime group covers the inspector, its options, the expectations it reads from a template, and the metadata it emits; a template change reaches both; a documentation change is checked for structure, links, and agreement with actual behavior. The unqualified verifier runs once on the final state and replaces the focused runs instead of following them, which previously ran both groups twice. The native scenario list becomes the candidate set: the scenarios a change can break are selected and the rest are recorded as not exercised. After a correction, only the affected checks repeat.

Independent acceptance is unchanged: high-risk work and an explicit review request still require the Advisor acceptance packet on an Advisor entry in a fresh thread. Advice, exploration, a worker's self-review, and a delegated check run do not satisfy it.

The acceptance packet keeps the field name `PRIMARY VERIFICATION`; its body now carries the executor. The three Advisor entries state that the field may name an executor other than the primary, and that the evidence and its coverage are judged, not who ran it.

## What this supersedes

- ADR-0004 carried forward ADR-0003's acceptance rules unchanged. The part of those rules that binds acceptance to key verification the primary reruns personally is replaced by the split above. The rest stands: the primary inspects actual changes, a report alone cannot establish success, high-risk work and explicit review requests require fresh independent acceptance, and missing evidence or unresolved material findings leave acceptance pending.
- ADR-0001 and ADR-0002 are historical; their rerun sentences describe the superseded rule.

## Basis

The user asked for this change on 2026-09-20 after repeated verification in intermediate steps: the primary reran checks a worker had just run, and separate work packages that shared one expensive setup were verified one at a time. The handoff `D:/Development/Local/prompts/docs/plans/codex-advisor-verification-handoff-2026-09.md` (2026-09-19) names four trigger locations against commit `09c21c8`. All four were re-read in the working tree before this change: the skill's acceptance section, the worker rework sentence and the acceptance packet field in the role contracts, and the scheduling section in the native operations reference.

Deleting the rerun sentence without a replacement rule was the main risk: with no criterion the primary either reruns everything anyway or accepts worker reports at face value, which is the hole ADR-0001 and ADR-0003 closed. The inspection duties above are the criterion, and they are cheap: reading a diff does not repeat an expensive run.

## Alternatives not adopted

- A dedicated check-executor role or native entry: ADR-0004 rejected a fourth role name for one request shape of the Advisor, and the same reason holds here. The existing roles carry it, and a writable delegate that ran the checks still does not satisfy read-only independent acceptance.
- Pinning the tier of a delegated check executor: the routing profile is the only place where dials are written, so a fixed tier here would have to change again with every model generation.
- Naming this repository's mirror and version-manual tests in the shipped reference: they are repo-only, and someone who installed the plugin into another project has no `docs/zh/` and no `docs/releases/`. `AGENTS.md` and `CLAUDE.md` keep them.
- Deleting the native scenario list along with the duplicate commands: the list is the set of routes this plugin advertises, so it is worth keeping as the candidate set that selection draws from.
- Renaming `PRIMARY VERIFICATION` to name the executor: the three shipped Advisor entries name the field in prose, so a rename costs six files and a compatibility break for a label, while the field body already states who ran each check.
- Shrinking the worker's verification field further: the worker needs its own checks to locate defects, and pushing basic debugging into acceptance costs more rework than the duplicate run it removes.
- Recording reuse in a cache or a task lifecycle state: the existing task record and the acceptance packet already carry executor, scope, and result.

## Revisit when

- The primary repeats a valid check after an executor or session change: state the reuse condition in the acceptance packet as well, not only in the skill.
- A delegated executor reports a pass it did not run: require the output location as evidence in the worker RETURN block.
- A host gains a way to share one prepared environment across threads: batching can move from prose guidance to a mechanism.
- Batched acceptance hides which work package failed: tighten the locatable-failure condition or split the batch by package.

## Notes

- Runtime files changed: `skills/orchestration/SKILL.md`, `references/role-contracts.md`, `references/operations.md`, and the three `ca-advisor-*` entries, each with its Chinese twin; `README.md` follows.
- The check-selection part of this record answers finding R07 in `.scratch/instruction-audit/confirmation-checklist.md`, which had stayed pending since 2026-09-13 because it needed an explicit behavioral decision. That entry now records the decision and its scope.
- `verify.sh`, `tests/test_zh_mirror.py`, and `tests/test_version_manual.py` check structure, not doctrine wording; they do not establish that a deployed plugin follows this split.
- Shipped version at the time of this record is `0.2.0`. A version bump, its manual, and the release are a separate user decision.
- Baseline commit `09c21c8`.
