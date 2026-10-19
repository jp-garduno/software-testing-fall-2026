def add(numbers: str) -> int:
    if numbers == "":
        return 0
    numbers = numbers.replace("\n", ",")
    return sum(int(n) for n in numbers.split(","))