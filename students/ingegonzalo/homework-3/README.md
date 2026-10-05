# Homework 3: Static Testing Setup

**Student**: Gonzalo Celis
**Project**: Personal Portfolio Site
**Language**: JavaScript

## Description

A personal portfolio site built on my Homework 1 project, showcasing my
background and projects. For this assignment I added three JavaScript
features (project search, light/dark theme toggle, smooth scrolling with
active-link highlighting) so the site has real logic to run static analysis
against.

## Setup Instructions

1. Install dependencies: `npm install`
2. Install pre-commit hooks: `pip install pre-commit && pre-commit install`
3. Open `index.html` in a browser to run the project (no build step needed)

## Pre-commit Hooks Configured

- trailing-whitespace
- end-of-file-fixer
- check-yaml
- check-json
- check-added-large-files
- prettier
- eslint

## Linting

- Run ESLint: `npm run lint` (or `npm run lint:report` to write `eslint-report.txt`)
- Run Prettier: `npm run format`
- Configuration lives in `.eslintrc.json` and `.prettierrc`
- Latest lint output is saved in `eslint-report.txt`
