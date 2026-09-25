# Sources and decision ledger: mainstay/crux/rescue tiers and process consultation (0.3.0)

This file is for traceability. The binding requirements are in [spec.md](spec.md). Part 1 holds the user's words verbatim; Part 2 is the organized result. Part 2 never replaces Part 1: when they seem to disagree, read the original and the ledger basis, then treat the spec as current.

Recorded 2026-09-26 from the Claude Code session that ran the discussion and wrote this spec.

## Part 1 — Originals (verbatim, not edited)

### 1.1 Records that already hold originals (cite, do not copy)

The discussion directory is `.agent-discuss/tiers-and-advisor-next-iteration/` in this checkout. It is untracked by git, reachable only in this working tree, and closed (its `final.md` exists), so it must not be edited. Versions are identified by SHA-256:

| File | Holds | SHA-256 |
|---|---|---|
| `request-001.md` | The first question (light versus standard, the `.scratch/` translation example) and the complete `/discuss` request, both in the user's words | `7d7dd72471aa35d3222afd34edfd9a83cfada78ec5a4f93cb19285f7e47ea4fc` |
| `request-002.md` | `request-001` unchanged, plus the user's round-2 decisions verbatim (Terra removal, escalation rule, crux guardrail question, calling-posture priority, "首轮准入采用GPT方案…其他按推荐…"), an expansion of what "GPT方案", "收窄选项", and "其他按推荐" referred to, and the GPT-session decision as relayed | `3ca1d08520f711e0d47d8cd75cdadb5cab899ffc93ce3cb4e7ccdce05bfe623c` |
| `claude/001.md` | Claude's first publication (analysis, not user words) | `8ac6ad4916b9023a161097a4656203796e4daee98e3002802ce66ed2d1e8348d` |
| `gpt/001.md` | GPT's first publication; relays the user's GPT-session decision | `59fd2d72310581df87538eddc994ac56ead071b117a29fd019ccad0de0ca63b8` |
| `gpt/002.md` | GPT's second publication (three disagreements, rescue-entry gap) | `0d35f7300a3929a82781081d6b113c669ed52dddf06c028475bdf54b1afa8191` |
| `final.md` | The conclusion the user confirmed before closing (2026-09-25 23:50 local) | `67eb045f8d130cc6a0b9b1c4fc76ea6c4d08bc799d750dd3779d679a45fc293a` |

Unavailable original: the user's own words in the GPT session are not reachable from this session. `gpt/001.md` relays them as: "保留独立验收，并引入自动传递上下文的咨询方式（推荐）". "（推荐）" is GPT's option label, not the user's wording. Treat this as relayed, not verbatim.

### 1.2 Originals that exist only in the Claude session (copied here verbatim)

**U1** — sent after the assistant began searching the web for a Pi advisor implementation (the session showed "[Request interrupted by user for tool use]" before it):

> 哦，插件我忘记给了：rpiv-mono

**U2** — sent while the assistant was reading the rpiv-advisor documentation:

> 本地已经拉取了源码了

