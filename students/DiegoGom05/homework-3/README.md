# Homework 3: Static Testing Setup

**Student**: Diego Gómez Ortiz
**Project**: Homework-3
**Language**: Javascript

## Description

This project is a simple calculator implemented using JavaScript, HTML, and CSS. It supports basic arithmetic operations such as addition, subtraction, multiplication, and division, including decimal numbers and error handling for division by zero.

## Setup Instructions

1. Install the project dependencies:
   npm install
2. Install the pre-commit hooks:
   pre-commit install
3. Run the project by opening index.html in a web browser.

## Pre-commit Hooks Configured

trailing-whitespace – Removes trailing whitespace.
end-of-file-fixer – Ensures files end with a newline.
check-yaml – Validates YAML files.
check-json – Validates JSON files.
check-added-large-files – Prevents accidentally committing large files.
prettier – Formats JavaScript, HTML, CSS, JSON, and YAML files.

## Testing

To run ESLint and check the JavaScript code for potential problems:

npx eslint .

To run Prettier:

npx prettier --write .

To run all configured pre-commit hooks manually:

pre-commit run --all-files
