"""Run the scenarios with the page object and browser setup of the Selenium suite in ../selenium."""

import importlib
import sys
from pathlib import Path

HOMEWORK_DIR = Path(__file__).resolve().parents[1]
FAILURE_SCREENSHOTS = HOMEWORK_DIR / "artifacts" / "behave"

sys.path.insert(0, str(HOMEWORK_DIR / "selenium"))


def before_all(context):
    context.driver = importlib.import_module("browser").create_driver()


def after_step(context, step):
    if step.status == "failed":
        FAILURE_SCREENSHOTS.mkdir(parents=True, exist_ok=True)
        context.driver.save_screenshot(str(FAILURE_SCREENSHOTS / f"{context.scenario.name}.png"))


def after_all(context):
    context.driver.quit()
