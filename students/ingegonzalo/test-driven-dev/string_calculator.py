import re
def add(numbers: str) -> int:
    if numbers == "":
        return 0
    if numbers.startswith("//"):
        header, numbers = numbers.split("\n", 1)
        delimiters = re.findall(r"\[(.+?)\]", header) or [header[2:]]
        for delimiter in delimiters:
            numbers = numbers.replace(delimiter, ",")
    numbers = numbers.replace("\n", ",")
    values = [int(n) for n in numbers.split(",")]
    negatives = [v for v in values if v < 0]
    if negatives:
        raise ValueError(
            "negatives not allowed: " + ", ".join(str(v) for v in negatives)
        )
    return sum(v for v in values if v <= 1000)