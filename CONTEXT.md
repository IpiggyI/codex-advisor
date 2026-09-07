# Codex Advisor

Shared vocabulary for the fork's two session work modes.

## Language

**Architect mode**:
A user-authorized work mode in which the primary agent owns design, task specifications, and acceptance, and delegates all implementation to implementers.
_Avoid_: Equating architect mode with the selected primary model, or allowing the architect to implement small changes.

**Advisor mode**:
A session work mode in which the primary agent carries out the work and consults an advisor for judgment.
_Avoid_: Treating advisor mode as an implementation route.

**Advisor**:
An agent consulted for judgment on a decision, a persistent problem, or delivery readiness. The primary agent owns the resulting decision and must explain any disagreement.
_Avoid_: Treating the advisor's recommendation as an automatic veto.

**Implementer**:
A delegated agent responsible for implementation within the task specification supplied by the primary agent.
_Avoid_: Treating the implementer as the owner of the session's architecture or final acceptance.

**Explorer**:
A delegated agent available independently of the primary agent's model or work mode that investigates scoped questions through read-only inspection and returns cited facts, evidence-based explanations, and unresolved gaps. The primary agent owns design decisions and the use of those findings.
_Avoid_: Requiring architect mode, assigning implementation, or treating exploration findings as an independent review.

**Independent reviewer**:
An agent with a fresh context that examines a deliverable after the architect's acceptance checks, for high-risk work or at the user's request.
_Avoid_: Treating every advisor consultation as a final review.
