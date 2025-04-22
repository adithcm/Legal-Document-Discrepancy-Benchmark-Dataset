from pathlib import Path

def print_dir_tree(
    root: str | Path,
    prefix: str = "",
    is_last: bool = True,
    _initial_call: bool = True,
) -> None:
    """
    Recursively print a tree‑like view of *root*.

    Parameters
    ----------
    root        : str | Path
        Directory whose contents you want to display.
    prefix      : str
        Used internally to build the graphic tree structure.
    is_last     : bool
        Whether *root* is the last item in its parent directory.
    _initial_call : bool
        Internal flag so the first call prints the root cleanly.

    Example
    -------
    >>> print_dir_tree(r"C:\Projects\demo")
    demo
    ├── data
    │   └── sample.csv
    └── src
        ├── __init__.py
        └── main.py
    """
    root = Path(root)
    connector = "└── " if is_last else "├── "

    # Print the node label (directory name on first call, filename otherwise)
    if _initial_call:
        print(root.name)
    else:
        print(f"{prefix}{connector}{root.name}")

    # Directories: recurse into children
    if root.is_dir():
        # Determine new prefixes for children
        new_prefix = prefix + ("    " if is_last else "│   ")
        # Sort so that directories appear before files, then alphabetical
        children = sorted(root.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))

        for idx, child in enumerate(children):
            last_child = idx == len(children) - 1
            print_dir_tree(child, new_prefix, last_child, _initial_call=False)


if __name__ == "__main__":
    print_dir_tree(r".\mini-eval\answers_v2")
    print_dir_tree(r".\mini-eval\documents_v2")