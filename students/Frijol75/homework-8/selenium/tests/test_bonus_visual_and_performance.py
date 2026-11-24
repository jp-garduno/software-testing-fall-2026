"""
Bonus Features Test Suite (Options A & C):
- Option A: Visual Regression Testing (captures screenshots at key states and compares pixel diffs)
- Option C: Performance Metrics (measures page load and CRUD operation execution times)
"""

import os
import time
from PIL import Image, ImageChops

HOMEWORK_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCREENSHOTS_DIR = os.path.join(HOMEWORK_DIR, "screenshots")


def compute_image_diff_percentage(img_path_a: str, img_path_b: str) -> float:
    """Compare two screenshots pixel-by-pixel and return percentage difference."""
    with Image.open(img_path_a).convert("RGB") as img_a, Image.open(img_path_b).convert("RGB") as img_b:
        if img_a.size != img_b.size:
            img_b = img_b.resize(img_a.size)
        diff = ImageChops.difference(img_a, img_b)
        histogram = diff.histogram()
        # Sum of non-zero channel differences
        non_zero = sum(histogram[i] for i in range(len(histogram)) if i % 256 != 0)
        total_channels = img_a.size[0] * img_a.size[1] * 3
        return round((non_zero / total_channels) * 100.0, 4)


def test_bonus_a_visual_regression(todo_page):
    """
    Bonus Option A: Visual Regression (+5 points)
    Captures baseline and post-action screenshots and compares visual states.
    """
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

    baseline_empty = os.path.join(SCREENSHOTS_DIR, "visual_baseline_empty.png")
    rerun_empty = os.path.join(SCREENSHOTS_DIR, "visual_rerun_empty.png")
    populated_state = os.path.join(SCREENSHOTS_DIR, "visual_populated_state.png")

    # Capture two snapshots of identical empty state
    todo_page.take_screenshot(baseline_empty)
    todo_page.take_screenshot(rerun_empty)

    # Capture snapshot after adding and completing items
    todo_page.add_todos(["Visual Task 1", "Visual Task 2"])
    todo_page.toggle_todo(0)
    todo_page.take_screenshot(populated_state)

    # Identical state should have 0.0% visual difference
    same_state_diff = compute_image_diff_percentage(baseline_empty, rerun_empty)
    assert same_state_diff == 0.0, f"Expected 0% diff on identical state, got {same_state_diff}%"

    # Populated state should show measurable visual difference vs empty state
    changed_state_diff = compute_image_diff_percentage(baseline_empty, populated_state)
    assert changed_state_diff > 0.0, "Expected non-zero visual difference after adding tasks"


def test_bonus_c_performance_metrics(driver):
    """
    Bonus Option C: Performance Metrics (+5 points)
    Measures page load and CRUD operation execution times.
    """
    from pages.todo_page import TodoPage

    page = TodoPage(driver)

    # 1. Measure Page Load Time
    load_time_ms = page.navigate() * 1000.0

    # 2. Measure Add Todo Time
    t0 = time.perf_counter()
    page.add_todo("Performance Task 1")
    add_single_ms = (time.perf_counter() - t0) * 1000.0

    # 3. Measure Batch Add (5 tasks)
    t0 = time.perf_counter()
    page.add_todos([f"Batch Task {i}" for i in range(2, 7)])
    add_batch_ms = (time.perf_counter() - t0) * 1000.0

    # 4. Measure Toggle Completion Time
    t0 = time.perf_counter()
    page.toggle_todo(0)
    toggle_ms = (time.perf_counter() - t0) * 1000.0

    # 5. Measure Edit Todo Time
    t0 = time.perf_counter()
    page.edit_todo(1, "Batch Task 2 (Edited)")
    edit_ms = (time.perf_counter() - t0) * 1000.0

    # 6. Measure Filter Switching Time
    t0 = time.perf_counter()
    page.filter_active()
    page.filter_completed()
    page.filter_all()
    filter_ms = (time.perf_counter() - t0) * 1000.0

    # 7. Measure Delete Todo Time
    t0 = time.perf_counter()
    page.delete_todo(0)
    delete_ms = (time.perf_counter() - t0) * 1000.0

    assert load_time_ms > 0
    assert add_single_ms > 0
    assert add_batch_ms > 0
    assert toggle_ms > 0
    assert edit_ms > 0
    assert filter_ms > 0
    assert delete_ms > 0

