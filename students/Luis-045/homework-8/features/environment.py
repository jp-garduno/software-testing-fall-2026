"""Create and close a fresh Selenium browser for every BDD scenario."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "selenium"))

from browser import create_driver  # pylint: disable=wrong-import-position


def before_scenario(context, _scenario):
    """Isolate scenario data in a temporary Chrome profile."""
    context.driver = create_driver()


def after_scenario(context, scenario):
    """Keep execution evidence and always release the browser process."""
    driver = getattr(context, "driver", None)
    if driver is None:
        return
    try:
        name = re.sub(r"[^a-z0-9]+", "-", scenario.name.lower()).strip("-")
        directory = ROOT / "screenshots"
        directory.mkdir(exist_ok=True)
        driver.save_screenshot(str(directory / f"bdd-{name}.png"))
    finally:
        driver.quit()
