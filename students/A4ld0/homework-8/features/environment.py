"""Start a fresh Selenium browser for every BDD scenario."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "selenium"))

from pages.browser import create_driver
from pages.todo_page import TodoPage


def before_scenario(context, scenario):
    context.driver = create_driver()
    context.todo_page = TodoPage(context.driver)


def after_scenario(context, scenario):
    if hasattr(context, "driver"):
        directory = ROOT / "screenshots"
        directory.mkdir(exist_ok=True)
        name = "".join(c if c.isalnum() else "-" for c in scenario.name)
        try:
            context.driver.save_screenshot(str(directory / f"bdd-{name}.png"))
        finally:
            context.driver.quit()

