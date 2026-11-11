"""Excel loader (bonus option D): order cases from a workbook, one sheet per category.

Kept apart from case_loaders.py so only the Excel tests need openpyxl.
"""

import pytest
from openpyxl import load_workbook

from case_loaders import DATA_DIR, order_case


def load_order_workbook(filename):
    """Read the order cases of every sheet in a workbook.

    Each sheet is one test category: its first row holds the column names (the
    same as the CSV) and every other row is a case. Cells can be typed (numbers,
    TRUE/FALSE) or plain text. The sheet name becomes part of the test id, for
    example "Shipping:shipping_weight_only", so `pytest -k Shipping` runs one sheet.
    """
    workbook = load_workbook(DATA_DIR / filename, data_only=True)
    params = []
    for sheet in workbook.worksheets:
        rows = sheet.iter_rows(values_only=True)
        columns = next(rows)
        for cells in rows:
            if all(cell is None for cell in cells):
                continue  # blank row left at the bottom of a sheet
            case = order_case(dict(zip(columns, cells)))
            params.append(pytest.param(case, id=f"{sheet.title}:{case['test_name']}"))
    return params
