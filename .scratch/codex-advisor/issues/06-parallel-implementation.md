# 06: Parallel Implementation with Explicit Ownership

Status: resolved

Blocked by: 03 - Authorized Architect Mode with Luna Implementation.

**What to build:** An authorized Astra architect completes independent implementation tasks concurrently when their ownership does not conflict, while retaining scheduling, verification, and acceptance responsibility. Tasks that depend on each other or would conflict are sequenced instead.

- [x] The architect can dispatch at least two independent bounded implementation tasks concurrently when the host has sufficient capacity, each with a complete specification and explicit nonconflicting ownership.
- [x] Tasks with dependencies or conflicting ownership are not treated as independent concurrent work. Limited host capacity results in sequencing rather than exceeding the limit or claiming nonexistent parallel execution.
- [x] Implementation scheduling stays with the primary agent; Implementers do not create further implementation delegations.
- [x] Parallel execution preserves user and peer edits, and each worker reports its own changes, checks, judgment calls, and gaps.
- [x] Architect-mode Luna calls remain at observed `max`. The scheduling behavior preserves each selected role's model and effort contract rather than inheriting a different primary-session setting.
- [x] The architect obtains every delegated report needed for the task, inspects all actual changes, and reruns key verification against the combined result before accepting completion.
- [x] A failed, blocked, or incomplete worker prevents acceptance of its affected work and is reported explicitly; another worker's success is not treated as evidence that the whole task is complete.
- [x] The scheduler preserves the independent-review obligations applicable to the combined deliverable instead of bypassing them because work ran concurrently.
- [x] Installed-plugin scenarios exercise two independent Luna tasks, dependent tasks, conflicting ownership, constrained host capacity, and incomplete worker output, with actual task and verification evidence.
- [x] This ticket can be verified with the Luna workflow from ticket 03 and does not require Sol support from ticket 05. It does not introduce a separate implementation model catalog or duplicate role-selection rules.

## Verification

Use two bounded changes with disjoint ownership and a meaningful combined check in a disposable repository. Observe actual overlap when host capacity permits, and verify sequencing for dependencies or conflicts. Reuse the role and evidence interfaces from the authorized Architect-mode workflow; do not count a requested parallel dispatch as proof that concurrent execution occurred.

## Acceptance

Completed on 2026-09-06. Installed scenarios confirm actual overlap between two
native Luna max workers, sequencing for dependencies, shared ownership and a single
worker slot, and pending whole-task acceptance when a worker reports incomplete
verification. The architect inspected actual changes and reran combined checks;
the requested independent review followed those checks on the combined result.
See [the acceptance record](../acceptance-05-06.md) for evidence and limits.
