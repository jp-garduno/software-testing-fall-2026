"""Shared primitives for test-data validation (bonus option C)."""

import json
from dataclasses import dataclass
from typing import Any, List


@dataclass(frozen=True)
class DataIssue:
    """A problem found in a test data file, located by file name and 1-based line number."""

    file: str
    line: int
    message: str

    def __str__(self) -> str:
        return f"{self.file}:{self.line}: {self.message}"


def is_number(value: Any) -> bool:
    """True for int/float (bool excluded)."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def is_integer(value: Any) -> bool:
    """True for int (bool excluded)."""
    return isinstance(value, int) and not isinstance(value, bool)


def parse_float(text: str) -> bool:
    """True when the text is a valid float literal."""
    try:
        float(text)
    except ValueError:
        return False
    return True


def array_item_lines(text: str, array_start: int) -> List[int]:
    """1-based line number where each element of the JSON array starting at `array_start` begins."""
    decoder = json.JSONDecoder()
    lines: List[int] = []
    pos = array_start + 1
    while True:
        while pos < len(text) and text[pos] in " \t\r\n,":
            pos += 1
        if pos >= len(text) or text[pos] == "]":
            return lines
        lines.append(text.count("\n", 0, pos) + 1)
        _, pos = decoder.raw_decode(text, pos)
