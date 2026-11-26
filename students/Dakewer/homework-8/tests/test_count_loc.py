"""Unit tests for scripts/count_loc.py, which produces the figures in the comparison report."""
from count_loc import code_lines


def test_python_count_skips_blanks_comments_and_docstrings(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text(
        '''"""Module docstring."""
# comment

def add(a, b):
    """Add two numbers."""
    return a + b
''',
        encoding="utf-8",
    )

    assert code_lines(str(source)) == 2


def test_javascript_count_skips_blanks_and_comments(tmp_path):
    source = tmp_path / "sample.js"
    source.write_text(
        """// comment

/**
 * Block comment
 */
const total = 1;
module.exports = { total };
""",
        encoding="utf-8",
    )

    assert code_lines(str(source)) == 2
