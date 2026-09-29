---
status: accepted
---

# Load the orchestration skill on events

## Decision

The skill description names the events that need the skill body: a primary is
asked to delegate or is about to delegate work, or to accept, rework, or escalate
a delegated result; the user authorizes Architect mode; a delivery needs
independent acceptance; or a primary, worker, or Explorer lacks applicable
selected posture or adoption instructions. Direct work that meets none of these
does not load the skill.

Process consultation is not a load event. The `SessionStart` hook injects the
primary's selected posture and adoption blocks, native entries carry each
delegate's, and the consultation server selects the advisor dial from the routing
profile. The skill's consultation paragraph now uses the blocks already in context
and reads the consultation mapping and `consult-posture.md` only when a block is
missing or inapplicable. The posture-selection rule itself is unchanged.

The user-level entry in `AGENTS.md` (maintained in the user's prompts repository)
changes from task-type triggers to the same events.

## Basis

The previous description, "Use when a primary agent implements or delegates work",
and the user-level entry, "before choosing how to carry out deliverable changes,
investigation beyond a bounded factual lookup, consequential decisions, or delivery
acceptance", both matched nearly every task, so the skill body loaded on the first
message of sessions that never delegated. The fable-advisor plugin showed the same
pattern in the user's Claude Code sessions from 2026-09-19 to 2026-09-28 (fable-advisor
ADR 0022).

A consultation trigger would restore the problem: the full posture asks for a
consultation before settling on the approach of any multi-step task. The injected
posture (`scripts/advisor-hooks.py` `posture()`) and server-side dial selection
(`scripts/consult_context.py` `route()`) already give the normal path everything
the skill paragraph required.

The decision was reviewed by a `gpt-6-astra` xhigh advisor in two rounds on
2026-09-28; the second round withdrew the consultation trigger in favour of the
conditional paragraph and added the missing-posture fallback event.

## Alternatives not adopted

- Keep consultation as a load event: loads the skill at the start of most
  multi-step tasks.
- Remove the user-level entry and rely on the description alone: the user added
  the entry because the skill was forgotten at delegation time.

## Revisit when

- Real sessions after the next release still load the skill in direct work with
  no delegation, at least twice.
- A delegation, Architect-mode task, or independent acceptance proceeds without
  the skill, once.
- The `SessionStart` posture injection or server-side dial selection changes.
