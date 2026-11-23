"""Behave hooks: start one Chrome for the run and give each scenario a TodoPage on an empty list."""

import sys
from pathlib import Path

SELENIUM_DIR = Path(__file__).resolve().parent.parent / "selenium"
sys.path.insert(0, str(SELENIUM_DIR))

# pylint: disable=wrong-import-position
from selenium import webdriver  # noqa: E402

from conftest import ARTIFACTS, _chrome_options  # noqa: E402
from pages.todo_page import TodoPage  # noqa: E402


def before_all(context):
    context.driver = webdriver.Chrome(options=_chrome_options())


def before_scenario(context, scenario):  # pylint: disable=unused-argument
    context.todo_page = TodoPage(context.driver)


def after_step(context, step):
    if step.status == "failed":
        ARTIFACTS.mkdir(exist_ok=True)
        context.driver.save_screenshot(str(ARTIFACTS / "behave-failure.png"))


def after_all(context):
    context.driver.quit()
