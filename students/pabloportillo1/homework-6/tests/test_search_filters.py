import pytest

from book import Book, BookDetails
from library import Library

CATALOG = [
    ("0306406152", "Clean Code", "Robert Martin", BookDetails("Software", 2008, 4.4)),
    ("0131103628", "The C Programming Language", "Brian Kernighan", BookDetails("Software", 1988, 4.7)),
    ("0201633612", "Design Patterns", "Erich Gamma", BookDetails("Software", 1994, 4.5)),
    ("0141439513", "Pride and Prejudice", "Jane Austen", BookDetails("Fiction", 1813, 4.3)),
    ("0061120084", "To Kill a Mockingbird", "Harper Lee", BookDetails("Fiction", 1960)),
]


@pytest.fixture(name="library")
def fixture_library():
    library = Library()
    for isbn, title, author, details in CATALOG:
        library.add_book(Book(isbn, title, author, details=details))
    return library


def titles(books):
    return [book.title for book in books]


def test_search_by_genre_returns_only_that_genre(library):
    assert set(titles(library.search(genre="Fiction"))) == {"Pride and Prejudice", "To Kill a Mockingbird"}


def test_search_without_criteria_returns_the_whole_catalog(library):
    assert len(library.search()) == len(CATALOG)


def test_search_by_genre_and_year_requires_both(library):
    assert titles(library.search(genre="Software", year=1994)) == ["Design Patterns"]


def test_search_by_minimum_rating_keeps_books_at_or_above_it(library):
    assert set(titles(library.search(min_rating=4.5))) == {"The C Programming Language", "Design Patterns"}


def test_search_results_are_sorted_by_title_by_default(library):
    assert titles(library.search(genre="Software")) == [
        "Clean Code",
        "Design Patterns",
        "The C Programming Language",
    ]


def test_search_sorted_by_rating_lists_the_best_rated_first(library):
    assert titles(library.search(genre="Software", sort_by="rating")) == [
        "The C Programming Language",
        "Design Patterns",
        "Clean Code",
    ]


def test_unrated_books_come_last_when_sorting_by_rating(library):
    assert titles(library.search(sort_by="rating"))[-1] == "To Kill a Mockingbird"


def test_search_sorted_by_year_lists_the_oldest_first(library):
    assert titles(library.search(genre="Software", sort_by="year")) == [
        "The C Programming Language",
        "Design Patterns",
        "Clean Code",
    ]
