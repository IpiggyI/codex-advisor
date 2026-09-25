# Codex Advisor 0.3.0: mainstay/crux/rescue Tiers and Process Consultation

Status: resolved

Date: 2026-09-26. Target plugin version `0.3.0`. This is a breaking change for callers of the eleven 0.2.0 entry names; `0.x` takes a minor bump. The grok lane moves to `0.4.0`. Baseline: commit `f812f9b`. Executor: Codex, in this checkout. Vocabulary: `CONTEXT.md`, which ticket 02 updates. Decision record: ADR-0006, written by ticket 02; ticket 01 supplies its mechanism section.

## Materials

### Required reading (binding or needed to act)

| Material | Location | Version | Use |
|---|---|---|---|
| This spec | `.scratch/tiers-and-advisor-consult/spec.md` | this file | Every current requirement, its owner, and its acceptance |
| Tickets | `.scratch/tiers-and-advisor-consult/issues/01-*.md` … `06-*.md` | — | Per-ticket scope, required reading, acceptance |
| Acceptance record | `.scratch/tiers-and-advisor-consult/acceptance.md` | — | Where every probe, live check, visual comparison, and the final sweep are recorded |
| Decision ledger | `.scratch/tiers-and-advisor-consult/sources.md` §2.4 | — | State and basis of every decision; read before proposing any change to one |
| Visual baseline | `docs/releases/0.2.0.html` | commit `f812f9b`, SHA-256 `d89f0f18ccfc0cb42156a5548bc531527372603ea12efb13d759e86589b6d4ea` | Visual system of `docs/releases/0.3.0.html` (ticket 06). Never edit it |
| Current runtime | `plugins/codex-advisor/` (skill, references, `agents/*.toml`, `agents/retire.txt`, `scripts/*.sh`, `.codex-plugin/plugin.json`), `docs/zh/`, `README.md`, `CONTEXT.md`, `tests/*.py` | `f812f9b` | What is being changed |
| Decision records | `docs/adr/0003-*.md`, `0004-*.md`, `0005-*.md` | `f812f9b` | What ADR-0006 supersedes and what stays (ADR-0004 lines 29 and 47 name the host facts to recheck) |
| Repository rules | `AGENTS.md`, `docs/agents/version-manual.md`, `docs/agents/issue-tracker.md` | `f812f9b` | Chinese mirror, version manual, tracker conventions |
| Live-check procedure | `plugins/codex-advisor/skills/orchestration/references/operations.md` §Install and discover (temporary `CODEX_HOME`) and §Invoke and validate | `f812f9b` | Running live checks without touching the user's real home |
| Live-check prior art | `.scratch/tier-role-pool/acceptance.md` §Live route check | `f812f9b` | Method and record shape for the route check |
| Reference implementation | `/home/hyy/develop/personal/GitHub/rpiv-mono/packages/rpiv-advisor/`: `advisor/execute.ts`, `advisor/context.ts`, `advisor/inventory.ts`, `advisor/register.ts` (`DEFAULT_PROMPT_GUIDELINES`), `prompts/advisor-system.txt` | commit `d74b1c99830a565f3df3f37e0a36616d17ffc574` | Consultation semantics and the guideline text that AC-7 adapts |
| Codex host documentation | Hooks <https://learn.chatgpt.com/docs/hooks>; App Server <https://learn.chatgpt.com/docs/app-server>; Subagents <https://learn.chatgpt.com/docs/agent-configuration/subagents> | Read 2026-09-25/26; re-read at execution and record the date | Host capabilities (tickets 01, 04, 05) |

### Traceability only (not binding)

| Material | Location | Use |
|---|---|---|
| Originals and ledger | `.scratch/tiers-and-advisor-consult/sources.md` Part 1 | The user's words, verbatim |
| Discussion record | `.agent-discuss/tiers-and-advisor-next-iteration/` (`request-001.md`, `request-002.md`, `claude/001.md`, `gpt/001.md`, `gpt/002.md`, `final.md`; SHA-256 values in `sources.md` §1.1) | How the decisions formed. The directory is untracked and closed; do not edit it |
| Magazine preview | `.scratch/manual-redesign/0.2.0-magazine.html` | Not adopted. It must not be used as a visual baseline |
| Claude Code advisor documentation | <https://code.claude.com/docs/en/advisor> (read 2026-09-25; returned HTTP 403 to the executor on 2026-09-26) | Background on the posture being migrated. Nothing here depends on it: the binding posture is AC-5 to AC-7, adapted from rpiv-advisor's `advisor/register.ts` |
| Handoff review | `.scratch/tiers-and-advisor-consult/handoff-review.md` (2026-09-26, against the task files it hashes) | The executor's pre-implementation review. Its findings F1–F5 were resolved into this spec and the tickets on 2026-09-26 (ledger D42–D46, open items O3 and O4) |

### Authority and conflicts

- This spec states the current requirements. Where `final.md` or any other discussion file differs, this spec wins, because later user decisions (`sources.md` U5, U6, U10) changed parts of `final.md`. The ledger records each change.
- The baseline page governs the visual system (see §Visual acceptance). This spec governs content. When new content needs a component the baseline lacks, compose it from the baseline's existing components. If that is not possible, stop and return (S7); do not invent a pattern, and never edit the baseline to match the result.
- No prototype or design screenshot exists for this task other than the baseline page. Screenshots taken in ticket 06 are evidence, not a baseline.
- The reference implementation informs consultation semantics only. Where it conflicts with this spec (for example its "commit the change" guideline), this spec wins.

## Problem Statement

The user runs Codex with `gpt-6-astra` at `xhigh` as the primary and delegates through this plugin. Four problems come from the 0.2.0 design.

1. **Tiers do not match how the user allocates work.** 0.2.0 has light and standard as a free first-round pool and senior behind a two-failure gate, with tiers that mix models and efforts. The user wants a workhorse tier that takes most daily work, an expert tier for hard points, and a standby tier used only when both fail. From long use, the user sees bigger gains from a stronger model than from a higher effort, and a distinct jump at `xhigh`. The 0.2.0 table uses `gpt-5.6-*` models and Terra; the user now runs the 6 series, which has no Terra.
2. **The Advisor is rarely consulted.** In the 30 days before 2026-09-25, 15 of 39 sessions that loaded the orchestration skill made no Advisor or reviewer call at all. That is a rough count; the method for identifying subagent sessions and skill loading was not validated. Four causes:
   - The skill words advice as optional: "Proactive advice is allowed", followed by three narrow required cases.
   - Each call costs a six-part decision packet, an installation check, a spawn, and an inspector run.
   - The skill text is not always in context: its body loaded in only 39 of 56 top-level sessions.
   - The decision default, `astra[medium]`, is weaker than the user's `astra[xhigh]` primary.

   Claude Code's advisor, by contrast, is a zero-parameter call that forwards the whole conversation, is always described to the model, and is consulted before committing to an approach, when stuck, and before declaring done.
3. **Actual model settings are not checked on every dispatch.** A caller-effort entry spawned without an effort inherits the parent's effort, and a full-history fork inherits the parent's model. Today only a manual inspector run catches either.
4. **Delegates need explicit consultation guidance before declaring done.**

## Solution

Rename the tiers to 主力 `mainstay`, 攻坚 `crux`, 后援 `rescue`. Tiers are ordered by model, and effort is only a finer grade inside a tier. The table uses `gpt-6-luna`, `gpt-6-sol`, `gpt-6-astra` exactly as the user wrote it.

