"""Part 3: BDD Scenarios execution test suite running features/todo.feature."""

import importlib.util
from pathlib import Path
import pytest
from bdd_runner import BDDContext, StepRegistry, parse_and_run_feature, _parse_table
from todo_driver import create_driver

BASE_DIR = Path(__file__).resolve().parent.parent
FEATURE_FILE = BASE_DIR / "features" / "todo.feature"
STEPS_FILE = BASE_DIR / "features" / "steps" / "todo_steps.py"


def _load_steps_registry() -> StepRegistry:
    spec = importlib.util.spec_from_file_location("todo_steps_mod", STEPS_FILE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.REGISTRY


def test_execute_all_gherkin_bdd_scenarios():
    """Execute all scenarios and Scenario Outlines in features/todo.feature."""
    registry = _load_steps_registry()
    results = parse_and_run_feature(FEATURE_FILE, registry, create_driver)

    # 6 regular scenarios + 3 examples in Scenario Outline = 9 executions
    assert len(results) == 9
    assert all(r["status"] == "passed" for r in results)

    titles = [r["scenario"] for r in results]
    assert "Add a new todo" in titles
    assert "Complete a todo" in titles
    assert "Unmark a completed todo" in titles
    assert "Edit an existing todo" in titles
    assert "Delete a todo" in titles
    assert "Clear completed todos" in titles
    assert titles.count("Filter todos") == 3


def test_bdd_runner_edge_cases():
    """Verify StepRegistry error handling and empty table parsing."""
    registry = StepRegistry()
    ctx = BDDContext(create_driver())
    with pytest.raises(KeyError, match="No step definition found"):
        registry.execute("When I perform an undefined step", ctx)

    assert _parse_table(["| only_header |"]) == []
