# Homework 3 - Python Calculator

**Student**: Kaito0110
**Project**: Python Calculator
**Language**: Python

## Description

This project is a simple calculator developed in Python. The purpose of the project is to practice software testing, code quality and Git workflow.

The calculator allows the user to perform different mathematical operations through a simple menu.

## Operations

The calculator includes the following operations:

- Addition
- Subtraction
- Multiplication
- Division
- Power
- Modulo
- Average
- Greater number
- Smaller number
- Percentage

## Project Structure

```text
homework-3/
├── src/
│   ├── calculator.py
│   ├── operations.py
│   └── utils.py
├── test_calculator.py
├── .pre-commit-config.yaml
├── .pylintrc
├── requirements.txt
├── README.md
└── REPORT.md
```

## Installation

Install the required dependencies with:

```bash
pip install -r requirements.txt
```

## Run the Calculator

From the repository root, run:

```bash
python students/Kaito0110/homework-3/src/calculator.py
```

The program will display a menu where the user can select the desired operation.

## Run the Tests

To run the unit tests, use:

```bash
pytest students/Kaito0110/homework-3/test_calculator.py
```

The project currently includes 10 unit tests that verify the calculator operations.

## Pre-commit Hooks Configured

The configuration includes these checks:

- trailing whitespace and end-of-file fixer
- YAML and JSON validation
- large-file, merge-conflict and private-key detection
- Black formatting
- isort import sorting
- Pylint static analysis

Install the hooks from the repository root with:

```bash
pre-commit install
pre-commit run --files students/Kaito0110/homework-3/src/calculator.py students/Kaito0110/homework-3/src/operations.py students/Kaito0110/homework-3/src/utils.py students/Kaito0110/homework-3/test_calculator.py
```

To run the configured checks across the repository, use:

```bash
pre-commit run --all-files
```

## Code Quality

The project uses pre-commit hooks to check the code before commits. The configuration includes tools such as Black, isort and Pylint. The Pylint configuration is stored in `.pylintrc`.

These tools help maintain consistent formatting and identify possible problems in the Python code.