- **First round.** Work starts in `mainstay`. It may start in `crux` when a key difficulty is already identified or interacting constraints must be handled. A capability failure moves the work to the next tier, never to another model inside the same tier. The model level never drops, unless no other choice exists.
- **Consultation.** Replace the Advisor's decision packet with a process consultation. The call takes zero parameters and carries the caller's current context automatically. The advisor gets no tools and returns a plan, a correction, or a stop signal. Primary, workers, and explorers can all call it.
- **Posture.** Callers get Claude Code's frequent-call posture when their model differs from the advisor's model, and a reduced posture (before committing to an approach, before declaring done) when it is the same model.
- **Always-on text.** A plugin-shipped `SessionStart` hook puts the primary's posture text in context, and each entry's instructions carry the delegate's.
- **Automatic verification.** Every dispatch's actual model and effort are checked automatically. Consultation follows the injected or entry-provided posture; no finish hook blocks a caller.
- **Acceptance.** Independent acceptance stays: a packet-based review in a fresh thread, now at a dial chosen by the tier of the accepted work.
- **Release.** Ship thirteen tier-named entries, their Chinese twins, and `0.3.0` with its version manual in the visual style of the 0.2.0 manual.

## Reasons That Bound Implementation Choices

These reasons decide trade-offs the requirements below leave open. An implementation that satisfies a requirement's wording while defeating its reason is wrong. Traceability: `sources.md` §2.3.

- **Tiers by model, effort inside.** The user observes a bigger gain from a stronger model than from a higher effort, and a distinct jump at `xhigh`. That is why an escalation never lowers the model level, and why an escalation that keeps the same model must at least raise the effort.
- **Wide first-round `crux`.** A known-hard task should not burn a `mainstay` attempt. The user accepts the over-routing risk and watches it by eye, which is why no counting machinery is added.
- **Automatic context instead of packets.** Writing a six-part packet was one cause of rare consultations, and a caller's summary drops facts and adds framing. A consultation that needs a caller-written summary misses the goal.
- **No tools for the advisor.** Frequent consultation needs low cost and latency per call. Checking facts belongs to the caller and to independent acceptance. Read-only tools are not "close enough".
- **Posture by model identity.** A consultation is worth making often when the advisor is a different, stronger model. A same-model consultation is the most expensive kind and adds a second view, not capability. Primaries outside the table, such as `gpt-5.6-terra`, must not fall through, so no family list is hard-coded.
- **Always-on text through a hook and through entries.** The skill body loaded in only 39 of 56 top-level sessions. Entries carry their own posture so delegates do not depend on an unverified hook capability.
- **No finish blocking.** Consultation guidance applies to callers without a hook intercepting the primary's or a worker's completion.
- **Per-dispatch automatic verification.** Omitted efforts and inherited fork models vary per dispatch. A manual inspector run per call was part of the friction being removed.
- **Keep independent acceptance.** A consultation sees the caller's reasoning and is anchored by it.
- **No commit step in the posture.** Commits need the user's explicit authorization each time.
- **Stop instead of fall back.** Every natural-looking fallback is either a rejected option or the problem being fixed: a primary `Stop` hook, skill-only text, a tool-bearing or packet-based consultation, `gpt-5.6-*` models.

## User Stories

1. As the user, I want three tiers named `mainstay`, `crux`, and `rescue`, so that the names say how often each tier should be used.
2. As a primary agent, I want the routing profile to list each tier's dials exactly as the user's table does, so that I do not reconstruct the table from prose.
3. As a primary agent, I want `mainstay` to be the default for new work, so that most tasks run on the cheaper models.
4. As a primary agent, I want to start in `crux` when I have already identified a key difficulty or interacting constraints, so that I do not waste a `mainstay` attempt on work I know is hard.
5. As a primary agent, I want no usage quota on `crux`, so that tier choice follows the work, not a ratio.
6. As the user, I want the narrow first-round admission kept in the records but not enabled, so that I can switch to it later if `crux` turns out to be overused.
7. As the user, I want to judge `crux` usage by my own observation, so that the plugin adds no markers, logs, or statistics for it.
8. As a primary agent, I want the first candidate in a cell to be its default and later candidates to be for work that depends more on judgment the packet cannot capture, so that in-tier choice has one rule.
9. As a primary agent, I want a capability failure to send the work to the next tier, so that I do not try every model in one tier first.
10. As a primary agent, I want the next tier's dial to be no lower in model level than the failed one, so that an escalation is never a downgrade.
11. As a primary agent, I want an escalation that stays on the same model to raise the effort, so that a "raise" always changes something.
12. As a primary agent, I want one capability failure defined as a failed attempt plus a failed same-dial rework with a capability diagnosis, so that intermediate test failures and environment problems do not move work.
13. As a primary agent, I want `rescue` reachable only through `crux` or the user's declaration, so that the standby tier stays rare.
14. As a primary agent, I want a `rescue` failure to go to the user, so that there is no tier beyond it.
15. As the user, I want the two observations behind the table recorded as declared assumptions with an invalidation trigger, so that the next model generation forces a review.
16. As a primary agent, I want a zero-parameter consultation that carries my current context automatically, so that I never write a summary packet to get advice.
17. As a primary agent, I want the consultation to see the tool calls of my current, unfinished turn and the post-compaction context, so that the advice matches what I actually know.
18. As a primary agent, I want the advisor to have no tools, so that consultations stay fast and cheap enough to make often.
19. As a primary agent, I want every consultation result to be exactly one of plan, correction, or stop, so that I know how to act on it.
20. As a primary agent, I want every consultation result to state the advisor's actual model and effort, so that I can see it did not run on my inherited model.
21. As a worker or explorer, I want to call the same consultation, so that a cheaper delegate can borrow the advisor's judgment at decision points.
22. As a caller, I want the advisor dial chosen from my tier, so that the advisor is never weaker than me.
23. As a primary agent whose model is not in the routing profile (for example `gpt-5.6-terra`), I want a defined advisor dial and posture, so that the plugin does not guess.
24. As a caller whose model differs from the advisor's, I want the full posture: consult before substantive work, when stuck, when changing approach, and before declaring done, and at least twice on multi-step tasks.
25. As a caller running the advisor's own model, I want the reduced posture: consult only before committing to an approach and before declaring done on multi-step tasks, so that same-model consultations stay rare.
26. As a caller, I want to reject advice directly when it conflicts with a user constraint, with the reason stated.
27. As a caller on a different model from the advisor, I want to make one reconcile call before rejecting advice for a reasoning flaw, so that I do not overrule a stronger model on my own reading.
28. As a caller on the same model as the advisor, I want to reject advice for a reasoning flaw directly, with the reason stated.
29. As the user, I want the posture text never to tell an agent to commit, so that commits keep needing my explicit authorization.
30. As the user, I want the key advice restated in the caller's next visible reply, so that I see it without opening tool output.
31. As the user, I want the primary's posture text injected at every session start by a plugin hook, so that it does not depend on the skill being loaded.
32. As the user, I want each delegate entry to carry its posture in its own instructions, so that delegates follow it without depending on an unverified hook capability.
33. As the user, I want worker consultation to follow the entry's posture without an automatic finish-blocking hook.
34. As the user, I want workers to finish without a hook inferring file-change ownership.
35. As the user, I want no before-done hook on the primary, because a primary's turn end is not a task end.
36. As the user, I want every dispatch's actual model and effort compared with the expected ones automatically, and a mismatch shown to the primary in the same session, so that inheritance mistakes are caught without a manual inspector run.
37. As the user, I want independent acceptance kept as a fresh-thread, packet-based review that a consultation can never replace.
38. As a primary agent, I want the acceptance dial chosen by the tier of the work being accepted, so that harder work gets a stronger reviewer.
39. As the user, I want a low-confidence acceptance verdict to leave acceptance pending and come to me, so that no automatic ladder replaces my decision.
40. As the user, I want thirteen native entries named by role and tier, so that I still never need to remember which model fills a tier.
41. As the user, I want the installer to delete the eleven 0.2.0 entry files as well as the eight 0.1.0 files, so that no old name stays discoverable.
42. As a maintainer, I want the verifier to prove that the routing profile, the templates, and the posture sections agree, so that the three places cannot drift.
43. As a maintainer, I want hook behaviour tested at the hook's command-line boundary, so that a hook change cannot silently break injection or dispatch verification.
44. As a maintainer, I want every new or changed runtime Markdown and TOML file to have its Chinese twin in the same change.
45. As a maintainer, I want ADR-0006 to name what it supersedes in ADR-0003, ADR-0004, and ADR-0005, and to record the host facts with invalidation checks.
46. As the user, I want a `0.3.0` version manual that looks like the 0.2.0 manual, checked by actually viewing both pages side by side.
47. As the user, I want push, marketplace upgrade, reinstall, and installer runs on my real homes left for me to authorize.
48. As the user, I want every live check to run in a temporary `CODEX_HOME` with credential copies deleted afterwards.

