import pytest
from src.book import Book
from src.library import Library


@pytest.fixture
def catalog():
    lib = Library()
    b1 = Book(
        isbn="1111111111",
        title="Refactoring",
        author="Martin Fowler",
        genre="Software Engineering",
        year=1999,
        rating=4.7,
    )
    b2 = Book(
        isbn="2222222222",
        title="Clean Code",
        author="Robert Martin",
        genre="Software Engineering",
        year=2008,
        rating=4.5,
    )
    b3 = Book(
        isbn="3333333333",
        title="Design Patterns",
        author="Gang of Four",
        genre="Software Architecture",
        year=1994,
        rating=4.8,
    )
    b4 = Book(
        isbn="4444444444",
        title="Introduction to Algorithms",
        author="Cormen et al.",
        genre="Computer Science",
        year=2009,
        rating=4.6,
    )
    lib.add_book(b1)
    lib.add_book(b2)
    lib.add_book(b3)
    lib.add_book(b4)
    return lib, b1, b2, b3, b4


def test_filter_by_genre(catalog):
    lib, b1, b2, b3, b4 = catalog
    results = lib.filter_books(genre="Software Engineering")
    assert results == [b1, b2]


def test_filter_by_year_range(catalog):
    lib, b1, b2, b3, b4 = catalog
    results = lib.filter_books(year_from=2000, year_to=2010)
    assert set(results) == {b2, b4}


def test_filter_by_min_rating(catalog):
    lib, b1, b2, b3, b4 = catalog
    results = lib.filter_books(min_rating=4.7)
    assert set(results) == {b1, b3}


def test_filter_combined_and_logic(catalog):
    lib, b1, b2, b3, b4 = catalog
    results = lib.filter_books(
        genre="Software Engineering",
        year_to=2000,
        min_rating=4.6,
    )
    assert results == [b1]


def test_filter_and_sort_by_year_descending(catalog):
    lib, b1, b2, b3, b4 = catalog
    results = lib.filter_books(sort_by="year", reverse=True)
    assert [b.year for b in results] == [2009, 2008, 1999, 1994]


def test_filter_and_sort_by_rating_ascending(catalog):
    lib, b1, b2, b3, b4 = catalog
    results = lib.filter_books(sort_by="rating", reverse=False)
    assert [b.rating for b in results] == [4.5, 4.6, 4.7, 4.8]


def test_filter_and_sort_by_title_alphabetical(catalog):
    lib, b1, b2, b3, b4 = catalog
    results = lib.filter_books(sort_by="title")
    assert results[0].title == "Clean Code"
    assert results[-1].title == "Refactoring"


def test_filter_books_handles_missing_attributes_and_unknown_sort():
    lib = Library()
    b1 = Book("1111111111", "Book Without Meta", "Author")
    lib.add_book(b1)

    assert lib.filter_books(genre="Fiction") == []
    assert lib.filter_books(year_from=2000) == []
    assert lib.filter_books(year_to=2000) == []
    assert lib.filter_books(min_rating=4.0) == []

    # Sort with books lacking year/rating
    assert lib.filter_books(sort_by="year") == [b1]
    assert lib.filter_books(sort_by="rating") == [b1]
    assert lib.filter_books(sort_by="unsupported_key") == [b1]
