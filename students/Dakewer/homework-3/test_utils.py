"""Tests for src/helpers/utils.py.

Run from the homework-3 directory with:
    python -m pytest test_utils.py -v
or:
    python -m unittest test_utils.py -v
"""
import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from helpers.utils import get_random_phrase  # noqa: E402  pylint: disable=wrong-import-position

class TestGetRandomPhrase(unittest.TestCase):
    def test_returns_an_item_from_the_list(self):
        phrases = ["Hola", "Bienvenido", "¿Qué película buscas?"]

        result = get_random_phrase(phrases)

        self.assertIn(result, phrases)

    def test_single_item_list_always_returns_that_item(self):
        result = get_random_phrase(["Única frase"])

        self.assertEqual(result, "Única frase")

    @patch("helpers.utils.random.choice")
    def test_delegates_selection_to_random_choice(self, mock_choice):
        mock_choice.return_value = "Frase elegida"
        phrases = ["Frase A", "Frase B", "Frase elegida"]

        result = get_random_phrase(phrases)

        mock_choice.assert_called_once_with(phrases)
        self.assertEqual(result, "Frase elegida")

    def test_empty_list_raises_index_error(self):
        # random.choice raises IndexError on an empty sequence; this
        # documents that get_random_phrase does not guard against it.
        with self.assertRaises(IndexError):
            get_random_phrase([])


if __name__ == "__main__":
    unittest.main()
