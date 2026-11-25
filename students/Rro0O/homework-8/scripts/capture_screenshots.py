"""Walk through the main flows with the Selenium page object and save a screenshot of each state."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "selenium"))

from driver_factory import create_driver  # noqa: E402  pylint: disable=wrong-import-position
from pages.todo_page import TodoPage  # noqa: E402  pylint: disable=wrong-import-position

OUTPUT = ROOT / "screenshots"


def main():
    OUTPUT.mkdir(exist_ok=True)
    driver = create_driver()
    try:
        page = TodoPage(driver)
        page.navigate()
        page.add_todos("Buy groceries", "Read book", "Walk the dog")
        driver.save_screenshot(str(OUTPUT / "01-tasks-created.png"))
        page.toggle_todo(1)
        driver.save_screenshot(str(OUTPUT / "02-task-completed.png"))
        page.filter_active()
        driver.save_screenshot(str(OUTPUT / "03-filter-active.png"))
        page.filter_completed()
        driver.save_screenshot(str(OUTPUT / "04-filter-completed.png"))
        page.filter_all()
        page.start_edit(0)
        page.type_in_edit(0, "Buy groceries and coffee")
        driver.save_screenshot(str(OUTPUT / "05-editing-task.png"))
        page.press_enter_in_edit(0)
        page.clear_completed()
        driver.save_screenshot(str(OUTPUT / "06-after-clear-completed.png"))
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
