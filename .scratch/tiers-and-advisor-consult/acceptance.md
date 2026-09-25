# Acceptance record: mainstay/crux/rescue tiers and process consultation (0.3.0)

Every probe, live check, visual comparison, and the final sweep for [spec.md](spec.md) is recorded here by the ticket that owns it. A section stays `pending` until its ticket fills it. Record the Codex version, the date, commands, observed values, thread IDs, and what each result does not establish.

## 01 Host probes and mechanism decision

Status: complete on 2026-09-26. B′ passes the eligibility checks below; S3 and S4 are cleared. P7 completes user-trusted execution and untrusted warning/skip evidence, and all temporary environments are removed. The initial blocked results below are retained as configuration-specific history and are superseded by P6/P7 where stated. Product implementation and acceptance remain separate.

### P1 Environment, sources, and scope

The primary executed the probes on WSL with `codex-cli 0.157.0`, starting at `2026-09-26T01:09:45+08:00`. Repository HEAD was `f812f9b64c0fb4aa4d45f9a6ae8102c451ab367b` on `main`. The starting status was exactly:

```text
?? .agent-discuss/
?? .scratch/tiers-and-advisor-consult/
```

The task-directory SHA-256 baseline was captured before any task-file edit. Paths in this table are relative to this task directory:

| File | SHA-256 |
|---|---|
| `acceptance.md` | `ad450c358a93c1f80b97845a8a49d91a1d6626e828458a3b024eb43818f67efa` |
| `handoff-review.md` | `46069f0ae81ee5a2c2ccac88bd7121cadd4b2c4ccdcac31fa72c30a915f55890` |
| `issues/01-host-probes-and-mechanism.md` | `b79a277d9815161387c3a13c33c142898bfbbf0ce364c8d5be0d3ef26befd89c` |
| `issues/02-doctrine-posture-glossary-adr.md` | `31d1cd12f04cb299618d529d2bac8c40691a776ad9e6901ca186faac96320156` |
| `issues/03-profile-entries-installer-inspector.md` | `829ee7c8249d3bfbaffb897c39c740b48eab83d2d74d9a683ccbce560f0f3c58` |
| `issues/04-process-consultation.md` | `bbd409ee8b3ce333372f9e0ce2cbbe8c14142413605892ca316658a6e83943d8` |
| `issues/05-plugin-hooks.md` | `c3c89336f9131f25d186c8e3e3ab4e35bd68153a2e4215f5276bb51952a66390` |
| `issues/06-readme-manual-release.md` | `612aa3e11bc9c21cdb9541cb5e96752fc6f6e204cf6bd5a186175d77f54961af` |
| `sources.md` | `51466c306f7666e973f14e4734ca97f0cdf130591fd069c0253f8e97f0802226` |
| `spec.md` | `35bad6333d963baffef313f5f7509cd974079bb2010091246c0386212cba5939` |

Read the installed 0.2.0 orchestration skill, current operations, routing profile, and role contracts; ADR-0004; the prior route-check method; the current spec and ticket 01; and the required decision-ledger rows. The reference repository remained at `d74b1c99830a565f3df3f37e0a36616d17ffc574`. Its `advisor/execute.ts:117` reconstructs the current branch at call time, and `:153` sends `tools: []`; `advisor/context.ts` removes the in-flight consultation call and supplies a user-role tail. Those are reference semantics, not evidence of Codex support.

Official sources fetched successfully and read on 2026-09-26:

