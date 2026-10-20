

\# Coverage Analysis



\## Overview



The TaskFlow project was tested using pytest and pytest-cov.

The goal was to check statement coverage and branch coverage,

including normal operations and error scenarios.



\## Results



The complete test suite contains 58 tests, and all 58 passed.



| Metric | Result |

|---|---:|

| Statements | 87 |

| Statements missed | 0 |

| Branches | 16 |

| Partial branches | 0 |

| Total coverage | 100% |



\## File Coverage



| File | Coverage |

|---|---:|

| src/\_\_init\_\_.py | 100% |

| src/notification\_service.py | 100% |

| src/task.py | 100% |

| src/task\_repository.py | 100% |

| src/task\_service.py | 100% |



\## Testing Approach



Unit tests check task creation, validation, title updates,

completion, and repository operations.



Integration tests check the interaction between the task

service, repository, and notification service.



Edge-case tests cover invalid inputs, empty repositories,

repeated operations, and missing tasks.



Mocking tests use unittest.mock to verify service interactions

without depending on real repository or notification objects.



\## Conclusion



The measured statement and branch coverage is 100%, which

exceeds the required target of more than 80%.



All 58 tests passed during the full test run. The results show

that the current tests cover the statements and branches

reported by pytest-cov.



Coverage does not guarantee that software has no defects, but

it helps identify code paths that have not been exercised.



The HTML report was generated in reports/coverage-html and

can be opened to inspect the detailed results.



