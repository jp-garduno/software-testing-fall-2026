"""One real Selenium browser per BDD scenario, with guaranteed cleanup."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "selenium"))
from pages.browser import create_driver  # pylint: disable=wrong-import-position
from pages.todo_page import TodoPage  # pylint: disable=wrong-import-position


def before_scenario(context, scenario):
    """Register cleanup before any scenario action can fail."""
    del scenario
    context.driver = create_driver()
    context.add_cleanup(context.driver.quit)
    context.todo = TodoPage(context.driver)


def after_scenario(context, scenario):
    """Keep failure evidence for the CI artifact."""
    if scenario.status == "failed":
        folder = Path("reports/live/bdd-failures")
        folder.mkdir(parents=True, exist_ok=True)
        context.todo.screenshot(folder / f"{scenario.line}.png")
