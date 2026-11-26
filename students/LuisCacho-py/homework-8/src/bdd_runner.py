"""Lightweight Gherkin BDD runner for executing features/todo.feature in pytest."""

from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
import re


class BDDContext:
    """Execution context shared across Given/When/Then steps in a scenario."""

    def __init__(self, driver: Any):
        self.driver = driver
        self.todo_page: Any = None
        self.table: Optional[List[Dict[str, str]]] = None


class StepRegistry:
    """Registry mapping Gherkin step patterns to Python step definition functions."""

    def __init__(self) -> None:
        self.steps: List[Tuple[str, re.Pattern, Callable]] = []

    def register(self, kind: str, pattern: str) -> Callable:
        """Decorator registering a step pattern with `{param}` placeholders."""
        escaped = pattern.replace("(", r"\(").replace(")", r"\)")
        regex_str = (
            "^"
            + re.sub(
                r"\{(\w+)(?::d)?\}",
                lambda m: r"(?P<" + m.group(1) + r">-?\d+)"
                if ":d" in m.group(0)
                else r"(?P<" + m.group(1) + r">.+)",
                escaped,
            )
            + "$"
        )
        compiled = re.compile(regex_str)

        def decorator(func: Callable) -> Callable:
            self.steps.append((kind, compiled, func))
            return func

        return decorator

    def execute(self, step_text: str, context: BDDContext) -> None:
        """Match and invoke a step definition for `step_text`."""
        cleaned = re.sub(r"^(Given|When|Then|And|But)\s+", "", step_text.strip())
        for _, compiled, func in self.steps:
            match = compiled.match(cleaned)
            if match:
                kwargs: Dict[str, Any] = {}
                for key, val in match.groupdict().items():
                    if val.lstrip("-").isdigit() and f"{{{key}:d}}" in compiled.pattern or key == "count":
                        kwargs[key] = int(val)
                    else:
                        kwargs[key] = val
                func(context, **kwargs)
                return
        raise KeyError(f"No step definition found for: {step_text}")


def _parse_table(table_lines: List[str]) -> List[Dict[str, str]]:
    rows = [
        [cell.strip() for cell in line.strip().strip("|").split("|")]
        for line in table_lines
    ]
    if len(rows) < 2:
        return []
    headers = rows[0]
    return [dict(zip(headers, row)) for row in rows[1:]]


def parse_and_run_feature(
    feature_path: Path,
    registry: StepRegistry,
    driver_factory: Callable[[], Any],
) -> List[Dict[str, Any]]:
    """Parse a Gherkin `.feature` file (including Background and Scenario Outlines) and run all scenarios."""
    lines = feature_path.read_text(encoding="utf-8").splitlines()
    background_steps: List[str] = []
    scenarios: List[Dict[str, Any]] = []

    mode: Optional[str] = None
    current: Optional[Dict[str, Any]] = None

    for raw_line in lines:
        line = raw_line.strip()
        ignored_prefixes = ("#", "Feature:", "As a ", "I want ", "So that ")
        if not line or line.startswith(ignored_prefixes):
            continue

        if line.startswith("Background:"):
            mode = "background"
            continue

        if line.startswith("Scenario Outline:") or line.startswith("Scenario:"):
            if current is not None:
                scenarios.append(current)
            is_outline = line.startswith("Scenario Outline:")
            title = line.split(":", 1)[1].strip()
            current = {
                "title": title,
                "is_outline": is_outline,
                "steps": [],
                "examples_lines": [],
            }
            mode = "scenario"
            continue

        if line.startswith("Examples:"):
            mode = "examples"
            continue

        if mode == "background":
            background_steps.append(line)
        elif mode == "scenario" and current is not None:
            if line.startswith("|"):
                current["steps"][-1]["table_lines"].append(line)
            else:
                current["steps"].append({"text": line, "table_lines": []})
        elif mode == "examples" and current is not None:
            if line.startswith("|"):
                current["examples_lines"].append(line)

    if current is not None:
        scenarios.append(current)

    executed_results: List[Dict[str, Any]] = []

    for scen in scenarios:
        if scen["is_outline"]:
            example_rows = _parse_table(scen["examples_lines"])
        else:
            example_rows = [{}]

        for row_vars in example_rows:
            driver = driver_factory()
            context = BDDContext(driver)
            for bg_step in background_steps:
                registry.execute(bg_step, context)

            for step_obj in scen["steps"]:
                step_text = step_obj["text"]
                for var_key, var_val in row_vars.items():
                    step_text = step_text.replace(f"<{var_key}>", var_val)
                context.table = (
                    _parse_table(step_obj["table_lines"])
                    if step_obj["table_lines"]
                    else None
                )
                registry.execute(step_text, context)

            driver.quit()
            executed_results.append(
                {
                    "scenario": scen["title"],
                    "variables": row_vars,
                    "status": "passed",
                }
            )

    return executed_results
