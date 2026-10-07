# Homework 3: Static Testing Setup

**Student**: Carlos Rubio
**Project**: Python Interactive Calculator
**Language**: Python

## Description

This project is a console-based interactive calculator that performs basic and advanced mathematical operations, including addition, subtraction, division, factorials, and logarithms. It maintains a calculation history during runtime and was purposefully built to implement, configure, and test static analysis tools and pre-commit hooks.

## Setup Instructions

1. **Install dependencies**:
   Run the following command to install the required static testing tools:
   ```bash
   py -m pip install pre-commit pylint black isort
   ```

2. **Run the project**:
    Start the interactive calculator by running:
    ```bash
    py src/calculator.py
    ```

## Pre-commit Hooks Configured

The .pre-commit-config.yaml file includes the following hooks to enforce code quality and formatting:

- trailing-whitespace
- end-of-file-fixer
- check-yaml
- check-json
- check-added-large-files
- black
- isort
- pylint

## Testing
To run the automated unit tests for the mathematical operations, execute the following command from the root directory:
```bash
py -m unittest test_calculator.py
```