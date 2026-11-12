from tools.coverage_report import render

DATA = {
    "meta": {"version": "7.16.0", "timestamp": "2026-11-11T21:30:00"},
    "files": {
        "src/b<module>.py": {
            "summary": {
                "num_statements": 10,
                "missing_lines": 2,
                "num_branches": 4,
                "num_partial_branches": 1,
                "percent_covered": 78.57,
                "percent_covered_display": "79",
            },
            "missing_lines": [7, 9],
        },
        "src/a.py": {
            "summary": {
                "num_statements": 5,
                "missing_lines": 0,
                "num_branches": 0,
                "num_partial_branches": 0,
                "percent_covered": 100.0,
                "percent_covered_display": "100",
            },
            "missing_lines": [],
        },
    },
    "totals": {
        "num_statements": 15,
        "missing_lines": 2,
        "num_branches": 4,
        "num_partial_branches": 1,
        "percent_covered": 84.21,
        "percent_covered_display": "84",
    },
}


def test_render_lists_files_sorted_with_missing_lines():
    page = render(DATA)

    assert page.index("src/a.py") < page.index("src/b&lt;module&gt;.py") < page.index('<td class="missing">7, 9</td>')


def test_render_marks_incomplete_coverage_as_partial():
    page = render(DATA)

    assert '<td class="partial">79%</td>' in page and "<h1>Homework 7 coverage: 84%</h1>" in page
