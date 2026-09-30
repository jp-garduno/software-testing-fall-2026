import datetime

CATEGORIES = ["food", "transport", "rent", "entertainment", "other"]


class Expense:
    """A single expense entry."""

    def __init__(self, amount, category, description="", date=None):
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date if date is not None else datetime.date.today()

    def is_valid(self):
        """Return True if the amount is positive and the category is known."""
        return self.amount > 0 and self.category in CATEGORIES

    def to_dict(self):
        """Serialize this expense to a plain dict."""
        return {
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": str(self.date),
        }


class ExpenseBook:
    """A collection of expenses."""

    def __init__(self, expenses=None):
        self.expenses = expenses if expenses is not None else []

    def add(self, expense):
        """Add an expense to the book if it is valid."""
        if expense.is_valid():
            self.expenses.append(expense)

    def total(self):
        """Return the sum of all expense amounts."""
        return sum(e.amount for e in self.expenses)

    def total_by_category(self, category):
        """Return the sum of amounts for a single category."""
        return sum(e.amount for e in self.expenses if e.category == category)
