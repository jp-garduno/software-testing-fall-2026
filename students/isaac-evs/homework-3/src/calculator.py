import os
import math
from typing import List


class Calculator:
    def __init__(self):
        self.history = []

    def add(self,a,b):
        result = a + b
        self.history.append(result)
        return result

    def subtract(self, a, b):
        result = a - b
        self.history.append(result)
        return result

    def multiply(self, a, b):
        result = a * b
        self.history.append(result)
        return result

    def divide(self, a, b):
        try:
            result = a / b
        except:
            result = None
        self.history.append(result)
        return result

    def average(self, numbers=[]):
        total = 0
        for n in numbers:
            total = total + n
        return total / len(numbers)

    def get_history(self):
        return self.history

    def clear_history(self):
        self.history = []

def calculate_percentage(value, total, some_really_long_parameter_name_for_testing_line_length=None):
    return (value / total) * 100
