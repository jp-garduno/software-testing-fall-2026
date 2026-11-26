"""Advanced feature 3: search with genre/year/rating filters and sorting."""

import pytest

from src.book import Book


def titles(books):
    return [book.title for book in books]


def test_search_without_filters_returns_whole_catalog(library):
    assert len(library.search()) == 3


def test_search_by_genre_is_case_insensitive(library):
    assert titles(library.search(genre="programming")) == ["Clean Code", "Refactoring"]


def test_search_by_year(library):
    assert titles(library.search(year=2002)) == ["Test Driven Development: By Example"]


def test_search_by_minimum_rating_is_inclusive(library):
    assert titles(library.search(min_rating=4.4)) == ["Clean Code", "Refactoring"]


def test_filters_are_combined_with_and_logic(library):
    assert titles(library.search(genre="Programming", min_rating=4.5)) == ["Refactoring"]


def test_search_returns_empty_list_when_no_book_matches_all_filters(library):
    assert library.search(genre="Testing", year=2018) == []


def test_books_without_rating_never_match_a_rating_filter(library):
    library.add_book(Book("1111111111", "Unrated", "Anon", genre="Programming"))
    assert "Unrated" not in titles(library.search(min_rating=0))


def test_books_without_genre_never_match_a_genre_filter(library):
    library.add_book(Book("1111111111", "No Genre", "Anon"))
    assert "No Genre" not in titles(library.search(genre="Programming"))


def test_results_can_be_sorted_by_title(library):
    assert titles(library.search(sort_by="title")) == [
        "Clean Code",
        "Refactoring",
        "Test Driven Development: By Example",
    ]


def test_results_can_be_sorted_by_rating_descending(library):
    assert titles(library.search(sort_by="rating", descending=True)) == [
        "Refactoring",
        "Clean Code",
        "Test Driven Development: By Example",
    ]


@pytest.mark.parametrize("descending", [False, True])
def test_books_missing_the_sort_field_go_last(library, descending):
    library.add_book(Book("1111111111", "Undated", "Anon"))
    assert titles(library.search(sort_by="year", descending=descending))[-1] == "Undated"


def test_sorting_by_unknown_field_raises(library):
    with pytest.raises(ValueError, match="Cannot sort"):
        library.search(sort_by="isbn")
