"""Run the Gherkin scenarios as part of the pytest suite."""

from pathlib import Path

from behave.__main__ import main as run_behave

FEATURES_DIR = Path(__file__).resolve().parent.parent / "features"


def test_all_bdd_scenarios_pass():
    exit_code = run_behave([str(FEATURES_DIR), "--format=pretty", "--no-color"])

    assert exit_code == 0, "At least one Behave scenario failed; see the captured output"
