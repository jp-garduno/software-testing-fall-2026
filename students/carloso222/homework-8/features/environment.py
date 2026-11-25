"""Behave hooks: one browser for the whole run, a fresh page for every scenario.

The Page Object and the WebDriver factory are shared with the Selenium suite (../selenium).
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "selenium"))

# pylint: disable=wrong-import-position
from pages.todo_page import TodoPage  # noqa: E402  # isort: skip
from support import settings  # noqa: E402  # isort: skip
from support.driver_factory import create_driver  # noqa: E402  # isort: skip

SCREENSHOTS_DIR = settings.SCREENSHOTS_DIR / "bdd"


def before_all(context):
    context.driver = create_driver()


def before_scenario(context, scenario):
    run_defects = context.config.userdata.getbool("run_known_defects", False)
    if "known_defect" in scenario.effective_tags and not run_defects:
        scenario.skip("Known defect of TodoMVC React: Escape does not cancel editing")
        return
    context.todo_page = TodoPage(context.driver)


def after_scenario(context, scenario):
    if scenario.status == "skipped":
        return
    if settings.SAVE_SCREENSHOTS or scenario.status == "failed":
        name = re.sub(r"[^A-Za-z0-9_.-]+", "_", scenario.name)
        context.todo_page.take_screenshot(SCREENSHOTS_DIR / f"{name}.png")


def after_all(context):
    context.driver.quit()
