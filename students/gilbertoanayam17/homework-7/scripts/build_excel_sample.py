"""Build test_data/order_calculations.xlsx from order_calculations.csv (bonus option D).

The workbook holds the same cases as the CSV, split into one sheet per test
category. The category of a case is the first word of its test_name.

Run from the homework-7 directory:  python scripts/build_excel_sample.py
"""

import csv
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font

DATA_DIR = Path(__file__).resolve().parent.parent / "test_data"

# test_name prefix -> sheet name
CATEGORY_SHEETS = {
    "simple": "Simple",
    "discount": "Discounts",
    "tax": "Tax",
    "shipping": "Shipping",
    "complex": "Complex",
}


def typed(column, text):
    """Store a CSV value the way a person would type it in Excel.

    Amounts and distances become numbers and is_express becomes TRUE/FALSE;
    everything else stays as text.
    """
    if column == "is_express":
        return text == "true"
    if column == "distance_km" or column.startswith("expected_"):
        return float(text)
    return text


def main():
    """Write one sheet per category, with a bold, frozen header row."""
    with open(DATA_DIR / "order_calculations.csv", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        columns = reader.fieldnames
        rows = list(reader)

    workbook = Workbook()
    workbook.remove(workbook.active)
    for prefix, title in CATEGORY_SHEETS.items():
        sheet = workbook.create_sheet(title)
        sheet.append(columns)
        for cell in sheet[1]:
            cell.font = Font(bold=True)
        sheet.freeze_panes = "A2"
        sheet.column_dimensions["A"].width = 42
        sheet.column_dimensions["B"].width = 60

        for row in rows:
            if row["test_name"].startswith(f"{prefix}_"):
                sheet.append([typed(column, row[column]) for column in columns])
        print(f"{title}: {sheet.max_row - 1} cases")

    workbook.save(DATA_DIR / "order_calculations.xlsx")


if __name__ == "__main__":
    main()
