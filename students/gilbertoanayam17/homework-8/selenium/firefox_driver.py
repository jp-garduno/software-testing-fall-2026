"""The WebDriver used by the Selenium suite, the BDD scenarios and the bonus tests."""

import os
import sys

# Imported from their own modules: selenium.webdriver loads Firefox lazily, which pylint cannot follow.
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver

# Narrower than the 899 px breakpoint at which TodoMVC's "learn" sidebar, loaded after the page,
# pushes the whole app 300 px to the right. Below it the layout never moves under a click.
WINDOW_SIZE = (800, 900)


def window_visible():
    """Show the browser window unless HEADLESS=1 is set or there is no screen to draw it on.

    CI servers set the CI variable, and a Linux machine without DISPLAY or WAYLAND_DISPLAY has no
    graphical session, so in both cases Firefox has to run headless or it would not start.
    """
    if os.environ.get("HEADLESS") == "1" or os.environ.get("CI"):
        return False
    if sys.platform.startswith("linux"):
        return bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))
    return True


def start_firefox():
    """Start Firefox, with a visible window by default (see window_visible).

    Selenium Manager finds or downloads geckodriver, and Firefox itself when it is not installed.
    """
    options = Options()
    if not window_visible():
        options.add_argument("-headless")
    # One CSS pixel per screen pixel, so screenshots are the same size with any display scaling.
    options.set_preference("layout.css.devPixelsPerPx", "1.0")
    driver = WebDriver(options=options)
    driver.set_window_size(*WINDOW_SIZE)
    return driver
