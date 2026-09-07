# Luna Explorer acceptance

Date: 2026-09-07. Implementation base: `113d5919b9c257060fbc43d869bed226a6e7c54b`.
Scope: native Explorer availability, caller-selected effort, skill default selection,
installation, and runtime evidence validation.

## Deterministic verification

The installation test first failed because the expected Explorer template was absent.
It passed after adding the role and installer support. The runtime test then failed
because `--explorer-effort` was unknown, and passed after adding the inspector option.
Both changes were tested through the existing public script interfaces.

The complete `sh plugins/codex-advisor/scripts/verify.sh` suite passed. It covers
all five role templates, installation and selective checks, refusal before partial
writes, preservation, expected model and effort, missing or conflicting permissions,
and restricted diagnostic output. Existing Luna Implementer max checks remain passing.
Plugin validation, skill validation, and whitespace checks passed. Shell syntax and
JSON/TOML parsing are the applicable static checks; this project has no typed application.

## Live verification

Codex CLI `0.153.4` ran in temporary installed homes and disposable workspaces under
`/tmp/codex-advisor-explorer.nPfxol`. Each home used the public marketplace/plugin
installation commands and companion role installer before new tasks. The user's
active installation and primary configuration were not changed. Temporary authentication
copies were removed after the calls. Scenario prompts, events, final responses,
workspace hashes, native rollouts, and projected observations remain under that root.

The fixture contains three source files. `api.preview` delegates to `receipt_total`,
which computes `taxable_total(amount) + fee`; `taxable_total` multiplies by `1.2`.
The independent expected answer is that the fee is not taxed and inputs `10, 3`
produce `15`. Source locations and reported tool activity were inspected directly.

| Scenario | Observed result | Primary / child thread |
|---|---|---|
| Astra outside skill, explicit medium | Native Luna Explorer at medium; fresh context; correct source explanation; no scoped mutations. | `01a07b33-06fc-77c0-9582-ae6b4050a47b` / `01a07b33-2a64-7452-9dff-a1e68901195d` |
| Sol outside skill, description-based selection | Sol selected the native Luna Explorer at low with fresh context. Final citation-check run returned correct per-file references and no scoped mutations. | `01a07b3a-00a2-7112-9441-4f05ba878869` / `01a07b3a-2b0f-7213-bbf2-975bc932574e` |
| Sol applying orchestration, default exploration selection | Skill selected the native Luna Explorer at medium; exact inspector validation passed; correct source explanation; no scoped mutations. | `01a07b35-dfba-7410-80b9-252e1c8d0d34` / `01a07b36-657e-7c31-b9f5-942c445fae38` |
| Luna outside skill, explicit native role | Luna primary called the native Luna Explorer at medium with fresh context; correct source references and result; no scoped mutations. | `01a07b38-3791-79a1-a11c-e92601699d25` / `01a07b38-69dd-7670-ae16-1bde79703297` |
| Explorer missing from isolated installation | Sol observed the missing selective role check, investigated directly, and returned the correct result. No child or expensive substitute was launched; no scoped mutations. | `01a07b38-b3bb-76f3-90f5-10ff698397ad` / none |

For every successful native-role scenario above, the narrow inspector passed for
the exact child UUID, `codex_advisor_luna_explorer`, `gpt-5.6-luna`, and requested
effort. Parent linkage and fresh-context spawn arguments were inspected separately.
Parent sessions retained their selected model and low effort. Child activity used
source reads and, in some cases, bytecode-disabled fixture evaluation; no child
delegated further. Actual permissions were `workspace-write` / `managed`, despite
the template's read-only request. These checks establish observed read-only behavior
within the fixture, not enforced isolation.

The final role differs from the earlier medium-call template only in more explicit
fresh-context discovery wording and per-file citation validation. The final template
was reinstalled and the affected low-effort selection/citation scenario rerun. Existing
medium-call evidence establishes the unchanged model and effort configuration.

## Evidence limits

- An initial Sol call selected the new role but used full-history inheritance. Its
  rollout included parent metadata, and the inspector correctly refused certification.
  The role description now gives the exact fresh-context argument; subsequent Sol
  calls used it and passed. No parser relaxation was introduced.
- One earlier low-effort report used cumulative line numbers from a multi-file read.
  The role now explicitly checks citations against each individual file. The final
  low-effort report matched the fixture. This is a sampled quality check, not a
  guarantee that every future model response contains accurate citations.
- In an unrestricted role-selection scenario, a Luna primary chose the built-in
  `explorer` instead of the plugin role. That built-in call created bytecode caches
  and is not counted as plugin read-only acceptance. The explicit plugin-role case
  passed. Outside-skill selection is optional, not a deterministic global default.
- Some outside-skill parents reported the canonical task path instead of the UUID;
  authoritative native records supplied the UUIDs above. Parent prose alone was not
  used as model or permission evidence.
- The missing-role scenario does not test a provider outage. Astra, Sol, and Luna
  are representative callers; other host-supported primaries and all possible prompts
  were not exhaustively exercised. No primary-model whitelist exists in the role.
- Low and medium were observed live. Other inspector-recognized effort strings have
  parser coverage only; they are not asserted to be supported by Luna or the account.
- No quantified quota savings, global routing guarantee, or hard read-only isolation
  claim is made. Recheck discovery, override behavior, and permission handling after
  a host upgrade.

## Review

Independent Standards and Spec reviews inspected the staged changes against the
implementation base and reported zero findings in each axis. Final review includes
the citation instruction and this acceptance record. The feature specification,
existing glossary, and amended architecture decision accompany the implementation;
unrelated untracked planning and instruction files remain outside the commit.
