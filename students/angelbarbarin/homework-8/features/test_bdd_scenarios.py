"""Runs the behave scenarios from pytest, so `pytest` alone executes the whole suite.

`behave features` still works on its own; this wrapper only lets the scenarios count as a
test (and their step definitions count in the coverage report) when the suite is run by pytest.
"""

from pathlib import Path

from behave.__main__ import main as behave_main

FEATURES_DIR = Path(__file__).resolve().parent


def test_all_bdd_scenarios_pass():
    exit_code = behave_main([str(FEATURES_DIR), "--format", "plain", "--no-capture", "--no-timings"])
    assert exit_code == 0, "At least one behave scenario failed (see the output above)"
