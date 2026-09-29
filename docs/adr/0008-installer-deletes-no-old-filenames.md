---
status: accepted
---

# The installer deletes no old entry filenames

## Decision

The companion installer overwrites this plugin's own files when they differ,
touches nothing else, and deletes no old filename. Its check mode reports only
missing and differing templates. The plugin ships no retire list. The installer
still refuses symlinked, non-regular, root, and dot-segment destinations.

The eleven `0.2.0` entry files on this machine's WSL and Windows sides are
removed once by hand, on each side after the new entries are installed there.
That step is recorded in the release's task record, not in the installer or the
README.

## Basis

The plugin is deployed only on this machine's WSL and Windows sides. This is the
user's statement of 2026-09-29; we have not verified it independently. The facts
checked on 2026-09-29 agree with it: `origin/main` was `09c21c8` (plugin `0.2.0`)
and `0.3.0` had never been pushed; both sides' plugin caches held only `0.2.0`;
each side's `agents` directory held the eleven `0.2.0` entry files and no `0.1.x`
file; the public GitHub repository had 0 forks and 0 stars. A public repository
cannot rule out another install.

Under that premise, the retire list, its installer code, and its tests maintain a
migration for files that exist only on this machine, where one manual removal
does the same job. The ruling is recorded in
[A01 of the round-3 audit checklist](../../.scratch/instruction-audit/round-3-confirmation-checklist.md#a01本机旧版入口的一次性清理及仓库侧改动).

## Alternatives not adopted

- Ship `0.3.0` with the retire logic, let it clean up once, and remove the logic
  in the next release: one more release and deployment, of a version the same
  audit was still changing.

## Revisit when

- Another machine or user is found to have installed `0.1.x` or `0.2.0` before
  this release. That install keeps its old entry files, and nothing reports them.

## What this supersedes

The quotations below are every complete sentence in ADR-0004 and ADR-0006 whose
rule this decision replaces.

From ADR-0004:

> The companion installer owns this plugin's installed files: it overwrites the eleven shipped entries when they differ, deletes the eight retired filenames when present, touches nothing else, and fails its check mode on drift or residue.

ADR-0006 already replaced the entry counts and retire set in that sentence. This
decision replaces its two remaining retirement clauses: deleting retired
filenames, and failing the check mode on residue. Ownership, overwrite, touching
nothing else, and failing the check mode on drift stand; drift is a missing or
differing template.

> The fork specification's user story 39 and its installer decision (never overwrite a modified destination): the installer now overwrites this plugin's own files and deletes its retired names.

Only "and deletes its retired names" is replaced; overwriting this plugin's own
files stands.

From ADR-0006:

> The eleven 0.2.0 entries join the eight 0.1.0 entries in the retire set.
