#!/usr/bin/env python3
import os
import re
import json
import sys

# ─── CONFIGURATION ───────────────────────────────────────────────────────────────
# Explicitly set your repository root path here:
REPO_ROOT = '/Users/mannanxanand/Legal-Document-Discrepancy-Benchmark-Dataset'
ENV_PATH  = os.path.join(REPO_ROOT, '.env')
GITIGNORE = os.path.join(REPO_ROOT, '.gitignore')

# Regex to match Google‐style API keys beginning with "AIzaSy"
KEY_PATTERN = re.compile(r'AIzaSy[0-9A-Za-z_\-]+')

# Store extracted keys
env_entries = {}

# ─── HELPERS ────────────────────────────────────────────────────────────────────
def ensure_gitignore():
    """Ensure '.env' is listed in .gitignore."""
    if os.path.exists(GITIGNORE):
        with open(GITIGNORE, 'r+', encoding='utf-8') as f:
            lines = f.read().splitlines()
            if '.env' not in lines:
                f.write('\n.env\n')
    else:
        with open(GITIGNORE, 'w', encoding='utf-8') as f:
            f.write('.env\n')

def write_env_file():
    """Write extracted keys to .env in KEY=VALUE format."""
    if not env_entries:
        return
    with open(ENV_PATH, 'w', encoding='utf-8') as f:
        for var, key in env_entries.items():
            f.write(f'{var}={key}\n')

# ─── FILE PROCESSING ────────────────────────────────────────────────────────────
def process_py(path):
    updated = False
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    new_lines = []
    for line in lines:
        if KEY_PATTERN.search(line):
            # Extract and stash os.environ keys
            m = re.search(r'os\.environ\["([^"]+)"\]\s*=\s*"([^"]+)"', line)
            if m:
                var, key = m.group(1), m.group(2)
                env_entries[var] = key
                new_lines.append(f'{var} = os.getenv("{var}")\n')
            # Skip all other key/comment lines
            updated = True
        else:
            new_lines.append(line)
    if updated:
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

def process_ipynb(path):
    updated = False
    try:
        nb = json.load(open(path, 'r', encoding='utf-8'))
    except Exception:
        return
    for cell in nb.get('cells', []):
        if cell.get('cell_type') != 'code':
            continue
        new_src = []
        for line in cell['source']:
            if KEY_PATTERN.search(line):
                m = re.search(r'os\.environ\["([^"]+)"\]\s*=\s*"([^"]+)"', line)
                if m:
                    var, key = m.group(1), m.group(2)
                    env_entries[var] = key
                    new_src.append(f'{var} = os.getenv("{var}")\n')
                updated = True
            else:
                new_src.append(line)
        cell['source'] = new_src
    if updated:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1)

# ─── MAIN ───────────────────────────────────────────────────────────────────────
def main():
    # 1. Ensure .gitignore
    ensure_gitignore()

    # 2. Walk and process files
    for root, _, files in os.walk(REPO_ROOT):
        if '.git' in root.split(os.sep):
            continue
        for fn in files:
            path = os.path.join(root, fn)
            if fn.endswith('.py'):
                process_py(path)
            elif fn.endswith('.ipynb'):
                process_ipynb(path)

    # 3. Write .env with all extracted keys
    write_env_file()

    print(f"✔ Extracted {len(env_entries)} API key(s) to {ENV_PATH}")
    print("✔ Updated source files to remove/commented all 'AIzaSy…' lines")
    print(f"✔ Updated .gitignore at {GITIGNORE}")

if __name__ == '__main__':
    main()
