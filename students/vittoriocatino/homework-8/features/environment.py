"""Behave lifecycle hooks with a fresh browser context for every scenario."""

import re
from playwright.sync_api import sync_playwright

from support import ROOT, page_type, chrome_launch_options


def before_all(context):
    """Start a real browser once for the feature suite."""
    context.runtime = sync_playwright().start()
    context.browser = context.runtime.chromium.launch(
        **chrome_launch_options(), headless=True
    )


def before_scenario(context, scenario):
    """Isolate cookies and storage, including Scenario Outline examples."""
    del scenario
    context.browser_context = context.browser.new_context(
        viewport={"width": 1280, "height": 900}
    )
    context.todo_page = page_type("playwright")(context.browser_context.new_page())


def after_scenario(context, scenario):
    """Capture final UI state and always dispose of the browser context."""
    try:
        name = re.sub(r"[^a-z0-9]+", "-", scenario.name.lower()).strip("-")
        destination = ROOT / "screenshots" / f"bdd-{name}.png"
        destination.parent.mkdir(exist_ok=True)
        context.todo_page.screenshot(destination)
    finally:
        context.browser_context.close()


def after_all(context):
    """Release browser processes even after a scenario assertion fails."""
    context.browser.close()
    context.runtime.stop()
