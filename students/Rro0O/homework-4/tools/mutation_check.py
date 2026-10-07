"""Poor man's mutation testing: break banking_system.py on purpose and see which test files notice.

Usage (from the homework-4 directory):  python tools/mutation_check.py

Each mutant is applied to a temporary copy of the project, the suite is run, and the test files that failed
are reported. A mutant that no test detects would be a gap in the test design.
"""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MUTANTS = [
    ("M01 daily limit uses >= instead of >", "+ value > self.get_daily_limit()", "+ value >= self.get_daily_limit()"),
    (
        "M02 balance check uses >= instead of >",
        "        if value > Decimal(str(self.balance)):\n",
        "        if value >= Decimal(str(self.balance)):\n",
    ),
    (
        "M03 suspension at balance <= minimum",
        "below_minimum = self.balance < self",
        "below_minimum = self.balance <= self",
    ),
    (
        "M04 fee waived at balance >= threshold",
        'self.balance > rules["fee_waiver_above"]',
        'self.balance >= rules["fee_waiver_above"]',
    ),
    ("M05 fee also charged on the 2nd", "if day.day != 1:", "if day.day not in (1, 2):"),
    ("M06 zero amount accepted", "if value <= 0:", "if value < 0:"),
    (
        "M07 fee affordable check uses <=",
        "if Decimal(str(self.balance)) < fee:",
        "if Decimal(str(self.balance)) <= fee:",
    ),
    ("M08 history excludes start day", 'tx["date"] >= first', 'tx["date"] > first'),
    ("M09 history excludes end day", 'tx["date"] <= last', 'tx["date"] < last'),
    ("M10 payment dated today rejected", "elif due < today:", "elif due <= today:"),
    ("M11 freeze allowed from any state", "if self.state != STATE_ACTIVE:", "if self.state == STATE_CLOSED:"),
    ("M12 opening balance == minimum rejected", "if initial_balance < minimum:", "if initial_balance <= minimum:"),
    ("M13 Savings limit is 2001", '"daily_limit": 2000', '"daily_limit": 2001'),
    ("M14 daily total never resets", "if self._last_activity_day != day:", "if self._last_activity_day is None:"),
    (
        "M15 Suspended accounts cannot operate",
        "OPERABLE_STATES = (STATE_ACTIVE, STATE_SUSPENDED)",
        "OPERABLE_STATES = (STATE_ACTIVE,)",
    ),
    ("M16 unfreeze allowed from any state", "if self.state != STATE_FROZEN:", "if self.state == STATE_CLOSED:"),
]


def run_suite(project):
    """Run pytest in ``project``; return the set of failing test files (empty when everything passes)."""
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "--tb=no", "-p", "no:cacheprovider"],
        cwd=project,
        capture_output=True,
        text=True,
        check=False,
    )
    return set(re.findall(r"FAILED tests/(test_\w+)\.py", proc.stdout)), proc.returncode


def main():
    """Apply every mutant and print a markdown table."""
    print("| Mutant | Killed | Detected by |")
    print("|---|---|---|")
    survivors = 0
    for name, old, new in MUTANTS:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "project"
            shutil.copytree(
                ROOT,
                project,
                ignore=shutil.ignore_patterns("node_modules", "htmlcov", ".pytest_cache", "coverage", "__pycache__"),
            )
            target = project / "src" / "banking_system.py"
            source = target.read_text(encoding="utf-8")
            if source.count(old) != 1:
                raise SystemExit(f"{name}: pattern found {source.count(old)} times, expected exactly 1")
            target.write_text(source.replace(old, new), encoding="utf-8")
            failing, code = run_suite(project)
        killed = code != 0
        survivors += not killed
        files = ", ".join(sorted(f.replace("test_", "") for f in failing)) or "-"
        print(f"| {name} | {'yes' if killed else 'NO'} | {files} |")
    print(f"\nMutants: {len(MUTANTS)}, killed: {len(MUTANTS) - survivors}, survived: {survivors}")


if __name__ == "__main__":
    main()
