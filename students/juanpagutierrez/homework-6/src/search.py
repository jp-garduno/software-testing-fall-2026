"""Catalog search with combinable filters and sorting."""


def _matches(book, genre, publication_year, min_rating):
    checks = [
        genre is None or book.genre == genre,
        publication_year is None or book.publication_year == publication_year,
        min_rating is None or (book.rating is not None and book.rating >= min_rating),
    ]
    return all(checks)


def search_books(books, genre=None, publication_year=None, min_rating=None, sort_by=None):
    """Return the ``books`` that match every given filter (AND logic), optionally sorted."""
    results = [book for book in books if _matches(book, genre, publication_year, min_rating)]
    if sort_by is not None:
        results.sort(key=lambda book: getattr(book, sort_by))
    return results
