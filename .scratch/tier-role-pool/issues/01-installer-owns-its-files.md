# 01: Companion installer owns its files

**What to build:** After a plugin update the user runs the companion installer once and the installed entries equal the shipped templates: differing own files are overwritten, retired names are deleted, nothing else is touched, and `--check` reports drift and residue. The installer becomes manifest-driven so that later tickets only add or remove template files and retire names. This ticket still ships the current eight entries; the retire list starts empty.

**Blocked by:** None (can start immediately).

**Status:** resolved

- [x] The manifest is the set of TOML templates shipped beside the installer; no per-role case table names files. A selective check names a template by its filename stem minus the plugin prefix (today `codex-advisor-`, later `ca-`), and the prefix is one variable.
- [x] A missing or differing manifest destination is written and reported as installed; an identical one is reported as unchanged. No backup file is left and no old-versus-new judgment is made.
- [x] A retire list of exact filenames exists (empty in this ticket). A present retire file is deleted by filename without reading it and reported as removed.
- [x] Files outside the manifest and retire list, including upstream `sol-advisor-*` entries, unrelated agents, and the primary configuration, are never read or written; a snapshot before and after an install shows them byte-identical.
- [x] `--check` writes nothing and exits non-zero listing every differing or missing manifest file and every present retire file; it exits zero only when all manifest files match and no retire file exists.
- [x] Symlinked destinations or ancestors, non-regular destinations, non-directory ancestors, the filesystem root, and dot path segments are still refused before any write, with no partial mutation.
- [x] Writes are atomic per file (temporary file in the target directory, then rename) so an interrupted install never leaves a half-written entry.
- [x] A `.gitattributes` at the repository root pins LF for text files so a Windows checkout compares byte-identical to installed copies.
- [x] The installation group of the verifier is rewritten to the new semantics: overwrite reported, unchanged reported, retire removal, check failing on drift and on residue, preservation of unrelated files, every refusal without partial mutation, default `CODEX_HOME` and relative target behaviour. The case that an old Sol template blocks the upgrade is removed. The installation group passes; the runtime group is unchanged and still passes.
- [x] The installer's usage text and the operations reference sentences that describe refusal of modified destinations are not edited here; ticket 03 rewrites the reference, and the usage text is updated to the new semantics in this ticket.

## Acceptance

Accepted 2026-09-16 by the primary. Lane: `generalPurpose` pinned `cursor-grok-4.6-xhigh` (requested, not confirmed). Tier 1: `sh plugins/codex-advisor/scripts/verify.sh` rerun by the primary, both groups pass; `git diff --stat` limited to `install-agents.sh` (150), `verify.sh` (188), new `.gitattributes` and `agents/retire.txt`. Tier 2: the primary read the installer in full — manifest is the `agents/*.toml` glob, retire list is `agents/retire.txt` (comments and blank lines skipped, names with `/` or `..` rejected), writes are `mktemp` + `mv -f`, retire removal accepts regular files and symlinks and refuses other non-regular entries, `--check-role` skips residue and says so in usage. Negative proof recorded by the lane: skipping the overwrite fails the installation group at the `INSTALLED` assertion.
