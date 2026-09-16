# Codex Advisor: Tier-Named Native Entries, First-Round Pool, and Self-Updating Installation

Status: ready-for-agent

Date: 2026-09-16. Target plugin version `0.2.0` (breaking for callers of the eight retired entry names; `0.x` minor). Baseline: commit `f37830f` (the 0.1.0 version manual and audit checklist). Vocabulary: `CONTEXT.md` (this round added First-round pool, Senior gate, Escalation ladder, Dial, Native entry, Routing profile, Companion installer; retired Implementer). Decision record: ADR-0004.

## Problem Statement

The eight native entries are named by model: Luna, Sol, and Astra Explorers and workers, plus an Astra Advisor and an Astra reviewer. The user selects a tier, but the plugin makes them remember which model currently sits in that tier. When a model changes generation, the entry name, the skill's table, the inspector's role options, and the installer's selectors all change together.

The dial values (which efforts a tier allows, which is the default, which model is preferred) live in the skill text. Adjusting one value means editing doctrine, and the doctrine still lets the primary agent choose a senior tier on its own first-round judgment. In the sibling plugin the user watched that freedom send routine work to the most expensive models, and does not want the plugin to leave that decision to the model.

The companion installer refuses to overwrite a changed destination and never deletes anything. After a rename, the eight old files stay in `$CODEX_HOME/agents` on both machines and remain discoverable; after any template edit the user must delete files by hand before the installer will proceed. The user's rule is that every file this plugin depends on reaches its live location through installation or update, never through hand copying. The Windows plugin cache also checks out with CRLF line endings while the installed copies are LF, so the byte comparison fails for reasons unrelated to content.

The eight TOML templates have no Chinese twin, unlike every runtime Markdown file. Independent acceptance is a separate native entry although it is one request shape of the Advisor role.

## Solution

Rename the native entries by role and capability tier. Eleven entries: `ca_explorer_light`, `ca_explorer_standard_m`, `ca_explorer_standard_h`, `ca_explorer_senior`, `ca_worker_light`, `ca_worker_standard_m`, `ca_worker_standard_h`, `ca_worker_senior`, `ca_advisor_light`, `ca_advisor_standard`, `ca_advisor_senior` (`ca` abbreviates codex-advisor). A tier with two models gets two entries: `_m` is the default candidate, `_h` the stronger alternative, `_l` would be a cheaper alternative. Every entry pins its model; an entry whose cell has a single effort also pins that effort, so a caller cannot reach the wrong dial by omission.

Move every dial value out of the skill text into a routing profile that ships as a reference beside the role contracts and operations references. The skill keeps only mechanism: light and standard are the first-round pool with free choice between them; senior is behind the senior gate; the escalation ladder R1 to R4 governs what happens after a failed acceptance. Changing a model or an effort touches the TOML and the routing profile, never the skill or the scripts.

Fold independent acceptance into the Advisor entries as a second request shape and retire the reviewer entry. Make the companion installer own its files: it overwrites the eleven shipped entries when they differ, deletes the eight retired names when present, and touches nothing else. Make the inspector generic: it reads the expected model and any pinned effort from the shipped TOML named on the command line. Give every TOML a parseable Chinese twin, pin LF line endings for distributed files, and release as `0.2.0` with its version manual.

## User Stories

