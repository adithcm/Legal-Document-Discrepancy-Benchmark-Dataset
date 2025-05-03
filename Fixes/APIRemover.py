#!/usr/bin/env python3
import os
import re
import json

# ─── CONFIG ─────────────────────────────────────────────────────────────────────
# If you run this from somewhere else, set REPO_ROOT to your repo path instead.
REPO_ROOT   = os.getcwd()
ENV_PATH    = os.path.join(REPO_ROOT, '.env')
GITIGNORE   = os.path.join(REPO_ROOT, '.gitignore')

# Match any Google-style API key beginning with "AIzaSy"
KEY_PATTERN = re.compile(r'AIzaSy[0-9A-Za-z_\-]+')

# Will hold { VAR_NAME: key_value } for any os.environ lines we strip
env_entries = {}

# ─── HELPERS ────────────────────────────────────────────────────────────────────
def ensure_gitignore():
    """Add '.env' to .gitignore if it's not already there."""
    lines = []
    if os.path.exists(GITIGNORE):
        with open(GITIGNORE, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
    if '.env' not in lines:
        with open(GITIGNORE, 'a', encoding='utf-8') as f:
            if lines and lines[-1].strip() != '':
                f.write('\n')
            f.write('.env\n')

def write_env_file():
    """Dump all extracted keys into .env as KEY=VALUE."""
    if not env_entries:
        return
    with open(ENV_PATH, 'w', encoding='utf-8') as f:
        for var, val in env_entries.items():
            f.write(f'{var}={val}\n')

# ─── FILE PROCESSING ────────────────────────────────────────────────────────────
def process_py(path):
    """Rewrite a .py: extract os.environ keys, drop any line with an 'AIzaSy...' in it."""
    updated = False
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if KEY_PATTERN.search(line):
            # If it's an os.environ assignment, extract var name + value
            if 'os.environ' in line:
                mvar = re.search(r'os\.environ\["([^"]+)"\]\s*=\s*"([^"]+)"', line)
                if mvar:
                    var_name, key_val = mvar.group(1), mvar.group(2)
                    env_entries[var_name] = key_val
                    # replace with getenv call
                    new_lines.append(f'{var_name} = os.getenv("{var_name}")\n')
                    updated = True
                    continue
            # Otherwise just drop the line (commented or not)
            updated = True
            continue
        # keep all other lines
        new_lines.append(line)

    if updated:
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

def process_ipynb(path):
    """Rewrite a .ipynb: same logic, but in code cells only."""
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
                if 'os.environ' in line:
                    mvar = re.search(r'os\.environ\["([^"]+)"\]\s*=\s*"([^"]+)"', line)
                    if mvar:
                        var_name, key_val = mvar.group(1), mvar.group(2)
                        env_entries[var_name] = key_val
                        new_src.append(f'{var_name} = os.getenv("{var_name}")\n')
                        updated = True
                        continue
                # otherwise drop the line
                updated = True
                continue
            new_src.append(line)
        cell['source'] = new_src

    if updated:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1)

# ─── MAIN ───────────────────────────────────────────────────────────────────────
def main():
    ensure_gitignore()

    for root, _, files in os.walk(REPO_ROOT):
        # skip any Git internals
        if '.git' in root.split(os.sep):
            continue
        for fname in files:
            full = os.path.join(root, fname)
            if fname.endswith('.py'):
                process_py(full)
            elif fname.endswith('.ipynb'):
                process_ipynb(full)

    write_env_file()

    print(f"✔️  Extracted {len(env_entries)} key(s) into '{ENV_PATH}'")
    print(f"✔️  Updated source files to remove all 'AIzaSy…' lines")
    print(f"✔️  Ensured '.env' is listed in '{GITIGNORE}'")

if __name__ == '__main__':
    main()
