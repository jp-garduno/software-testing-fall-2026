"""Statistics module for computing descriptive statistics.

Provides functions to compute mean, median, mode, standard deviation,
variance, and other common statistical measures.
"""

import math
from collections import Counter


def mean(data):
    """Compute the arithmetic mean of a list of numbers.

    Args:
        data: A non-empty list of numeric values.

    Returns:
        The arithmetic mean.

    Raises:
        ValueError: If data is empty.
    """
    if not data:
        raise ValueError("Cannot compute mean of empty list")
    return sum(data) / len(data)


def median(data):
    """Compute the median of a list of numbers.

    Args:
        data: A non-empty list of numeric values.

    Returns:
        The median value.

    Raises:
        ValueError: If data is empty.
    """
    if not data:
        raise ValueError("Cannot compute median of empty list")
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2
    return sorted_data[mid]


def mode(data):
    """Compute the mode(s) of a list of numbers.

    Args:
        data: A non-empty list of numeric values.

    Returns:
        A list of the most frequent value(s).

    Raises:
        ValueError: If data is empty.
    """
    if not data:
        raise ValueError("Cannot compute mode of empty list")
    counter = Counter(data)
    max_count = max(counter.values())
    return [value for value, count in counter.items() if count == max_count]


def variance(data, population=True):
    """Compute the variance of a list of numbers.

    Args:
        data: A non-empty list of numeric values.
        population: If True, compute population variance; otherwise sample.

    Returns:
        The variance.

    Raises:
        ValueError: If data is empty or sample variance with one element.
    """
    if not data:
        raise ValueError("Cannot compute variance of empty list")
    if not population and len(data) < 2:
        raise ValueError("Sample variance requires at least 2 data points")
    data_mean = mean(data)
    squared_diffs = [(x - data_mean) ** 2 for x in data]
    divisor = len(data) if population else len(data) - 1
    return sum(squared_diffs) / divisor


def std_dev(data, population=True):
    """Compute the standard deviation of a list of numbers.

    Args:
        data: A non-empty list of numeric values.
        population: If True, compute population std dev; otherwise sample.

    Returns:
        The standard deviation.

    Raises:
        ValueError: If data is empty.
    """
    return math.sqrt(variance(data, population))


def percentile(data, percent):
    """Compute a percentile of a list of numbers.

    Args:
        data: A non-empty list of numeric values.
        percent: The percentile to compute (0–100).

    Returns:
        The value at the given percentile.

    Raises:
        ValueError: If data is empty or percent is out of range.
    """
    if not data:
        raise ValueError("Cannot compute percentile of empty list")
    if not 0 <= percent <= 100:
        raise ValueError("Percentile must be between 0 and 100")
    sorted_data = sorted(data)
    index = (percent / 100) * (len(sorted_data) - 1)
    lower = int(index)
    upper = lower + 1
    if upper >= len(sorted_data):
        return sorted_data[lower]
    fraction = index - lower
    return sorted_data[lower] + fraction * (sorted_data[upper] - sorted_data[lower])


def summary(data):
    """Return a dictionary of descriptive statistics for a dataset.

    Args:
        data: A non-empty list of numeric values.

    Returns:
        A dict with keys: min, max, mean, median, mode, std_dev, variance.
    """
    if not data:
        raise ValueError("Cannot summarize empty data")
    return {
        "min": min(data),
        "max": max(data),
        "mean": mean(data),
        "median": median(data),
        "mode": mode(data),
        "std_dev": std_dev(data),
        "variance": variance(data),
        "count": len(data),
    }