1. As a primary agent, I want to pick a native entry by role and tier, so that I do not have to know which model currently fills that tier.
2. As a primary agent, I want a tier with two candidate models to expose both as separate entries with a fixed default, so that I can take the cheaper default and reach the stronger one deliberately.
3. As a primary agent, I want every entry to pin its model, so that a delegated call never inherits my own session model.
4. As a primary agent, I want an entry whose tier allows exactly one effort to pin that effort, so that forgetting to pass an effort cannot select a different dial.
5. As a primary agent, I want an entry whose tier allows several efforts to leave the effort to me, so that I can choose within the allowed dials on the first attempt.
6. As a primary agent, I want the allowed efforts, their default, and the candidate order for every tier in one routing profile, so that I read one table before the first allocation.
7. As a primary agent, I want the skill to tell me that light and standard are one first-round pool with no precondition between them, so that I do not treat light to standard as an escalation.
8. As a primary agent, I want the skill to tell me that senior is reached only through the senior gate or a user declaration, so that I do not send first-round work to the most expensive tier on my own judgment.
9. As a primary agent, I want the escalation ladder written as four rules, so that the same problem does not climb three efforts on one model.
10. As a primary agent, I want the senior gate to coincide with the decision-type consultation after two failed complete attempts, so that the Advisor's verdict also settles whether senior is warranted.
11. As a primary agent, I want the Advisor's decision shape to default to the standard tier and its acceptance shape to the light tier, so that routine judgment and routine acceptance stay cheap.
12. As a primary agent, I want the Advisor to reach senior only when its own verdict reports low confidence or the user declares it, so that Advisor escalation does not follow worker failures.
13. As a primary agent, I want one Advisor entry per tier that answers both the decision packet and the acceptance packet, so that independent acceptance does not need a fourth role.
14. As a primary agent, I want independent acceptance to still require a fresh thread after primary checks, so that folding it into the Advisor entries does not weaken the acceptance rule.
15. As a primary agent, I want each entry's description to name its role, tier, model, and whether its effort is fixed, so that I can select it from the agent list without loading the skill.
16. As a primary agent, I want the delegate's instructions to state only what the delegate itself must do, so that caller duties are not repeated into every entry.
17. As a user, I want a model generation change to touch only the affected TOML and the routing profile, so that the skill text and the scripts stay unchanged.
18. As a user, I want the routing profile to ship inside the plugin, so that a value change reaches both machines through the same plugin update as everything else.
19. As a user, I want the companion installer to overwrite this plugin's own installed entries when they differ from the shipped templates, so that I never hand-reconcile after an update.
20. As a user, I want the companion installer to delete the eight retired entry files when it finds them, so that old names do not linger as discoverable agents.
21. As a user, I want the companion installer to leave every other file alone, so that upstream Sol Advisor files, unrelated agents, and my primary configuration are untouched.
22. As a user, I want the installer's check mode to fail when an installed entry differs from its template or a retired file is still present, so that drift and residue are both visible.
23. As a user, I want selective checks to accept the tier-based short names, so that I can check one role without typing model names.
24. As a user, I want the installer to keep refusing symlinked, non-regular, root, and dot-segment destinations, so that a wrong target directory still cannot be damaged.
25. As a user, I want distributed files to check out with LF line endings on Windows, so that the installer's byte comparison compares content, not line endings.
26. As a user, I want the inspector to take an entry name and, where the entry leaves it open, the effort I passed, so that a table change never needs an inspector change.
27. As a user, I want the inspector to read the expected model and any pinned effort from the shipped TOML, so that there is one source for what an entry should run.
28. As a user, I want the inspector to stop judging whether an effort is allowed, so that policy stays in the routing profile and the inspector reports mechanism only.
29. As a user, I want the inspector to keep requiring parent linkage, working directory, and permission evidence and to keep emitting only allowlisted metadata, so that the evidence contract does not weaken.
30. As a repository maintainer, I want every TOML template to have a parseable Chinese twin with identical configuration keys, so that a translated entry cannot drift in model or effort.
31. As a repository maintainer, I want the mirror check to cover TOML files and to compare keys, so that twin drift fails a test rather than a reader.
32. As a repository maintainer, I want a check that every entry named in the routing profile has a shipped TOML with the same model, so that the two places a dial lives cannot disagree.
33. As a repository maintainer, I want a check that all entries of one role carry identical delegate instructions, so that eleven copies of the same text cannot drift.
34. As a repository maintainer, I want the verifier's runtime cases to be driven by the shipped TOMLs, so that adding or renaming an entry does not add hand-written cases.
35. As a repository maintainer, I want the retirement of the eight old names and their replacements named in the upgrade notes, so that a user of 0.1.0 learns why `agent_type` calls fail.
36. As a repository maintainer, I want the word Implementer retired everywhere in favor of Worker, so that one concept has one name.
37. As a repository maintainer, I want the Chinese twins of the rewritten skill, references, and routing profile updated in the same change, so that the mirror test stays green and the known mistranslation of the failure-reassessment rule is corrected.
38. As a repository maintainer, I want an ADR that records these decisions and names what it supersedes in ADR-0003 and the original fork spec, so that a future reader knows why the ladder, the gate, and the installer policy changed.
39. As a user, I want a version manual for 0.2.0 that describes the whole version and the delta from 0.1.0, so that I can read what I installed without reading the ADR or the diff.
40. As a user, I want the grok lane recorded as the next version with its mechanism decided, so that this version does not grow to cover it.

