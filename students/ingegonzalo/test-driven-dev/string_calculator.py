import re

MAX_VALUE = 1000
DEFAULT_DELIMITERS = [",", "\n"]


def add(numbers: str) -> int:
    if numbers == "":
        return 0
    delimiters, body = _split_header(numbers)
    values = _parse_values(body, delimiters)
    _reject_negatives(values)
    return sum(v for v in values if v <= MAX_VALUE)


def _split_header(numbers: str):
    if not numbers.startswith("//"):
        return DEFAULT_DELIMITERS, numbers
    header, body = numbers.split("\n", 1)
    custom = re.findall(r"\[(.+?)\]", header) or [header[2:]]
    return DEFAULT_DELIMITERS + custom, body


def _parse_values(body: str, delimiters: list) -> list:
    ordered = sorted(delimiters, key=len, reverse=True)
    pattern = "|".join(re.escape(d) for d in ordered)
    return [int(token) for token in re.split(pattern, body)]


def _reject_negatives(values: list) -> None:
    negatives = [v for v in values if v < 0]
    if negatives:
        raise ValueError(
            "negatives not allowed: " + ", ".join(str(n) for n in negatives)
        )