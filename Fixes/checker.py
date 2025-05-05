#!/usr/bin/env python3
import os
import filecmp
import sys

# 👇 Define your paths here:
BACKUP_PATH = '/Users/mannanxanand/backup'
CLONE_PATH  = '/Users/mannanxanand/Legal-Document-Discrepancy-Benchmark-Dataset'

def compare_dirs(dir1, dir2):
    """
    Recursively compare dir1 and dir2.
    Prints:
      - only in dir1
      - only in dir2
      - in both but different
    """
    dcmp = filecmp.dircmp(dir1, dir2)
    if dcmp.left_only:
        print(f"\nOnly in {dir1!r}:")
        for name in sorted(dcmp.left_only):
            print("  ", name)
    if dcmp.right_only:
        print(f"\nOnly in {dir2!r}:")
        for name in sorted(dcmp.right_only):
            print("  ", name)
    if dcmp.diff_files:
        print(f"\nDiffering files in both:")
        for name in sorted(dcmp.diff_files):
            print("  ", name)
    # Recurse into common subdirectories
    for sub in dcmp.common_dirs:
        compare_dirs(
            os.path.join(dir1, sub),
            os.path.join(dir2, sub)
        )

def main():
    # Validate directories
    if not os.path.isdir(BACKUP_PATH):
        print(f"Error: backup path {BACKUP_PATH!r} is not a directory")
        sys.exit(1)
    if not os.path.isdir(CLONE_PATH):
        print(f"Error: clone path {CLONE_PATH!r} is not a directory")
        sys.exit(1)

    print(f"Comparing\n  Backup: {BACKUP_PATH}\n  Clone : {CLONE_PATH}\n")
    compare_dirs(BACKUP_PATH, CLONE_PATH)
    print("\nDone.")

if __name__ == "__main__":
    main()