## Implementation Decisions

### Native entries

- Eleven TOML templates, filenames `ca-<role>-<tier>[-m|-h].toml`, `name` fields `ca_<role>_<tier>[_m|_h]`. The `ca_` prefix namespaces this plugin's files inside a directory shared with upstream Sol Advisor files; the filename mirrors the `name` with hyphens.
- Model pins: Explorer light Luna; Explorer standard `_m` Luna, `_h` Terra; Explorer senior Sol; worker light Luna; worker standard `_m` Sol, `_h` Astra; worker senior Astra; Advisor light, standard, senior Astra. Model identifiers are `gpt-5.6-luna`, `gpt-5.6-terra`, `gpt-5.6-sol`, `gpt-6-astra`.
- Effort pins, only where the cell has one effort: worker light `max`; Explorer standard `_m` `max`; worker standard `_h` `low`; Advisor light `low`; Advisor standard `medium`. The other six entries omit `model_reasoning_effort`; the caller passes it with `fork_turns` set to none, as the host requires for per-spawn overrides.
- Explorer and Advisor entries keep `sandbox_mode = "read-only"`. Worker entries inherit the parent sandbox.
- Retired entries, deleted by the installer when present: `codex-advisor-astra-advisor`, `codex-advisor-astra-explorer`, `codex-advisor-astra-implementer`, `codex-advisor-astra-reviewer`, `codex-advisor-luna-explorer`, `codex-advisor-luna-implementer`, `codex-advisor-sol-explorer`, `codex-advisor-sol-implementer` (each with the `.toml` suffix).
- `description` states role, tier, model, and either the fixed effort or that the caller passes it. It does not list allowed efforts; the routing profile does.
- `developer_instructions` per audit finding R05: the role's permissions, the packet it expects, its return shape, the fresh-thread and no-further-delegation rules, and the instruction not to infer its own runtime settings. Caller duties (consultation triggers, lifecycle transitions, metadata collection, primary verification) are removed. All entries of one role carry byte-identical instructions. Advisor instructions carry both return shapes: RECOMMENDATION / EVIDENCE / ASSUMPTIONS / TRADEOFFS / GAPS for the decision packet and READINESS / FINDINGS / VERIFICATION / GAPS for the acceptance packet.

### Routing profile

- A new reference beside the role contracts and operations references, in the skill. Contents in order: declaration date and anchored models; a table from role and tier to entry names and dials in the notation `model[a*, b, c]` (every listed effort is a first-round option, `*` is the default, listed model order is candidate order); the Advisor defaults (decision shape standard, acceptance shape light); one sentence pointing to the skill for pool, gate, and ladder; the adjustment method (which places change and which checks to run).
- Initial values: Explorer light `gpt-5.6-luna[high*, xhigh]`; Explorer standard `gpt-5.6-luna[max]` then `gpt-5.6-terra[medium*, high]`; Explorer senior `gpt-5.6-sol[medium*, high]`; worker light `gpt-5.6-luna[max]`; worker standard `gpt-5.6-sol[high*, xhigh]` then `gpt-6-astra[low]`; worker senior `gpt-6-astra[medium*, high]`; Advisor light `gpt-6-astra[low]`, standard `gpt-6-astra[medium]`, senior `gpt-6-astra[high*, xhigh]`.
- The profile is the only place dial values are written. The skill text, the README, and the TOML descriptions do not repeat efforts or defaults. The version manual freezes the table for its version.

### Skill and references

