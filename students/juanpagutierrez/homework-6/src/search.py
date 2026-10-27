"""Catalog search with combinable filters and sorting."""


def search_books(books, genre=None):
    """Return the ``books`` that match every given filter."""
    return [book for book in books if genre is None or book.genre == genre]
