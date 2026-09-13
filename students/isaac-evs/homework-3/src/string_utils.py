import re


def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def truncate(text, max_length=50):
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def word_count(text):
    words = text.split()
    return len(words)

def is_palindrome(text):
    cleaned = re.sub(r'[^a-z0-9]', '', text.lower())
    return cleaned == cleaned[::-1]

def capitalize_words(text):
    result = ""
    for word in text.split(" "):
        result = result + word.capitalize() + " "
    return result.strip()

def reverse_words(text):
    return " ".join(reversed(text.split()))
