# 02: Generic inspector driven by the shipped templates

**What to build:** The primary verifies a delegated call with `--agent <entry name>` and, when the entry leaves effort to the caller, `--effort <effort>`. The inspector reads the expected model and any pinned effort from the shipped template with that name, so renaming or re-dialling an entry never changes the inspector. Policy about which efforts a tier allows leaves the inspector. This ticket still runs against the current eight templates.

**Blocked by:** 01 (both tickets edit the verifier).

**Status:** resolved

- [x] `--agent NAME` selects the template whose `name` field equals NAME from the templates directory resolved beside the script; an unknown name fails with a diagnostic and no output.
- [x] When the template pins `model_reasoning_effort`, that is the expected effort; a `--effort` that differs from the pin is rejected. When the template does not pin it, `--effort` is required and is the expected effort.
- [x] The expected model is the template's `model`. Observed model, effort, and agent role must equal the expectations; a mismatch fails as today.
- [x] No allowed-effort validation remains: any non-empty effort string is accepted as the expectation and compared to the observed value.
- [x] Unchanged: exactly one UUID-matched rollout; a role check requires parent linkage, working directory, sandbox and permission evidence; conflicting values across turn contexts are rejected; the output object contains only the allowlisted keys; no prompt or credential bytes appear in stdout or stderr; without `--agent` generic evidence is emitted.
- [x] The eight retired per-role options (`--luna`, `--sol-effort`, `--astra-effort`, `--explorer-effort`, `--sol-explorer-effort`, `--astra-explorer-effort`, `--advisor-effort`, `--reviewer-effort`) fail with a diagnostic naming `--agent`; `--review-primary-effort` and `--select-review-effort` keep their existing diagnostic.
- [x] The runtime group of the verifier is rewritten to iterate over every shipped template: for each, an accepted case with matching metadata (pinned or a passed effort), rejections for mismatched model, effort, role, sandbox, permission, parent, and working directory, a `--effort` mismatch against a pin, a missing `--effort` for an unpinned template, and the payload-leak assertion. Hand-written per-role cases are removed. Both verifier groups pass.
- [x] The inspector's usage text describes the new options; the operations reference is left to ticket 03.

## Acceptance

Accepted 2026-09-16 by the primary. Lane: `generalPurpose` pinned `cursor-grok-4.6-xhigh` (requested, not confirmed). Tier 1: full `verify.sh` rerun by the primary, both groups pass; `git diff --stat`: inspector 136 lines, verifier 671 lines. Tier 2: the primary read the inspector's option parsing and template resolution — `awk` extraction of top-level `name`/`model`/`model_reasoning_effort` stopping at the first `"""`, duplicate-name and unknown-name failures, pinned-effort equality rule, `--effort` without `--agent` rejected; the retired ten options fail before any rollout is read. Negative proof recorded by the lane: dropping the model comparison fails the runtime group at the named assertion.

Carried over to ticket 04 (contract gap on the primary's side, not a lane defect): the contract told the lane to keep the old text of the `--review-primary-effort` / `--select-review-effort` diagnostic, which still points at the now-retired `--reviewer-effort`; ticket 04 changes that diagnostic to name `--agent` and adjusts the verifier assertion.