- The allocation section states mechanism only: role by output (evidence, change, judgment); tier chosen inside the first-round pool by judgment dependence, cheapest adequate dial at its default; senior only through the senior gate (two capability-attributed complete failed attempts inside the pool, or a user declaration; for the Advisor, a low-confidence verdict or a user declaration); the escalation ladder R1 rework ticket same thread same dial, R2 raise in a fresh thread with the current-state handoff when rework fails and the cause is capability (higher effort of the same model or another model), R3 the same model raised at most once, R4 a major execution problem may skip the rework ticket and change model, counted as one failure. It points to the routing profile for every value.
- The complete-attempt definition, the fresh-thread rule for every effort or model change, Architect mode, the required-advice triggers, and the acceptance rules stay as ADR-0003 wrote them. The sentence that no fixed ladder is imposed is replaced by the ladder.
- The operations reference replaces the eight-row entry table with the eleven entries (entry name, install selector, pinned or caller-selected effort) and rewrites the invocation, inspector, and installer procedures for the new shapes. The role-contracts reference merges the independent-acceptance packet under the Advisor heading as its second request shape and drops the reviewer entry name.
- Implementer is retired as a term; Worker is used throughout the skill, references, README, glossary, and entry names.

### Companion installer

- Manifest: the eleven templates. For each, a missing or differing destination is written (reported as installed), an identical destination is reported as unchanged. No `.bak`, no old-versus-new judgment.
- Retire list: the eight old filenames. A present file is deleted and reported as removed, by exact filename, without reading its content.
- Everything outside the manifest and retire list is never read or written.
- Check mode writes nothing and fails on any differing or missing manifest file and on any present retire file, listing each.
- Selective check accepts the tier-based short names (`explorer-light`, `explorer-standard-m`, `explorer-standard-h`, `explorer-senior`, `worker-light`, `worker-standard-m`, `worker-standard-h`, `worker-senior`, `advisor-light`, `advisor-standard`, `advisor-senior`).
- Existing refusals stay: symlinked destination or ancestor, non-regular destination, non-directory ancestor, filesystem root, dot path segments. The staged-copy-then-link write is replaced by an atomic write suited to overwriting.
- A `.gitattributes` at the repository root pins LF for text files so the Windows plugin cache checks out byte-identical to the installed copies (audit finding R01).

### Inspector

- Options become `--agent <entry name>` plus `--effort <effort>` when the named entry does not pin one. The expected model, and the expected effort when pinned, are read from the shipped TOML resolved beside the script; `--effort` given for a pinned entry must equal the pin or is rejected. Without `--agent`, generic evidence is emitted as today.
- The inspector no longer validates that an effort belongs to an allowed set; the routing profile owns that policy.
- Unchanged: exactly one UUID-matched rollout, required parent linkage and working directory for a role check, required sandbox and permission evidence, conflict rejection, allowlisted output only, no prompt or credential bytes.
- The retired primary-derived review options keep failing with their diagnostic.

### Chinese twins

- Every shipped TOML has a twin at the same relative path under the Chinese mirror directory, as parseable TOML. `name`, `model`, `model_reasoning_effort` (presence and value), and `sandbox_mode` (presence and value) equal the template; `description` and `developer_instructions` are the translation and contain Chinese text.
- The mirror test extends from Markdown-only to Markdown plus TOML: existence both ways for both types, key equality for TOML. The rewritten skill, both references, and the new routing profile get updated twins in the same change; the twin of the skill corrects the failure-reassessment sentence noted as audit finding R02.

### Records and release

- ADR-0004 records the decisions above, supersedes ADR-0003's no-fixed-ladder sentence and its reviewer-as-distinct-entry wording, revises the fork spec's user story 39 (installer refusal) into the overwrite-own-files policy, and records the 0.3.0 grok lane mechanism as a note.
- Audit checklist: R01 recorded as update (this batch), R05 as simplify (this batch), R08 as clarified by the profile notation, R02 as corrected with the twin rewrite. The others stay pending.
- README: install, use, roles (entry names and tiers, no dial values), check and update, and an upgrade section that names the eight retired entries and their replacements.
- Version `0.2.0` in the plugin manifest; version manual for `0.2.0`; the marketplace manifest carries no version field and does not change.

## Testing Decisions

A good check observes behaviour at a boundary a caller uses: the installer and inspector at their command-line boundaries with temporary directories and synthetic rollouts, the mirror and manual checks over the working tree. No check reads internal function names or prompt wording.

