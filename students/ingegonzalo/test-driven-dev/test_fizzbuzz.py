
from fizzbuzz import fizzbuzz


class TestFizzBuzz:

    # Divisible entre 3
    def test_fizzbuzz_on_three(self):
        assert fizzbuzz(3) == 'Fizz'

    def test_fizzbuzz_on_six(self):
        assert fizzbuzz(6) == 'Fizz'

    def test_fizzbuzz_on_twentyseven(self):
        assert fizzbuzz(27) == 'Fizz'

    # Divisible entre 5
    def test_fizzbuzz_on_five(self):
        assert fizzbuzz(5) == 'Buzz'
    
    def test_fizzbuzz_on_ten(self):
        assert fizzbuzz(10) == 'Buzz'
    
    # Divisible entre 3 y 5
    def test_fizzbuzz_on_fifteen(self):
        assert fizzbuzz(15) == 'FizzBuzz'
        
    def test_fizzbuzz_on_thirty(self):
        assert fizzbuzz(30) == 'FizzBuzz'
