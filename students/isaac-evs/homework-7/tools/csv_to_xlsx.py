"""Build test_data/order_calculations.xlsx from the CSV: one sheet per test category.

Usage (from the homework-7 directory):  python tools/csv_to_xlsx.py
Numbers are stored as numeric cells and true/false as booleans, as they would be in a hand-made workbook.
"""

import csv
from pathlib import Path

from openpyxl import Workbook

DATA_DIR = Path(__file__).resolve().parent.parent / "test_data"
NUMERIC_COLUMNS = (
    "distance_km",
    "expected_subtotal",
    "expected_discount",
    "expected_tax",
    "expected_shipping",
    "expected_total",
)


def convert(value, column):
    """Convert a CSV text cell to the most natural Excel cell type."""
    if column in NUMERIC_COLUMNS and value != "":
        return float(value)
    if column == "is_express":
        return value == "true"
    return value if value != "" else None


def main():
    with open(DATA_DIR / "order_calculations.csv", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        header, rows = reader.fieldnames, list(reader)
    workbook = Workbook()
    workbook.remove(workbook.active)
    for category in dict.fromkeys(row["category"] for row in rows):
        sheet = workbook.create_sheet(category)
        sheet.append(header)
        for row in rows:
            if row["category"] == category:
                sheet.append([convert(row[column], column) for column in header])
    workbook.save(DATA_DIR / "order_calculations.xlsx")
    print(f"wrote {len(workbook.sheetnames)} sheets: {', '.join(workbook.sheetnames)}")


if __name__ == "__main__":
    main()
