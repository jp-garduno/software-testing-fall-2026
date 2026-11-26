"""Behave hooks: reuse the Selenium page object and give each scenario a browser."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "selenium"))

from pages.browser import create_driver  # noqa: E402  # pylint: disable=wrong-import-position


def before_scenario(context, _scenario):
    context.driver = create_driver()


def after_step(context, step):
    if step.status.name in ("failed", "error"):
        folder = ROOT / "reports" / "behave-failures"
        folder.mkdir(parents=True, exist_ok=True)
        context.driver.save_screenshot(str(folder / f"line-{step.line}.png"))


def after_scenario(context, _scenario):
    driver = getattr(context, "driver", None)
    if driver:
        driver.quit()
