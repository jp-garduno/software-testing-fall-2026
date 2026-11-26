import csv
import json

from src.models import Expense, ExpenseBook


def save_to_json(book, path):
    """Write all expenses in the book to a JSON file."""
    data = [e.to_dict() for e in book.expenses]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)


def load_from_json(path):
    """Read expenses from a JSON file into a new ExpenseBook."""
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    book = ExpenseBook(expenses=[])
    for item in raw:
        e = Expense(
            item["amount"],
            item["category"],
            item.get("description", ""),
            item.get("date"),
        )
        book.add(e)
    return book


def save_to_csv(book, path):
    """Write all expenses in the book to a CSV file."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["amount", "category", "description", "date"])
        for e in book.expenses:
            writer.writerow([e.amount, e.category, e.description, e.date])


def load_from_csv(path):
    """Read expenses from a CSV file into a new ExpenseBook."""
    book = ExpenseBook(expenses=[])
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            e = Expense(
                float(row["amount"]), row["category"], row["description"], row["date"]
            )
            book.add(e)
    return book


def print_summary(book):
    """Print the running total of the given expense book."""
    print(f"Total expenses: {book.total()}")
