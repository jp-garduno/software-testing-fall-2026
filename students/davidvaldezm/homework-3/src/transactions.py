"""Validate and represent expense transactions."""

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation


def parse_amount(value):
    """Convert a positive amount with at most two decimal places."""
    if isinstance(value, bool):
        raise ValueError("Boolean values are not amounts")
    try:
        amount = Decimal(str(value))
    except InvalidOperation as error:
        raise ValueError("Amount must be numeric") from error
    if not amount.is_finite() or amount <= 0:
        raise ValueError("Amount must be positive and finite")
    if amount.as_tuple().exponent < -2:
        raise ValueError("Amount must have at most two decimal places")
    return amount


def normalize_category(value):
    """Normalize nonempty category names for consistent grouping."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Category must be a nonempty string")
    return value.strip().lower()


@dataclass(frozen=True)
class Transaction:
    """An immutable validated expense."""

    amount: Decimal
    category: str
    description: str = ""

    def __post_init__(self):
        """Validate even direct construction of transactions."""
        object.__setattr__(self, "amount", parse_amount(self.amount))
        object.__setattr__(self, "category", normalize_category(self.category))
        if not isinstance(self.description, str):
            raise ValueError("Description must be a string")

    def to_dict(self):
        """Return a JSON-safe representation without float rounding."""
        return {
            "amount": str(self.amount),
            "category": self.category,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, record):
        """Load a record while rejecting missing or unknown fields."""
        if not isinstance(record, dict):
            raise ValueError("Transaction must be an object")
        expected = {"amount", "category", "description"}
        if set(record) != expected:
            raise ValueError("Transaction fields do not match schema")
        return cls(**record)
