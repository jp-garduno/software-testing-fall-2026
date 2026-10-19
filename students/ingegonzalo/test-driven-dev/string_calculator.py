def add(numbers: str) -> int:
    if numbers == "":
        return 0
    return sum(int(n) for n in numbers.split(","))