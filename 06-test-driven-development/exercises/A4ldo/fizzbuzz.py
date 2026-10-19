def test_returns_one():
    assert fizzbuzz(1) == 1

def test_returns_fizz():
    assert fizzbuzz(3) == "Fizz"

def test_returns_fizz_for_multiple_of_three():
    assert fizzbuzz(6) == "Fizz"

def test_returns_buzz():
    assert fizzbuzz(5) == "Buzz"

def test_returns_buzz_for_multiple_of_five():
    assert fizzbuzz(10) == "Buzz"

def test_returns_fizzbuzz():
    assert fizzbuzz(15) == "FizzBuzz"

def test_returns_fizzbuzz_for_multiple_of_three_and_five():
    assert fizzbuzz(30) == "FizzBuzz"