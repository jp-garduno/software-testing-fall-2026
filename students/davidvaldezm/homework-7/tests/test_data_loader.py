"""Check that bad fixtures fail with actionable source locations."""

import pytest

from tests import data_loader


@pytest.fixture(name="fixture_file")
def fixture_file_writer(tmp_path, monkeypatch):
    """Write an isolated fixture in the loader's data directory."""
    monkeypatch.setattr(data_loader, "DATA_DIR", tmp_path)

    def write(filename, contents):
        (tmp_path / filename).write_text(contents, encoding="utf-8")
        return filename

    return write


def test_reports_bad_csv_header(fixture_file):
    """Reject a CSV with missing required columns."""
    path = fixture_file("bad.csv", "test_name,items\n")
    with pytest.raises(ValueError, match=r"bad\.csv:1: unexpected CSV header"):
        data_loader.order_cases(path)


def test_reports_bad_csv_type(fixture_file):
    """Report the CSV column and row for an invalid boolean."""
    header = ",".join(data_loader.ORDER_CASE["required"])
    row = "sample,[],regular,NONE,0,yes,,,0,0,0,0,0"
    path = fixture_file("bad.csv", f"{header}\n{row}\n")
    with pytest.raises(ValueError, match=r"bad\.csv:2: is_express"):
        data_loader.order_cases(path)


def test_reports_json_syntax(fixture_file):
    """Preserve the JSON decoder's line number for syntax errors."""
    path = fixture_file("bad.json", '[\n  {"test_name": }\n]')
    with pytest.raises(ValueError, match=r"bad\.json:2: Expecting value"):
        data_loader.json_cases(path)


def test_reports_json_schema(fixture_file):
    """Locate an invalid record even after a multi-line valid record."""
    path = fixture_file(
        "bad.json",
        """[
  {
    "test_name": "first",
    "as_of": "2026-11-11",
    "customer": null,
    "expected": {"is_valid": false, "errors": []}
  },
  {
    "test_name": "second",
    "as_of": "2026-13-01",
    "customer": null,
    "expected": {"is_valid": false, "errors": []}
  }
]""",
    )
    with pytest.raises(ValueError, match=r"bad\.json:8: as_of"):
        data_loader.json_cases(path)


def test_reports_missing_workflow_steps(fixture_file):
    """Check that the nested workflows array receives schema validation."""
    path = fixture_file(
        "bad.json",
        """{
  "workflows": [
    {"name": "order", "as_of": "2026-11-11", "order_id": "1",
     "payment_responses": [], "expected_charges": []}
  ]
}""",
    )
    with pytest.raises(
        ValueError, match=r"bad\.json:3:.*'steps' is a required property"
    ):
        data_loader.json_cases(path, workflows=True)
