"""Small collection of string manipulation helper functions."""

import re


def slugify(text):
    """Convert text into a lowercase, dash-separated slug."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def truncate(text, max_length=50):
    """Truncate text to max_length characters, appending '...' if cut."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def word_count(text):
    """Return the number of whitespace-separated words in text."""
    words = text.split()
    return len(words)


def is_palindrome(text):
    """Return True if text reads the same forwards and backwards."""
    cleaned = re.sub(r"[^a-z0-9]", "", text.lower())
    return cleaned == cleaned[::-1]


def capitalize_words(text):
    """Capitalize the first letter of every word in text."""
    result = ""
    for word in text.split(" "):
        result = result + word.capitalize() + " "
    return result.strip()


def reverse_words(text):
    """Reverse the order of words in text."""
    return " ".join(reversed(text.split()))
