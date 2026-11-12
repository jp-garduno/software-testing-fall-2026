import csv


def low_stock_report(inventory, threshold = 5):
    lines = []
    for p in inventory.low_stock(threshold):
        lines.append("{0}: {1} units left (reorder point {2})".format(p.sku, p.quantity, threshold))
    return "\n".join(lines)


def valuation_report(inventory):
    rows = []
    for sku in inventory.products:
        p = inventory.products[sku]
        rows.append({"sku": p.sku, "name": p.name, "quantity": p.quantity, "value": p.value()})
    rows.sort(key = lambda r: r["value"], reverse = True)
    return rows


def export_valuation_csv(inventory, path):
    rows = valuation_report(inventory)
    f = open(path, "w")
    writer = csv.DictWriter(f, fieldnames = ["sku", "name", "quantity", "value"])
    writer.writeheader()
    for r in rows:
        writer.writerow(r)
    f.close()
    return path


def movement_report(log):
    s = log.summary()
    return "Received {0}, issued {1}, net {2} across {3} movements. This line is intentionally very long so that the line-length rule has something to complain about.".format(s["received"], s["issued"], s["net"], s["entries"])
