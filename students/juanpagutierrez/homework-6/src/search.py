"""Catalog search with combinable filters and sorting."""

SORTABLE_FIELDS = ("title", "author", "publication_year", "rating")


def _matches(book, genre, publication_year, min_rating):
    checks = [
        genre is None or book.genre == genre,
        publication_year is None or book.publication_year == publication_year,
        min_rating is None or (book.rating is not None and book.rating >= min_rating),
    ]
    return all(checks)


def search_books(books, genre=None, publication_year=None, min_rating=None, sort_by=None, descending=False):
    """Return the ``books`` that match every given filter (AND logic), optionally sorted."""
    results = [book for book in books if _matches(book, genre, publication_year, min_rating)]
    if sort_by is not None and sort_by not in SORTABLE_FIELDS:
        raise ValueError(f"Cannot sort by {sort_by!r}; choose one of {', '.join(SORTABLE_FIELDS)}")
    if sort_by is not None:
        results = _sorted(results, sort_by, descending)
    return results


def _sorted(books, field, descending):
    """Sort by ``field``; books without a value always go last."""
    with_value = [book for book in books if getattr(book, field) is not None]
    without_value = [book for book in books if getattr(book, field) is None]
    with_value.sort(key=lambda book: getattr(book, field), reverse=descending)
    return with_value + without_value
