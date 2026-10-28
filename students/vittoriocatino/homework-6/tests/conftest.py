"""Shared pytest configuration for the source layout."""

import sys
from pathlib import Path


SOURCE_DIRECTORY = Path(__file__).parents[1] / "src"
sys.path.insert(0, str(SOURCE_DIRECTORY))
