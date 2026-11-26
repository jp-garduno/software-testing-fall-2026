"""Validator module for input validation utilities.

This module provides functions for validating common data types
such as emails, phone numbers, ages, and more.
"""

import re


def validate_email(email):
    """Validate an email address format.

    Args:
        email: The email string to validate.

    Returns:
        True if the email is valid, False otherwise.
    """
    if not isinstance(email, str):
        return False
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_age(age):
    """Validate that an age is a positive integer within a human range.

    Args:
        age: The age value to validate.

    Returns:
        True if age is between 0 and 150, False otherwise.
    """
    if not isinstance(age, int):
        return False
    return 0 <= age <= 150


def validate_phone(phone):
    """Validate a phone number (10–15 digits, optional leading +).

    Args:
        phone: The phone string to validate.

    Returns:
        True if the phone number format is valid, False otherwise.
    """
    if not isinstance(phone, str):
        return False
    pattern = r"^\+?[1-9]\d{9,14}$"
    return bool(re.match(pattern, phone))


def validate_password(password):
    """Validate password strength.

    A valid password must be at least 8 characters long, contain at least
    one uppercase letter, one lowercase letter, one digit, and one special
    character.

    Args:
        password: The password string to validate.

    Returns:
        True if the password meets strength requirements, False otherwise.
    """
    if not isinstance(password, str):
        return False
    if len(password) < 8:
        return False
    has_upper = bool(re.search(r"[A-Z]", password))
    has_lower = bool(re.search(r"[a-z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_special = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))
    return has_upper and has_lower and has_digit and has_special


def validate_url(url):
    """Validate a URL format (http or https).

    Args:
        url: The URL string to validate.

    Returns:
        True if the URL format is valid, False otherwise.
    """
    if not isinstance(url, str):
        return False
    pattern = r"^https?://[^\s/$.?#].[^\s]*$"
    return bool(re.match(pattern, url))


def validate_credit_card(card_number):
    """Validate a credit card number using the Luhn algorithm.

    Args:
        card_number: The card number string (digits only).

    Returns:
        True if the card number passes the Luhn check, False otherwise.
    """
    if not isinstance(card_number, str):
        return False
    digits = card_number.replace(" ", "").replace("-", "")
    if not digits.isdigit() or len(digits) < 13:
        return False
    total = 0
    reverse_digits = digits[::-1]
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0
