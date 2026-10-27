"""Catalog search with combinable filters and sorting."""

from dataclasses import dataclass
from typing import Optional

SORTABLE_FIELDS = ("title", "author", "publication_year", "rating")


@dataclass(frozen=True)
class SearchQuery:
    """Filters combined with AND logic, plus an optional sort order."""

    genre: Optional[str] = None
    publication_year: Optional[int] = None
    min_rating: Optional[float] = None
    sort_by: Optional[str] = None
    descending: bool = False

    def __post_init__(self):
        if self.sort_by is not None and self.sort_by not in SORTABLE_FIELDS:
            raise ValueError(f"Cannot sort by {self.sort_by!r}; choose one of {', '.join(SORTABLE_FIELDS)}")

    def matches(self, book):
        """True when ``book`` satisfies every filter that was given."""
        checks = [
            self.genre is None or book.genre == self.genre,
            self.publication_year is None or book.publication_year == self.publication_year,
            self.min_rating is None or (book.rating is not None and book.rating >= self.min_rating),
        ]
        return all(checks)

    def run(self, books):
        """Return the matching ``books``, sorted if a sort field was given."""
        results = [book for book in books if self.matches(book)]
        if self.sort_by is None:
            return results
        return _sorted(results, self.sort_by, self.descending)


def _sorted(books, field, descending):
    """Sort by ``field``; books without a value always go last."""
    with_value = [book for book in books if getattr(book, field) is not None]
    without_value = [book for book in books if getattr(book, field) is None]
    with_value.sort(key=lambda book: getattr(book, field), reverse=descending)
    return with_value + without_value
