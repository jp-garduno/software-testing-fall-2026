"""Count lines of code for the comparison report: non-blank, non-comment lines (docstrings count as code)."""

import sys
from pathlib import Path


def count_loc(path):
    """Return the number of non-blank lines that are not pure '#' comments."""
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    return sum(1 for line in lines if line.strip() and not line.strip().startswith("#"))


if __name__ == "__main__":
    for name in sys.argv[1:]:
        print(f"{count_loc(name):5d}  {name}")
