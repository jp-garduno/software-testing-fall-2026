"""Reports built on top of the inventory and the movement log."""

import csv

CSV_FIELDS = ["sku", "name", "quantity", "value"]


def low_stock_report(inventory, threshold=5):
    """Return one line per product that has fallen to the reorder point."""
    lines = [
        f"{product.sku}: {product.quantity} units left (reorder point {threshold})"
        for product in inventory.low_stock(threshold)
    ]
    return "\n".join(lines)


def valuation_report(inventory):
    """Return every product with its value, most valuable first."""
    rows = [
        {
            "sku": product.sku,
            "name": product.name,
            "quantity": product.quantity,
            "value": product.value(),
        }
        for product in inventory.products.values()
    ]
    rows.sort(key=lambda row: row["value"], reverse=True)
    return rows


def export_valuation_csv(inventory, path):
    """Write the valuation report to a CSV file and return its path."""
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(valuation_report(inventory))
    return path


def movement_report(log):
    """Return a one-line summary of everything the log has recorded."""
    totals = log.summary()
    return (
        f"Received {totals['received']}, issued {totals['issued']}, "
        f"net {totals['net']} across {totals['entries']} movements."
    )
