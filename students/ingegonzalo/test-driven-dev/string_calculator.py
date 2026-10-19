def add(numbers: str) -> int:
    if numbers == "":
        return 0
    if numbers.startswith("//"):
        header, numbers = numbers.split("\n", 1)
        numbers = numbers.replace(header[2:], ",")
    numbers = numbers.replace("\n", ",")
    return sum(int(n) for n in numbers.split(","))