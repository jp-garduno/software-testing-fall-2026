"""behave hooks: one Chrome for the whole run, a fresh page for every scenario.

The step definitions reuse the Selenium Page Object from ../selenium/pages, so the BDD layer
only translates Gherkin sentences into page actions.
"""

import sys
from pathlib import Path

SELENIUM_DIR = Path(__file__).resolve().parent.parent / "selenium"
SCREENSHOT_DIR = Path(__file__).resolve().parent.parent / "screenshots" / "bdd-failures"
if str(SELENIUM_DIR) not in sys.path:
    sys.path.insert(0, str(SELENIUM_DIR))

from driver_factory import create_driver  # noqa: E402  pylint: disable=wrong-import-position


def before_all(context):
    context.driver = create_driver()


def after_step(context, step):
    """Keep a screenshot of the browser for every failed step."""
    if step.status == "failed":
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        name = "".join(char if char.isalnum() else "_" for char in context.scenario.name)
        context.driver.save_screenshot(str(SCREENSHOT_DIR / f"{name}.png"))


def after_all(context):
    context.driver.quit()