## Implementation Decisions

Requirement IDs are referenced by the tickets. "Derived" marks the spec's closure of a confirmed decision (ledger state Derived); it binds like the rest, and only the user may change it.

### Tiers and routing (TR)

- **TR-1** The tiers are `mainstay`, `crux`, and `rescue`. They replace light, standard, and senior for explorer, worker, and advisor. A tier is set by its models; effort is a finer grade inside the tier. The intent is that most tasks end in `mainstay` and very few reach `rescue`.
- **TR-2** The models are `gpt-6-luna`, `gpt-6-sol`, and `gpt-6-astra`. Terra is removed because the 6 series has none. No `gpt-5.6-*` model appears in the table.
- **TR-3** Dials, in the routing-profile notation `model[a*, b]`: every listed effort is allowed; `*` marks the default; `›` separates candidates in usage order.

  | Role | `mainstay` | `crux` | `rescue` |
  |---|---|---|---|
  | explorer | `gpt-6-luna[high*, xhigh]` › `gpt-6-sol[medium*, high]` | `gpt-6-luna[max]` › `gpt-6-sol[xhigh]` | `gpt-6-astra[medium*, high]` |
  | worker | `gpt-6-luna[max]` › `gpt-6-sol[high]` | `gpt-6-sol[xhigh*, max]` › `gpt-6-astra[low*, medium]` | `gpt-6-astra[high*, xhigh]` |
  | advisor | `gpt-6-astra[low*, medium]` | `gpt-6-astra[high]` | `gpt-6-astra[xhigh]` |

  The default of worker `crux` `astra` is `low` (Derived, ledger D4). The cell was unmarked, and the first listed effort is the default because order is usage order.
- **TR-4** Inside a cell, order is usage order: the first candidate is the default. Take a later candidate when the outcome depends more on judgment the packet cannot capture.
- **TR-5** First-round admission. New work starts in `mainstay`. It may start in `crux` when a key difficulty is already identified or interacting constraints must be handled. There is no usage quota. `rescue` is never a first-round choice unless the user declares it.
- **TR-6** Reserved, not enabled. A narrower first-round `crux` admission is kept in the records only: invisible failure (available checks cannot establish correctness), costly failure (a failed attempt blocks dependent work or is hard to revert), evidence of predicted failure (diagnosis already failed, or the same problem has a failure record), or a user declaration. Only the user enables it, based on their own observation.
- **TR-7** Escalation. After a capability failure, the work moves to the next tier; it does not move to another model of the same tier unless no other choice exists.
  - The next dial's model level is not lower than the failed dial's (`gpt-6-luna` < `gpt-6-sol` < `gpt-6-astra`), unless no other choice exists.
  - If it is the same model, the effort must be higher.
  - Above that floor, choose by the difficulty the failure exposed. Example: an explorer failing on `gpt-6-sol[high]` in `mainstay` escalates to `crux` `gpt-6-sol[xhigh]`, not `gpt-6-luna[max]`.
- **TR-8** Failure counting.
  - One capability failure is a complete attempt that fails acceptance, plus one rework in the same thread at the same dial that also fails, with the diagnosis attributing the cause to capability.
  - Rework is not counted separately. Environment problems and contract gaps are not failures.
  - A major execution problem (repeated tool failures, runaway, a reserved item touched) may skip the rework and counts as one failure.
  - The path is `mainstay` → `crux` → `rescue` → the user. `rescue` is reached only through `crux` or a user declaration; a task that started in `crux` reaches `rescue` after one `crux` failure.
  - R3 stays as a guard: a model is raised at most once.
- **TR-9** The routing profile records two declared assumptions: a model change gains more than an effort increase, and `xhigh` is a distinct jump. Both are invalidated by the next model generation change. The rumour that Anthropic will remove effort levels is not a basis for any rule.

### Process consultation, posture, acceptance (AC)

- **AC-1** Independent acceptance stays: a packet-based review in a fresh thread, allowed read-only checks, after the primary's own checks. It is required for high-risk work or an explicit review request, as today. A consultation never substitutes for it.
- **AC-2** The acceptance dial follows the tier of the accepted work:
  - `mainstay` work → `ca_advisor_mainstay` at its default effort.
  - `crux` work → `ca_advisor_crux`.
  - `rescue` work → `ca_advisor_rescue`.
  - Work the primary authored → the lowest advisor dial not weaker than the primary's dial. Ordering: model level first (`gpt-6-luna` < `gpt-6-sol` < `gpt-6-astra`), then effort (`low` < `medium` < `high` < `xhigh` < `max`). If no advisor dial is not weaker, use the strongest, `gpt-6-astra[xhigh]`.
  - A primary whose exact model id is not in the routing profile (for example `gpt-5.6-terra`) → `gpt-6-astra[xhigh]` (Derived, D16a).
  - Work built by several tiers → the highest tier involved (Derived, D16a).
  - A verdict that reports low confidence leaves acceptance pending and goes to the user. There is no automatic re-review at a higher dial.
- **AC-3** Process consultation replaces the Advisor decision packet.
  - It is callable with zero parameters by the primary, by any worker, and by any explorer.
  - It automatically carries the caller's current effective context: everything the caller's model would receive on its next request. That is the latest compaction summary if any, every message and tool call/result after it (including the earliest turns still in context), and the tool calls and results of the caller's current, unfinished turn. A recent-turn window qualifies only if it provably covers all of that for every session state, not just in the tested scenario. Details already removed by compaction are not recovered (Derived, D43).
  - The advisor model runs with no tools. Read-only tools do not count as no tools. Evidence is the actual tool set of the advisor request, as sent or as recorded by the host, shown empty. A refused tool attempt, one unavailable tool, or the model saying it has no tools is not evidence (Derived, D44).
  - It returns exactly one of a plan (concrete next steps), a correction (the caller is on a wrong path), or a stop signal (halt and escalate to the user). The advisor produces no user-facing output.
  - Every result states the advisor's actual model and effort.
  - A failed consultation returns an explicit failure, never fabricated advice.
  - It reaches the advisor model only through Codex's own authenticated paths (native spawn, App Server, `codex exec`). The component never reads, copies, or transmits credentials itself (Derived, D41).
  - The mechanism is chosen by ticket 01 (§Mechanism decision).
