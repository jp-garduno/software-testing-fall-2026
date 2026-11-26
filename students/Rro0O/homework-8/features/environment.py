"""Behave hooks: one fresh browser per scenario."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "selenium"))

from driver_factory import create_driver  # noqa: E402  pylint: disable=wrong-import-position


def before_scenario(context, _scenario):
    context.driver = create_driver()


def after_scenario(context, _scenario):
    context.driver.quit()
