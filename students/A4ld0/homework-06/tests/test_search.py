import pytest
from src.book import Book


def test_book_search_metadata():
    book = Book("1234567890", "Dune", "Herbert", genre="Sci-Fi", publication_year=1965, rating=4.5)
    assert (book.genre, book.publication_year, book.rating) == ("Sci-Fi", 1965, 4.5)


def test_search_exact_genre(library):
    library.add_book(Book("0000000000", "Other", "Author", genre="Sci-Fi"))
    assert [b.isbn for b in library.search_books(genre="Sci-Fi")] == ["0000000000"]


def test_search_publication_year(library):
    library.add_book(Book("0000000000", "Other", "Author", publication_year=1965))
    assert [b.isbn for b in library.search_books(publication_year=1965)] == ["0000000000"]


@pytest.mark.parametrize("rating", [0, 4.5])
def test_search_exact_rating(library, rating):
    library.add_book(Book("0000000000", "Other", "Author", rating=rating))
    assert [b.isbn for b in library.search_books(rating=rating)] == ["0000000000"]


def test_search_default_title_order(library):
    library.add_book(Book("0000000000", "Atlas", "Author"))
    assert [b.title for b in library.search_books()] == ["Atlas", "Dune"]


@pytest.mark.parametrize("field", ["author", "publication_year", "rating"])
def test_search_configurable_sort(library, field):
    library.add_book(Book("0000000000", "Atlas", "Zed", publication_year=2000, rating=5))
    library.add_book(Book("1111111111", "Zebra", "Abel", publication_year=1900, rating=1))
    expected = ["1111111111", "1234567890", "0000000000"] if field == "author" else [
        "1111111111", "0000000000", "1234567890"]
    assert [b.isbn for b in library.search_books(sort_by=field)] == expected


def test_search_invalid_sort(library):
    with pytest.raises(ValueError, match="sort"):
        library.search_books(sort_by="available_copies")


def test_search_text_order_ignores_case(library):
    library.add_book(Book("0000000000", "atlas", "Author"))
    assert [b.title for b in library.search_books()] == ["atlas", "Dune"]