- **AC-4** The consultation dial follows the caller:
  - A `mainstay` entry → `gpt-6-astra[low]`.
  - A `crux` entry → `gpt-6-astra[high]`.
  - A `rescue` entry → `gpt-6-astra[xhigh]`.
  - The primary → the lowest advisor dial not weaker than the primary's dial, with the AC-2 ordering. If none is not weaker, use `gpt-6-astra[xhigh]`. A primary model not in the routing profile gets `gpt-6-astra[xhigh]`.
  - The advisor has no ladder of its own.
- **AC-5** Posture choice. Compare the caller's exact model id with the model id of the advisor dial AC-4 assigns to that caller. The same model gets the **reduced posture**; a different model gets the **full posture**. No list of model families is hard-coded.
  - The user's current primary (`gpt-6-astra`, `xhigh`) gets the reduced posture.
  - A `gpt-5.6-terra` primary gets the full posture.
  - Entries on `gpt-6-luna` or `gpt-6-sol` get the full posture; entries on `gpt-6-astra` get the reduced posture.
  - The **full posture**:
    - Consult before substantive work. Orientation does not count: finding files, reading sources, seeing what is there.
    - Consult when stuck: errors recurring, an approach not converging, results that do not fit.
    - Consult when considering a change of approach.
    - Consult before declaring done, after making the deliverable durable (written or saved, never committed).
    - On multi-step tasks, consult at least once before committing to an approach and once before declaring done. A short task whose next step follows directly from the tool output just read needs no consultation.
    - When earlier evidence points one way and the advice another, make one reconcile call instead of silently switching.
  - The **reduced posture**: consult only before committing to an approach and before declaring done, on multi-step tasks.
  - Both postures: restate the key guidance in the next visible reply.
- **AC-6** Adoption.
  - Adopt advice by default.
  - Deviate, with a stated reason, when following a step fails empirically or primary-source evidence contradicts a specific claim. A passing self-test is not evidence the advice is wrong.
  - Reject directly, with a stated reason, advice that conflicts with a user constraint, an authorization, a reserved interface, or a repository rule.
  - Rejecting for a reasoning flaw depends on the models. If the advisor's model differs from the caller's, first make one reconcile call ("I found X, you suggest Y; which constraint breaks the tie?"). If the models are the same, the caller may reject directly with a stated reason (Derived, D22).
  - Advice grants no authorization, veto, or new requirement.
- **AC-7** The posture text is the canonical text of both variants plus the AC-6 rules. It adapts rpiv-advisor's `DEFAULT_PROMPT_GUIDELINES` with these changes:
  - "commit the change" is removed; durable means written or saved.
  - The triggers are imperative, never "allowed".
  - The reduced variant keeps only its two triggers.
  - The restate-in-next-reply rule stays.
- **AC-8** Always-on text. A plugin-shipped `SessionStart` hook puts the primary's posture variant (AC-5) into the primary session's context at every session start, including a resumed session, whether or not the orchestration skill is loaded. A delegate never receives two different variants (see EN-5). This holds once the user has trusted the hooks (AC-12).
- **AC-9 — Cancelled by the user on 2026-09-26.** No `SubagentStop` enforcement ships. The worker still follows its canonical consultation posture, but no hook blocks its finish or infers its file changes. No hook blocks the primary's `Stop` (D30). This supersedes D29, the earlier AC-9 deferral, and O3's blocking clause; it does not weaken consultation success validation.
- **AC-10** Per-dispatch verification.
  - Every native dispatch of a `ca_*` entry has its actual model and effort compared automatically with the expected ones. Expected means the pinned effort, or the effort passed at spawn. A caller-effort entry spawned without an effort is a mismatch.
  - Every consultation result's actual model and effort are compared with the AC-4 dial.
  - A mismatch is shown to the primary in the same session without a manual inspector run, and the affected work stays pending.
  - Installation checks stay reusable for the task.
- **AC-11** No observation machinery. Nothing adds markers, persistent logs, or statistics for watching behaviour. The user judges effects by their own observation. Necessary temporary execution state lives only for one session and is deleted at completion or cannot be read by any later session. Nothing is written to the repository, to `CODEX_HOME`, or to any path meant to outlive the session. Nothing is aggregated across sessions.
- **AC-12** Hook trust is the user's gate. The Codex Hooks documentation (read 2026-09-26) says:
  - Non-managed hooks, including plugin-bundled ones, run only after the user reviews and trusts them in `/hooks`.
  - Installing or enabling a plugin does not trust its hooks.
  - Trust is keyed to each hook's current hash, so a new or changed hook is skipped until trusted again. Codex prints a startup warning pointing to `/hooks`.

  Consequences:
  - The plugin, its installer, and its documentation never mark hooks trusted, never edit trust state, and never pass `--dangerously-bypass-hook-trust` in anything the user runs (Derived, D42).
  - Install, update, and release instructions include the `/hooks` review: after first install, and after every update that changes a hook definition (DR-8, DR-10, DR-11).
  - Tests and live checks distinguish "skipped because untrusted" from "trusted but failing". An untrusted skip is never evidence for or against AC-8 to AC-10, and never triggers S5.
  - Automated live checks may use the trust bypass only in a temporary home under O4(a), selected by the user on 2026-09-26. At least one run still requires the user's `/hooks` trust, and one must record the untrusted skip and its warning.
  - D49: the user waived repeating the manual trust test after the final cross-platform launcher change. Earlier trusted/untrusted results remain evidence for their tested definitions; manual trust execution of the final definition is unverified. This waiver does not change installation or update trust requirements.
  - The plugin adds no detection of its own for untrusted hooks; the host's startup warning is the signal (Derived, D46).

### Native entries, installer, inspector (EN)

- **EN-1** Thirteen native entries, filenames `ca-<role>-<tier>[-m|-h].toml`, `name` fields `ca_<role>_<tier>[_m|_h]`. `_m` is the first (default) candidate and `_h` the second. Effort is pinned where the cell has one effort (the ADR-0004 rule):

  | Entry | Model | Effort |
  |---|---|---|
  | `ca_explorer_mainstay_m` | `gpt-6-luna` | caller (`high*`, `xhigh`) |
  | `ca_explorer_mainstay_h` | `gpt-6-sol` | caller (`medium*`, `high`) |
  | `ca_explorer_crux_m` | `gpt-6-luna` | pinned `max` |
  | `ca_explorer_crux_h` | `gpt-6-sol` | pinned `xhigh` |
  | `ca_explorer_rescue` | `gpt-6-astra` | caller (`medium*`, `high`) |
  | `ca_worker_mainstay_m` | `gpt-6-luna` | pinned `max` |
  | `ca_worker_mainstay_h` | `gpt-6-sol` | pinned `high` |
  | `ca_worker_crux_m` | `gpt-6-sol` | caller (`xhigh*`, `max`) |
  | `ca_worker_crux_h` | `gpt-6-astra` | caller (`low*`, `medium`) |
  | `ca_worker_rescue` | `gpt-6-astra` | caller (`high*`, `xhigh`) |
  | `ca_advisor_mainstay` | `gpt-6-astra` | caller (`low*`, `medium`) |
  | `ca_advisor_crux` | `gpt-6-astra` | pinned `high` |
  | `ca_advisor_rescue` | `gpt-6-astra` | pinned `xhigh` |

  Explorer and advisor entries keep `sandbox_mode = "read-only"`; worker entries inherit the parent sandbox. Advisor entries answer the acceptance (REVIEW) packet only; the DECISION packet shape is removed. If the ticket 01 mechanism needs extra native entries for consultation, ticket 04 adds them under the same naming rule and updates the routing profile, manifest, twins, and checks.
