from src.string_utils import (
    capitalize_words,
    is_palindrome,
    reverse_words,
    slugify,
    truncate,
    word_count,
)


def test_slugify_converts_to_lowercase_dashes():
    assert slugify("Hello World!") == "hello-world"


def test_truncate_shortens_long_text():
    assert truncate("a" * 60, max_length=10) == "aaaaaaaaaa..."


def test_truncate_keeps_short_text_unchanged():
    assert truncate("short", max_length=10) == "short"


def test_word_count_counts_words():
    assert word_count("the quick brown fox") == 4


def test_is_palindrome_true_for_palindrome():
    assert is_palindrome("A man a plan a canal Panama") is True


def test_is_palindrome_false_for_non_palindrome():
    assert is_palindrome("hello world") is False


def test_capitalize_words():
    assert capitalize_words("hello world") == "Hello World"


def test_reverse_words():
    assert reverse_words("hello world") == "world hello"
