
from fizzbuzz import fizzbuzz


class TestFizzBuzz:

    # Divisible entre 3
    def test_fizzbuzz_on_three(self):
        assert fizzbuzz(3) == 'Fizz'

    def test_fizzbuzz_on_six(self):
        assert fizzbuzz(6) == 'Fizz'

    def test_fizzbuzz_on_twentyseven(self):
        assert fizzbuzz(27) == 'Fizz'
