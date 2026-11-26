\# TaskFlow - White Box Testing \& Coverage



\## Description



TaskFlow is a simple task management application developed in Python. It allows users to create, retrieve, list, update, complete, and delete tasks.



The project was developed to practice white box testing, including unit testing, integration testing, edge-case testing, mocking, and code coverage measurement.



\## Project Structure



\- `src/task.py`: Task model and input validation.

\- `src/task\_repository.py`: Stores and manages tasks.

\- `src/task\_service.py`: Implements task management operations.

\- `src/notification\_service.py`: Handles task notifications.

\- `tests/test\_task\_unit.py`: Unit tests.

\- `tests/test\_task\_service\_integration.py`: Integration tests.

\- `tests/test\_coverage\_edge\_cases.py`: Edge-case tests.

\- `tests/test\_mocking.py`: Mocking tests.

\- `reports/coverage-analysis.md`: Coverage results and analysis.

\- `reports/analysis-report.md`: White box testing analysis.

\- `reports/reflection.md`: Personal reflection.

\- `reports/coverage-html/`: Generated HTML coverage report.

\- `reports/screenshots/`: Screenshots of testing evidence.



\## Requirements



\- Python 3

\- pytest

\- pytest-cov



Install the dependencies with:



```bash

python -m pip install -r requirements.txt

```



\## Running the Tests



Run the complete test suite:



```bash

python -m pytest -v

```



Run tests with statement and branch coverage:



```bash

python -m pytest -v --cov=src --cov-branch --cov-report=term-missing --cov-report=html:reports/coverage-html

```



\## Testing Strategy



The project includes unit tests for individual components, integration tests for interactions between services, edge-case tests for invalid inputs and repeated operations, and mocking tests using `unittest.mock`.



The tests verify normal behavior, validation rules, error handling, repository operations, and notification calls.



\## Results



The complete test suite contains 58 tests, and all 58 passed in the full test run.



The measured statement coverage and branch coverage were both 100%. These results exceed the assignment target of more than 80%.



The HTML coverage report is generated in `reports/coverage-html/index.html`.



\## Limitations



High code coverage does not guarantee that an application is free of defects. The tests measure the execution of statements and branches, but additional requirements and scenarios could be added in future versions.

