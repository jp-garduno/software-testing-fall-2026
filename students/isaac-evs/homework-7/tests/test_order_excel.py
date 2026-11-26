"""Order calculation tests driven by an Excel workbook with one sheet per test category (bonus option D)."""

import re

import pytest
from data_loader import (
    COMPONENTS,
    ORDER_XLSX,
    load_order_cases,
    load_order_cases_xlsx,
    parse_order_row,
    read_order_rows,
    read_order_rows_xlsx,
    run_order_case,
)
from openpyxl import load_workbook


@pytest.mark.parametrize("case", load_order_cases_xlsx())
def test_order_calculation_from_excel(case):
    result = run_order_case(case)
    for component in COMPONENTS:
        assert result[component] == pytest.approx(case["expected"][component], abs=0.005), f"{component} mismatch"


@pytest.mark.parametrize("case", load_order_cases_xlsx(error_cases=True))
def test_invalid_input_from_excel_is_rejected(case):
    with pytest.raises(ValueError, match=re.escape(case["expected_error"])):
        run_order_case(case)


def test_workbook_has_one_sheet_per_category():
    categories = {row["category"] for row in read_order_rows()}
    sheets = load_workbook(ORDER_XLSX, read_only=True).sheetnames
    assert set(sheets) == categories
    assert len(sheets) == len(categories)


def test_every_row_sits_on_the_sheet_of_its_category():
    workbook = load_workbook(ORDER_XLSX, read_only=True, data_only=True)
    for sheet in workbook.worksheets:
        header, *body = list(sheet.iter_rows(values_only=True))
        category_column = header.index("category")
        assert {row[category_column] for row in body} == {sheet.title}


def test_excel_and_csv_describe_the_same_cases():
    """The workbook is generated from the CSV; this fails if one is edited without the other."""
    from_csv = {case["test_name"]: case for case in map(parse_order_row, read_order_rows())}
    from_xlsx = {case["test_name"]: case for case in map(parse_order_row, read_order_rows_xlsx())}
    assert from_xlsx == from_csv


def test_both_sources_yield_the_same_number_of_params():
    assert len(load_order_cases_xlsx()) == len(load_order_cases())
    assert len(load_order_cases_xlsx(error_cases=True)) == len(load_order_cases(error_cases=True))
