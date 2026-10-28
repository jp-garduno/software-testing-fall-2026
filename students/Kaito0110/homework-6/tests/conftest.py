"""Pytest configuration to ensure homework-6 root is on sys.path."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
