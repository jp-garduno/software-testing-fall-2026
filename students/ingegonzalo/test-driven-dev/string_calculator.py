def add(numbers: str) -> int:
    if numbers == "":
        return 0
    if numbers.startswith("//"):
        header, numbers = numbers.split("\n", 1)
        numbers = numbers.replace(header[2:], ",")
    numbers = numbers.replace("\n", ",")
    values = [int(n) for n in numbers.split(",")]
    negatives = [v for v in values if v < 0]
    if negatives:
        raise ValueError(
            "negatives not allowed: " + ", ".join(str(v) for v in negatives)
        )
    return sum(values)