| Source | Fact used | Limit |
|---|---|---|
| [Hooks](https://learn.chatgpt.com/docs/hooks) | Plugin hook discovery, hash-based `/hooks` trust, context injection, subagent events, and `SessionEnd`. | Documentation is not a trusted-hook execution result. |
| [App Server](https://learn.chatgpt.com/docs/app-server) | In-progress `lastTurnId` is rejected; omitting it forks with an interruption marker. | The marker alone does not establish whether a completed tool result reaches the next model request. |
| [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | Template model/effort precedence; caller effort when a template pins only its model. | Account availability was checked separately in P2. |
| [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) and [configuration schema](https://developers.openai.com/codex/config-schema.json) | Tool switches and `features.tool_registry.turn_metadata_includes_tool_info`. | The fetched configuration schema is an official snapshot, not proof that all settings affect this host's exposed tools. |

The exact installed App Server protocol schema was generated with `codex app-server generate-json-schema --experimental --out <temporary>/schema`. Its start/fork/resume/turn schemas were examined. No actual empty model-request tool inventory was obtained from those schemas or the inspected runtime records.

### Temporary installation and command shapes

All model probes used disposable homes under `/home/hyy/ca-tier-probe-ou6tpics/`, outside `/tmp`. Only the required authentication/configuration copies were used. The copied config retained connection/provider and plugin settings; unrelated MCP servers, user hooks, project settings, and memory use were excluded. Parent requests used `gpt-6-astra[low]`. No probe changed the user's installation, trust state, marketplace, or repository runtime files.

The working checkout installed successfully through the required route:

```sh
CODEX_HOME=<temporary-home> codex plugin marketplace add /home/hyy/develop/personal/GitHub/codex-advisor
CODEX_HOME=<temporary-home> codex plugin add codex-advisor@codex-advisor
sh <temporary-home>/plugins/cache/codex-advisor/codex-advisor/0.2.0/scripts/install-agents.sh --target-dir <temporary-home>/agents
```

All three commands exited 0. The installed plugin root was under the temporary home; all eleven existing templates matched the installer manifest. Additional `probe_pinned`, `probe_model`, and `probe_consult` entries were newly created throwaway templates in that home; shipped installed entries were not hand-edited.

The P2/P3/native P4 parent command was `CODEX_HOME=<temporary-home> codex exec -C <temporary-workspace> --skip-git-repo-check --json -m gpt-6-astra -c 'model_reasoning_effort="low"' -`, with the bounded probe prompt on stdin. Each P2 child used `agent_type=default`, explicit `model`, explicit `reasoning_effort`, and `fork_turns=none`, and returned `PROBE_OK` without tools or further delegation. Children ran sequentially. Generic inspection used `sh plugins/codex-advisor/scripts/inspect-agent-runtime.sh --sessions-dir <temporary-home>/sessions <child-UUID>`.

### P2 Dial availability

The requested and observed values below agree. Every row has a completed child response and inspector exit 0. All observed child working directories were the temporary workspace; observed sandbox/permission metadata was `read-only` / `managed`. This does not independently establish hard isolation, model quality, cost, or stability.

| Requested model | Requested effort | Observed model | Observed effort | Child thread | Inspector |
|---|---|---|---|---|---|
| `gpt-6-luna` | `high` | `gpt-6-luna` | `high` | `01a0d98d-31ac-7de3-9880-f640aee31e7e` | 0 |
| `gpt-6-luna` | `xhigh` | `gpt-6-luna` | `xhigh` | `01a0d98e-297b-7931-bf8a-a6be0bb3c1ae` | 0 |
| `gpt-6-luna` | `max` | `gpt-6-luna` | `max` | `01a0d98e-56f3-73e3-a7d5-ec00bfb843ce` | 0 |
| `gpt-6-sol` | `medium` | `gpt-6-sol` | `medium` | `01a0d98e-7f9a-7771-b8ca-691e992a6990` | 0 |
| `gpt-6-sol` | `high` | `gpt-6-sol` | `high` | `01a0d98e-adce-7842-8bbf-91fb586f10fa` | 0 |
| `gpt-6-sol` | `xhigh` | `gpt-6-sol` | `xhigh` | `01a0d98e-ccbd-7413-a6f9-3e026b55c581` | 0 |
| `gpt-6-sol` | `max` | `gpt-6-sol` | `max` | `01a0d98e-f3ca-7810-b67e-c8c4cf0f2ab9` | 0 |
| `gpt-6-astra` | `low` | `gpt-6-astra` | `low` | `01a0d98f-2350-72d0-a0e2-c95d0008fdff` | 0 |
| `gpt-6-astra` | `medium` | `gpt-6-astra` | `medium` | `01a0d98f-4c35-7350-810f-8221e99c80d2` | 0 |
| `gpt-6-astra` | `high` | `gpt-6-astra` | `high` | `01a0d98f-73d5-7f60-873e-9ea5fe9b4fe5` | 0 |
| `gpt-6-astra` | `xhigh` | `gpt-6-astra` | `xhigh` | `01a0d98f-9edc-7a31-bd92-7021aacdd049` | 0 |

The first row's parent was `01a0d98d-19ab-7cf1-8b81-5eafdffd762e`; the other ten shared parent `01a0d98e-09fe-7c51-b898-5d15a744afea`. Parent association was inspected for every child.

### P3 Precedence

Parent: `01a0d990-b7d0-72e1-b579-0f8cc8818e6c`, running `gpt-6-astra[low]`. All three children completed with `PROBE_OK`.

| Case | Template | Spawn arguments | Observed metadata | Child | Inspector / verdict |
|---|---|---|---|---|---|
| Pinned conflict | `probe_pinned`: `gpt-6-luna[high]` | `model=gpt-6-sol`, `reasoning_effort=medium`, `fork_turns=none` | `gpt-6-luna[high]` | `01a0d990-cf01-7763-870b-98e94738e6e8` | Exit 0; both template pins won. |
| Caller effort | `probe_model`: `gpt-6-sol`, effort omitted | `reasoning_effort=xhigh`, `fork_turns=none` | `gpt-6-sol[xhigh]` | `01a0d990-ef04-75f2-8a7b-319126b95b55` | Exit 0; template model and caller effort held. |
| Full-history overrides | Built-in `default`, no template pins | `model=gpt-6-luna`, `reasoning_effort=high`, `fork_turns=all` | Inherited `turn_context` at `gpt-6-astra[low]`, then child context at `gpt-6-luna[high]` | `01a0d991-1420-7c72-b96a-82abb5637b04` | Exit 1: conflicting routing evidence. The call was accepted, but the current inspector does not certify this mixed-history case. |

The full-history observation differs from ADR-0004's prior account of overrides. It does not establish a loss of template precedence: the two template cases passed, and the full-history case had no pins. S2 was not triggered by the tested pin cases. No inspector change was made in ticket 01. A future mechanism using full-history forks must resolve this evidence boundary before claiming certified routing.

### P4 Consultation configurations

Each configuration must pass every eligibility check and all three caller routes. A failed or unproven cell leaves that configuration ineligible. Tests whose prerequisites failed were not expanded to spend quota on a configuration already lacking eligibility.

| Configuration | Unfinished-turn nonce | Actual dial | Compaction | Actual empty request tool set | Earliest effective context | Primary / worker / explorer | Result |
|---|---|---|---|---|---|---|---|
| A1: pinned `probe_consult`, `fork_turns=1` | Failed: child reported nonce absent; nonce absent from its rollout. | `gpt-6-astra[low]`, inspector 0. | Untested after nonce failure. | Unproven; no actual request inventory obtained. | Untested; no rule proving a fixed one-turn window covers every effective context. | Primary tested; worker/explorer untested. | Ineligible. |
| A8: same template, `fork_turns=8` | Failed: child reported nonce absent; nonce absent from its rollout. | `gpt-6-astra[low]`, inspector 0. | Untested after nonce failure. | Unproven; no actual request inventory obtained. | Untested; no rule proving a fixed eight-turn window covers every effective context. | Primary tested; worker/explorer untested. | Ineligible. |
| A' with in-progress `lastTurnId` | Fork rejected before advisor execution. | No advisor request. | Untested after rejection. | Untested after rejection. | Untested after rejection. | Primary request tested; delegates untested. | Ineligible. |
| A' without `lastTurnId`, then resume and turn | Stored fork contained completed nonce output, but the resumed model answered `MISSING`. | Resume selected `gpt-6-astra`; follow-up turn explicitly requested `low`, with matching turn context. | Untested after nonce failure. | Unproven; a stored dynamic-tool definition is not an empty request tool set. | Untested after nonce failure. | Primary tested; delegates untested. | Ineligible. |
| B1 executor prerequisite: `codex exec` with the first tool-disable configuration below | Context reconstruction not implemented. | `gpt-6-astra[low]` in turn context. | Untested. | Failed: the actual `exec` custom-tool call successfully returned the clock result. | Untested. | Direct executor only; zero-parameter MCP caller routes untested. | This executor configuration is ineligible. |
| B2 executor prerequisite: extended disable configuration plus request-tool metadata flag | Context reconstruction not implemented. | `gpt-6-astra[low]` in turn context. | Untested. | Unproven: `exec` returned `code-mode host is disabled`; no actual empty request inventory was obtained. A refused call is not proof under D44. | Untested. | Direct executor only; zero-parameter MCP caller routes untested. | No eligibility established. |

Native P4 used the P3 parent. A shell call generated `9b589de4d990476b0114f442f0a77bb2`, and the parent spawned each candidate during that same unfinished turn without putting the nonce in the child message. A1 child: `01a0d991-45ea-7a70-91c0-4bcf393d0490`; A8 child: `01a0d991-7641-72a3-b6ea-68eb961f0723`.

App Server used JSON-RPC over stdio in the same temporary home. `thread/start` supplied two fixture dynamic tools; the source called `probe_nonce`, received a random result, then remained suspended at `probe_hold`. Source thread: `01a0d992-8350-7333-bb40-4fbcd9306dad`. Active turn: `01a0d992-83ab-7933-9eff-f8cde154c322`. `thread/fork` with that `lastTurnId` returned error `-32600`: `lastTurnId '01a0d992-83ab-7933-9eff-f8cde154c322' identifies an in-progress turn`. Omitting the parameter created `01a0d992-9699-70e1-a066-660583a805d7` with an interrupted turn and the completed nonce tool item. `thread/resume` and a new `turn/start` asked for the inherited nonce without supplying it; the answer was `MISSING`. The source turn was released and interrupted before stopping the server. No model-facing completeness claim is inferred from the stored fork's contents.

B1 thread: `01a0d995-087a-75d0-aa94-2f068127bcd6`. Configuration overrides were `features.shell_tool=false`, `features.apply_patch_freeform=false`, `features.view_image=false`, `features.goals=false`, `features.request_permissions_tool=false`, `features.default_mode_request_user_input=false`, `features.image_generation=false`, `features.apps=false`, `agents.enabled=false`, `tools.update_plan.enabled=false`, `tools.experimental_request_user_input.enabled=false`, and `web_search="disabled"`. Its rollout contains the completed `custom_tool_call` named `exec`, input `text(await tools.clock__curr_time({}));`, and the matching tool output with `current_time="2026-09-25 17:20:22 UTC"`. This is actual successful tool execution, not an availability self-report.

B2 thread: `01a0d998-b0a8-73f1-86b4-5691c8070cb2`. It added `features.code_mode=false`, `features.code_mode_host=false`, `features.code_mode_only=false`, `features.sleep_tool=false`, `features.current_time_reminder=false`, `features.browser_use=false`, `features.computer_use=false`, `features.tool_suggest=false`, and `features.tool_registry.turn_metadata_includes_tool_info=true`. The request-tool flag is described in the fetched schema as including authoritative tool information in per-turn request metadata. It did not expose an actual request inventory in the inspected rollout or CLI output. The same custom-tool call received `code-mode host is disabled`; that refusal is deliberately not classified as either an empty tool set or a successful tool call.

Other native window values, full-history consultation with pinned advisor settings, alternative App Server configurations, forced compaction, long-session earliest-context cases, MCP session discovery/reconstruction, and consultation from a worker/explorer remain untested. No bounded-window completeness rule or empty-tool configuration was established. These gaps do not justify substituting a packet, a tool-bearing advisor, or a different model table.

### Decision advice

Before concluding S3, the primary requested one read-only decision consultation using installed `ca_advisor_standard`, fresh context, pinned `gpt-6-astra[medium]`. Parent: `01a0d996-7299-7c33-8a8b-ce0a80c482c9`; advisor: `01a0d996-b595-7a73-bf41-a6de466fb605`. The role-aware inspector exited 0. The advisor identified the tool-metadata flag and remaining code-mode switches as a cheap additional probe; the primary ran B2. The advisor also distinguished template precedence from the mixed-history inspector failure. This was decision advice, not independent delivery acceptance.

### P5 Hooks and trust boundary

A throwaway copy of tracked checkout files added only a fixture `hooks/hooks.json` and a fixture command under its plugin. The command would record its event inside the disposable probe directory and inject `HOOK_CONTEXT_62417`. A second temporary home installed that copy through the local marketplace route. The first marketplace-add attempt failed because the copied config retained the original marketplace path; removing that registration in the temporary home and adding the throwaway copy resolved it. `codex plugin list --json` then reported the copy installed and enabled. An intervening run before that correction is excluded from hook evidence.

| Capability / documented fact | Trust state | Observed result | Evidence / remaining check |
|---|---|---|---|
| Fresh plugin hooks require `/hooks` trust and are skipped with a warning. | Untrusted; no trust record created and no bypass used. | Fixture did not run. No `/hooks` warning was observed in the captured `codex exec` output or inspected rollout; therefore the full skip-and-warning requirement is unverified. | Thread `01a0d995-03cb-7250-8bf1-ca2e7a4f7c8e`; no fixture output file. |
| Interactive trust/warning surface | Untrusted | CLI stopped at its folder-trust gate. The primary exited without trusting the folder or hooks. | No model request or trusted-hook evidence from that attempt. |
| Plugin hook execution with the authorized temporary bypass | Bypassed under O4(a), after the user's reply. | Passed: the fixture ran and the primary reported its injected `HOOK_CONTEXT_62417`. | Thread `01a0d99f-4d47-76b3-8124-5fb7ec7e25f6`. The host emitted its bypass warning. This does not replace a user-trusted run. |
| `SessionStart` input and new-session injection | Bypassed under O4(a). | Captured `session_id`, `transcript_path`, `cwd`, `hook_event_name`, `model`, `permission_mode`, `source`; `source=startup`. The injected marker reached the primary. | The initial probe and the multi-event probe below. |
| Resumed-session injection | Bypassed under O4(a). | Hook invocation with `source=resume` observed. A separate distinct-marker check is recorded below. | Parent `01a0d9a1-0ecb-7473-8dc7-cf8dd765793a`. |
| `SessionStart` in subagents | Bypassed under O4(a). | No child `SessionStart` event was observed in either of the two tested native child routes; both emitted `SubagentStart`. | Scoped observation only; other entry and spawn configurations remain untested. |
| `SubagentStart` fields and model/effort visibility | Bypassed under O4(a). | Captured `session_id`, `turn_id`, `transcript_path`, `cwd`, `hook_event_name`, `model`, `permission_mode`, `agent_id`, `agent_type`. `model` identified the child in the differing-model case. No effort field was present. | The Luna child emitted `model=gpt-6-luna` under an Astra parent. |
| `SubagentStop` block and loop prevention | Bypassed under O4(a). | `decision=block` made each worker continue, call the clock, and finish with `PROBE_CONTINUED`. First stop had `stop_hook_active=false`; second had `true`. | Captured `agent_transcript_path`, `agent_id`, `agent_type`, `last_assistant_message`, and the common/turn fields. Exit-code-2 blocking was not tested. |
| Spawn `PostToolUse` input and response | Bypassed under O4(a). | Actual tool name was `collaborationspawn_agent`; input contained `agent_type`, `task_name`, `fork_turns`, and the explicitly passed `reasoning_effort` in the caller-effort case. Response contained the canonical task path, not a child UUID. | Child UUID was available in `SubagentStart`. Joining events and automatic comparison were not implemented or accepted; S6 remains undetermined. |
| `SessionEnd` | Bypassed under O4(a). | Main-thread event fired with `reason=other`; fields were `session_id`, `transcript_path`, `cwd`, `hook_event_name`, `reason`. | This proves event availability, not the future component's complete state-cleanup behavior. |
| Hook run trusted by the user through `/hooks` | Not yet trusted by the user. | Pending. | O4(a) retains this required manual gate. |

The user resolved O3 and O4 through structured replies on 2026-09-26. O3(a) counts only a successful consultation; failure still blocks once and leaves the work pending until success or the user's release. O4(a) allows the trust bypass only in temporary-home live checks, retains a run trusted by the user through `/hooks`, and retains the untrusted skip-and-warning case. These explicit decisions authorized corresponding updates to the spec's AC-12/Open Decisions text and `sources.md` section 2.5, beyond ticket 01's original two-file evidence scope. They do not waive S3. No trusted-state edit or primary stop hook was used.

After that authorization, the fixture expanded to `SessionStart`, `SubagentStart`, `SubagentStop`, `PostToolUse`, and `SessionEnd`. Every fixture change was exposed by removing and re-adding the plugin through the temporary local marketplace, never by editing its installed copy. Commands used the P2 parent shape plus `--dangerously-bypass-hook-trust`. The multi-event parent was `01a0d9a1-0ecb-7473-8dc7-cf8dd765793a`; its `ca_worker_standard_h` child was `01a0d9a1-2dc6-71b3-8ace-6991282d0698`, observed at `gpt-6-astra[low]`, with role-aware inspector exit 0. A second parent `01a0d9a2-7b22-76e0-b546-9af77c98d85d` spawned a newly created throwaway `ca_worker_probe` template pinning `gpt-6-luna` but leaving effort to the caller. Explicit `reasoning_effort=high` produced child `01a0d9a2-8f95-7d91-8c26-995a0c36d623`, observed at `gpt-6-luna[high]`, with generic inspector exit 0. The fixture blocked once per child ID; it did not implement product file-change or consultation detection.

The first resume reused the startup marker, which could not by itself prove fresh context delivery. The distinct-marker probe changed the temporary fixture to inject a new value only when `source=resume`, reinstalled the copy, and resumed the existing parent without putting the marker's value in the prompt. The model returned the newly injected `HOOK_RESUMED_99031`; the command exited 0. This establishes resumed injection for that bypassed route.

### Stop conditions and handoff

| Condition | Status | Evidence |
|---|---|---|
| S1 | Not triggered for all eleven required dials. | P2: all completed; actual model/effort matched; all inspectors exited 0. |
| S2 | Not triggered in the tested pinned/caller-effort cases. | P3. Full-history inspection remains uncertified and is not generalized to template precedence. |
| S3 | Triggered: no eligible configuration established. | P4. Keep the mechanism pending; do not start ticket 02. |
| S4 | Not determined. | No eligible mechanism exists yet whose worker/explorer routes could be accepted. |
| S5 | Not triggered in the tested bypass runs; user-trusted route pending. | Plugin loading, primary injection, and JSON stop blocking worked under O4(a). The untrusted skip is not a failure. |
| S6 | Not determined. | Automatic per-dispatch hook route untested. |
| S9 | Not triggered for the current plugin/entries and hook fixture. | Local installation and updated hook execution succeeded. User-trusted execution and a future consultation component remain unverified. |

Ticket 01 cannot meet its all-clear acceptance while S3 is triggered and hook rows remain pending. Product implementation, typechecking, product tests, version changes, final independent acceptance, commits, pushes, and real-home updates were not performed. This project has no typed application; this ticket produced evidence only. The final product test/review/commit steps of `implement` remain pending with the blocked implementation.

Scope verification completed by the primary on 2026-09-26. Probe work changes only `acceptance.md` section 01 and the `spec.md` mechanism status. The subsequent explicit user decisions additionally change the spec's AC-12/Open Decisions text and `sources.md` section 2.5. Hash comparison confirmed the other seven task files unchanged and no new task files. Reversing only the authorized ledger edits reproduced its original SHA-256; the spec matched its original snapshot after accounting for the mechanism status and the explicit O3/O4 decisions. Acceptance sections 02 through Final remained unchanged. The primary matched all eleven P2 rows to completed child metadata and inspected both native-fork nonce records and the distinct resume result. These checks validate the record and its scope; they do not accept a product implementation.

`git diff --check` exited 0, the tracked `git diff --stat` was empty, and `git status --short` still matched the two starting untracked directories. A direct whitespace/section check covered the untracked Markdown files, which Git's empty tracked diff cannot validate. No dedicated parser or schema exists for this evidence document; product tests and the implementation code review remain pending with tickets 02–06.

Cleanup completed and was verified on 2026-09-26. No Codex process tied to the temporary directory remained. Both disposable homes, copied credentials, cached plugins, workspaces, probe templates/scripts, downloaded schemas/docs, hook state, raw logs, and the temporary directory pointer were deleted. `/home/hyy/ca-tier-probe-ou6tpics/` no longer exists. The tables above retain the non-secret findings and thread IDs; their underlying temporary rollouts are intentionally no longer available. The next execution must obtain user direction for S3 before starting dependent implementation. The user-trusted hook run and untrusted warning evidence also remain pending.

### P6 Authorized continuation and selected mechanism

The user explicitly authorized continued investigation on 2026-09-26: “没看到结构化选项；授权继续”. This reopened the investigation without weakening AC-3. All continuation probes used `codex-cli 0.157.0` and disposable homes under `/home/hyy/ca-consult-reprobe-pfgxoqcr/`. The repository HEAD and starting Git status were unchanged. A fresh SHA-256 baseline covered all ten task files. The local marketplace route, remove/add after each fixture change, and companion installer were retained. Neither the real installation nor its trust state was changed.

#### Empty tools and automatic caller identity

The official configuration reference/schema and App Server documentation were fetched on 2026-09-26. The schema describes `model_catalog_json` as a process-start setting, not a per-thread override. `codex debug models --bundled` exposed the default model's experimental clock tool, explaining why the earlier feature switches alone were insufficient. A startup catalog retaining the exact model ID but setting `shell_type="disabled"`, `apply_patch_tool_type=null`, `experimental_supported_tools=[]`, `supports_search_tool=false`, and tool-usage instruction flags false, combined with the normal tool feature switches, produced an actual empty inventory. An attempted `tool_mode` catalog field was not present in the loaded catalog and is not part of the mechanism.

The additional feature switches were `shell_tool`, `view_image`, `goals`, `request_permissions_tool`, `default_mode_request_user_input`, `image_generation`, `apps`, `code_mode`, `code_mode_host`, `code_mode_only`, `sleep_tool`, `current_time_reminder`, `browser_use`, `computer_use`, `tool_suggest`, `multi_agent_v2`, and `plugins`, all false; `agents.enabled`, `tools.update_plan.enabled`, and `tools.experimental_request_user_input.enabled` were false, and `web_search` was `disabled`. These settings are qualified together, not individually certified disable switches.

The host's `CODEX_ROLLOUT_TRACE_ROOT` records actual inference request bodies through `inference_started.request_payload.path`. A local unauthenticated HTTP fixture first confirmed that the captured payload is the request body, not transport authentication headers. The authenticated empty-tool probe, thread `01a0d9af-e0bd-7562-b0e7-e83b4a7606c6`, then returned `PROBE_OK` at actual `gpt-6-astra[low]`, with `additional_tools.tools=[]` and no top-level tools. This is host request evidence, not an advisor self-report. The component invokes native Codex authentication; it never reads, copies, or transmits credentials. Only test setup copied the necessary authentication configuration.

Zero-argument MCP caller identification succeeded in thread `01a0d9b5-5305-7980-a4eb-c5a22b523a81`. Host `tools/call.params._meta` supplied `threadId`, `sessionId`, `itemId`, and `x-codex-turn-metadata` containing thread, turn, model, and effort. The MCP process did not receive `CODEX_HOME`, `CODEX_THREAD_ID`, `CODEX_SESSION_ID`, or `PLUGIN_ROOT`; those environment variables are not the discovery contract. The probe used accurate read-only/non-destructive annotations after a call without annotations was rejected under approval policy `never`.

#### Configuration comparison and decision

An A′ revision forked before the active turn (`ephemeral=true`, `excludeTurns=true`), then used `thread/inject_items` to append the current turn's raw response items. The official App Server documentation explicitly states that this method appends prebuilt Responses API items to model-visible history. The source `01a0d9bd-6013-7b01-b15f-d86c8e44c571` and advisor `01a0d9bd-b483-7f83-ab92-d944216c8049` passed the nonce and empty-tool checks. A twelve-turn sequence and manual compaction also passed. However, automatic compaction inside one active turn exposed a real failure: source `01a0d9c1-9429-7171-98f8-312810a4417b` had seven effective input items, while advisor `01a0d9c1-e32b-7e82-951c-94a19bda5203` retained only six of those, omitted the new summary, and restored the removed large tool result. The nonce alone still passed. This A′ revision is ineligible.

Selected **B′: zero-argument MCP, single-snapshot effective-history reconstruction, and native App Server structured injection**. It extends candidate B by using `thread/start` plus `thread/inject_items` instead of flattening the context into a `codex exec` prompt. It uses no turn-count window and no caller-written summary:

1. Bind the host-supplied caller identity to exactly one rollout and the current consultation boundary.
2. Replay `response_item` records in order, replacing the accumulated history at each `compacted.replacement_history`. Stop before the in-flight consultation item. Preserve structured content, tool pairing, and opaque reasoning; do not restore pre-compaction items.
3. Start a fresh ephemeral App Server thread with the empty-tool startup configuration and the source base instructions. Inject the reconstructed structured items, then consultant-specific developer instructions and the consultation request. Fresh host scaffolding is additional context; it must not weaken caller constraints.
4. Check every actual advisor request's model, effort, and tool inventory from the host trace. Missing or contradictory evidence is an explicit failure. The trace/catalog are temporary implementation inputs, not persistent observation logs.

The probe rejects an absent consultation boundary, absent compaction replacement history, or rollback reconstruction it has not qualified. Production must also validate thread/turn/item binding, supported item shapes, truncation, context overflow, cancellation, and its exact output contract. Explicit failure is allowed by AC-3; silently shortening or reconstructing a summary is not. These are ticket 04 obligations, not claims that the throwaway probe is a finished component.

The primary compared actual caller and advisor requests, preserving item order, roles, content, tool outputs, and encrypted reasoning. Comparison normalization removes transport IDs, internal attribution metadata, and optional null-valued fields only. Caller tool inventory is omitted under the spec's explicit implementer choice. The counts below are ordered source-item inclusion, not equality of the entire request: the advisor adds its own host scaffolding and consultation instructions.

| B′ check | Source thread | Advisor thread | Actual result |
|---|---|---|---|
| Earliest context after eleven uncompacted turns, then a same-turn tool nonce | `01a0d9c4-4596-72e3-9b6c-16b68d188f89` | `01a0d9c5-198a-78d1-9442-c5f3bb00fc7a` | 31/31 ordered input items preserved; earliest constraint and nonce recovered. |
| Forced compaction, later marker, and a fresh same-turn nonce | Same source | `01a0d9c5-9dec-7da1-8a80-4164d80fb69a` | 22/22 items preserved; summary, earliest retained constraint, later marker, and nonce recovered. |
| Automatic compaction during the unfinished turn | `01a0d9c3-992a-7082-992f-eb2d14b94527` | `01a0d9c3-f1b2-7501-aa93-ddceab634365` | 7/7 post-compaction items preserved; one effective summary; removed large tool output absent. |
| Native worker at `gpt-6-luna[high]` | `01a0d9c6-f8b2-78d3-908f-afd54d2c448d` | `01a0d9c7-2b54-78b3-8999-ea4e66a687d1` | Zero-argument call; 10/10 items preserved; nonce recovered; encrypted reasoning bytes preserved across model boundary. |
| Native explorer at `gpt-6-luna[high]` | `01a0d9c7-b50d-7623-8301-105a9b687b65` | `01a0d9c7-e337-7a90-ad8e-0c4fe6ae2dce` | Zero-argument call; 9/9 items preserved; nonce recovered. |
| Relative installed component path and truncated tool output | `01a0d9cc-b9fc-7821-a450-464d20edeca2` | `01a0d9cc-f687-78b0-8f94-b8f5c5067b21` | 9/9 items preserved, including the caller-visible result truncated to 1,500 output tokens; nonce recovered. |
| Image attachment without caller transcription | `01a0d9cf-3da4-74f0-bfff-59acd2249ee5` | `01a0d9cf-6b19-7613-a8fe-cfba163e3ea7` | 9/9 items preserved, including image content; advisor read `coral-pine-68317` from the image and recovered the separate tool nonce. |

Every advisor request in this table ran through the native `official` provider at `gpt-6-astra[low]`, matching the low-effort primary or mainstay probe caller's AC-4 target, with actual `additional_tools.tools=[]` and no top-level tools. Every completed probe command exited 0. The worker/explorer parent was `01a0d9c6-7588-74a0-8a4f-4e0dc3cecec5`; each temporary role pinned Luna high and retained its role's developer instructions. Both role-aware inspectors exited 0 with the expected parent, role, model, effort, temporary working directory, and observed read-only/managed permission metadata. This does not independently prove isolation.

Portable loading was tested through `.mcp.json` with `command="python3"`, `args=["./scripts/consult-probe.py"]`, and `cwd="."`. The host resolved that working directory to the installed plugin root. The script identified its temporary home from the verified versioned cache layout, not credentials or a caller-supplied path. The two `${CLAUDE_PLUGIN_ROOT}`/`${PLUGIN_ROOT}` argument attempts and a relative argument without `cwd` failed MCP initialization; they are not selected. App Server `mcpServerStatus/list` reported `connected` with the zero-property tool schema for the selected configuration, and the truncated-output live call confirmed execution after reinstall.

The first continuation decision advisor, `01a0d9c0-6b07-7a23-bf24-2c13d5deeebf` (parent `01a0d9c0-1bde-75d2-bff3-451fdbc9e6cf`), independently identified the intra-turn compaction flaw and recommended the decisive actual-request comparison. A fresh advisor, `01a0d9cb-0033-70e2-9c5f-079ae9ff5c79` (parent `01a0d9ca-9387-7a61-b53e-1f53279f317f`), inspected B′ and reran the five initial comparisons. It recommended selection once portable loading and truncation passed; the primary then verified both and the image case. Both were `ca_advisor_standard` at actual `gpt-6-astra[medium]`, role-aware inspector exit 0, read-only/managed. These were decision consultations, not independent product acceptance.

B′ is selected because it is the only configuration qualified across all five eligibility checks and all three caller routes. Structured injection preserves roles, images, tool items, and opaque reasoning that text serialization would flatten. Remaining untested configurations stay untested; no universal claim is made about other native forks or transports. Requalify after a host version, rollout schema, model catalog, MCP metadata, cache-layout, or request-trace format change. Audio/video inputs, rollback, parallel tool races, and other non-exercised shapes are not certified by these probes; the component must fail explicitly rather than claim complete reconstruction where it cannot establish it.

#### Automatic dispatch checking and remaining trust gate

The same temporary plugin also shipped a `PostToolUse` fixture. It joined the actual spawn arguments to child session metadata using the parent UUID and native task path, then read the child's actual `turn_context`. No persistent join state is necessary for this route. The fixture compared pins or the explicit caller effort and injected its verdict through `hookSpecificOutput.additionalContext`. Under the authorized temporary hook-trust bypass:

- Worker and explorer dispatches above produced `DISPATCH_MATCH`, with actual Luna high.
- An intentional `ca_worker_senior` spawn omitted the caller-selected effort. Child `01a0d9c8-470a-7492-bad3-92fb309a0893` actually inherited Astra low. The hook reported `DISPATCH_MISMATCH_WORK_PENDING`, including missing expected effort and observed low; the parent quoted that warning and left acceptance pending. This demonstrates an automatic same-session route for AC-10 and clears S6's host-capability concern. It does not accept the future complete hook implementation.

Untrusted CLI runs skipped the fixture's `SessionStart`, but still did not expose the documented `/hooks` warning in captured output. An interactive launch again stopped at the folder-trust gate; the primary exited without choosing trust. The user-trusted `/hooks` run and the interactive untrusted warning remain pending. No hook trust was written or selected by the primary. Per ticket 01's explicit waiting-row rule, these checks do not block ticket 02, but must be resolved before ticket 05 starts.

Current stop-condition assessment: S1 and S2 retain P2/P3's passed evidence; S3 and S4 are cleared by B′; S5 remains not triggered by the exercised bypass route, with user-trusted execution pending; S6 is not triggered by the automatic positive/negative dispatch probe; S9 is not triggered by the installed relative-path component and hook execution. No product implementation, release, or real-home update is accepted by this section.

Continuation scope verification completed before ticket 02: exactly `acceptance.md` and `spec.md` differ from the continuation's ten-file SHA-256 baseline; the other eight task files are unchanged. No tracked file changed. The primary checked the new request-comparison results and native route inspections, task-file whitespace, and `git diff --check` (exit 0). No dedicated Markdown parser/schema applies to the evidence record. Product tests and the implementation review remain pending with product implementation.

Continuation cleanup completed on 2026-09-26. A process inspection found no remaining Codex/probe process tied to the temporary root. `/home/hyy/ca-consult-reprobe-pfgxoqcr/` and `/tmp/ca-consult-reprobe-path` were deleted and their absence verified, including both homes, copied credentials, installed fixtures, raw logs/traces, scripts, schemas/docs, and image. This section retains non-secret results and IDs; the temporary underlying records are intentionally unavailable after cleanup. The required user-trusted hook and warning checks must use a newly prepared temporary home before ticket 05.

### P7 User-trusted execution and untrusted skip

Prepared `/home/hyy/ca-hook-trust-jw6yp7ek/` on 2026-09-26 from the unchanged tracked HEAD using a new temporary home, the required local marketplace installation route, and only necessary authentication configuration. This is separate from the deleted P6 environment. Its only fixture hook is `SessionStart`: it records session/event/source/model metadata to a temporary receipt and injects a fixed marker. It neither modifies a project nor handles credentials or trust. The user was given the `script -q -f` command that captures the interactive CLI, asked to retain the untrusted warning, review/trust this hook through `/hooks`, then exit. No bypass is used for this check. User action and the subsequent trusted execution are pending; the home, copied credentials, and transcript must be removed after the check. Tickets 02–04 can continue while waiting; ticket 05 cannot start until this gate is resolved.

The user reported completing trust and exiting. The primary's subsequent no-bypass check, thread `01a0d9dd-47af-72c1-942a-cc7b1fb6c613`, returned `MISSING`, and no fixture receipt existed. The captured interactive command explains the discrepancy: it set `C0DEx_HoME`, not `CODEX_HOME`, so that launch did not use the prepared temporary configuration. The host's hooks feature is enabled in the temporary home. A prepared `trust-check.sh` now sets the exact environment key internally, avoiding another manual transcription of it. The corrected user-trust action remains pending; the primary did not alter any trust state.

The user then ran the corrected script and reported completion. The captured host UI shows the user selecting **Trust all and continue** in the startup **Hooks need review** dialog. This is the host's interactive trust gate presented before entering the session; the record does not claim the user typed `/hooks`. A subsequent `codex exec` without bypass, thread `01a0d9e1-e5d5-7fa0-9f66-56fbd8cc2b9b`, returned `HOOK_USER_TRUST_30941`, exited 0, and produced the matching receipt: `SessionStart`, `source=startup`, `model=gpt-6-astra`.

The primary changed only the temporary fixture's timeout from 5 to 6 and reinstalled through remove/add, producing a new hook hash without editing trust state. In the next interactive launch the primary selected **Continue without trusting**. The host showed **Hooks need review** for one new/changed hook. Thread `01a0d9e3-0490-7a80-9788-0e3802b681aa` returned `MISSING`; the receipt file still contained only the earlier trusted execution. The `/hooks` overview showed `SessionStart: Installed 1, Active 0, Review 1` and `1 hook needs review before it can run`. The primary exited without granting trust. These observations establish an untrusted skip and the host's interactive warning; no additional literal startup message pointing to `/hooks` was observed.

O4's user-trust and untrusted-warning cases are complete. The concrete startup dialog is the current host's presentation of the same user-owned trust action. S5 is not triggered. Product hook acceptance remains ticket 05's responsibility. On 2026-09-26 the primary stopped the two managed daemons belonging to this temporary home, removed `/home/hyy/ca-hook-trust-jw6yp7ek/` and `/tmp/ca-hook-trust-path`, and verified absence. Copied credentials, raw captures, receipts, fixture source, and installed copies were deleted; only these non-secret findings remain.

## 02 Doctrine, posture text, glossary, ADR-0006

Status: accepted by the primary for ticket 02 on
2026-09-26. This record covers the doctrine, canonical
posture text, glossary, and ADR record only. Tickets 03–06 and final product
acceptance also remain pending.

The ticket 02 worker ran in thread `01a0d9d5-0103-7373-87a4-520488baf6d8`, parent
`01a0d989-47e5-7562-9ba3-373aef463838`, through installed entry
`ca_worker_standard_m` at observed `gpt-5.6-sol[high]`. The role-aware inspector
exited 0. Observed sandbox and permission metadata were `danger-full-access` and
`disabled`; the working directory was this repository. The worker made no commit,
branch, push, real-home installation, or external change.

### Changes and decisions

- Replaced the old allocation and recovery doctrine in runtime `SKILL.md` with
  `mainstay`/`crux`/`rescue` admission, next-tier escalation, failure counting,
  zero-argument process consultation, posture/adoption pointers, and AC-2 acceptance
  selection. Complete-attempt, fresh-thread, Architect-mode, and primary acceptance
  ownership meanings remain.
- Added `references/consult-posture.md` with exactly six matching delimiter lines
  around the full, reduced, and adoption blocks. Exact model identity selects the
  posture; an unknown model follows the same comparison, with `gpt-5.6-terra` as
  the example and no family list. The reduced block explicitly has only its two
  multi-step triggers. The text includes durable-before-call, next-visible-reply,
  reconcile, every AC-6 exception, and no commit step.
- Kept the Explorer and Worker packets unchanged byte for byte. The Advisor contract
  now contains only independent acceptance; consultation takes no packet. Updated
  only the two ticket-owned operations sections; an automated comparison confirmed
  every byte outside them unchanged in both languages.
- Rewrote the glossary terms required by DR-6. Retired terms remain only on `_Avoid_`
  lines. Added ADR-0006 with the thirteen-entry decision, B-prime mechanism and
  limits, host facts and invalidation checks, `/hooks` user gate, the `0.4.0` grok
  lane, and every superseded sentence from ADR-0003/4/5 as an exact quotation.
- Used `<!-- consult-posture:<variant>:start/end -->` as the stable delimiter syntax.
  The English and Chinese files preserve these delimiters character for character.
  `openai.yaml` did not name a retired concept and was not changed. ADR-0005's
  ownership, evidence reuse, batching, and scenario-selection rules remain; only
  its obsolete delegated-check tier-selection clause is superseded.

Changed deliverable paths are `CONTEXT.md`,
`docs/adr/0006-mainstay-crux-rescue-and-process-consultation.md`, runtime
`SKILL.md`, `references/consult-posture.md`, `references/role-contracts.md`, and
`references/operations.md`, plus the four matching runtime Markdown twins under
`docs/zh/`.

### Verification

`python3 tests/test_zh_mirror.py` exited 0: `27/27 passed, 0 failed`, including all
four runtime Markdown pairs changed or added by this ticket.

`sh plugins/codex-advisor/scripts/verify.sh` exited 0:

```text
PASS: fork metadata, overwrite, unchanged, retire, check drift/residue, preservation, refusals
PASS: generic inspector, table-driven templates, retired options, payload filtering
VERIFY PASSED: selected deterministic checks (no live routing claim)
```

The scoped retired-term search used this command, with the two operations sections
extracted by their headings and `CONTEXT.md` `_Avoid_` lines excluded:

```sh
set -o pipefail
pattern='first-round pool|senior gate|decision packet|DECISION packet|Proactive advice is allowed|\b(light|standard|senior)\b'
failed=0
if rg -n -i "$pattern" plugins/codex-advisor/skills/orchestration/SKILL.md plugins/codex-advisor/skills/orchestration/references/consult-posture.md plugins/codex-advisor/skills/orchestration/references/role-contracts.md docs/zh/skills/orchestration/SKILL.md docs/zh/skills/orchestration/references/consult-posture.md docs/zh/skills/orchestration/references/role-contracts.md; then failed=1; fi
if awk '/^## Recover and hand off actual state$/{on=1} /^## Schedule and check combined work$/{on=0} /^## Advice and independent acceptance$/{on=1} /^## Observe permissions$/{on=0} on' plugins/codex-advisor/skills/orchestration/references/operations.md | rg -n -i "$pattern"; then failed=1; fi
if awk '/^## 恢复并把实际状态交接出去$/{on=1} /^## 调度并检查合并后的工作$/{on=0} /^## 建议与 independent acceptance$/{on=1} /^## 观察权限$/{on=0} on' docs/zh/skills/orchestration/references/operations.md | rg -n -i "$pattern"; then failed=1; fi
if rg -n -i "$pattern" CONTEXT.md | rg -v '_Avoid_'; then failed=1; fi
exit "$failed"
```

The combined command exited 0 with no matches. The separate `SKILL.md` and twin
search also exited 0 with no matches:

```sh
if rg -n 'gpt-|[[:alnum:]._-]+\[(low|medium|high|xhigh|max)' plugins/codex-advisor/skills/orchestration/SKILL.md docs/zh/skills/orchestration/SKILL.md; then exit 1; else exit 0; fi
```

`git diff --check` exited 0 with no output. Because the new ADR and posture files
are untracked, the supplemental `git diff --no-index --check /dev/null <file>` run
covered each new deliverable and the acceptance record, and exited 0 after treating
the normal no-index difference status as success.

Supplemental structure checks also passed: both posture references contain six
delimiter lines; every one of the 18 ADR quote blocks is an exact normalized
substring of ADR-0003, ADR-0004, or ADR-0005; the unowned operations bytes and the
Explorer/Worker contract prefixes equal `HEAD` in both languages.

Two initial supplemental-check commands failed because of command defects, before
they evaluated the deliverable: the first ADR quote validator had an invalid Python
generator expression (`SyntaxError`), and the first no-index wrapper assigned zsh's
read-only variable `status`. Their corrected reruns are the passing results above.

### Gaps

No new documentation test was added, per the ticket. The verifier states that it
makes no live routing claim; this ticket's doctrine is established by mirror,
structure, exact-text, scope, and diff checks. Runtime consultation, entry routing,
hooks, README/manual, and integrated acceptance belong to later tickets.
The primary inspected all changed and new English and Chinese deliverables, including
the corrected advisory-attempt definition and trust provenance. The required checks
above remain valid for this state; the post-correction mirror test passed 27/27 and
the primary's whitespace check exited 0. Ticket 02 is accepted; ticket 03 may begin.

The user-trusted and untrusted-skip hook paths have now passed in the correct
temporary `CODEX_HOME`: the user trusted the hook in the startup review dialog;
the primary selected "Continue without trusting" for the changed-hash case. The
trusted no-bypass thread returned the injected marker and wrote a `SessionStart`
receipt; the changed-hash untrusted thread returned `MISSING` without a new receipt
while the `/hooks` overview showed one hook awaiting review.
ADR-0006 records the non-secret results and thread IDs. This establishes the host
trust boundary, not the future product hook implementation. Old tier terms remain
in the routing profile, templates, scripts, README, the unowned operations sections,
historical ADRs, and earlier release material because later tickets own those
locations.

## 03 Routing profile, entries, installer, inspector

Status: ticket 03 accepted by the primary on 2026-09-26 after deterministic
verification, complete diff inspection, and all thirteen live routes passed.
Model-setting evidence comes from the live checks, not the deterministic tests.

The ticket 03 worker ran in thread `01a0d9eb-7cd5-7fe0-8b1e-b2cbd0602159`,
parent `01a0d989-47e5-7562-9ba3-373aef463838`, through the installed 0.2.0
entry `ca_worker_standard_m` at observed `gpt-5.6-sol[high]`. The role-aware
inspector exited 0. Observed sandbox and permission metadata were
`danger-full-access` and `disabled`; the working directory was this repository.

### Changes and decisions

- The English and Chinese routing profiles now carry the TR-3 table cell by
  cell, including the worker `crux` Astra default of `low`, candidate order,
  AC-4 consultation mapping, AC-2 acceptance mapping and its Derived cases,
  the model/effort ordering for "not weaker", both TR-9 assumptions and their
  next-model-generation invalidation trigger, and the adjustment method. The
  profiles contain neither a 5.6 model nor Terra.
- Thirteen tier-named templates and thirteen Chinese twins replace the eleven
  0.2.0 pairs. The six single-effort entries pin effort; all other entries leave
  it to the caller. Explorer and Advisor entries request read-only sandboxing,
  workers inherit the parent sandbox, same-role instruction bodies are identical,
  Advisor instructions answer only the REVIEW packet, and no posture section is
  present before ticket 04.
- `retire.txt` retains the eight 0.1.0 filenames and adds the exact eleven 0.2.0
  filenames. The installer remains manifest-driven and keeps its overwrite,
  unchanged, retire, check, selective-check, preservation, atomic-write, and
  refusal behavior. Its selectors come from the thirteen filenames.
- The inspector interface and implementation did not change. Runtime tests discover
  all templates and therefore now exercise thirteen cases. The owned operations
  sections list all entries and selectors, show pinned effort only for pinned
  entries, preserve the generic inspector interface, and retain the general
  ADR-0005 scenario-selection, evidence-reuse, and unexercised-path rules.

### Deterministic verification

`sh plugins/codex-advisor/scripts/verify.sh` exited 0:

```text
PASS: profile/template equality, negative model fixture, exact retire set, negative retire fixtures
PASS: fork metadata, overwrite, unchanged, retire, check drift/residue, preservation, refusals
PASS: generic inspector, table-driven templates, retired options, payload filtering
VERIFY PASSED: selected deterministic checks (no live routing claim)
```

The profile check rejects a copied template map after one model is replaced by
`fixture-wrong-model`. The retire check derives the fixed eleven-file historical
set from ADR-0004 and rejects both a missing-file fixture and an equal-size fixture
containing `ca-fixture-typo.toml`. The installer fixture seeds all nineteen retired
files, asserts nineteen removals, preserves an unrelated file, and passes a final
`--check`.

`python3 tests/test_zh_mirror.py` exited 0 with `31/31 passed, 0 failed`: five
Markdown pairs, thirteen template pairs by existence, and thirteen template pairs
by equal configuration keys plus Chinese prose.

A supplemental structural check exited 0 after comparing the three TR-3 rows in
`spec.md` with the routing profile after removing entry-name prefixes. It also
parsed both template sets and reported:

```text
PASS: TR-3 cells, 13-entry role counts, identical role bodies, REVIEW-only Advisors, no posture sections
```

The stage search over `plugins/codex-advisor/` and `docs/zh/`, excluding only
`agents/retire.txt` and `.codex-plugin/plugin.json`, exited 0 with no old entry
name and no old tier word. A separate search of both routing profiles exited 0
with no `gpt-5.6` or Terra. `git diff --check` exited 0; a supplemental
`git diff --no-index --check` loop covered all twenty-six untracked templates and
also passed.

During development, the first supplemental TR-3 comparison failed because its
temporary parser did not normalize indentation and Markdown backticks. A mechanical
end-of-file cleanup then wrote a literal `\\n` into the new templates; the full
verifier and mirror test rejected the invalid TOML. The templates were corrected,
and every final check above was rerun on the current bytes.

### Live route check

The primary ran all thirteen native routes on 2026-09-26 with Codex `0.157.0`, in `/home/hyy/ca-tier-routes-rcwpu1wb/home`, installed from this checkout through the required local marketplace route and companion installer. Each parent ran at `gpt-6-astra[low]`, with one fresh child, `fork_turns=none`, and effort passed only for caller-selected entries. Every parent and inspector exited 0, and each parent returned the fixture first line `ROUTE_FIXTURE_74216`.

| Entry | Effort passed | Actual model | Actual effort | Sandbox / permission | Child thread | Inspector |
|---|---|---|---|---|---|---|
| `ca_advisor_crux` | `omitted` | `gpt-6-astra` | `high` | read-only / managed | `01a0d9f5-f781-78c2-8529-b6e458f9bed5` | 0 |
| `ca_advisor_mainstay` | `low` | `gpt-6-astra` | `low` | read-only / managed | `01a0d9f6-4a88-7403-9165-74c8f7a1621d` | 0 |
| `ca_advisor_rescue` | `omitted` | `gpt-6-astra` | `xhigh` | read-only / managed | `01a0d9f6-8bcf-7ca2-8f2c-97d4739d81af` | 0 |
| `ca_explorer_crux_h` | `omitted` | `gpt-6-sol` | `xhigh` | read-only / managed | `01a0d9f6-d8f9-7a83-8361-da28c2c9095c` | 0 |
| `ca_explorer_crux_m` | `omitted` | `gpt-6-luna` | `max` | read-only / managed | `01a0d9f7-261a-7e93-a2de-2ba109cd926a` | 0 |
| `ca_explorer_mainstay_h` | `medium` | `gpt-6-sol` | `medium` | read-only / managed | `01a0d9f7-87a9-7331-ad99-893e807dca2c` | 0 |
| `ca_explorer_mainstay_m` | `high` | `gpt-6-luna` | `high` | read-only / managed | `01a0d9f7-cf48-70b1-a449-34584f890c12` | 0 |
| `ca_explorer_rescue` | `medium` | `gpt-6-astra` | `medium` | read-only / managed | `01a0d9f8-1bb5-7f11-b4f7-4667f6fc7f06` | 0 |
| `ca_worker_crux_h` | `low` | `gpt-6-astra` | `low` | read-only / managed | `01a0d9f8-62ee-73f2-8228-f9888d82ce9d` | 0 |
| `ca_worker_crux_m` | `xhigh` | `gpt-6-sol` | `xhigh` | read-only / managed | `01a0d9f8-a7a2-7871-a9d0-87900dfa8ad0` | 0 |
| `ca_worker_mainstay_h` | `omitted` | `gpt-6-sol` | `high` | read-only / managed | `01a0d9f8-fa28-79c1-b392-7151673ebbc1` | 0 |
| `ca_worker_mainstay_m` | `omitted` | `gpt-6-luna` | `max` | read-only / managed | `01a0d9f9-4a14-7cb3-97dc-1032b56d31f8` | 0 |
| `ca_worker_rescue` | `high` | `gpt-6-astra` | `high` | read-only / managed | `01a0d9f9-a0c8-7ae0-a3ee-9d8a30ba3e09` | 0 |

Each child's recorded parent and working directory matched its actual CLI parent and the disposable workspace. Parent IDs, in table order: `01a0d9f5-d7fb-7402-9991-c775989f44aa`, `01a0d9f6-29cb-7790-89a8-62b995e874f9`, `01a0d9f6-6de6-7c01-a8ed-f4affaa3be16`, `01a0d9f6-b749-75a3-a479-147d4f3a2244`, `01a0d9f7-0509-73a3-b3ec-f19a4708f867`, `01a0d9f7-64f0-7461-bf89-e3de8b179e1b`, `01a0d9f7-ac5a-70b1-9d0c-5a46d0425fbd`, `01a0d9f7-f9c0-7f00-a278-89b645e444c2`, `01a0d9f8-4224-7cb0-9da5-62acc1d5f390`, `01a0d9f8-883c-7553-866c-46baf25bfc6d`, `01a0d9f8-d210-77b1-a6c3-2e2f9eba5fdf`, `01a0d9f9-22a1-7ba0-982e-f839489f593b`, `01a0d9f9-7ec6-7da3-9782-4ea1f569831b`.

The installer removed all eleven old filenames seeded from `HEAD` and installed exactly thirteen new templates. After the worker adjusted only whitespace outside TOML values, the primary confirmed every parsed field of all thirteen cached and working-tree templates equal, refreshed the plugin through remove/add, and reran the companion installer. Completed calls remain applicable because model, effort, description, and developer-instruction values were unchanged. No installed file was hand-edited.

The primary inspected all new templates in both languages, both profiles, the installer/verifier diff, and the owned operations sections. The new negative checks reject the intended wrong-model, missing-retire, and same-count wrong-retire cases. Ticket 03 passes its deliverable and live-route checks. The observed read-only policy came from the fixture parent; this verifies routing and wiring, not general isolation, quality, cost, or stability. Consultation and hooks remain untested product work.

Route cleanup completed on 2026-09-26: the primary stopped the temporary home's managed daemons, removed its home (including credentials and sessions), workspace, route logs, results JSON, installer output, and route harness, and verified their absence. The same outer temporary root retains only non-secret official schemas/docs and separate unauthenticated isolation fixtures needed for ticket 04; those are removed when that probe batch finishes. No real installation or trust state changed.

## 04 Process consultation

Status: ticket 04 accepted by the primary on 2026-09-26. Deterministic checks,
real primary/worker/explorer consultations, isolation, cancellation, and cleanup passed.

- Live consultations from the primary, a worker, and an explorer: caller, caller model, expected dial, observed advisor model and effort, nonce result, compaction result, earliest-context result, the request's actual tool set, and thread IDs.

### Implementation and deterministic evidence

The worker ran in thread `01a0d9fc-4bc5-7a51-9b93-1ee293114827`, parent
`01a0d989-47e5-7562-9ba3-373aef463838`, through an installed 0.2.0 worker entry
at observed `gpt-6-astra[low]`. The primary's role-aware inspector exited 0 and
reported `danger-full-access` / `disabled` with this repository as working
directory. The worker used synthetic homes and a substitute native executable;
it did not read real credentials/configuration or caller transcripts, call a
model, install into a real home, commit, branch, or push.

The implementation adds `.mcp.json`, the manifest's `mcpServers` field, and three
runtime modules under `scripts/`: `process-consultation.py` provides the
zero-argument MCP boundary and cancellation; `consult_context.py` binds host
identity, reconstructs one rollout snapshot, validates content/pairing, and reads
dials from the profile; `consult_native.py` handles native authenticated execution,
isolation, structured output, actual request checks, and cleanup. No dependency
was added. Version and manifest descriptions are untouched.

The reducer uses no window or caller summary. It replaces earlier history at
`compacted.replacement_history`, preserves raw roles, images, opaque reasoning,
and paired tool calls/results, including caller-visible truncated output, and
stops before the identified consultation item, including code-mode wrappers.
Unknown content/events, rollback, missing replacement history, inconsistent
identity, and unpaired parallel calls fail. Caller tool inventory is omitted, as
the specification permits. Every actual advisor request must contain source
items in order; comparison ignores only item-level transport `id`, the qualified
`internal_chat_message_metadata_passthrough`, and optional null fields. It never
removes `call_id` or changes content. Silent automatic compaction fails explicitly.

The executor enumerates all MCP inventory pages without caller context, closes
that native process, disables each name through a quoted TOML inline map, and
verifies empty MCP capabilities and hooks before injection. It uses the bundled
catalog's exact slug with disabled tools and the qualified feature vector,
including disabled memories and host skill discovery. Every actual inference
request must show the expected model/effort and an explicit empty tool set. At
the primary's direction, the verifier accepts either P6's empty
`additional_tools.tools` or explicit top-level `tools=[]`, rejecting a nonempty
inventory at either location and rejecting absent evidence.

The primary subsequently isolated a bundled-catalog `tool_mode=code_mode_only`
field that retained code-mode wrappers despite false feature flags. Native
unauthenticated catalog inspection showed that omitting this field restores
P6's qualified catalog shape. The component now removes the field rather than
inventing a disabled value. The executable fixture supplies the field and rejects
any generated catalog retaining it. Actual request tool validation remains strict.

The existing caller tool-call event means started. Returned
`structuredContent.status=succeeded` with a valid plan/correction/stop and matched
expected/actual dial means succeeded. Returned `status=failed` with `isError=true`
has a code/message and no advice; a missing terminal result is not success. A
valid stop counts as successful consultation. There is no retry. The native
deadline is 180 seconds. Cancellation terminates the native process tree and
removes the call's temporary directory. Catalogs, trace payloads, captured output,
logs, and SQLite state are temporary; the component opens no credential files.

All ten explorer/worker templates and their Chinese twins carry the exact
canonical full/reduced block plus adoption block inside
`process-consultation:start/end` delimiters. Exact profile model identity chooses
the variant. Advisors have no posture section. The installation group checks
these rules and same-role identity outside the section in both languages. Its
three negative fixtures reject a one-character edit, a full-posture entry given
the reduced variant, and an advisor given a section. A separate comparison with
the accepted ticket 03 snapshot proved every other template byte unchanged.
The operations section and twin document use, routing, results, failure, session
observability, isolation, cleanup, and the extra native initialization cost;
their verifier sections include the new group.

Worker verification on 2026-09-26:

- `sh plugins/codex-advisor/scripts/verify.sh`: final rerun exit 0, all
  installation, posture, inspector cases and **45 MCP-boundary tests** passed
  after the first live shape correction.
- `sh plugins/codex-advisor/scripts/verify.sh --consultation`: exit 0, **45 tests**
  passed after adding the primary's observed `world_state` / `token_usage_record`
  shapes and qualified attribution normalization, then passed again after the
  bundled `tool_mode` correction. Existing installation/runtime checks were
  unchanged by those corrections.
- `python3 tests/test_zh_mirror.py`: exit 0, **31/31 passed, 0 failed**.
- `git diff --check`: exit 0. Supplemental Python compilation and the accepted
  baseline template-byte comparison also exited 0. The worker inspected the
  scoped diff and all new implementation/fixture files.

The boundary suite launches a copied component from a synthetic versioned cache
and substitutes the native executable, without importing private functions.
Coverage includes every tier, primary Astra xhigh/Sol high/unknown Terra/Astra
medium, earliest context through 80 uncompacted messages, unfinished tools,
compaction, images, opaque reasoning and truncation; all result variants and
error/abort/empty/overflow/malformed output; actual dial mismatch including an
earlier request; missing/changed context; missing/nonempty tool evidence and
missing trace; MCP/hook leakage; identity/layout/content/rollback/pairing failures;
cancellation with a descendant; and unchanged synthetic `CODEX_HOME` plus cleaned
temporary directories. The inventory fixture includes pagination and names with
dots, quotes, a backslash, and non-ASCII text.

The first full run found a test-harness lambda returning the removed record as
keyword arguments; the corrected run passed. An initial acceptance-note insertion
also rejected a stale expected status line without writing; the worker reloaded
the concurrent primary edits before inserting this section. Neither establishes
a product defect. Live behavior, installed loading, native filesystem isolation,
and Windows execution are not proven by these fixtures. Product acceptance stays
with the primary; live findings and follow-up corrections are recorded separately.

The primary's worker route exposed `inter_agent_communication_metadata` with
`{"trigger_turn":true}` before the already-recorded user task message. The reducer
now accepts exactly that boolean-only metadata shape; its delegate fixture still
asserts unchanged raw task/history injection. Tool/history validation failures
after reading a request also retain the observed `actual` model/effort, as the
result contract requires. Six focused failure cases passed with that assertion;
earlier failures with no observed request still report `actual=null`. The updated
`--consultation` group exited 0 with **46 tests** passing after both corrections.

### Native isolation probes

The delegate live follow-up qualified raw `agent_message` items with nonempty
`author`/`recipient`, `input_text` and opaque `encrypted_content` blocks. The
component validates those fields and preserves the complete item without role
conversion or decryption. Delegate fixtures now include the native shape and
compare exact injected bytes; a changed encrypted block in the actual request
fails context verification, while empty author/recipient/encrypted content fail
before execution. The primary supplied this shape from worker
`01a0da16-28aa-7443-a10f-dc4c672c7dd4` and explorer
`01a0da15-f041-7a12-89c4-012fe1aa7d85`; the worker did not inspect those sessions.
After this correction, `sh plugins/codex-advisor/scripts/verify.sh --consultation`
exited 0 with **50 tests** passing. Modified Python syntax and `git diff --check`
also passed. The unchanged mirror/installation/runtime results remain applicable.

The primary fetched the official App Server and Hooks pages and the configuration
schema on 2026-09-26, and generated protocol schemas with Codex `0.157.0`. These
preparation probes used an unauthenticated disposable home under the existing
temporary probe root; they supplied no caller context and requested no inference.
A native thread startup attempted an unauthenticated WebSocket connection, which
returned 401; it is not an authenticated consultation or model-availability result.

- A `mcp_servers={}` startup override retained an existing fixture server. An empty
  map is not a supported way to clear inherited configuration.
- Native `initialize` alone did not start the fixture. `mcpServerStatus/list` did
  start it and enumerate its tool. Closing native stdin and waiting for normal exit
  left none of the fixture MCP process IDs alive.
- Three configured names, `fixture-one`, `fixture_two`, and `fixture.dot`, were
  returned over three pages with `limit=1`. A second process with the startup TOML
  override `mcp_servers={"fixture-one"={enabled=false},"fixture_two"={enabled=false},"fixture.dot"={enabled=false}}`
  returned all three with empty tools and did not start a fixture server.
- With `features.hooks`, `features.codex_hooks`, and `features.plugin_hooks` false,
  `hooks/list` returned an empty hooks list for the temporary working directory.
  The enabled control returned one enabled but untrusted user hook. This proves
  the host inventory change, not execution of a trusted hook: the control did not
  run it, and no untrusted skip is counted as execution evidence.
- The native process used a temporary working directory, `log_dir`, `sqlite_home`,
  and `CODEX_ROLLOUT_TRACE_ROOT`, `history.persistence="none"`, disabled plugins,
  memories and goals, `skip_host_skill_discovery=true`, and an ephemeral thread.
  A first thread initialization created the ordinary `.sandbox_migration` file
  containing only `v1`. After that ordinary initialization, the two-stage probe
  left the source home's file-size/mtime snapshot unchanged. Native databases and
  traces were confined to the temporary state location. This establishes only
  the exercised initialized-home path; product normal, error, and cancellation
  paths must still be checked. The initial probe wrapper had a PID newline-split
  error after successful native shutdown; the corrected rerun passed.

Decision advice came from fresh installed `ca_advisor_standard` thread
`01a0d9f2-a978-7301-a06f-96f58e3c6086`, actual `gpt-6-astra[medium]`, parent
`01a0d989-47e5-7562-9ba3-373aef463838`, role-aware inspector exit 0. Observed
permissions were `danger-full-access` / `disabled`; the packet prohibited writes,
model calls, credential reads, and delegation, and its activity was read-only.
On the new probe evidence, advice confirmed that native service initialization
does not violate AC-3's limit on the advisor model's actual tools. It adds startup
cost and can run existing services' startup behavior, which must be disclosed.
No caller context may be supplied to the enumeration phase, and its tool/resource
descriptions or errors must not enter the advisor input or persistent records.
The primary adopts two-stage native enumeration and disabling, with preflight and
every-request checks. This is implementation advice, not independent acceptance.

AC-11 is not waived: consultation-specific content, thread records, logs, traces,
databases, counters, or markers remain temporary even when Codex writes them.
Existing host installation/migration bookkeeping without consultation state is
classified separately; no general exemption for native writes is inferred. A
product path requiring new persistent consultation state must fail or return to
the user under S8. These probe scripts/docs remain temporary until product wiring
no longer needs them; route credentials and route logs were already removed.

### Primary product checks in progress

The primary installed each tested revision through the X-2 marketplace remove/add
route and ran its cached companion installer in the temporary home at
`/home/hyy/ca-consult-product-u9awq0t2/home`. Actual native request traces are copied
only inside that disposable test root by a test-only PATH wrapper, before the
product removes its temporary state. This adds no product observation switch.

The first product checks exposed omitted native record types (`world_state`,
`token_usage_record`, and `inter_agent_communication_metadata`) and the structured
`agent_message` used for encrypted delegate task delivery. The primary compared
actual caller requests to the source items before qualifying each shape. State
and usage metadata are not extra messages; rendered instructions are retained as
response items. Encrypted agent messages remain structured and byte-exact. The
only comparison normalization is item-level transport `id`, optional nulls, and
`internal_chat_message_metadata_passthrough`; roles, text, `call_id`, images, and
encrypted bytes stay exact.

The first native advisor request correctly failed the empty-tool check because the
bundled catalog's `tool_mode=code_mode_only` had been copied into the custom catalog.
An unauthenticated native catalog comparison established the cause. Omitting that
field restores the P6-qualified catalog; assigning an invented disable value is
not used. The corrected actual requests below have `additional_tools.tools=[]`
and no top-level tools. These implementation corrections do not change B′ or
relax its success criteria.

| Product check | Caller | Advisor | Primary evidence |
|---|---|---|---|
| Primary at its actual required dial | `01a0da13-36a5-7792-a9d3-7e95048549c6` | `01a0da13-a5cb-7e01-9083-5f4edbc1bef6` | Actual `gpt-6-astra[xhigh]`; empty tools; 16/16 effective source items and source base instructions preserved; plan contains earliest constraint and same-turn nonce. |
| Eleven completed uncompacted turns, then consultation | `01a0da14-7285-72c0-a0b7-ace599a737ab` | `01a0da15-2c9c-7a80-abae-0dde46d9d1c3` | Actual `gpt-6-astra[low]`; empty tools; 34/34 source items and base preserved; earliest token and fresh nonce recovered. No turn window exists. |
| Native manual compaction and later context | Same caller | `01a0da15-ec91-7043-8058-600b07cff276` | Actual `gpt-6-astra[low]`; empty tools; 21/21 post-compaction items and base preserved; retained earliest token, later marker, and fresh nonce recovered. |

The primary verified native trace payloads directly, not the advisor's self-report.
Each successful product response has `status=succeeded`, one `plan`, matching
`actual`/`expected`, and distinct caller/advisor IDs. Each tested normal/failed
native call removed its temporary catalog, trace, logs and databases. Delegate,
configured-service isolation and cancellation checks remain in progress. The
source homes and test-only retained traces are not yet cleaned while these checks
run; ticket 04 is not accepted yet.

### Primary acceptance and cleanup

The final worker and explorer product calls passed after X-2 refresh. Worker
`01a0da19-47e9-75b2-bd3f-76133faaf931`, parent
`01a0da19-23e7-7b00-b2a6-7f79d710b930`, ran the installed
`ca_worker_mainstay_m` at actual `gpt-6-luna[max]`. Explorer
`01a0da19-489d-74d0-9a1d-421ceb9c5368`, parent
`01a0da19-23e7-7d23-aee6-39c1a2f04b18`, ran
`ca_explorer_mainstay_m` at actual `gpt-6-luna[high]`. Both role-aware inspectors
exited 0, with the expected temporary cwd and parent. The host applied
`danger-full-access` / `disabled` to both; these fixtures prohibited edits and
performed no edits. This is behavioral scope evidence, not sandbox isolation.

Their advisors were respectively `01a0da19-a095-78b1-a533-3f01e406a55a` and
`01a0da19-c50f-78e3-9c1c-752ba7c8d02a`, both actual `gpt-6-astra[low]`, with
actual empty request tools. Each retained 12/12 effective source items in order,
including encrypted `agent_message` content, and returned a valid plan containing
its earliest constraint and same-turn tool nonce. Each parent completed with exit
0 and reported the exact structured result.

A separate synthetic active-rollout fixture exercised the installed product's
real native authenticated executor with an additional configured MCP service.
Advisor `01a0da1a-613a-78d0-a32b-b185c2fbd793` succeeded at actual
`gpt-6-astra[low]` with no tools. The sentinel service started once during inventory,
received no tool call, and had no surviving process after native shutdown.
An initialized-home size/mtime snapshot was identical before and after the entire
consultation (`homeDelta=[]`), including the plugin cache. A cancellation at the
MCP boundary returned `status=failed`, `code=cancelled`, and no advice; its home
snapshot also remained identical, and the server exited 0. The deterministic
cancellation scenario separately starts a descendant and proves process-tree
termination. Configured hook suppression was covered by the earlier native
inventory probe and the product hook-leak negative fixture; this is not a claim
that product hooks have been implemented or accepted.

On the final ticket-04 bytes, the primary ran unqualified `verify.sh` (exit 0,
50 consultation boundary tests plus installation/posture/runtime checks),
`tests/test_zh_mirror.py` (exit 0, 31/31), and `git diff --check` (exit 0).
The primary inspected all new runtime and fixture code, the verifier changes,
operations in both languages, and all template posture variants; deterministic
checks prove canonical byte equality and identity outside the sections. The three
required negative posture fixtures and malformed context/output/dial/tool cases
fail for the intended requirements. Unsupported rollback, concurrent unfinished
calls and unqualified content fail explicitly. Windows live behavior was not
exercised and is outside this ticket's authorized live scope.

Every product temporary native directory was absent after its call. After the
batch, the primary found no process tied to either disposable root and deleted
both `/home/hyy/ca-consult-product-u9awq0t2` and
`/home/hyy/ca-tier-routes-rcwpu1wb`, their pointers, credentials, sessions, traces,
logs, workspaces, schemas, and fixtures. No real-home installation, trust edit,
commit, push, or release occurred. Ticket 04 satisfies AC-3/AC-4, consultation
AC-10, EN-5 and its AC-11 scope. The earlier in-progress paragraphs are dated
execution history; this paragraph is the current acceptance state.

## 05 Plugin hooks

Status: retained AC-8 and dispatch AC-10 behavior passed on 2026-09-26,
with deterministic, bypassed live, and user-trusted product checks. A later
cross-platform launcher change passes current deterministic and bypassed checks;
the user waived renewed manual trust execution of the changed definition (D49),
which remains explicitly unverified. After an
earlier deferral, the user explicitly cancelled AC-9 automatic finish blocking,
authorized ticket 06 and fresh Astra xhigh final acceptance, and authorized
commit/push plus WSL/Windows updates after acceptance. Scope changes are D47 in
the decision ledger. Only successful consultation counts; failures remain pending
until success or user release, without a stop hook. A subsequent user instruction
narrows delivery to a local commit only (D48): no push or real installation update.
Temporary-environment cleanup is complete; the final section records its scope.

### Native file-effect and dispatch probe

The primary re-fetched https://learn.chatgpt.com/docs/hooks on 2026-09-26 and
ran a temporary-home hook fixture on Codex 0.157.0, using the O4-authorized
trust bypass. The current checkout was installed via X-2 and the cached companion
installer. The fixture only records temporary test inputs; it is not product code.
Parent `01a0da1f-54a7-73b0-8d86-490047e7c0c2` spawned
`ca_worker_crux_h` child `01a0da1f-7756-7960-8e93-43798cc9d525` with explicit
`low` effort. The CLI completed with exit 0.

- Shell Python `Path.write_text` created `shell-write.txt`. Its `PostToolUse`
  input had `tool_name=Bash` and the command; `tool_response` was an empty string.
  It contained no changed-file or per-process write attribution.
- `apply_patch` created `patch-write.txt`; the response explicitly named the
  successful added file. The following read-only `cat` command returned file
  content, with no file-effect field either.
- The child rollout had `session_meta`, `event_msg`, `response_item`,
  `world_state`, `turn_context`, `inter_agent_communication_metadata`, and
  `token_usage_record`. Event subtypes were only `task_started`, `item_completed`,
  `token_count`, `task_complete`; no patch/file-write event existed in this sample.
- Spawn `PostToolUse` input includes role, task name and effort. Its response is
  a JSON string containing the canonical task path. `SubagentStart` then gives
  child UUID, role, model, child transcript path and parent session UUID. Worker
  tool hooks also carry child `agent_id`/`agent_type`. The first stop reported
  `stop_hook_active=false`.

The exact AC-9 condition cannot be established from the exercised shell hook
output alone. Command text/exit status is not a file-effect record; workspace
snapshots can attribute another worker's changes to a read-only worker. This is
not S5: the host's ability to block a stop remains proven. It is S8 if the product
must narrow the meaning of changed files or introduce a new execution restriction.
Unexercised OS-level tracing and arbitrary MCP editing paths are not claimed
impossible; no qualified general attribution mechanism has been established.

A fresh read-only decision Advisor, `01a0da1d-f1bc-7712-bfcf-b4bf81c75699`, ran as
installed `ca_advisor_standard`, actual `gpt-6-astra[medium]`, parent
`01a0d989-47e5-7562-9ba3-373aef463838`; role-aware inspector exited 0.
Observed permissions were `danger-full-access` / `disabled`; its activity was
read-only. It recommended continuing AC-8/AC-10, using the proven parent/path/child
join, and returning the exact AC-9 gap to the user rather than inventing a write
heuristic. The primary adopted that advice and asked whether to retain AC-9 pending
or explicitly limit enforcement to provable changes. The user chose to retain
the exact condition and defer AC-9. No command heuristic, shared-workspace
snapshot rule, or reduced enforcement scope was adopted.

A further startup-timing probe, parent
`01a0da24-6ca3-7400-98f2-bba08e7db4af`, read the transcript's first header from
inside the actual `SessionStart` callback. It existed, matched the session UUID,
and had `source=exec`, `thread_source=user`, with no parent or agent role. This
supports identity validation before injection; it does not prove every future
host timing shape. The bypassed CLI returned its marker and exited 0.

Implementation worker `01a0da22-5064-7eb2-9aa7-50dd7823537f` is the installed
`ca_worker_standard_h`, actual `gpt-6-astra[low]`, parent
`01a0d989-47e5-7562-9ba3-373aef463838`, role-aware inspector exit 0. Its packet
owns AC-8 and dispatch AC-10 only and forbids live model calls, credential reads,
real installation, trust changes, and further delegation. Actual permissions are
`danger-full-access` / `disabled`; the primary retains live verification.

- Product live results and the outstanding user-trusted run appear below.
- AC-11 hook write-site review found no writes; temporary test-home cleanup
  remains pending until the user-trusted run completes.

### AC-8 and native-dispatch AC-10 implementation batch

The scoped worker implemented these two paths on 2026-09-26. This is partial
ticket 05 delivery: AC-9 and whole-ticket acceptance remain pending. It did not
run real model calls, install the plugin, modify trust, or read live homes.

- `hooks/hooks.json` uses the host's default plugin location and invokes
  `scripts/advisor-hooks.py` on `SessionStart` and native spawn `PostToolUse`.
  No manifest override, primary `Stop`, or `SubagentStop` hook was added.
- Session startup validates the supplied transcript header, excludes delegate
  identities, and emits byte-equal canonical posture and adoption blocks. The
  routing profile currently has one exact advisor model across all dials; the
  hook verifies that fact instead of guessing absent startup effort. Multiple
  advisor models or missing identity/model/canonical evidence produce pending.
- Dispatch verification reads expected model and pinned effort from the shipped
  template; absent a pin, explicit spawn effort is required. Pins override spawn
  effort. It joins the native response string's task path with parent identity and
  exactly one child header. Child root session, parent, role, nested source identity,
  model and effort must agree. A two-second bounded retry permits delayed child
  header/turn visibility. Missing, ambiguous or contradictory evidence remains
  pending; matching dispatches are silent. No manual inspector invocation is used.
- AC-11 write-site audit: the product hook has no write site. It only reads host
  transcripts, profile, posture and templates, and emits its result on stdout.
  Both the manifest's `python3 -B` and the script's bytecode setting prevent cache
  writes. There are no session counters, retained observations or cleanup state.
  Fixture writers exist only in `verify-hooks.py` and use an automatically removed
  temporary directory. No trust detection or trust mutation is present.
- The worker read the official [Hooks documentation](https://learn.chatgpt.com/docs/hooks)
  fetched by the primary on 2026-09-26 at
  `/home/hyy/ca-hooks-docs-blutphfr/hooks.txt`: plugin default location and
  `PLUGIN_ROOT`, common transcript fields, `SessionStart`, `PostToolUse`, JSON
  `additionalContext`, and the trust gate. Native field shapes follow the primary's
  P5 and section 05 probes; transcript format remains a requalification boundary.

Worker checks, all exit 0:

- `sh plugins/codex-advisor/scripts/verify.sh`: installation and inspector groups,
  50 consultation cases, and the new hooks group passed. Full output:
  `/tmp/codex-advisor-ticket05-verify.log` (temporary executor evidence).
- The hooks group exercises the actual manifest commands with pinned JSON inputs:
  exact full/reduced/adoption output for the requested primary models; startup,
  resume, compact and clear; delegate exclusion; all thirteen entry matches;
  pinned-effort precedence; wrong actual model/effort; missing caller effort;
  native string response/path/header join; delayed evidence; missing, duplicate,
  conflicting and malformed evidence. Every pending case also fails its assertion
  with the command disabled. Profile ambiguity and missing canonical text are
  tested in a disposable plugin fixture. AC-9 cases are deliberately not run.
- `python3 tests/test_zh_mirror.py`: 31/31 passed. Runtime operations and its
  Chinese twin document hooks, trust, bounded evidence handling and `--hooks`.
- `git diff --check`: passed. The worker inspected the actual scoped diff and
  all four new files, retaining the prior tickets' changes in shared files.

Executable bytes frozen for primary live verification:

- `hooks/hooks.json`: SHA-256 `79ee4ecd5ef668687f5f2d4dfe75ad4669cfb66bfa9db7f6fe56cc6e6f233f3b`.
- `scripts/advisor-hooks.py`: SHA-256 `d31c9bebc5011d39c77fdb09ffabd622469ca446fa801913fb9bb9bd05fc6ec4`.

Live hook trust, startup/resume delivery and actual native dispatch remain the
primary's checks. Deterministic fixtures do not establish those host behaviors.

### Primary live verification of the frozen hooks

The primary checked the installed product on Codex 0.157.0 on 2026-09-26.
The disposable home is `/home/hyy/ca-hooks-product-amsg5f8z/home`; installation
used X-2 and the cached companion installer. The recorder fixture's `hooks.json`
was removed before these runs. Installed and checkout hook/script hashes equal
the frozen hashes above. No shipped installed template was hand-edited.

| Case | Trust | Thread | Actual request evidence and result |
|---|---|---|---|
| Astra startup | O4 temporary bypass | `01a0da29-b782-79e0-b74e-5cc82c80a78c` | Astra xhigh; one byte-equal reduced block and one adoption block in developer input; full absent. Exit 0. |
| Sol startup | O4 temporary bypass | `01a0da29-b790-7d13-bcb7-e6229b129270` | Sol high; one byte-equal full block and one adoption block in developer input; reduced absent. Exit 0. |
| Astra resume | O4 temporary bypass | Same Astra thread, new turn `01a0da2a-53a9-7f51-8f36-a85024b2e11c` | Actual request has the original injection at item 6 and a new, byte-equal reduced/adoption developer item at item 10 after the prior answer. Exit 0; this is fresh injection, not only retained context. |
| Matching dispatch | O4 temporary bypass | Parent `01a0da2a-5304-7421-bfa5-6c1a245dc593`; child `01a0da2a-6a2b-7e82-853d-49cd71e136eb` | `ca_worker_crux_h`, explicit low, actual Astra low. No pending warning in subsequent parent requests. Child has its template posture only. Exit 0. |
| Missing caller effort | O4 temporary bypass | Parent `01a0da2b-14c5-78a0-a515-4ca4bf5352a7`; child `01a0da2b-288b-72a0-a67a-a78b91df49e3` | Caller omitted effort. Before any manual inspector, the next parent request contains developer text: `Codex Advisor: affected work remains pending. A caller-effort entry was spawned without reasoning_effort.` Parent reports it. Exit 0. |
| Untrusted product hooks | Untrusted; no bypass | Interactive PTY 60038 | Startup displayed `Hooks need review`, two new/changed hooks. Primary selected `Continue without trusting`. `/hooks` displayed `2 hooks need review before they can run`: SessionStart and PostToolUse each installed 1, active 0, review 1. Primary exited with `/quit`, exit 0, without granting trust. |
| User-trusted product hooks | User trusted both hooks in the host startup review; no bypass | `01a0da34-43b2-7d10-9ecd-e20e6f201b34` | Astra low; actual developer input contains exactly one byte-equal reduced block and one adoption block, no full block. Exit 0, `POSTURE_RECEIVED`. |

The primary inspected actual `inference_started` request payloads under
`evidence/{posture-astra,posture-sol,posture-resume,route-match,route-missing}-trace/`
in the disposable root, rather than relying on model acknowledgments. Subsequent
role-aware inspectors for both children exited 0, with parent/path association
matching the table. The missing-effort child's actual inherited low setting does
not discharge the explicit caller-effort requirement. Both children observed
`danger-full-access` / `disabled`; these bounded checks are not isolation proof.

The primary read the final hooks operations text and Chinese twin, the verifier
integration, and the implementation/test files. The worker's full verifier,
31/31 mirror check, and diff check remain applicable because executable bytes
have not changed. Hook write-site review finds no product state to retain at
session end. Temporary test homes and their evidence remain until the required
user-trusted run is verified, then must be removed. Terra, compact and clear
injection are covered by deterministic fixtures, not claimed as live runs here.
All AC-9 blocking scenarios remain unimplemented and untested by user decision.

The user's `trust-check.sh` recording shows the correct temporary home, the
host's two-hook review, selection of `Trust all and continue`, and exit 0 at
2026-09-26 04:12:27 +08:00. The subsequent primary check invoked `codex exec`
without `--dangerously-bypass-hook-trust`; its actual request trace establishes
injection independently of the user's report and the model's acknowledgment.
The interactive host presented the trust action at startup, as in ticket 01;
the earlier untrusted `/hooks` inspection identified the same two product hooks.

The user subsequently authorized commits, pushes, and updates on WSL and Windows
after completion. That authorization is recorded and must not be requested again.
After the user asked what the worker stop hook means, the primary explained all
three proposed hook responsibilities. The user explicitly selected cancellation
of automatic worker finish blocking, continuation to 06, fresh Astra xhigh final
acceptance, then commit/push and WSL/Windows updates. This is an explicit scope
change, not an inferred waiver. No real-installation hook trust was granted by
that release instruction; the product still requires host review in each real home.

Read-only continuation advice ran in fresh thread
`01a0da34-06d6-7253-ab23-2599524dc59e`, installed `ca_advisor_standard`, actual
Astra medium, inspector exit 0. It confirmed that the earlier general continuation
instruction alone did not remove the explicit dependency or final-review gate.
Its advice is not authorization or final acceptance. Standards/spec pre-review
threads are `01a0da35-b74d-7cf2-ad3b-9883af800993` and
`01a0da36-0849-79a1-982e-574b731281f5`, each fresh `ca_advisor_light`, actual
Astra low, inspector exit 0. All three observed `danger-full-access` / `disabled`;
their packets prohibit edits and live model calls. Pre-review does not replace
the final Astra xhigh acceptance required by the spec.

### Cross-platform startup and cleanup verification

Standards pre-review identified ignored Windows `taskkill` failures. The same
ticket 04 worker corrected the native process lifecycle using Windows Job Objects:
a one-byte, unbuffered startup gate prevents native descendants starting before
containment; termination requires successful native APIs and zero active job
processes. Failed cleanup produces an explicit error and retains an earlier
failure code in its diagnostic. Codex resolves to a native executable, either
on PATH or uniquely inside the qualified official npm package layout; `.cmd`
wrappers are not executed with configuration arguments. Runtime file reads use
UTF-8 explicitly. The primary inspected the changed implementation and boundary
tests. The long reconstruction function noted as a nonblocking style concern
was left unchanged because it did not establish a correctness defect.

Worker checks: POSIX consultation group discovered 61 cases, passed 53 and
explicitly skipped eight Windows-only cases; Windows Python 3.12.4, with
`PYTHONUTF8` unset, passed all 61. Evidence was captured in
`/tmp/ca04-cleanup-final-{posix,windows}.log`. Windows cases use real Kernel32
APIs with a synthetic native executable, covering normal completion, cancellation,
orphan descendants holding stdio, six API failures, cancellation plus failed
cleanup, UTF-8 content, and native npm executable lookup. They are not a claim
of authenticated Windows model execution.

The primary found Windows `python3` to be a nonworking WindowsApps alias
(exit 9009), while `python` resolves to Python 3.12.4. The shared POSIX launcher
selects a working Python >=3.11 from `python3`, `python`, or `py -3`; it sets UTF-8
stdio, disables bytecode writes, and fails explicitly if none qualifies. MCP,
hooks, and verifier use it. Its negative tests check a failing preferred
interpreter, preserved arguments/stdin, and total interpreter unavailability.
Hook reads also use explicit UTF-8. This changes hook definitions and therefore
requires renewed user review when installed; no trust record was changed by the agent.

Primary Windows checks in temporary `ca-hooks-win-ps4wyrza` passed exact
full/adoption output from the shipped hook command and MCP initialize/tools-list
through the shipped launcher, using Git Bash and no `PYTHONUTF8`. They did not
read credentials or call a model. The current checkout was reinstalled through
X-2 as 0.3.0 in the existing WSL temporary home. A current real consultation,
caller `01a0da4b-c156-75f3-a8a8-a094faad1812`, advisor
`01a0da4b-e942-7ac3-a5c7-d5e546fd6d92`, returned a structured successful plan
with `CONSULT_CURRENT_49357` and matching Astra low expected/actual settings.
The primary inspected the actual tool result. This check used O4's temporary
bypass; it does not replace renewed user-trusted execution of the new definition.

On 2026-09-26 the user explicitly declined repeating the manual trust test (D49).
That repetition is waived and no longer blocks delivery. Manual trust execution
of the final launcher definition remains unverified. Earlier user-trusted runs
and the untrusted warning/skip remain scoped to their recorded definitions.
Installation/update instructions still require `/hooks`; no trust bypass ships.

## 06 README, manifest, version manual, release preparation

Status: implemented and primary-verified on 2026-09-26 under D47/D48; final
independent acceptance remains separate. Host thread capacity prevented a new
worker dispatch, so the primary implemented this ticket directly, as X-2 allows.

README documents the thirteen entries without dial values, admission and
recovery, consultation/posture/adoption, the two hooks, acceptance, updates and
the eleven retired 0.2.0 names with replacements. Manifest version is 0.3.0;
descriptions and keywords describe current behavior without model names. The
marketplace manifest is unchanged. The Chinese manual covers the whole version
and its delta with ADR-0006 references. Cancelled stop enforcement is not presented
as a delivered feature or a deferred defect.

Baseline SHA-256 before and after:
`d89f0f18ccfc0cb42156a5548bc531527372603ea12efb13d759e86589b6d4ea`.
The primary read the shipped baseline source and opened its rendered hero before
writing. The final manual's CSS and JavaScript are byte-equal to the baseline.
All thirteen frozen entry/dial pairs were compared to the routing profile and
match, including every allowed effort and default. No magazine preview was used.

| Scene | Settings | Images | Primary visual observation | Result |
|---|---|---|---|---|
| V1 | 1440x900, light, hero | `visual/V1-baseline.png`, `visual/V1-0.3.0.png` | Same rail, grid, typography, palette, map, actions and fact strip; version and prose differ. | Pass |
| V2 | 1440x900, light, entries | `visual/V2-baseline.png`, `visual/V2-0.3.0.png` | Same section/table/cell styling and spacing; thirteen names and revised dial contents fit. | Pass |
| V3 | 1440x900, light, delta | `visual/V3-baseline.png`, `visual/V3-0.3.0.png` | Same accent border, heading and change-list styles; new content reuses existing cards and table components. | Pass |
| V4 | 390x844, light, hero | `visual/V4-baseline.png`, `visual/V4-0.3.0.png` | Same sticky compact rail, horizontal navigation, single-column hero and mobile type; no page overflow. | Pass |
| V5 | 1440x900, dark, hero | `visual/V5-baseline.png`, `visual/V5-0.3.0.png` | Same dark palette, map/card contrast, controls and grid. | Pass |

All five pairs were opened and inspected. Playwright with cached Chromium 1243
rendered each version in an isolated context at identical settings. All ten
scenes had zero page errors, zero external requests, valid fragment links and
no document-width overflow; `visual/checks.json` records the scoped checks.
The manual test passed 3/3 and the mirror test 31/31; `git diff --check` passed.

Release commands are preparation only. Under the latest D48 instruction they
are **not authorized to execute**: push, marketplace upgrades, reinstalls and
real-home installer runs remain unperformed. After a future release authorization:

```sh
git push origin main
# Then run on each installation using its native Codex and home:
codex plugin marketplace upgrade codex-advisor
codex plugin remove codex-advisor@codex-advisor
codex plugin add codex-advisor@codex-advisor
plugin_dir="$(codex plugin list --json | jq -r '.installed[] | select(.pluginId == "codex-advisor@codex-advisor") | .source.path')"
sh "$plugin_dir/scripts/install-agents.sh"
sh "$plugin_dir/scripts/install-agents.sh" --check
```

Open a fresh interactive session on each side and review changed hooks in
`/hooks`. Windows shell commands require Git Bash and a Windows home, without
inheriting a WSL-only `CODEX_HOME`. A local commit is authorized after acceptance.

## Final acceptance

Status: accepted by the primary on 2026-09-26 after primary checks and fresh
independent senior acceptance. D47 cancels AC-9; D49 waives only the repeated
manual trust check. Delivery is a local commit only under D48.

### Primary verification

The primary ran unqualified `sh plugins/codex-advisor/scripts/verify.sh` (exit 0,
`/tmp/ca03-final-verify.log`), including installation, runtime, consultation and
hooks. Consultation discovered 61 cases: 53 passed, eight Windows-only cases
were explicitly skipped. The separate Windows run passed all 61 cases, as scoped
above. The primary inspected its output and all added Windows failure assertions.
After the final operations-document clarification, mirror checks passed 31/31,
manual checks passed 3/3, and `git diff --check` exited 0. No runtime code changed
after the complete verifier run. This repository has no application typecheck.

### Requirement sweep

| IDs | Evidence and outcome |
|---|---|
| TR-1, TR-4, TR-5, TR-6, TR-7, TR-8 | Section 02 doctrine inspection: tier names, candidate order, broad admission, reserved narrow admission, upward floor and complete-failure definition. |
| TR-2, TR-3, TR-9 | Section 03 profile/template comparisons and 13/13 native routes; profile records generation-bound assumptions. |
| AC-1, AC-2 | Section 02 skill and acceptance packet retain independent review and tier/primary dial selection. This delivery's separately authorized fresh senior review remains below. |
| AC-3, AC-4 | Sections 01/P6 and 04: zero-argument boundary, effective history including compaction/current turn/earliest items, actual empty request tools, dial assertions, all three caller roles and explicit failures; current consultation recheck above. |
| AC-5, AC-6, AC-7 | Sections 02/04: canonical full/reduced/adoption blocks, exact identity selection, byte equality and negative fixtures. |
| AC-8 | Section 05 actual startup/resume requests, delegate exclusion and exact canonical output. |
| AC-9 | Cancelled by D47; no finish-blocking hook ships. |
| AC-10 | Sections 04/05: native spawn automatic match/missing-effort evidence and consultation actual-request checks. |
| AC-11 | Write-site audit below and deterministic cleanup/negative cases; no hook write sites. |
| AC-12 | Sections 01/P7 and 05 trusted/untrusted evidence; final-definition manual repetition explicitly waived by D49. README, operations and manual preserve the trust gate. |
| EN-1, EN-2, EN-3, EN-4 | Section 03: thirteen entries, nineteen retire names, upgrade/refusal/check behavior, unchanged inspector interface and table-driven checks. |
| EN-5, EN-6 | Sections 03/04/05 canonical byte comparisons, same-role invariance, no advisor posture, delegate hook exclusion; mirror 31/31. |
| DR-1, DR-3, DR-4, DR-6, DR-7 | Section 02 source inspection, canonical blocks, packets, glossary and explicit ADR supersessions; grok lane is 0.4.0. |
| DR-2 | Section 03 profile and template checks; dial values remain in the profile and allowed templates/frozen manual. |
| DR-5 | Sections 02–05 operations sections and twins; current Windows prerequisite/cleanup behavior documented. |
| DR-8, DR-9, DR-10, DR-11 | Section 06 README, 0.3.0 manifest, unchanged marketplace, five inspected visual pairs, unchanged baseline and prepared-only release commands. |
| X-1, X-2 | D48 permits only a local commit; temporary installations used the prescribed route; task executed with installed 0.2.0 entries. |
| X-3, X-4, X-5 | Cross-component write-site/temporary-state audit below, mirrors, and final obsolete-text search; no unrelated cleanup. |

### Write sites and goal-drift checks

The hooks read input/profile/session evidence and emit stdout; they create no
files. Consultation disables bytecode, writes its model catalog only under a
`TemporaryDirectory`, routes native logs/SQLite/request traces to that directory,
starts an ephemeral thread, and terminates its processes before directory cleanup.
It reads the caller rollout and public profile; it does not read credentials.
Normal host initialization remains a documented prerequisite. The deterministic
tests exercise cleanup, cancellation, explicit API failures and isolation.

Each goal-drift item was checked against its owning evidence:

1. Actual consultation model/effort are verified from every recorded request.
2. Zero arguments and effective-history reconstruction exclude caller summaries and include the unfinished turn.
3. Actual request tool inventories are empty; read-only tools do not qualify.
4. Session injection equals one canonical variant plus adoption; exact model identity selects it, including the unknown-model fixture.
5. Neither primary `Stop` nor worker `SubagentStop` is registered.
6. Template posture equality and no self-model inference pass installation checks.
7. The active profile contains only the declared sixth-generation models.
8. Broad `crux` admission is active; narrow admission remains reserved; first-round `rescue` needs the user.
9. The ladder retains next-tier, model-level and same-model effort floors.
10. Consultation is distinct from independent acceptance; this delivery passed its separate fresh review below.
11. Runtime temporary state is scoped and cleaned; repository acceptance records are task evidence, not product observation machinery.
12. All five manual comparison pairs were opened, and the baseline hash is unchanged.
13. Installer tests and the live upgrade fixture remove all eleven retired 0.2.0 names.
14. Earliest-effective-context and compaction/live nonce cases cover more than a recent-turn window.
15. Empty tools are established from actual request traces, not model self-report.
16. Install/update/release instructions retain `/hooks`; earlier trusted/untrusted runs are recorded; only final-definition repetition is waived.
17. Failure outcomes contain no advice and do not satisfy consultation success.

The final X-5 search used
`rg -n 'ca_(explorer|worker|advisor)_(light|standard(_[mh])?|senior)|first-round pool|senior gate|decision packet|\b(light|standard|senior)\b' plugins/codex-advisor docs/zh README.md -g '!retire.txt' -g '!*.pyc'`.
It returned only README upgrade lines 183–197; no forbidden active-runtime or
mirror occurrence remained. Ledger rejected items D11/D12/D15/D23/D30/D35/D39/D40
were compared to the ladder, acceptance, adoption, hooks and profile: none is
reintroduced. Historical explanations and explicit prohibitions remain allowed.

### Independent acceptance and final disposition

The user explicitly authorized the installed 0.2.0 `ca_advisor_senior` entry at
`gpt-6-astra[xhigh]`. Native `spawn_agent` used `fork_turns=none` and created
`/root/final_senior_acceptance`, thread
`01a0da57-35c6-7e03-965e-ffd6c8cb9fd3`. The installed inspector exited 0 and
confirmed the entry, exact model/effort, parent
`01a0d989-47e5-7562-9ba3-373aef463838`, and this repository working directory.
The observed permission profile was `disabled` / `danger-full-access`; the
read-only packet and unchanged state are evidence of conduct, not enforced isolation.

The fresh reviewer returned **ready, high confidence**, with no material findings.
It inspected the complete tracked diff, new files, all runtime implementation and
boundary tests, both platform logs, translated entries, ADR/decision consistency,
the full manual, and all ten saved screenshots. Its own read-only checks covered
Python syntax, thirteen entry/twin configurations, the unchanged manual baseline,
and `git diff --check` (exit 0). It did not repeat model calls. The primary
confirmed actual tool activity and matching before/after hashes for all 76 scoped
product/document files. Snapshot SHA-256 was
`201b744e713baa0d6772cc703c36bde9e402b2b1ae1fd2773e4518bf6ff54e65`.
Only task status and acceptance records changed after this review.

The primary accepts the retained scope. Residual evidence limits: final-definition
manual trust execution is waived, not proven; Windows authenticated model
consultation was not exercised; prior raw live traces were intentionally cleaned,
so the review used the retained observations; host compatibility is scoped to the
qualified Codex 0.157.0 paths. No push or real installation update was performed.

### Cleanup and local delivery

The primary stopped and verified exit of the two daemon processes whose command
paths belonged to the temporary product home. It then removed and verified absence
of `ca-hooks-product-amsg5f8z` (including credential copies, caches, sessions and
traces), `ca-hooks-docs-blutphfr`, Windows `ca-hooks-win-ps4wyrza`,
`ca-manual-verify-ru_i1erh`, `ca04-baseline-aa25432t`, and 23 task-specific
temporary logs, pointers and the review hash snapshot. Earlier probe environments
were already removed at their recorded checkpoints. No matching temporary process
remained. Repository task records and visual evidence remain as delivery evidence;
the pre-existing `.agent-discuss/` and real installations remain outside the change.

The commit includes this task's product, documentation and acceptance evidence.
Release commands above remain preparation only. The local commit identifier is
reported by the primary after Git creates it.
