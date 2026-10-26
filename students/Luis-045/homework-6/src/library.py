"""Catalog, member registration, and library operations."""


class Library:
    """Coordinate inventory and member loans."""

    def __init__(self):
        self.catalog = {}
        self.members = {}