- **EN-2** `agents/retire.txt` keeps the eight 0.1.0 names and adds the eleven 0.2.0 filenames, from `ca-explorer-light.toml` to `ca-advisor-senior.toml`.
- **EN-3** Installer selectors are the tier-based short names of the thirteen entries (`explorer-mainstay-m` … `advisor-rescue`). The overwrite-own, retire, check, and refusal semantics of ADR-0004 are unchanged.
- **EN-4** The inspector keeps its evidence contract and `--agent`/`--effort` interface. Its tests stay table-driven over the shipped templates.
- **EN-5** Each explorer and worker entry's `developer_instructions` contain one delimited posture section.
  - The section equals, byte for byte, the canonical variant that AC-5 assigns to that entry: full for `gpt-6-luna`/`gpt-6-sol` entries, reduced for `gpt-6-astra` entries.
  - Outside that section, all entries of one role stay byte-identical.
  - Advisor entries have no posture section.
  - The section states the rule's outcome; it never asks the delegate to infer its own model.
  - If ticket 01 finds that `SessionStart` also fires in subagent sessions, the hook must not inject a second variant into them.
- **EN-6** Every new or changed runtime Markdown file under `plugins/codex-advisor/` and every TOML template has its Chinese twin under `docs/zh/`, in the same change.

### Doctrine, records, release (DR)

- **DR-1** `SKILL.md`:
  - The allocation, ladder, and admission text follows TR-1…TR-8.
  - The first-round pool, the senior gate, and the decision packet are removed.
  - The "Seek judgment when it changes a decision" section is replaced by the consultation posture and the adoption rules (AC-3…AC-6), pointing to the posture reference.
  - The acceptance text follows AC-1/AC-2.
  - The complete-attempt definition, the fresh-thread rule, Architect mode, and ADR-0005 acceptance ownership are unchanged in meaning.
  - No model name or effort value appears in `SKILL.md`.
- **DR-2** `references/routing-profile.md` contains:
  - the declaration date and the anchored models;
  - the TR-3 table with entry names;
  - the AC-4 consultation mapping and the AC-2 acceptance mapping;
  - the dial ordering used by "not weaker";
  - the TR-9 declared assumptions with their invalidation trigger;
  - the adjustment method.

  It remains the only place where dial values are written.
- **DR-3** A new `references/consult-posture.md` holds the canonical AC-7 text: the full variant, the reduced variant, and the adoption rules, each in a delimited block that EN-5 and AC-8 copy or read without modification. It has a Chinese twin.
- **DR-4** `references/role-contracts.md` keeps the explorer and worker packets, keeps the acceptance packet with the AC-2 dial and the low-confidence rule, removes the decision packet, and states that consultation takes no packet.
- **DR-5** `references/operations.md` is updated section by section by the owning tickets:
  - ticket 02: §Recover and hand off actual state, §Advice and independent acceptance;
  - ticket 03: §Install and discover, §Select a native entry, §Invoke and validate, and the verifier groups in §Verify changes;
  - ticket 04: a new §Process consultation;
  - ticket 05: a new §Hooks and the hooks group in §Verify changes.
- **DR-6** `CONTEXT.md`:
  - Add mainstay, crux, rescue, process consultation, full and reduced posture, and reconcile call.
  - Rewrite capability tier, escalation ladder, independent acceptance, and routing profile.
  - Retire first-round pool, senior gate, and decision packet, and add `_Avoid_` entries for them.
- **DR-7** ADR-0006 records the decisions of this spec and names every sentence it supersedes in ADR-0003, ADR-0004, and ADR-0005. At minimum that covers ADR-0004's first-round pool, senior gate, eleven entries, Advisor defaults, and its "0.3.0 grok lane" note, which becomes `0.4.0`. It also records the ticket 01 mechanism decision and the host facts, each with an invalidation check. It records AC-12's `/hooks` review as the one user step that ADR-0004's "everything arrives through installation or update" rule cannot remove, because it is a host security gate.
- **DR-8** `README.md` covers install, use, the thirteen entries by role and tier without dial values, consultation and hooks, check and update, and an upgrade section naming the eleven retired 0.2.0 entries and their replacements. The install and update steps include the AC-12 `/hooks` review and say that untrusted hooks are skipped with a startup warning.
- **DR-9** `plugin.json`: `version` becomes `0.3.0`. `description`, `shortDescription`, `longDescription`, and `keywords` describe the new tiers, consultation, and hooks without model names. Any `hooks` or consultation-component fields are added by the tickets that need them.
- **DR-10** `docs/releases/0.3.0.html`:
  - It is Chinese and contains `本版说明` and `相对上一版`, per `docs/agents/version-manual.md`.
  - `本版说明` is complete for 0.3.0: install (including the AC-12 `/hooks` review), use, entries and tiers, the frozen routing-profile table, admission, escalation, consultation and posture, hooks, acceptance, checks, and known limits.
  - `相对上一版` lists every change from 0.2.0 with its reason and an ADR-0006 reference.
  - The visual system follows §Visual acceptance.
- **DR-11** Release steps are listed, not run: push to `origin`, then on WSL and Windows run the marketplace upgrade, the plugin reinstall, the companion installer, and the `/hooks` review of the plugin's hooks in a fresh interactive session (AC-12). ADR-0006 records the grok lane as `0.4.0`.

### Cross-cutting (X)

- **X-1** Commits, pushes, marketplace upgrades, plugin reinstalls, and installer runs against the user's real `CODEX_HOME` need the user's explicit authorization at the time. Without it, Codex leaves changes in the working tree and reports.
- **X-2** Codex executes this spec under the installed 0.2.0 plugin.
  - Do not dispatch the new entry names from the user's real installation.
  - Every live check uses a temporary `CODEX_HOME` per operations.md §Install and discover. Copy only the needed `auth.json`/`config.toml`, and delete copies, workspaces, and logs afterwards.
  - **Install the working tree into the temporary home this way**, verified on 2026-09-26 with Codex `0.156.0` and no model call:

    ```sh
    export CODEX_HOME=<temporary dir>
    codex plugin marketplace add <this checkout's absolute path>
    codex plugin add codex-advisor@codex-advisor
    ```

    The plugin is copied to `$CODEX_HOME/plugins/cache/codex-advisor/codex-advisor/<version>/`. After every change, run `codex plugin remove codex-advisor@codex-advisor` and then `codex plugin add` again so the copy matches the working tree. Install the entries with that copy's `scripts/install-agents.sh`.
  - Codex warns that it will not create helper binaries under `/tmp`. If a check depends on them, place the temporary home outside `/tmp`.
  - Never push, never upgrade or edit the user's real marketplace, and never touch the real `CODEX_HOME` to make a live check see local changes. If the local route above cannot expose a change, stop (S9).
  - Live-check parents run at the cheapest setting, for example `-c model_reasoning_effort="low"`, because the copied `config.toml` makes every parent `gpt-6-astra[xhigh]`. Only scenarios that test the primary's own model or effort use it: the AC-4 primary cases, `SessionStart` injection by model, and the primary consultation.
  - Never hand-edit installed entries.
  - Architect mode is not authorized by this spec.
