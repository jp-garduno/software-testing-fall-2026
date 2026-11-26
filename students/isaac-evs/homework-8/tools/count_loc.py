"""Count lines of code for the comparison report: non-blank lines that are neither comments nor docstrings.

Comment lines start with '#', '//', '/*' or '*'. For Python files, docstring lines are excluded too (found with
the ast module), so Python docstrings and JavaScript JSDoc comments are treated alike.
Usage: python tools/count_loc.py FILE [FILE ...]
"""

import ast
import sys
from pathlib import Path

COMMENT_PREFIXES = ("#", "//", "/*", "*")


def docstring_lines(source):
    """Return the set of 1-based line numbers occupied by docstrings in Python source."""
    lines = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = node.body
            if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant):
                if isinstance(body[0].value.value, str):
                    lines.update(range(body[0].lineno, body[0].end_lineno + 1))
    return lines


def count_loc(path):
    """Return the number of non-blank, non-comment, non-docstring lines in a file."""
    path = Path(path)
    source = path.read_text(encoding="utf-8")
    skip = docstring_lines(source) if path.suffix == ".py" else set()
    return sum(
        1
        for number, line in enumerate(source.splitlines(), start=1)
        if line.strip() and not line.strip().startswith(COMMENT_PREFIXES) and number not in skip
    )


def main():
    """Print the count for each file given on the command line, then the total."""
    grand_total = 0
    for name in sys.argv[1:]:
        loc = count_loc(name)
        grand_total += loc
        print(f"{loc:5d}  {name}")
    print(f"{grand_total:5d}  total")


if __name__ == "__main__":
    main()
