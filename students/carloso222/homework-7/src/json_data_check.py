"""Validate the customer and workflow JSON files (required fields, types) and report line numbers."""

import json
from pathlib import Path
from typing import Any, Callable, List, Optional, Tuple

from src.data_checks import DataIssue, array_item_lines
from src.order_workflow import ACTIONS

_DATA_ACTIONS = ("validate_customer", "create_order")


def _load(path: Path) -> Tuple[Optional[Any], str, List[DataIssue]]:
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text), text, []
    except json.JSONDecodeError as error:
        return (
            None,
            text,
            [DataIssue(path.name, error.lineno, f"invalid JSON: {error.msg}")],
        )


def _customer_problems(case: Any) -> List[str]:
    if not isinstance(case, dict):
        return ["case must be an object"]
    problems = []
    if not isinstance(case.get("test_name"), str) or not case["test_name"]:
        problems.append("test_name must be a non-empty string")
    if not isinstance(case.get("customer"), dict):
        problems.append("customer must be an object")
    expected = case.get("expected")
    if not isinstance(expected, dict):
        return problems + ["expected must be an object"]
    if not isinstance(expected.get("is_valid"), bool):
        problems.append("expected.is_valid must be a boolean")
    errors = expected.get("errors")
    if not isinstance(errors, list) or not all(isinstance(e, str) for e in errors):
        problems.append("expected.errors must be a list of strings")
    return problems


def _step_problems(index: int, step: Any) -> List[str]:
    if not isinstance(step, dict):
        return [f"steps[{index}] must be an object"]
    problems = []
    if step.get("action") not in ACTIONS:
        problems.append(f"steps[{index}].action must be one of {', '.join(ACTIONS)}")
    if step.get("action") in _DATA_ACTIONS and not isinstance(step.get("data"), dict):
        problems.append(f"steps[{index}].data must be an object")
    if not isinstance(step.get("expected"), dict):
        problems.append(f"steps[{index}].expected must be an object")
    return problems


def _workflow_problems(workflow: Any) -> List[str]:
    if not isinstance(workflow, dict):
        return ["workflow must be an object"]
    problems = []
    if not isinstance(workflow.get("name"), str) or not workflow["name"]:
        problems.append("name must be a non-empty string")
    steps = workflow.get("steps")
    if not isinstance(steps, list) or not steps:
        return problems + ["steps must be a non-empty list"]
    for index, step in enumerate(steps):
        problems += _step_problems(index, step)
    return problems


def _check_items(
    path: Path, items: List[Any], lines: List[int], check: Callable[[Any], List[str]]
) -> List[DataIssue]:
    issues = []
    for index, item in enumerate(items):
        line = lines[index] if index < len(lines) else 1
        issues += [
            DataIssue(path.name, line, f"item #{index + 1}: {problem}")
            for problem in check(item)
        ]
    return issues


def validate_customers_json(path: Path) -> List[DataIssue]:
    """Validate customer_validation.json (a list of cases)."""
    data, text, issues = _load(path)
    if issues:
        return issues
    if not isinstance(data, list):
        return [DataIssue(path.name, 1, "top level must be a list of cases")]
    return _check_items(
        path, data, array_item_lines(text, text.index("[")), _customer_problems
    )


def validate_workflows_json(path: Path) -> List[DataIssue]:
    """Validate order_workflows.json ({"reference_date": ..., "workflows": [...]})."""
    data, text, issues = _load(path)
    if issues:
        return issues
    if not isinstance(data, dict) or not isinstance(data.get("workflows"), list):
        return [
            DataIssue(
                path.name, 1, "top level must be an object with a 'workflows' list"
            )
        ]
    start = text.index("[", text.index('"workflows"'))
    found = _check_items(
        path, data["workflows"], array_item_lines(text, start), _workflow_problems
    )
    if not isinstance(data.get("reference_date"), str):
        found.append(
            DataIssue(path.name, 1, "reference_date must be a string (YYYY-MM-DD)")
        )
    return found
