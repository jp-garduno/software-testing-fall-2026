"""Run from the homework folder: python tools/check_quality.py."""
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from time import perf_counter

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs/evidence"
EVIDENCE.mkdir(parents=True, exist_ok=True)
environment = dict(os.environ, PYTEST_DISABLE_PLUGIN_AUTOLOAD="1", PYTHONUTF8="1")


def pytest_run(arguments, log_name):
    started = perf_counter()
    result = subprocess.run([sys.executable, "-m", "pytest", *arguments], cwd=ROOT,
