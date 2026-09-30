---
status: accepted
---

# Windows launch through Git's sh

## Decision

The MCP server keeps `sh ./scripts/run-python.sh ./scripts/process-consultation.py`
as its launch command. Each hook in `hooks/hooks.json` adds `commandWindows`: its
`command` with `$PLUGIN_ROOT` written as `$env:PLUGIN_ROOT`. On Windows, Git for
Windows' `bin` directory, which holds `sh.exe`, must be on PATH; the user adds
`C:\Program Files\Git\bin` to the Windows user PATH once per machine. The plugin
ships no Windows launcher.

## Basis

On 2026-09-30, Codex on the user's Windows side warned at startup: "MCP client
for codex_advisor failed to start: MCP startup failed: program not found". Its
primary sessions had never received a consultation posture: their rollouts hold
no posture block, while WSL sessions whose hooks carry the same trust hashes do.

Codex CLI `0.159.2` source, tag `rust-v0.159.2`, read 2026-09-30:

- On Windows, a stdio MCP server's program is resolved with
  `which::which_in(program, PATH, cwd)`; a program that is not found there fails
  startup with "program not found". A relative `cwd` in a plugin's `.mcp.json`
  resolves against the plugin root.
- On Windows, hook commands run through the session shell: PowerShell with
  `-NoProfile -Command`, or `%COMSPEC% /C` when no PowerShell is found. A hook's
  `commandWindows`, alias `command_windows`, replaces `command` there.
- Plugin hooks receive `PLUGIN_ROOT`, `CLAUDE_PLUGIN_ROOT`, `PLUGIN_DATA`, and
  `CLAUDE_PLUGIN_DATA`. `PLUGIN_ROOT` is
  `<codex home>/plugins/cache/<marketplace>/<plugin>/<version>`. The Codex home
  is `~/.codex` as written when `CODEX_HOME` is unset, and its canonical `\\?\`
  form when `CODEX_HOME` is set.

The installed `0.159.2` binaries on the WSL and Windows sides both contain the
`commandWindows` key.

The Windows side on 2026-09-30: PATH held `C:\Program Files\Git\cmd`, which has
no `sh.exe`. `bash` resolved to `C:\Windows\System32\bash.exe`, the WSL launcher.
`python` resolved to Python 3.12.4 and `python3` to the Microsoft Store stub,
which `run-python.sh` skips. Neither the user nor the machine environment sets
`CODEX_HOME`; WSL passes it only to processes that WSL starts.

A command-layer emulation on that side on 2026-09-30 ran a fresh copy of the
plugin with the final `hooks.json`:

- With `C:\Program Files\Git\bin` on PATH, `sh` resolved to Git's `sh.exe`, and
  the MCP launch answered `initialize` and listed `process_consultation`, from a
  plain and from a `\\?\` working directory.
- `commandWindows` under PowerShell 7 and Windows PowerShell 5.1 returned the
  exact canonical posture for a `gpt-6.1-sol` and a `gpt-5.6-terra` session
  when `PLUGIN_ROOT` had the plain form.
- With a `\\?\` `PLUGIN_ROOT`, `sh` could not open the script.
- Under `cmd.exe`, `$env:PLUGIN_ROOT` stayed unexpanded and `sh` exited 127.
- Without Git's `bin` on PATH, neither PowerShell found `sh`, and the MCP launch
  had no `sh` to resolve.

The emulation reproduced the host's launch commands; it did not start Codex. The
installed host's hook and MCP runs on Windows are observed after the update.

## Alternatives not adopted

- Ship a Windows `.cmd` launcher and start the MCP server through it by relative
  path, leaving PATH alone: the interpreter selection in `run-python.sh` would be
  kept in two languages, and the relative-path launch would need requalification
  on both sides.
- Launch through `bash`: on a Windows machine with WSL, the `bash` on PATH is the
  WSL launcher and runs the command inside Linux.

## Revisit when

- A Codex update after `0.159.2` changes Windows hook execution, MCP program
  resolution, or the `commandWindows` field.
- A Windows side sets `CODEX_HOME`, which gives `PLUGIN_ROOT` the `\\?\` form.
- A Windows session still shows the MCP startup warning, or receives no posture,
  after the PATH change and the hook review in `/hooks`.
- Git for Windows no longer ships `sh.exe` in its `bin` directory.
