"""Tests for HistoryManager."""

# pylint: disable=wrong-import-position,redefined-outer-name
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from history import HistoryManager


@pytest.fixture
def manager():
    """Provide a fresh HistoryManager instance for each test."""
    return HistoryManager()


def test_log_adds_entry(manager):
    manager.log("add", (1, 2), 3)
    assert manager.count() == 1


def test_log_entry_fields(manager):
    entry = manager.log("add", (1, 2), 3)
    assert entry["operation"] == "add"
    assert entry["result"] == 3


def test_to_json_produces_valid_json(manager):
    manager.log("add", (1, 2), 3)
    parsed = json.loads(manager.to_json())
    assert len(parsed) == 1


def test_most_common_operation(manager):
    manager.log("add", (1, 2), 3)
    manager.log("add", (2, 2), 4)
    manager.log("subtract", (5, 1), 4)
    assert manager.most_common_operation() == "add"


def test_most_common_operation_empty(manager):
    assert manager.most_common_operation() is None


def test_filter_by_operation(manager):
    manager.log("add", (1, 2), 3)
    manager.log("subtract", (5, 1), 4)
    result = manager.filter_by_operation("add")
    assert len(result) == 1


def test_clear(manager):
    manager.log("add", (1, 2), 3)
    manager.clear()
    assert manager.count() == 0


def test_count(manager):
    manager.log("add", (1, 2), 3)
    manager.log("add", (1, 2), 3)
    assert manager.count() == 2


def test_save_to_file_success(manager, tmp_path):
    manager.log("add", (1, 2), 3)
    file_path = tmp_path / "history.json"
    manager.save_to_file(str(file_path))
    assert file_path.exists()
    saved = json.loads(file_path.read_text())
    assert len(saved) == 1


def test_save_to_file_invalid_path(manager, capsys):
    manager.log("add", (1, 2), 3)
    manager.save_to_file("/nonexistent-dir/history.json")
    captured = capsys.readouterr()
    assert "Could not save history" in captured.out
