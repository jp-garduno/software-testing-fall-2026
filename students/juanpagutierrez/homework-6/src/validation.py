"""Shared input validation helpers."""


def require_text(value, field_name):
    """Raise ValueError unless ``value`` is a non-blank string."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} is required")
