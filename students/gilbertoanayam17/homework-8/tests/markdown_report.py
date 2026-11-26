"""Writes the Markdown reports of the bonus tests."""


def table(header, rows):
    """Lines of a Markdown table aligned the way prettier formats it, so the pre-commit hook leaves it alone."""
    all_rows = [header, *rows]
    widths = [max(3, *(len(row[column]) for row in all_rows)) for column in range(len(header))]

    def line(cells):
        return "| " + " | ".join(cell.ljust(width) for cell, width in zip(cells, widths)) + " |"

    return [line(header), line(["-" * width for width in widths]), *(line(row) for row in rows)]


def write(path, lines):
    """Save with LF line endings on every platform, which is what prettier leaves in the repository."""
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
