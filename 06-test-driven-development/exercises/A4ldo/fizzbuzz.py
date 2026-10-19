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

def test_returns_number_for_non_multiple_of_three_or_five():
    assert fizzbuzz(7) == 7

def FizzBuzz(n):
    if n % 3 == 0 and n % 5 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    else:
        return str(n)