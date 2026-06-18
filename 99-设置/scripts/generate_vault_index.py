#!/usr/bin/env python3
"""Recursive vault index generator — matches original format depth-for-depth."""
import os, yaml
from datetime import datetime, timezone

VAULT = "/Users/haoxc/__Data/00_Knowledges/Vault_HXC3.1(Apple)"
EXCLUDE_DIRS = {".git", ".obsidian", ".github", ".trash", ".DS_Store", "__pycache__"}
EXCLUDE_PREFIX = ("__", ".")  # skip hidden/dunder dirs

def count_md(dirpath):
    """Recursive .md count."""
    total = 0
    try:
        for root, dirs, files in os.walk(dirpath):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(EXCLUDE_PREFIX)]
            total += sum(1 for f in files if f.endswith('.md'))
    except PermissionError:
        pass
    return total

def scan_dir(dirpath, relpath):
    """Recursively scan a directory, return list of child dicts (or empty)."""
    children = []
    try:
        entries = sorted(os.listdir(dirpath))
    except PermissionError:
        return children

    for name in entries:
        if name in EXCLUDE_DIRS or name.startswith(EXCLUDE_PREFIX):
            continue
        full = os.path.join(dirpath, name)
        if not os.path.isdir(full):
            continue

        child_rel = os.path.join(relpath, name) if relpath else name
        child = {
            'name': name,
            'path': child_rel,
            'note_count': count_md(full),
        }
        # MOC (folder note)
        moc_path = os.path.join(full, f"{name}.md")
        if os.path.exists(moc_path):
            child['moc'] = os.path.join(child_rel, f"{name}.md")

        # Recurse
        sub = scan_dir(full, child_rel)
        if sub:
            child['children'] = sub

        children.append(child)
    return children

def build():
    rules_path = os.path.join(VAULT, "99-设置/vault-rules.yaml")
    rules = {}
    if os.path.exists(rules_path):
        with open(rules_path) as f:
            rules = yaml.safe_load(f).get('directories', {})

    l1_dirs = {}
    entries = sorted(os.listdir(VAULT))
    for name in entries:
        if name in EXCLUDE_DIRS or name.startswith(EXCLUDE_PREFIX):
            continue
        full = os.path.join(VAULT, name)
        if not os.path.isdir(full):
            continue

        rule = rules.get(name, {})
        entry = {
            'path': name,
            'role': rule.get('role', 'unknown'),
            'description': rule.get('description', ''),
            'note_count': count_md(full),
        }
        moc_path = os.path.join(full, f"{name}.md")
        if os.path.exists(moc_path):
            entry['moc'] = os.path.join(name, f"{name}.md")

        children = scan_dir(full, name)
        if children:
            entry['children'] = children

        l1_dirs[name] = entry

    index = {
        'version': '1.0.0',
        'generated': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'vault_root': VAULT,
        'total_directories': len(l1_dirs),
        'directories': l1_dirs,
    }

    out_path = os.path.join(VAULT, "99-设置/vault-index.yaml")
    with open(out_path, 'w') as f:
        yaml.dump(index, f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=200)

    print(f"✅ vault-index.yaml regenerated: {len(l1_dirs)} L1 dirs")
    for d, v in l1_dirs.items():
        print(f"  {d}/  ({v['note_count']} .md)")

build()
