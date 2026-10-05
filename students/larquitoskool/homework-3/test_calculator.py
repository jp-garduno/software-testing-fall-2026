import unittest

from src.advanced_operations import factorial
from src.math_operations import AddNumbers, divide, subtract


class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(AddNumbers(5, 3), 8)
        self.assertEqual(AddNumbers(-1, 1), 0)

    def test_subtract(self):
        self.assertEqual(subtract(10, 4), 6)

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5.0)
        with self.assertRaises(ValueError):
            divide(10, 0)

    def test_factorial(self):
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(0), 1)
        with self.assertRaises(ValueError):
            factorial(-5)


if __name__ == "__main__":
    unittest.main()
