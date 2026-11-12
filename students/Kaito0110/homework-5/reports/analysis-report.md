\# White Box Testing Analysis Report



\## 1. Introduction



White box testing is a software testing technique that examines the internal structure, logic, and execution paths of an application. Unlike black box testing, which focuses on inputs and outputs without requiring knowledge of the implementation, white box testing uses knowledge of the source code to design tests. The purpose of this assignment was to apply this technique to TaskFlow, a task management application developed in Python.



The project includes task validation, repository operations, task management services, and notifications. These components provide different paths and conditions that can be tested.



\## 2. Testing Strategy



The testing strategy combined unit testing, integration testing, edge-case testing, and mocking.



Unit tests focused on individual components. They checked task creation, default values, valid and invalid priorities, task ID validation, title validation, completion, and title updates. Repository operations were also tested, including adding tasks, retrieving tasks, listing all tasks, updating existing tasks, and deleting tasks.



Integration tests verified how the service, repository, and notification components work together. For example, creating a task should store it in the repository and send a notification. Completing a task should update its completion status and send a completion notification. Error scenarios were also tested, including attempts to retrieve, update, complete, or delete tasks that do not exist.



Edge-case tests focused on inputs and situations that might be overlooked during normal testing. Examples included titles containing only spaces or tabs, empty repositories, repeated completion operations, and attempts to create tasks with invalid values.



Mocking tests used Python's `unittest.mock` library to isolate the service from its dependencies. These tests verified that repository and notification methods were called correctly and that notifications were not sent when task creation failed.



\## 3. Coverage Results



The test suite was executed using pytest and pytest-cov, including branch coverage measurement. The full test run completed with 58 passing tests.



The coverage report measured 87 statements and 16 branches across the project. No statements or branches were missed, resulting in 100% statement coverage and 100% branch coverage. Each source file included in the report reached 100% coverage.



These results exceed the assignment requirement of more than 80% coverage. The HTML report was generated in `reports/coverage-html/` to provide a detailed view of the results.



\## 4. Findings and Limitations



The results indicate that the tests exercise the statements and branches measured by pytest-cov. Testing both normal operations and error scenarios helped verify expected behavior and improve confidence in the implementation.



However, coverage is not the same as correctness. A test can execute a line of code without proving that every possible outcome is correct. The current suite also focuses on the application's implemented behavior, so additional requirements could introduce new scenarios that need testing.



\## 5. Conclusion



The assignment demonstrated how white box testing can help identify untested code paths and verify application behavior. Combining unit, integration, edge-case, and mocking tests provided different levels of verification. The final result was 58 passing tests and 100% measured statement and branch coverage. Future improvements could include additional property-based tests and more complex workflows.

