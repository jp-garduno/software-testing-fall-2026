"""Pytest configuration ensuring homework-7 root and src/ are importable."""

import os
import sys

HW_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(HW_ROOT, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
if HW_ROOT not in sys.path:
    sys.path.insert(0, HW_ROOT)
