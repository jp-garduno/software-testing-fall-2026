import statistics

from src.models import CATEGORIES


def category_breakdown(book):
    """Return a dict mapping each category to its total amount."""
    return {cat: book.total_by_category(cat) for cat in CATEGORIES}


def average_expense(book):
    """Return the mean expense amount, or 0 if the book is empty."""
    if not book.expenses:
        return 0
    amounts = [e.amount for e in book.expenses]
    return statistics.mean(amounts)


def biggest_expense(book):
    """Return the single largest expense, or None if the book is empty."""
    biggest = None
    for e in book.expenses:
        if biggest is None or e.amount > biggest.amount:
            biggest = e
    return biggest


def monthly_total(book, year, month):
    """Return the total amount spent in a given year/month."""
    return sum(
        e.amount for e in book.expenses if e.date.year == year and e.date.month == month
    )


def percentage_by_category(book):
    """Return a dict mapping each category to its percentage of the total."""
    grand_total = book.total()
    result = {}
    for cat in CATEGORIES:
        cat_total = book.total_by_category(cat)
        result[cat] = 0 if grand_total == 0 else (cat_total / grand_total) * 100
    return result


class ReportBuilder:
    """Builds a human-readable text report for an expense book."""

    def __init__(self, book):
        self.book = book

    def build(self):
        """Return the report as a multi-line string."""
        lines = ["Expense Report", f"total: {self.book.total()}"]
        for cat, pct in percentage_by_category(self.book).items():
            lines.append(f"{cat}: {pct:.2f}%")
        return "\n".join(lines)
