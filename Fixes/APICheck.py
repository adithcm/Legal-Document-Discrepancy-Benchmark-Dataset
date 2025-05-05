#!/usr/bin/env python3
import os
import re
import json
import sys

# 👇 Update this path if your repo root is elsewhere
REPO_ROOT    = '/Users/mannanxanand/Legal-Document-Discrepancy-Benchmark-Dataset'
OUTPUT_FILE  = 'found_key_files.txt'  # will be created in the current working dir

# Regex to match API keys starting with AIzaSy
KEY_PATTERN = re.compile(r'AIzaSy[0-9A-Za-z_\-]+')


def scan_py_file(path):
    matches = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for i, line in enumerate(f, start=1):
            if KEY_PATTERN.search(line):
                matches.append((i, line.strip()))
    return matches


def scan_ipynb_file(path):
    matches = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        return matches

    for cell in data.get('cells', []):
        if cell.get('cell_type') != 'code':
            continue
        for i, line in enumerate(cell.get('source', []), start=1):
            if KEY_PATTERN.search(line):
                matches.append((i, line.strip()))
    return matches


def main():
    findings = {}
    for root, _, files in os.walk(REPO_ROOT):
        if '.git' in root.split(os.sep):
            continue
        for fname in files:
            path = os.path.join(root, fname)
            if fname.endswith('.py'):
                results = scan_py_file(path)
            elif fname.endswith('.ipynb'):
                results = scan_ipynb_file(path)
            else:
                continue

            if results:
                findings[path] = results

    # Console output
    if not findings:
        print("No API keys starting with 'AIzaSy' found in .py or .ipynb files.")
    else:
        print("Potential API key occurrences:\n")
        for path, entries in findings.items():
            print(f"File: {path}")
            for lineno, content in entries:
                print(f"  Line {lineno}: {content}")
            print()

    # Write only the file paths into OUTPUT_FILE
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
        for path in sorted(findings.keys()):
            out.write(path + '\n')

    print(f"→ Wrote list of {len(findings)} file(s) to '{OUTPUT_FILE}'.")


if __name__ == '__main__':
    main()

