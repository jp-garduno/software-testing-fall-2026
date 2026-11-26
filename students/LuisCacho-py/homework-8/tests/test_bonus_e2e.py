"""Bonus & Coverage tests: Visual Regression (Option A), Performance Metrics (Option C), and POM edge cases."""

from pathlib import Path
import pytest
from todo_driver import By, Keys, create_driver
from todo_page import TodoPage
from performance_visual import compare_screenshots, summarize_performance_metrics

BASE_DIR = Path(__file__).resolve().parent.parent
SCREENSHOTS_DIR = BASE_DIR / "screenshots"


def test_visual_regression_and_screenshot_generation(tmp_path):
    """Capture screenshots at key workflow milestones and compare visual baselines (Bonus Option A)."""
    driver = create_driver()
    page = TodoPage(driver)
    page.navigate()

    # 1. Initial empty state screenshot
    empty_shot = SCREENSHOTS_DIR / "01-empty-state.png"
    assert page.take_screenshot(str(empty_shot)) is True
    assert empty_shot.exists()

    # 2. Tasks added state screenshot
    page.add_todos(["Design Page Object Model", "Implement Selenium Suite", "Implement Playwright Suite"])
    added_shot = SCREENSHOTS_DIR / "02-tasks-created.png"
    assert page.take_screenshot(str(added_shot)) is True

    # 3. Completed state screenshot
    page.toggle_todo(0)
    page.toggle_todo(1)
    completed_shot = SCREENSHOTS_DIR / "03-tasks-completed.png"
    assert page.take_screenshot(str(completed_shot)) is True

    # 4. Filtered active state screenshot
    page.filter_active()
    active_shot = SCREENSHOTS_DIR / "04-filtered-active.png"
    assert page.take_screenshot(str(active_shot)) is True

    # 5. Filtered completed state screenshot
    page.filter_completed()
    comp_filter_shot = SCREENSHOTS_DIR / "05-filtered-completed.png"
    assert page.take_screenshot(str(comp_filter_shot)) is True

    # Compare identical re-render vs modified state
    duplicate_shot = tmp_path / "duplicate.png"
    page.take_screenshot(str(duplicate_shot))
    same_cmp = compare_screenshots(str(comp_filter_shot), str(duplicate_shot))
    assert same_cmp["identical"] is True
    assert same_cmp["diff_bytes"] == 0

    diff_cmp = compare_screenshots(str(empty_shot), str(added_shot))
    assert diff_cmp["identical"] is False
    assert diff_cmp["diff_bytes"] > 0
    assert diff_cmp["diff_ratio"] > 0.0
    driver.quit()


def test_performance_metrics_collection_and_summary():
    """Verify operation timings are tracked and summarized accurately (Bonus Option C)."""
    assert summarize_performance_metrics([])["total_operations"] == 0

    driver = create_driver()
    page = TodoPage(driver)
    page.navigate()
    page.add_todos(["Benchmark Task 1", "Benchmark Task 2"])
    page.toggle_todo(0)
    page.filter_active()
    page.filter_completed()
    page.filter_all()
    page.clear_completed()

    summary = summarize_performance_metrics(page.metrics)
    assert summary["total_operations"] == 8
    assert summary["total_duration_ms"] >= 0.0
    assert "add_todo" in summary["by_action"]
    assert summary["by_action"]["add_todo"]["count"] == 2
    driver.quit()


def test_page_object_and_driver_defensive_branches():
    """Test out-of-range indices, unknown filters, and element attributes for 100% coverage."""
    driver = create_driver()
    page = TodoPage(driver)
    page.navigate()

    # Empty state lookups
    with pytest.raises(LookupError):
        driver.find_element(By.CSS_SELECTOR, ".todo-list li")
    with pytest.raises(LookupError):
        driver.find_element(By.CSS_SELECTOR, ".nonexistent")
    assert driver.find_elements(By.CSS_SELECTOR, ".nonexistent") == []

    # Out-of-range index errors
    with pytest.raises(IndexError):
        page.toggle_todo(0)
    with pytest.raises(IndexError):
        page.is_todo_completed(0)
    with pytest.raises(IndexError):
        page.delete_todo(0)
    with pytest.raises(IndexError):
        page.edit_todo(0, "New")
    with pytest.raises(IndexError):
        page.cancel_edit_todo(0, "Cancel")
    with pytest.raises(ValueError, match="Unknown filter name"):
        page.filter_by_name("Archived")

    # Element properties and attributes
    new_input = driver.find_element(By.CLASS_NAME, "new-todo")
    new_input.send_keys("Draft" + Keys.ESCAPE)
    assert new_input.get_attribute("value") == ""

    page.add_todo("Sample")
    li_el = driver.find_element(By.CSS_SELECTOR, ".todo-list li")
    label_el = li_el.find_element(By.CSS_SELECTOR, "label")
    assert label_el.text == "Sample"

    # Edit input backspace and attributes
    li_el.double_click()
    assert "editing" in li_el.get_attribute("class")
    edit_el = li_el.find_element(By.CSS_SELECTOR, ".edit")
    edit_el.send_keys("X" + Keys.BACK_SPACE + Keys.ENTER)
    assert page.get_visible_todos() == ["Sample"]

    toggle_el = li_el.find_element(By.CSS_SELECTOR, ".toggle")
    assert toggle_el.is_selected() is False
    assert toggle_el.is_displayed() is True
    assert toggle_el.text == ""
    assert toggle_el.get_attribute("unknown") == ""

    with pytest.raises(ValueError, match="Unsupported child selector"):
        li_el.find_element(By.CSS_SELECTOR, ".unknown-child")

    # Filter link text and class attributes
    f_all = driver.find_element(By.CSS_SELECTOR, "a[href='#/']")
    f_act = driver.find_element(By.CSS_SELECTOR, "a[href='#/active']")
    f_cmp = driver.find_element(By.CSS_SELECTOR, "a[href='#/completed']")
    clr_btn = driver.find_element(By.CLASS_NAME, "clear-completed")

    assert f_all.text == "All" and f_all.get_attribute("class") == "selected"
    page.filter_active()
    assert f_act.text == "Active" and f_act.get_attribute("class") == "selected"
    page.filter_completed()
    assert f_cmp.text == "Completed" and f_cmp.get_attribute("class") == "selected"
    assert clr_btn.text == "Clear completed"
    assert clr_btn.is_displayed() is False

    # Stale element check after deletion
    page.filter_all()
    page.delete_todo(0)
    with pytest.raises(RuntimeError, match="Stale element reference"):
        _ = li_el.text
    driver.quit()