- Existing seam, installer: the verifier's installation group already exercises a temporary target with unrelated files, repeat installs, selective checks, refusals, and preservation. It is rewritten for the new semantics: a differing own file is overwritten and reported; an identical one is unchanged; a present retire file is removed; check mode fails on drift and on residue and writes nothing; unrelated and upstream files survive byte-identical; every existing refusal still refuses without partial mutation. The case that an old Sol template blocks the upgrade is deleted; the reverse is now the requirement.
- Existing seam, static template checks: the verifier's installation group already parses every TOML and asserts prefixes. It gains: the routing profile names exactly the shipped entries and each named entry's TOML pins the same model; all entries of one role carry identical `developer_instructions`; an entry pins `model_reasoning_effort` exactly when the spec says its cell has one effort; Explorer and Advisor entries are read-only.
- Existing seam, inspector: the verifier's runtime group already writes synthetic rollouts and asserts accept or reject plus payload filtering. It becomes table-driven over the eleven TOMLs: for each entry, the pinned or a passed effort is accepted with matching metadata, a mismatched model, effort, role, sandbox, permission, parent, or working directory is rejected, `--effort` on a pinned entry must equal the pin, and the retired options keep failing.
- Existing seam, mirror test: extended to TOML with key equality; a twin whose `model` differs from its template must fail.
- Existing seam, version manual test: unchanged; it must pass for `0.2.0`.
- Live route check after installation on this machine: one tiny spawn per entry in a fresh Codex task (eleven spawns), reading each thread's metadata through the inspector; recorded in the acceptance record with any unexercised entry named. This establishes dispatch, not quality.
- Text checks: no occurrence of `Implementer`, `implementer`, `reviewer` as an entry, or any retired entry name in the plugin, the README, or the mirror, except the retire list and the upgrade notes.

Prior art: the verifier's two groups, the mirror test, the version manual test, and the acceptance records under the earlier feature directories.

## Out of Scope

- The grok lane (0.3.0). Mechanism decided: a Node runner wrapping the `grok` CLI with a spec and receipt flow through the shell, ported from the sibling plugin's runner. Design, naming, tests, and doctrine wording for it get their own spec.
- A user-level routing profile file, a companion installer target for it, or reading the sibling plugin's profile.
- Changes to the sibling plugin. Aligning its codex-lane cells to this table is a ticket in that repository; this spec only records the pointer.
- Architect mode, the fresh-thread policy, the required-advice triggers, and the acceptance rules beyond folding the reviewer entry into the Advisor.
- Audit findings R04, R06, R07, R09, R10, R11, R12.
- Verifying that the Codex host shows custom-agent descriptions to the primary agent, or that `gpt-5.6-terra` and Luna `xhigh` are available on the user's plan; the live route check records what is observed.
- Upstream sync.

## Further Notes

- Posture: an upstream task artifact exists, so the orchestrating posture applies by default. Coordination artifacts (this directory, ADR-0004, `CONTEXT.md`, `AGENTS.md`, audit checklist, version field) are written by the primary agent; deliverables (plugin templates, skill and references, scripts, tests, README, mirror, version manual, `.gitattributes`) go through workers. The user may switch to the implementing posture by declaring it.
- Tickets: 01 native entries and their Chinese twins (templates, slim instructions, retire of the reviewer, mirror test extension); 02 routing profile, skill allocation section, references, and their twins; 03 companion installer and `.gitattributes` with the installation verifier group; 04 inspector and the runtime verifier group; 05 README, glossary consistency, audit checklist entries; 06 version manual 0.2.0 and release. 01 and 02 are independent; 03 and 04 depend on 01 for the entry names; 05 depends on 01 and 02; 06 depends on all.
- Assumptions with invalidation checks: the host's custom-agent precedence rules are as the official subagents documentation stated on 2026-09-16 (file values win; per-spawn `model` and `reasoning_effort` need `fork_turns` none) — recheck after a Codex CLI upgrade past 0.154.0; `gpt-5.6-terra` and Luna `xhigh` are callable on the user's plan — the live route check settles it; the eight retired filenames are the only files this installer ever wrote — recheck the installed directories before running the installer on a machine not listed here.
- Sibling pointer: the sibling plugin's routing profile lists different codex-lane dials in four cells; the user chose this table as authoritative. A follow-up in that repository updates its canonical profile and runs its installer.
- Sources: the grilling of 2026-09-16 (three rounds), the sibling plugin's ADR 0016 and ADR 0018, the official Codex subagents documentation read on 2026-09-16, the instruction audit checklist of 2026-09-13.