- **X-3** AC-11 holds across the whole change. Final acceptance checks it (§Requirement ownership).
- **X-4** A runtime file and its twin change together; `python3 tests/test_zh_mirror.py` passes at every ticket's acceptance.
- **X-5** Outside the retire list, the README upgrade section, ADR history, earlier version manuals, and the 0.3.0 manual's `相对上一版`, none of these appear in the plugin, the mirror, or the README:
  - the eleven 0.2.0 entry names;
  - the tier words light, standard, and senior used as tiers;
  - "first-round pool", "senior gate", or "decision packet".

  X-5 applies in full at final acceptance. Before that, a ticket's own text search covers only the files that ticket owns, so it never fails on text a later ticket still has to change (tickets 02 and 03 name their scopes).

### Mechanism decision (filled by ticket 01)

Ticket 01 writes here, and in ADR-0006, the consultation mechanism it selects, with its evidence reference in `acceptance.md`.

- **Candidates:**
  - A: native spawn with a positive-integer `fork_turns` and a pinned advisor entry.
  - A': App Server `thread/fork`, then `thread/resume` with a model override.
  - B: an MCP tool that rebuilds the context from the session record and calls `codex exec`.
- **Eligibility:** a configuration is eligible only if all five checks pass:
  1. the current unfinished turn's tool calls are visible (nonce test);
  2. the actual model and effort equal the AC-4 dial;
  3. the post-compaction context is visible (summary plus later messages);
  4. the advisor has no tools, shown by the request's actual empty tool set (AC-3);
  5. the earliest still-effective context is visible. In a session with more uncompacted turns than any window the configuration uses, a constraint stated in the first uncompacted turn reaches the advisor. A configuration with a bounded window must also state the rule that makes the window cover the whole current effective context in every session state (AC-3).

  It must also be callable from the primary, a worker, and an explorer. One failed configuration rejects only that configuration; untested configurations are recorded as untested.
