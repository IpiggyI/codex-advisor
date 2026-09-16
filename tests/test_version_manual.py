#!/usr/bin/env python3
"""Current plugin.json version has docs/releases/<version>.html only, with both required phrases."""
import json
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN_JSON = os.path.join(
    REPO_ROOT, "plugins", "codex-advisor", ".codex-plugin", "plugin.json"
)
RELEASES = os.path.join(REPO_ROOT, "docs", "releases")
PHRASES = ("本版说明", "相对上一版")


def main():
    with open(PLUGIN_JSON, encoding="utf-8") as fh:
        version = json.load(fh)["version"]
    html_path = os.path.join(RELEASES, "%s.html" % version)
    md_path = os.path.join(RELEASES, "%s.md" % version)
    html_rel = os.path.relpath(html_path, REPO_ROOT).replace(os.sep, "/")
    md_rel = os.path.relpath(md_path, REPO_ROOT).replace(os.sep, "/")
    failed = 0
    total = 3

    if os.path.isfile(md_path):
        print("FAIL  markdown twin must not exist: %s" % md_rel)
        failed += 1
    else:
        print("PASS  no markdown twin %s" % md_rel)

    if not os.path.isfile(html_path):
        print("FAIL  missing %s" % html_rel)
        failed += 1
        print("%d/%d passed, %d failed" % (total - failed, total, failed))
        return 1
    print("PASS  %s exists for plugin.json version %s" % (html_rel, version))

    with open(html_path, encoding="utf-8") as fh:
        text = fh.read()
    missing = [p for p in PHRASES if p not in text]
    if missing:
        print("FAIL  %s missing phrases: %s" % (html_rel, ", ".join(missing)))
        failed += 1
    else:
        print("PASS  %s has both required phrases" % html_rel)

    print("%d/%d passed, %d failed" % (total - failed, total, failed))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
