"""Catalog search with combinable filters and sorting."""


def search_books(books, genre=None, publication_year=None, min_rating=None):
    """Return the ``books`` that match every given filter."""
    return [book for book in books
            if (genre is None or book.genre == genre)
            and (publication_year is None or book.publication_year == publication_year)
            and (min_rating is None or (book.rating is not None and book.rating >= min_rating))]
