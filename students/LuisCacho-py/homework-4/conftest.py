"""Root conftest.py — ensures src/ is importable in all environments."""

import sys
from pathlib import Path

# Add the project root (homework-4/) to sys.path so that
# `from src.banking_system import ...` works regardless of how
# pytest is invoked (local, CI, or from a parent directory).
ROOT = Path(__file__).parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