- **Selection:** among eligible configurations, ticket 01 chooses and records its reasons (implementer's choice). If none is eligible, stop (S3/S4).

Status: decided on 2026-09-26 after the user authorized continued investigation. Select **B′: zero-argument MCP, effective-history reconstruction from one caller rollout snapshot, and native App Server structured injection**. This extends candidate B with `thread/start` and `thread/inject_items` instead of text serialization through `codex exec`. See [acceptance.md, section 01 P6](acceptance.md#p6-authorized-continuation-and-selected-mechanism) for every tested configuration, thread ID, actual request comparison, and limitation.

The component binds host MCP `_meta` thread/turn/item identity to one caller record, reconstructs all effective `response_item` history, replaces that history at each `compacted.replacement_history`, and excludes the in-flight consultation. It uses no bounded turn window and accepts no caller summary. It preserves roles, tool calls/results, image content, and opaque reasoning. A fresh ephemeral App Server thread receives source base instructions, the structured history, and consultant-specific instructions that preserve caller constraints. An unsupported or incomplete reconstruction returns an explicit failure.

The advisor process starts with a model catalog that removes shell, patch, and experimental tools, together with the qualified tool-disable settings. Every advisor request's actual empty tool set and actual AC-4 dial are checked through the host inference-request trace. Trace/catalog files are temporary, subject to AC-11; the component never handles credentials. The installed MCP configuration uses a relative script path and `cwd="."`, verified to resolve to the plugin root. Caller-home discovery uses the qualified versioned cache layout, with explicit failure on an unsupported layout.

Eligibility passed for an unfinished-turn nonce; the actual dial and empty request tools; forced and intra-turn automatic compaction; the earliest constraint after eleven uncompacted turns; and primary, worker, and explorer callers. Additional checks preserved truncated output, image content, and encrypted reasoning across the Luna-to-Astra boundary. B′ is selected because it is the only qualified configuration and structured injection retains content that prompt serialization would flatten. The fork-plus-current-turn splice is rejected because it resurrected pre-compaction history and omitted a new intra-turn summary.

These are mechanism probes on Codex `0.157.0`, not product acceptance. Ticket 04 implements and verifies AC-4 routing, strict result validation, identity binding, supported content shapes, explicit failures, cancellation, and temporary-state cleanup. Requalify after host/schema/catalog/MCP metadata/cache-layout/request-trace changes. Unsupported rollback or other unqualified context shapes must fail explicitly. The user-trusted hook run and untrusted warning/skip evidence passed in acceptance section 01 P7. This host presented the user's trust action in its startup review dialog; `/hooks` independently showed the changed hook inactive and awaiting review. All probe environments were removed.

## Decision Boundaries

- **Must follow:** every TR, AC, EN, DR, and X requirement; every ledger item in state Confirmed or Derived. A Rejected ledger item must not be reintroduced in any form, including as a fallback.
- **Implementer's choice** (record the choice and reason in the ticket's acceptance section):
  - the consultation mechanism among eligible configurations;
  - the consultation component's language, file layout, and internal structure;
  - whether the consultation includes the caller's tool inventory;
  - the transcript evidence used for dispatch identity and consultation result validation, within AC-11 (the format is unstable, so tests must pin fixtures);
  - how AC-10 is automated (a `SubagentStart` hook, a `PostToolUse` hook on the spawn tool, invoking the inspector, or another automatic per-dispatch route);
  - the delimiter syntax of the posture section;
  - the wording of README and the version manual within DR-8/DR-10;
  - screenshot tooling;
  - test organisation.
- **Needs the user:**
  - any change to a Confirmed or Derived decision;
  - enabling TR-6;
  - anything in §Stop and return;
  - any release step in X-1;
  - a new visual pattern the baseline cannot express;
  - the open decisions below.

## Open Decisions

Both decisions below were resolved by explicit user replies on 2026-09-26 during ticket 01. Option (a) is binding for each; the other options remain here only as decision history. These decisions do not waive any stop condition or the required user-trusted hook run.

Later on 2026-09-26 the user explicitly cancelled AC-9's automatic worker finish
blocking, retained posture injection, dispatch verification and consultation,
authorized ticket 06, and declared a fresh Astra xhigh Advisor for final acceptance.
The user initially authorized commit, push, and WSL/Windows updates after
acceptance, then narrowed delivery to a local commit only: do not push or update
either real installation. The former ticket 05 dependency now consumes only its retained scope.
The original O3 alternatives below are history: only successful consultation still
counts, and failures remain pending until success or user release, but no stop hook
enforces that policy. O4 and the real-installation hook trust gate remain unchanged.

- **O3 — Resolved: option (a). What counts as the before-done consultation for AC-9, and what a failed one means.** Ticket 04 must make started, succeeded (a valid plan, correction, or stop at the expected dial), and failed consultations distinguishable. Ticket 05 follows option (a):
  - (a) Only a successful consultation counts. After a failed one, the hook still blocks once, within the existing one-block limit. The failure is shown to the primary, and the worker's work stays pending until a successful consultation or the user's release.
  - (b) Only a successful consultation counts. After a failed one, the hook still blocks once, within the existing one-block limit. The failure is shown to the primary, but the work's status is not changed by it.
  - (c) Any consultation attempt counts. A failure is shown to the primary.
- **O4 — Resolved: option (a). Hook trust route for automated live checks in a temporary `CODEX_HOME`.** Automated checks may follow option (a); the required run trusted by the user through `/hooks` remains a user gate:
  - (a) Allow `--dangerously-bypass-hook-trust` only in temporary-home live checks. At least one run must use hooks the user trusted through `/hooks`, and one run must record the untrusted skip and its warning.
  - (b) No bypass. Every hook live check uses hooks the user trusted through `/hooks` in the temporary home, and the user re-trusts after each hook change.

## Stop and Return

Stop the affected work, record the evidence in `acceptance.md`, and return to the user when any of these happens. Do not substitute a rejected option.

- **S1** `gpt-6-luna` or `gpt-6-sol` is not callable on the account, or any TR-3 dial fails to run at its model and effort. Do not substitute `gpt-5.6-*` models or change the table.
- **S2** On Codex `0.156.0` or later, a template's `model` or `model_reasoning_effort` no longer takes precedence as ADR-0004 recorded, so pinned dials cannot be guaranteed.
- **S3** No consultation configuration passes all five eligibility checks. Do not ship a packet-based or tool-bearing consultation.
- **S4** The eligible mechanism cannot be called from a worker or an explorer.
- **S5** With the hooks trusted (AC-12), plugin-shipped hooks do not load or `SessionStart` cannot inject context. A skip because the hooks are untrusted is not S5. Do not fall back to a primary `Stop` hook (D30) or to skill-only text.
- **S6** AC-10 cannot be automated by any per-dispatch route.
- **S7** Ticket 06 content cannot be expressed with the baseline's components.
- **S8** Any change to a Confirmed or Derived decision appears necessary.
- **S9** The X-2 local install route cannot make a temporary home run this checkout's current plugin, including its hooks and consultation component.

## Requirement Ownership

| Requirements | Established by | Consumed by | Accepted when | Observable evidence |
|---|---|---|---|---|
| TR-2, TR-3 host availability; S1, S2 | 01 | 02, 03 | End of 01 | Probe table in `acceptance.md` §01: each TR-3 dial run with observed model and effort, thread ID, inspector exit |
| AC-3 mechanism, eligibility; S3, S4 | 01 | 04 | End of 01 | Per-configuration five-check table in `acceptance.md` §01; §Mechanism decision filled |
| AC-8/AC-9/AC-10 host capability; AC-12 trust facts; S5, S6 | 01 | 05, 06 | End of 01, except the rows that need trusted running hooks, which are filled before 05 starts (O4) | Hook capability table in `acceptance.md` §01, with the trust state of every run |
| TR-1, TR-4…TR-8 doctrine text; DR-1, DR-4, DR-6, DR-7 | 02 | 03–06 | End of 02 | Text checks in ticket 02; mirror test |
| TR-2, TR-3, TR-9 in the routing profile; DR-2 | 03 (kept with the templates so the verifier's profile-to-template check never runs against a half-changed pair) | 04, 05, 06 | End of 03 | `verify.sh` installation group; routing-profile table equals TR-3 cell by cell |
| AC-5, AC-6, AC-7 canonical text (DR-3) | 02 | 04 (EN-5), 05 (AC-8), 06 (manual) | End of 02 text; again at 04 and 05 | `consult-posture.md` has both variants and the adoption rules, no "commit" step; 04 and 05 checks compare against it byte for byte |
| AC-1, AC-2 doctrine | 02 | 03 (advisor entries), 06 | End of 02 | Role-contracts and SKILL text checks |
| EN-1…EN-4, EN-6, DR-5 (03 sections) | 03 | 04, 05, 06 | End of 03 | `verify.sh` installation and runtime groups; live route check of 13 entries in `acceptance.md` §03 |
| AC-3, AC-4, AC-10 (consultation part), EN-5 (posture sections, added with the consultation so no entry points to a missing feature), DR-5 (04 section) | 04 | 05, 06 | End of 04 | Consultation test group; posture checks and their negative proofs in the installation group; live consultation table in `acceptance.md` §04 |
| AC-8, AC-10 (dispatch part), AC-11 (hook state), AC-12 (untrusted versus failing), DR-5 (05 section); AC-9 cancelled | 05 | 06 | End of the retained scope of 05 | Hooks test group; live hook table in `acceptance.md` §05 with the trust state of each run |
| AC-12 user-facing trust step | 06 | final | End of 06 | README, manual, and release commands each contain the `/hooks` review for first install and for updates that change hooks |
| DR-8, DR-9, DR-10, DR-11 | 06 | final | End of 06 | `tests/test_version_manual.py`; visual table and screenshots in `acceptance.md` §06 |
| X-1…X-5, every Rejected ledger item stays out, goal-drift list | every ticket (own scope) | — | Final acceptance stage, after 06 | Final sweep in `acceptance.md` §Final: text searches, file-write review of hooks and consultation for AC-11, independent acceptance verdict |

Final acceptance stage, owned by the Codex primary after ticket 06:

- Run the unqualified `verify.sh`, both tests, and `git diff --check`.
- Sweep every requirement ID against its evidence.
- Run the X-5 and rejected-item searches.
- Review every file write in hooks and consultation code against AC-11.
- Check the goal-drift list below item by item.
- Obtain independent acceptance. This change blocks agents and forwards full context, which static checks cannot fully establish, so it is treated as high-risk under the installed doctrine.
  - The dial follows AC-2 (user decision U10.2): the work spans several tiers and includes primary-authored parts on `gpt-6-astra[xhigh]`, so the dial is `gpt-6-astra[xhigh]`.
  - Under the installed 0.2.0 plugin that dial is `ca_advisor_senior` at effort `xhigh`, run in a fresh thread.
  - The 0.2.0 doctrine opens the senior Advisor only on a user declaration. The user supplied that declaration on 2026-09-26 with the scope amendment above; do not ask again. Never substitute `ca_advisor_light` or `ca_advisor_standard`.
- Record everything in `acceptance.md` §Final.

## Goal-Drift Checks

Each of these can satisfy some acceptance text and still miss the goal. Each must be ruled out explicitly at the owning ticket and again at final acceptance.

- A consultation that returns advice while running on the caller's inherited model (AC-3, AC-10).
- A consultation that receives a summary the caller wrote instead of the automatic context, or that misses the current unfinished turn (AC-3).
- An advisor that has read-only tools during consultation (AC-3).
- A `SessionStart` hook that injects the old permissive wording, both variants, or a variant chosen by model-family name instead of model identity (AC-5, AC-7, AC-8). A `gpt-5.6-terra` primary must get the full posture.
- A worker finish-blocking hook after AC-9 was cancelled, or any primary `Stop` hook (D30).
- Posture sections in entries that differ from the canonical text or tell a delegate to infer its model (EN-5).
- A routing profile that keeps `gpt-5.6-*` models or Terra (TR-2).
- First-round `crux` blocked by the reserved narrow rule, or `rescue` offered at first round (TR-5, TR-6).
- An escalation that switches models inside a tier, or lowers the model level (TR-7).
- A consultation accepted as independent acceptance, or independent acceptance skipped for high-risk work (AC-1).
- Logs, markers, or state files added "for testing" that persist after the session (AC-11).
- A version manual that passes `tests/test_version_manual.py` but is not visually the 0.2.0 system, or that nobody looked at (DR-10).
- An installer that leaves 0.2.0 entry files installed (EN-2).
- A consultation that sees only the most recent turns, so that a still-effective constraint from an earlier turn is lost, while the nonce and compaction checks pass (AC-3, eligibility check 5).
- A "no tools" claim backed only by a refused tool attempt or the model's own statement (AC-3, eligibility check 4).
- Hooks that pass only under the trust bypass or in a pre-trusted test home, while the user's install and update steps omit the `/hooks` review (AC-12).
- A failed consultation presented as a completed consultation.

## Testing Decisions

A good check observes behaviour at a boundary a caller uses: a script's command line, a hook's stdin/stdout/exit code, the consultation's call interface, a rendered page. No check reads internal function names or prompt wording beyond the canonical posture text, which is itself a contract.

1. **Existing seam, `verify.sh` installation group.** Extended for the thirteen templates:
   - the routing profile names exactly the shipped entries, with the same model and pinned efforts;
   - pinned exactly when the cell has one effort;
   - explorer and advisor entries read-only;
   - same-role instructions identical outside the posture section;
   - each posture section byte-equal to the variant AC-5 assigns (computed from the routing profile's model identities, not a family list);
   - advisor entries without a posture section;
   - retire list containing the eleven 0.2.0 names;
   - installer overwrite, retire, check, and refusal cases.

   Ticket 03 adds the profile, template, and retire checks. Ticket 04 adds the three posture checks (section equality, none in advisor templates, identity outside the section). Until ticket 04, the existing same-role check stays unchanged.
2. **Existing seam, `verify.sh` runtime group.** The inspector cases stay table-driven over the thirteen templates.
3. **New seam, `verify.sh` hooks group** (for example `--hooks`; the unqualified run includes it). Each hook is run at its command-line boundary with JSON events on stdin; assert stdout and exit code:
   - `SessionStart` with model `gpt-6-astra` (reduced), `gpt-6-sol` (full), `gpt-5.6-terra` (full), including a resumed session;
   - no worker or primary finish-blocking hook is registered;
   - the AC-10 route with a matching dispatch (silent), a mismatched model, a mismatched effort, and a caller-effort entry spawned without an effort (each surfaced).
4. **New seam, consultation boundary** (a `verify.sh` group). The component is called with zero parameters, and the model call is replaced by a fixture executor. Assert:
   - the fixture context including an unfinished turn, a compaction summary, and a constraint from the earliest uncompacted turn of a long session reaches the executor;
   - the executor is invoked with no tools and with the AC-4 dial for each caller type;
   - the result is exactly one of plan, correction, or stop, with model and effort;
   - executor error, abort, and empty output return explicit failures;
   - no file is written outside AC-11's per-session location.
5. **Existing tests.** `python3 tests/test_zh_mirror.py` (Markdown and TOML twins) and `python3 tests/test_version_manual.py` (for `0.3.0`).
6. **Live checks in a temporary `CODEX_HOME`**, recorded in `acceptance.md`: ticket 01 probes; ticket 03 route check of the thirteen entries (one spawn each, inspector per child); ticket 04 consultations from a primary, a worker, and an explorer, with the nonce, compaction, earliest-context, and no-tools checks; ticket 05 hook behaviour in real sessions, each run recording whether the hooks were trusted through `/hooks`, bypassed (only if O4 allows it), or untrusted. These establish dispatch and wiring, not quality or cost. They consume the account's quota: keep each scenario to the smallest prompt that shows the behaviour, and run parents at the cheapest setting except where X-2 says otherwise. Install the working tree only by the X-2 route.
7. **Visual comparison** of the version manual, per §Visual acceptance.

Prior art: the verifier's two groups, the mirror and manual tests, `.scratch/tier-role-pool/acceptance.md` for the live route check record, and rpiv-advisor's tests (`advisor.execute.test.ts`, `advisor.strip.test.ts`) for consultation behaviour cases.

## Visual Acceptance (Version Manual)

- **Baseline:** `docs/releases/0.2.0.html` at commit `f812f9b` (SHA-256 above). The magazine preview is not a baseline.
- **Scenes.** Render the baseline and `docs/releases/0.3.0.html` with identical settings:
  - V1: the hero and side rail at 1440×900, light scheme.
  - V2: the entries and dial-table section (the counterpart of 0.2.0's 十一个入口) at 1440×900.
  - V3: the start of `相对上一版` with its change cards at 1440×900.
  - V4: the hero at 390×844, below the 760px breakpoint.
  - V5: the hero at 1440×900 in the dark colour scheme.
- **Must match the baseline:** typefaces, light and dark palettes, the rail-and-main layout grid, heading, kicker, card, table, callout, and code styles, breakpoint behaviour, print styles, and self-contained assets (no external requests).
- **Allowed to differ:** text, section count and order, row and card counts, table contents, and new sections composed from existing components.
- **Method:**
  - Capture both pages with a headless Chromium. The Playwright-cached binary `/home/hyy/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome` was present on 2026-09-26; any equivalent is allowed.
  - Save the PNG pairs under `.scratch/tiers-and-advisor-consult/visual/` as `<scene>-baseline.png` and `<scene>-0.3.0.png`.
  - Open and look at every pair.
  - Write per-scene observations and a pass or fail in `acceptance.md` §06.
- **Functional versus visual:** functional checks (the manual test, required phrases, content completeness per DR-10) are separate and never substitute for this. A visual failure is fixed in `0.3.0.html`, never by editing the baseline.

## Out of Scope

- The grok lane, which is now `0.4.0`.
- Enabling TR-6.
- Any marker, log, or statistic for observing tier or consultation use.
- A primary `Stop` hook.
- Changes to the sibling plugin.
- Architect mode, the fresh-thread policy, and ADR-0005 acceptance ownership beyond the dial and the removal of the decision packet.
- Measuring quality, cost, or stability gains.
- Windows-side live checks: the release steps for Windows are user-gated.

## Further Notes

- **Tickets and order:**
  - 01 host probes and the mechanism decision;
  - 02 doctrine, posture text, glossary, ADR-0006;
  - 03 routing profile, native entries, installer, inspector, route check;
  - 04 process consultation and the entries' posture sections;
  - 05 plugin hooks;
  - 06 README, `plugin.json`, version manual, release preparation;
  - then the final acceptance stage.

  The chain is linear because tickets 02 to 05 each own separate sections of `operations.md` and `plugin.json`.
- **Assumptions and invalidation checks:**
  - `gpt-6-luna`/`gpt-6-sol` availability is user-reported; the Subagents documentation mentions both. Ticket 01 settles it.
  - The `fork_turns` override rule was read from the spawn tool's description in Codex `0.155.1` session records (2026-09-19, 2026-09-22), not observed. Ticket 01 settles it on the installed version.
  - The Hooks documentation (read 2026-09-25 and 2026-09-26) says:
    - plugins can ship hooks, and `SessionStart`/`UserPromptSubmit` can add context;
    - hook input carries `session_id`, `transcript_path`, and `model`, with an unstable transcript format;
    - non-managed hooks need the user's `/hooks` trust, keyed to their hash (AC-12);
    - `SubagentStop` input carries `agent_type`, `agent_transcript_path`, and `stop_hook_active`, and `{"decision": "block", "reason": …}` or exit code 2 continues the subagent;
    - `SubagentStart` input lists `turn_id`, `agent_id`, `agent_type`, and `permission_mode`, with no model or effort.

    Ticket 01 verifies each fact on the installed host.
  - The App Server documentation says a fork taken mid-turn without `lastTurnId` records an interruption marker instead of the partial turn, and documents no tool-disabling parameter. The handoff review (2026-09-26) also reports that a `lastTurnId` naming an in-progress turn is rejected. Ticket 01 verifies it.
- **Posture vocabulary:** "full" and "reduced" name the two AC-5 variants everywhere: code, docs, twins, and the manual.