**U3** — after the assistant answered `gpt/002.md` point by point (that answer's conclusions are what `final.md` §一.A.8 and §一.B.6/B.9 and §五 record):

> 剩下几个问题不必再过一遍GPT了，我敲定按你现在说的来，可以收口讨论了

**U4** — answer to the structured question "按上面的正文写入 final.md 并关闭讨论吗？关闭后不能再发布、读取或修订请求。":

> 我有要调整的地方，先别写入

**U5** — the adjustments that followed U4:

> 1. `astra[xhigh]` 主会话用精简姿态 是举例还是限制成xhigh了？如果是限制 是为什么呢？
> 2. 观察由我肉眼判断，不要为此改变工作逻辑、增加本地日志等
> 3. 完成前咨询不要作为后续可选，在本版本一并加入，不要挤牙膏

**U6** — answer to the structured question "完成前咨询的钩子范围选哪个？选定后我就把对应正文写入 final.md 并关闭讨论。". Chosen option label and its description as shown to the user:

> 方案 B 后关闭 (Recommended) — 只用 SubagentStop 拦 worker；主会话靠常驻说明。正文 B.8、理由、放弃选项和待验证第 4 条按右侧预览修改，其余不变。

**U7** — answer to "request-002 按上面的草稿写入吗？写入后不能修改或删除，只能再追加新版本。":

> 按草稿写入 (Recommended) — 保留 request-001 全文，追加你的原话、展开说明和 GPT 会话里的决定。

**U8** — the `/to-spec` request that produced this directory (arguments verbatim):

> 执行会交由Codex完成，在写spec和票据时遵守下面的提示词规则：
> 请按以下交接要求整理规划文档：
> 1. 在现有任务目录或讨论记录中，保存原始需求原文及影响交付结果的后续补充原文，并整理讨论中的关键要点，包括目标、约束、取舍、确认理由和遗留问题。原文与整理结果分别标识，不能用摘要覆盖原文。决定须区分已确认、已替代、已否决和未决，并保留对应依据。已有完整记录直接引用；无法取得的原文标明缺失，不凭记忆编造。
> 2. 正式规格必须覆盖本任务涉及的已确认目标、功能、视觉、交互、数据语义和约束。将具体决定写成可执行、可观察的要求，不能压缩成模糊形容词。影响实施取舍的关键理由应进入规格，不能只留在讨论记录中。
> 3. 明确哪些决定必须遵守，哪些细节允许实施者自行选择，哪些变化需要用户重新决定。分别说明文字规格、原型和截图约束哪些事项；出现冲突时不能笼统地将其中一类降为参考，也不能擅自补做产品决定。
> 4. 每项有效要求都有责任票或责任阶段，以及可观察的验收依据。跨票要求写明由谁建立、由谁沿用，以及何时验收，避免共同要求在拆分后无人负责。
> 5. 在任务入口登记材料的准确位置和用途，区分实施必读材料与历史溯源材料。每票提供开始前必读、必看的具体入口。本次明确允许并要求保留原始需求记录、讨论记录、规格、原型、截图和验证入口，不适用技能中笼统的“避免具体文件路径”规则。检查引用可达，并能辨认所采用的版本。
> 6. 视觉任务分别验收功能和画面。明确采用哪版原型、哪些场景及允许差异，要求实际查看设计画面，并将实现画面与基准对照。不能以功能测试通过代替视觉符合，也不能根据实现结果自行修改设计基准。
> 7. 整理完成后，先对照原始需求和有效决定，检查是否存在遗漏、降级、擅自增加或重新引入已否决内容；再假设接手者没有当前聊天上下文，仅凭任务入口及实施必读材料，检查其能否知道要做什么、为什么、哪些决定不能改变，以及如何判断完成。特别检查是否存在“满足验收文字，却偏离已确认目标”的具体成品。发现缺口先补齐规格和受影响票据；需要用户决定的事项明确保留为未决，不能靠实施者猜测。
>
> 共同要求集中在规格中维护，票据引用适用部分，避免重复产生分歧。原始需求和讨论记录用于溯源；正式规格及其指定依据表达当前有效要求。沿用现有任务记录和目录，不另建内容重复的文档体系。

**U9** — the assistant's proposal the user confirmed in U10.1, reproduced verbatim because the confirmation refers to it:

> 1. **`verify.sh` 的安装组**：已有。扩展到 13 个入口、新的 retire list、路由表与模板一致、姿态段落与模型级别一致。
> 2. **`verify.sh` 的运行组**：已有。inspector 继续按模板逐个入口驱动。
> 3. **新增钩子组**：在命令行边界上，把 JSON 事件喂给每个钩子，断言输出和退出码。覆盖三种情况：`SessionStart` 在不同模型下的注入内容；`SubagentStop` 在有改动未咨询、有改动已咨询、无改动三种场景下的行为；`SubagentStart` 在模型匹配和不匹配时的行为。
> 4. **过程咨询工具**：在它的对外边界上测试，模型调用用夹具替身代替。
> 5. **现有两项测试**：`tests/test_zh_mirror.py` 和 `tests/test_version_manual.py`。
> 6. **实机检查**：在临时 `CODEX_HOME` 里跑三类：13 个入口的路由检查、机制实验、钩子的实际行为。
> 7. **画面对照**：版本手册用无头 Chromium 截图，与基准页面对照。
>
> - **我对"不增加日志"的理解，请你确认**：
>   - 允许：完成前强制咨询需要知道"本会话是否已经咨询过"。只用于这个判断、会话结束就失效的临时状态，我认为可以。
>   - 不允许：持久记录，以及任何用于统计或观察的数据。
> - **姿态说明怎么交给子代理**：写进每个入口的 `developer_instructions`。入口的模型是钉死的，所以 luna 和 sol 入口写完整姿态，astra 入口写精简姿态，不依赖尚未验证的钩子能力。相应地，`verify.sh` 里"同角色说明逐字相同"的检查改为：姿态段落以外的部分同角色相同，姿态段落按模型级别相同。

U10.5 later replaced "by model level" in the last bullet with a model-identity comparison; the resulting assignment for the shipped entries is unchanged (luna and sol entries differ from the `astra` advisor model, `astra` entries match it).

**U10** — answers to the five `/to-spec` questions. Question text, then the chosen option and its description, verbatim:

1. "上面列的 7 个测试接缝（含新增的钩子组和过程咨询工具边界），以及对“不增加日志”的理解，符合你的预期吗？" → **符合 (Recommended)** — 按上面的接缝写进 spec；只用于强制咨询、会话结束即失效的临时状态允许存在。
2. "独立验收用哪个顾问 dial？验收结论报告低置信度时怎么办？（final.md 取消了顾问自己的升级梯子，原来“低置信度转 senior 顾问”的路径随之失效，目前没有替代规则。）" → **按被验收工作所在档 (Recommended)** — mainstay 档完成的工作用 astra[low*, medium]，crux 用 astra[high]，rescue 用 astra[xhigh]；主会话自己完成的工作取不弱于主会话的最低一档。低置信度时验收保持待定，交给用户决定。
3. "新版本说明书的画面基准用哪个？`.scratch/manual-redesign/0.2.0-magazine.html` 是一份没有采纳记录的预览稿，和已发布的 `docs/releases/0.2.0.html` 不同。" → **沿用 0.2.0.html (Recommended)** — 以已发布的 docs/releases/0.2.0.html 为画面基准，版式、配色、组件保持一致。
4. "上一轮 spec 把 0.3.0 预留给了 grok lane。这次改动用什么版本号？" → **本次用 0.3.0 (Recommended)** — 本次改动发布为 0.3.0，grok lane 顺延到 0.4.0。本次入口改名是破坏性变更，0.x 升 minor。
5. "主会话的模型不属于 luna、sol、astra 任一系列时（例如其他厂商或其他系列的模型），调用姿态和顾问 dial 怎么定？模型级别规则在这种情况下无法比较强弱。" → the user typed:

   > 按完整姿态；我补充一下：不能写死成luna、sol、astra，应该和advisor的模型对比是否一致，一致是就是精简姿态不一致就是完整姿态；比如说：虽然没有6-terra但是我要是使用5.6-terra呢？这个时候不能抓瞎呀

   The option "按完整姿态" had this description: 视为有更强的顾问可问：注入完整姿态，顾问用 astra[xhigh]。

**U11** — the `/to-tickets` request (arguments verbatim) and the answer to its breakdown question "按哪种拆法重写票据？":

> 按此规范检查一遍票据，之前没走这个skill

> 保持现有 6 张

The chosen option's description: 只修格式、依赖边和姿态段落的顺序问题，不重拆。

**U12** — the request to check the executor's handoff review (`handoff-review.md`, 2026-09-26), verbatim:

> 读取 @.scratch/tiers-and-advisor-consult/handoff-review.md ，对照原始需求、有效决定及正式规格，核对执行者理解的成品和提出的问题，不只检查其是否理解了现有规划。
> 确认的规划缺口修入规格及相关票据，不只在聊天中解释；执行者误读指出依据；需用户决定的事项保留未决。返回修正位置和待决问题，不开始实施。

### 1.3 Session messages that do not affect the deliverable

"发布一版", "阅读GPT发布" (twice), and the `/discuss` and `/to-spec` command invocations themselves only drove the discussion protocol. They are listed so a reader knows nothing was dropped.

## Part 2 — Organized result (not verbatim)

### 2.1 Goals

- **G1 Tier redesign.** Replace light/standard/senior with 主力 `mainstay`, 攻坚 `crux`, 后援 `rescue`: tiers ordered by model, effort as a finer grade inside a tier. Most tasks end in `mainstay`; very few reach `rescue`. Basis: `request-001` (user text), `final.md` §一.A.1.
- **G2 Absorb the Claude Code advisor calling posture.** The user observed that the 0.2.0 plugin rarely calls its Advisor while Claude Code calls its advisor often; the posture is the main thing to migrate. Basis: `request-002` (fourth bullet), `final.md` §一.B.3.
- **G3 Keep independent acceptance** beside the new automatic-context consultation. Basis: relayed GPT-session decision (`gpt/001.md`), `final.md` §一.B.1.

### 2.2 Constraints

- Everything a live location depends on arrives through plugin install or the companion installer (ADR-0004); nothing is hand-copied.
- Commits, pushes, marketplace upgrades, and runs against the user's real `CODEX_HOME` need the user's explicit authorization at that time (user global rule; 0.2.0 ticket 07 precedent).
- Observation of effects is by the user's own eye: no markers, persistent logs, or statistics added for observation (U5.2). Transient per-session state used only for enforcement is allowed (U10.1).
- Before-done enforcement was requested in U5.3 and cancelled by D47 on 2026-09-26.
- Posture choice must not be hard-coded to model family names (U10.5).

### 2.3 Trade-offs and the reasons the user accepted

- **Tier by model.** The user observed a bigger gain from changing model than from raising effort, and a distinct jump at `xhigh`. These are recorded as declared assumptions with the next model generation change as the invalidation trigger (`final.md` §一.A.9).
- **Wide first-round `crux` admission.** Forcing `mainstay` to fail first on a known-hard task wastes an attempt. The risk of over-routing is accepted and watched by the user; the narrow option is kept in reserve (`request-002`; `final.md` §一.A.5–A.6).
- **Escalate across tiers, not within.** This avoids trying every model of one tier; the model-level floor prevents a downgrade such as explorer `sol[high]` → `luna[max]` (`final.md` §一.A.7).
- **Keep independent acceptance.** A consultant that sees the executor's reasoning is anchored by it and is not independent (`final.md` §二).
- **Reduced posture when the caller already runs the advisor's model.** Claude Code's frequent-call posture pays off when a weaker executor asks a stronger model; a same-model consultation is the most expensive and adds a second view, not capability (`final.md` §二; generalized by U10.5).
- **Advisor has no tools during consultation.** Frequent calls need low per-call cost and latency; verification belongs to the executor and to independent acceptance (`final.md` §二).
- **Before-done enforcement only on subagents.** A hook cannot tell a primary's turn end from task completion, and blocking every primary turn would make an `astra` primary re-read the full transcript each turn (U6; `final.md` §二).

### 2.4 Decision ledger

States: **Confirmed** (binding now), **Confirmed-reserved** (kept, not enabled), **Derived** (the spec's closure of a confirmed decision; binding, but the user may override), **Superseded** (replaced by a later user decision), **Rejected** (must not be reintroduced), **Open** (needs a user decision; none may be guessed).

| ID | Decision | State | Basis | Spec |
|---|---|---|---|---|
| D1 | Tiers `mainstay`/`crux`/`rescue` replace light/standard/senior for explorer, worker, advisor | Confirmed | `request-001`; `final.md` §一.A.1 | TR-1 |
| D2 | Models `gpt-6-luna`, `gpt-6-sol`, `gpt-6-astra`; Terra leaves the table because the 6 series has none | Confirmed | `request-002` bullet 1 | TR-2 |
| D3 | The user's table is authoritative; table wins over prose (worker `mainstay` is `sol[high]`, not `sol[medium*, high]`) | Confirmed | `request-002` ("表和正文不一致都不重要"); `final.md` §一.A.3 | TR-3 |
| D4 | Worker `crux` `astra[low, medium]` default is `low` | Derived | Unmarked cell; `final.md` §一.A.3 says fill at implementation; §一.A.4 "排列顺序约等于使用顺序" makes the first listed effort the default | TR-3 |
| D5 | In-tier order ≈ usage order; in-tier choice by judgment the packet cannot capture | Confirmed | `request-001`; `final.md` §一.A.4 | TR-4 |
| D6 | First-round `crux` allowed when a key difficulty is identified or interacting constraints must be handled; default `mainstay`; no usage quota | Confirmed | `request-002` ("首轮准入采用GPT方案"); `final.md` §一.A.5 | TR-5 |
| D7 | Narrow first-round admission (invisible failure, costly failure, evidence of predicted failure, user declaration) | Confirmed-reserved | `request-002` ("先把收窄选项保留"); `final.md` §一.A.6 | TR-6 |
| D8 | Observation by the user's eye; no markers, logs, or statistics for it | Confirmed | U5.2; `final.md` §一.A.6, §一.B.10 | AC-11, X-3 |
| D8a | Explicit markers, local logs, or statistics to watch first-round `crux` | Superseded by D8 | `final.md` draft before U5; U5.2 | — |
| D9 | Escalation floor: model level not lower (luna < sol < astra) unless no other choice; same model needs a higher effort; above the floor, choose by the exposed difficulty | Confirmed | `request-002` bullet 2 and "其他按推荐"; `gpt/001.md`; `final.md` §一.A.7 | TR-7 |
| D10 | Capability-failure counting; path `mainstay` → `crux` → `rescue` → user; `rescue` only through `crux` or a user declaration; first-round `crux` reaches `rescue` after one `crux` failure; R3 kept | Confirmed | U3; `final.md` §一.A.8 | TR-8 |
| D11 | `rescue` requires two accumulated failures (retry inside `crux`) | Rejected | Conflicts with escalate-not-switch; `final.md` §三 | — |
| D12 | Same-tier model switch after a capability failure (unless no other choice) | Rejected | `request-001`; `final.md` §三 | — |
| D13 | Declared assumptions (model change beats effort; `xhigh` jump) in the routing profile, invalidated by the next generation change; the Anthropic rumour is not a basis | Confirmed | `final.md` §一.A.9 | TR-9 |
| D14 | Keep independent acceptance (packet, fresh thread, read-only checks); consultation never substitutes | Confirmed | Relayed GPT-session decision; `final.md` §一.B.1 | AC-1 |
| D15 | Replace the whole Advisor and drop independent acceptance | Rejected | `final.md` §三 | — |
| D16 | Acceptance dial by the tier of the accepted work; primary-authored work uses the lowest advisor dial not weaker than the primary; a low-confidence verdict leaves acceptance pending and goes to the user | Confirmed | U10.2 | AC-2 |
| D16a | Work built by several tiers is accepted at the highest tier involved; a primary whose model is not in the routing profile gets `astra[xhigh]` | Derived | Closure of D16 and D20 (U10.5 option description) | AC-2 |
| D17 | Process consultation: automatic current context, advisor has no tools, returns exactly one of plan / correction / stop | Confirmed | `final.md` §一.B.2 | AC-3 |
| D18 | Workers and explorers may call the consultation | Confirmed | `request-002` ("其他按推荐"); `final.md` §一.B.4 | AC-3 |
| D19 | Consultation dial follows the caller: `mainstay` caller → `astra[low*, medium]`, `crux` → `astra[high]`, `rescue` → `astra[xhigh]`, primary → lowest advisor dial not weaker; the advisor has no ladder of its own | Confirmed | `final.md` §一.B.5 | AC-4 |
| D20 | Posture by comparing the caller's model with the advisor model it would consult: same model → reduced posture; different → full posture; no hard-coded family list; a primary model not in the routing profile gets the full posture and `astra[xhigh]` | Confirmed | U10.5 | AC-5 |
| D20a | "`astra[xhigh]` primary uses the reduced posture" | Superseded by D20 (it was an example, U5.1) | `request-002`; U5.1 | — |
| D20b | Posture by model level (luna/sol full, astra reduced, regardless of effort) | Superseded by D20 | `final.md` §一.B.3; U10.5 | — |
| D21 | Adoption: default adopt; deviate with a reason when following fails or primary-source evidence contradicts; a constraint conflict is rejected directly with a reason; advice grants no authorization | Confirmed | U3; `final.md` §一.B.6 | AC-6 |
| D22 | Rejecting for a reasoning flaw: advisor model different from the caller's → one reconcile call first; same model → may reject directly with a reason | Derived | `final.md` §一.B.6 said "higher model" versus "same model"; D20 removed the model order for posture, so the same identity comparison is applied here | AC-6 |
| D23 | Reject a stronger advisor's advice directly for a reasoning flaw (GPT's `gpt/002.md` position) | Rejected | U3; `final.md` §三 | — |
| D24 | Record a category for every non-adoption | Superseded by D8 (it existed only to feed a later check) | `final.md` draft before U5; U5.2 | — |
| D25 | Posture text rewritten from rpiv-advisor's guidelines without the "commit the change" step; restate key guidance in the next visible reply | Confirmed | `gpt/001.md`; `final.md` §一.B.7 | AC-7 |
| D26 | Reuse rpiv-advisor's guidelines as-is | Superseded by D25 | `claude/001.md`; `final.md` §三 | — |
| D27 | Always-on posture: a plugin-shipped `SessionStart` hook injects the primary's posture text | Confirmed | `final.md` §一.B.8 | AC-8 |
| D28 | Delegates carry their posture variant in their entry's `developer_instructions`; the same-role identical-instructions check is narrowed to exclude the posture section | Confirmed | U9 (confirmed in U10.1) | EN-5 |
| D29 | Before-done enforcement: plugin-shipped `SubagentStop` hook on workers, this version | Superseded by D47 | U5.3; U6; `final.md` §一.B.8 | AC-9 cancelled |
| D29a | Before-done enforcement as an optional later step | Superseded by D29 | U5.3 | — |
| D30 | `Stop` hook blocking every primary turn (方案 A) | Rejected | U6; `final.md` §三 | — |
| D31 | Per-dispatch automatic verification of actual model and effort; installation evidence reusable | Confirmed | `gpt/002.md`; U3; `final.md` §一.B.9 | AC-10 |
| D32 | Check model settings once per task per entry | Superseded by D31 | `claude/001.md`; `final.md` §三 | — |
| D33 | Transient per-session enforcement state is allowed; persistent or statistical records are not | Confirmed | U10.1 | AC-11 |
| D34 | Consultation mechanism: candidates A (native spawn, positive-integer `fork_turns`), A' (App Server `thread/fork`), B (MCP tool reading the session record, calling `codex exec`); each judged per configuration against four checks; one failure rejects only that configuration | Confirmed (method) | `gpt/002.md`; U3; `final.md` §五.2 | AC-3, ticket 01 |
| D35 | Advisor tiers varying only effort and forming their own ladder | Rejected | `final.md` §三 | — |
| D36 | Version `0.3.0`; the grok lane moves to `0.4.0` | Confirmed | U10.4 | DR-9, DR-11 |
| D37 | Version manual visual baseline: shipped `docs/releases/0.2.0.html`; the magazine preview is not adopted | Confirmed | U10.3 | DR-10 |
| D38 | Test seams as proposed in U9 | Confirmed | U10.1 | spec §Testing Decisions |
| D39 | The Anthropic rumour about removing effort levels as a rule basis | Rejected | `final.md` §三 | — |
| D40 | The old light/standard free choice with the two-failure senior gate | Rejected (replaced by D6, D9, D10) | `final.md` §三 | — |
| D41 | The consultation reaches models only through Codex's own authenticated paths and never reads, copies, or transmits credentials itself | Derived | The user's standing rule to keep credentials out of logs and reports, and operations.md's credential handling for live checks; it closes candidate B's option of calling a model API with copied credentials | AC-3 |
| D42 | Hook trust is the user's gate. The plugin, installer, and docs never mark hooks trusted, never edit trust state, and never pass `--dangerously-bypass-hook-trust` in anything the user runs. Install, update, and release steps include the `/hooks` review. Tests distinguish an untrusted skip from a failure | Derived | Codex Hooks documentation read 2026-09-26 (plugin hooks are not trusted by install; trust is keyed to the hook hash; untrusted hooks are skipped with a startup warning); the user's standing rule that security gates and privilege changes need explicit authorization; handoff review F2 | AC-12 |
| D43 | "Current effective context" means everything the caller's model would receive on its next request: the latest compaction summary, every later message and tool call/result including the earliest still in context, and the unfinished turn. A recent-turn window is eligible only if it provably covers all of it | Derived | D17 and the goal that a consultation must not lose facts a summary would drop (spec §Reasons); handoff review F3 | AC-3; eligibility check 5 |
| D44 | "No tools" is shown by the advisor request's actual empty tool set, not by a refused attempt or the model's own statement | Derived | D17 ("no tools", read-only excluded); handoff review F4 | AC-3; eligibility check 4 |
| D45 | Tickets 02 and 03 scope their text searches to the files they own; X-5 applies in full at final acceptance; ticket 01 judges its file changes against its start state | Derived | Ticket file ownership; handoff review F1 | X-5; tickets 01–03 |
| D46 | The plugin adds no detection of its own for untrusted hooks; the host's startup warning pointing to `/hooks` is the signal | Derived (scope choice) | Codex Hooks documentation read 2026-09-26; no user request for plugin-side detection; avoids new scope | AC-12 |
| D47 | No automatic worker finish blocking. Retain primary posture injection, native-dispatch verification, and process consultation. Continue ticket 06; fresh Astra xhigh final acceptance, then commit/push and update WSL and Windows | Confirmed | Explicit user selection on 2026-09-26 after explanation of AC-9; supersedes its earlier deferral and O3's hook-blocking clause | AC-9 cancelled; retained AC-8/AC-10; 06 and final acceptance authorized; X-1 release authorization |
| D48 | After acceptance, create a local commit only; do not push or update WSL/Windows installations | Confirmed; supersedes D47's release scope only | Later explicit user instruction on 2026-09-26 | X-1; final local delivery |
| D49 | Skip repeating the manual trust run after adding the cross-platform launcher; retain prior trusted/untrusted evidence and disclose that the final hook definition was not retested with manual trust | Confirmed | User declined the repeated test on 2026-09-26 | AC-12 verification only; product trust requirements unchanged |

### 2.5 Open items

The two decisions surfaced by the executor's handoff review (`handoff-review.md`, 2026-09-26) were resolved by explicit user replies during ticket 01 on 2026-09-26. The spec's §Open Decisions retains the alternatives and marks option (a) selected for each.

- **O3 — Success policy retained; hook clause superseded by D47.** Only a successful consultation counts; the primary sees failures, and the work stays pending until successful consultation or user release. There is no automatic worker finish block.
- **O4 — Confirmed, option (a).** `--dangerously-bypass-hook-trust` is allowed only for automated live checks in a temporary `CODEX_HOME`. At least one run must still use hooks the user trusted through `/hooks`, and one must record the untrusted skip and its warning. No authorization was given to edit trust state or bypass trust in a real home.

The items below become user decisions only if a probe result forces them; the spec's stop-and-return conditions (spec §Stop and return) say when:

- **O1** — which consultation mechanism ships. This is not a user decision while at least one candidate passes all four checks; the ticket 01 rule in the spec decides. If none passes, it becomes a user decision.
- **O2** — whether the narrow first-round admission (D7) is enabled. This is the user's call, made from their own observation, at any time after release.
