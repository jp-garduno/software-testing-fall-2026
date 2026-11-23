"""Create and close a fresh Selenium browser for every BDD scenario."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "selenium"))

from browser import create_driver  # pylint: disable=wrong-import-position


def before_scenario(context, _scenario):
    """Isolate scenario data in a temporary Chrome profile."""
    context.driver = create_driver()


def after_scenario(context, _scenario):
    """Release the browser after every scenario, including failed scenarios."""
    driver = getattr(context, "driver", None)
    if driver is not None:
        driver.quit()
