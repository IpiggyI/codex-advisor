#!/usr/bin/env python3
"""One-to-one existence: every plugins/codex-advisor **/*.md and **/*.toml
has a docs/zh/<same relative path> twin; TOML twins match selected keys."""
import os
import sys
import tomllib

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN = os.path.join(REPO_ROOT, "plugins", "codex-advisor")
ZH = os.path.join(REPO_ROOT, "docs", "zh")
CJK_START = 0x4E00
CJK_END = 0x9FFF
TOML_REQUIRED = ("name", "model")
TOML_OPTIONAL = ("model_reasoning_effort", "sandbox_mode")


def collect(root, suffix):
    rels = []
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            if name.endswith(suffix):
                full = os.path.join(dirpath, name)
                rel = os.path.relpath(full, root).replace(os.sep, "/")
                rels.append(rel)
    rels.sort()
    return rels


def has_cjk(text):
    return isinstance(text, str) and any(
        CJK_START <= ord(ch) <= CJK_END for ch in text
    )


def load_toml(path):
    with open(path, "rb") as fh:
        return tomllib.load(fh)


def main():
    passed = 0
    failed = 0

    plugin_md = collect(PLUGIN, ".md")
    zh_md = collect(ZH, ".md")
    plugin_md_set = set(plugin_md)
    zh_md_set = set(zh_md)

    for rel in plugin_md:
        twin = os.path.join(ZH, *rel.split("/"))
        if os.path.isfile(twin):
            print("PASS  plugins/codex-advisor/%s → docs/zh/%s" % (rel, rel))
            passed += 1
        else:
            print("FAIL  missing twin: docs/zh/%s" % rel)
            failed += 1

    for rel in sorted(zh_md_set - plugin_md_set):
        print("FAIL  orphan twin: docs/zh/%s" % rel)
        failed += 1

    plugin_toml = collect(PLUGIN, ".toml")
    zh_toml = collect(ZH, ".toml")
    plugin_toml_set = set(plugin_toml)
    zh_toml_set = set(zh_toml)

    for rel in plugin_toml:
        twin = os.path.join(ZH, *rel.split("/"))
        if os.path.isfile(twin):
            print("PASS  plugins/codex-advisor/%s → docs/zh/%s" % (rel, rel))
            passed += 1
        else:
            print("FAIL  missing twin: docs/zh/%s" % rel)
            failed += 1

    for rel in sorted(zh_toml_set - plugin_toml_set):
        print("FAIL  orphan twin: docs/zh/%s" % rel)
        failed += 1

    for rel in sorted(plugin_toml_set & zh_toml_set):
        src = os.path.join(PLUGIN, *rel.split("/"))
        twin = os.path.join(ZH, *rel.split("/"))
        src_data = load_toml(src)
        twin_data = load_toml(twin)
        mismatch = None
        for key in TOML_REQUIRED:
            if src_data.get(key) != twin_data.get(key):
                mismatch = key
                break
        if mismatch is None:
            for key in TOML_OPTIONAL:
                if (key in src_data) != (key in twin_data) or src_data.get(
                    key
                ) != twin_data.get(key):
                    mismatch = key
                    break
        if mismatch is not None:
            print("FAIL  toml key mismatch (%s): docs/zh/%s" % (mismatch, rel))
            failed += 1
            continue
        desc = twin_data.get("description", "")
        inst = twin_data.get("developer_instructions", "")
        if not has_cjk(desc):
            print("FAIL  missing CJK in description: docs/zh/%s" % rel)
            failed += 1
            continue
        if not has_cjk(inst):
            print("FAIL  missing CJK in developer_instructions: docs/zh/%s" % rel)
            failed += 1
            continue
        print("PASS  toml keys and CJK: docs/zh/%s" % rel)
        passed += 1

    total = passed + failed
    print("%d/%d passed, %d failed" % (passed, total, failed))
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
