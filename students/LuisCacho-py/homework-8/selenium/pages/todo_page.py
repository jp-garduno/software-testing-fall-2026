"""Selenium Page Object Model module re-exporting TodoPage for selenium/pages/todo_page.py."""

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from todo_page import TodoPage  # noqa: E402  # pylint: disable=wrong-import-position

__all__ = ["TodoPage"]
