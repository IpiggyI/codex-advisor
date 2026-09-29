# Native 角色契约

把所选数据包作为 [operations.md](operations.md) 所述 spawn `message` 的正文发送。Advisor 验收数据包在 [independent-acceptance.md](independent-acceptance.md) 中。

## Explorer

~~~text
QUESTION
<Specific source question, definitions, callers, or behavior to trace.>

SCOPE
<Absolute workspace path, source boundary, exclusions, and known constraints.>

PERMISSIONS
Inspect read-only. Do not write, format, implement, or delegate.
The primary owns design decisions and acceptance.

RETURN
FINDINGS: <observations, precise per-file source locations, and examined scope>
EXPLANATION: <evidence-based reasoning; label inferences>
GAPS: <unavailable sources, failed checks, and unresolved questions>
~~~

独立核对其引用与实际路由。否定性搜索只在已检查范围内确立缺失。发现不足时，可以转为 primary 直接调查，或改用另一项已授权分配；披露任何未核验的调用。
探索既不是实现，也不是独立最终验收。

## Worker

所有 Worker 入口使用同一份五部结果契约。角色职责与档位无关。

~~~text
OBJECTIVE
<Observable outcome, acceptance conditions, original task reference, and sources.>

FILES AND OWNERSHIP
<Absolute workspace path, exact owned files/modules, excluded scope, and current
changes. You are not alone in the codebase; preserve concurrent and unrelated
edits and adapt to others' work. Surface conflicts instead of overwriting them.>

INTERFACES
<Inputs, outputs, behavior, callers, and shared interfaces that must be retained.>

CONSTRAINTS
<Binding decisions, user boundaries, resources, and reserved choices. Inspect the
original task and relevant sources. Perform implementation yourself; do not delegate
implementation further. Resolve unclear expected behavior, conflicting requirements,
and changes to reserved interfaces with the primary before dependent edits.>

VERIFICATION
<The checks this contract requires, expected results, and failure conditions.
Run them, plus whatever your own debugging needs; checks that span other work
packages or the whole delivery belong to the primary's schedule. Inspect the
full resulting diff and report failed, skipped, or unavailable checks.>

RETURN
COMPLETION: <complete, partial, or blocked, with reason>
CHANGES: <actual files and behavior changed>
VERIFICATION: <commands, exit status, and relevant observed output>
JUDGMENT CALLS: <local decisions within the contract>
GAPS: <ambiguity, conflicts, risks, and unverified results>
~~~
