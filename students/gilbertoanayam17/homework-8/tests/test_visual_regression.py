"""Bonus A: visual regression with Selenium and Pillow.

Each checkpoint rebuilds one state of the app, takes a screenshot of it and compares it pixel by
pixel with the baseline saved by an earlier run. The first run on a platform has nothing to compare
with, so it saves the baseline and passes. Baselines are kept per platform because Windows and
Linux render fonts differently.

Every run saves its images in screenshots/visual/actual/ and rewrites screenshots/visual/report.md. A
checkpoint that changed also leaves a copy with the changed pixels painted red in screenshots/visual/diff/.
"""

import shutil
import sys
from pathlib import Path

import markdown_report
import pytest
from PIL import Image, ImageChops

VISUAL_DIR = Path(__file__).resolve().parent.parent / "screenshots" / "visual"
BASELINE_DIR = VISUAL_DIR / "baseline" / sys.platform
ACTUAL_DIR = VISUAL_DIR / "actual"
DIFF_DIR = VISUAL_DIR / "diff"
REPORT = VISUAL_DIR / "report.md"

PIXEL_TOLERANCE = 32  # a color channel has to move more than this (out of 255) to count as a change
MAX_CHANGED_RATIO = 0.001  # a checkpoint fails when more than 0.1 % of its pixels changed


def build_mixed_list(todo_page):
    todo_page.add_todos("Task 1", "Task 2", "Task 3")
    todo_page.toggle_todo(1)


def build_active_view(todo_page):
    build_mixed_list(todo_page)
    todo_page.filter_active()


def build_completed_view(todo_page):
    build_mixed_list(todo_page)
    todo_page.filter_completed()


CHECKPOINTS = {
    "empty-list": lambda todo_page: None,
    "mixed-list": build_mixed_list,
    "active-view": build_active_view,
    "completed-view": build_completed_view,
}


def count_changed_pixels(baseline_path, actual_path, diff_path):
    """Pixels where some channel moved more than PIXEL_TOLERANCE. If there are any, draw them in red."""
    with Image.open(baseline_path) as baseline_file, Image.open(actual_path) as actual_file:
        baseline = baseline_file.convert("RGB")
        actual = actual_file.convert("RGB")
    if baseline.size != actual.size:
        return actual.width * actual.height  # a different size means the whole layout moved

    red, green, blue = ImageChops.difference(baseline, actual).split()
    largest_change = ImageChops.lighter(ImageChops.lighter(red, green), blue)
    mask = largest_change.point(lambda value: 255 if value > PIXEL_TOLERANCE else 0)
    changed = mask.histogram()[255]
    if changed:
        diff_path.parent.mkdir(parents=True, exist_ok=True)
        Image.composite(Image.new("RGB", actual.size, (255, 0, 0)), actual, mask).save(diff_path)
    return changed


@pytest.fixture(name="report_rows", scope="module")
def fixture_report_rows():
    """Collects one row per checkpoint and writes the report once all of them ran."""
    rows = []
    yield rows
    markdown_report.write(
        REPORT,
        [
            "# Visual Regression Report",
            "",
            f"Platform `{sys.platform}`, compared with `baseline/{sys.platform}/`. A checkpoint fails when more "
            f"than {MAX_CHANGED_RATIO:.1%} of its pixels changed by more than {PIXEL_TOLERANCE}/255 in some color "
            "channel.",
            "",
            *markdown_report.table(("Checkpoint", "Result", "Changed pixels", "Changed"), rows),
        ],
    )


@pytest.mark.parametrize("checkpoint", CHECKPOINTS)
def test_screenshot_matches_baseline(checkpoint, todo_page, report_rows):
    CHECKPOINTS[checkpoint](todo_page)
    actual = ACTUAL_DIR / f"{checkpoint}.png"
    baseline = BASELINE_DIR / f"{checkpoint}.png"
    ACTUAL_DIR.mkdir(parents=True, exist_ok=True)

    todo_page.save_app_screenshot(actual)

    if not baseline.exists():
        BASELINE_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(actual, baseline)
        report_rows.append((checkpoint, "new baseline", "-", "-"))
        return

    diff = DIFF_DIR / f"{checkpoint}.png"
    changed = count_changed_pixels(baseline, actual, diff)
    with Image.open(actual) as image:
        ratio = changed / (image.width * image.height)
    result = "match" if ratio <= MAX_CHANGED_RATIO else "CHANGED"
    report_rows.append((checkpoint, result, str(changed), f"{ratio:.3%}"))

    assert ratio <= MAX_CHANGED_RATIO, f"{changed} pixels ({ratio:.2%}) differ from the baseline, see {diff}"
