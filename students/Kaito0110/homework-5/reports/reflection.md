\# Reflection on White Box Testing



Working on this assignment helped me understand how white box testing can be used to examine the internal logic of an application. Before doing these tests, it was easier to think about testing only in terms of whether a feature worked correctly. However, this project showed me the importance of checking different conditions, error scenarios, and execution paths.



One of the most useful parts was creating tests for invalid inputs and edge cases. For example, a task title containing only spaces should not be accepted, and operations involving a task that does not exist should return an error. These situations might not appear during normal use, but they are important for making an application more reliable.



I also learned the difference between unit and integration testing. Unit tests helped me verify individual components, while integration tests checked whether the service, repository, and notification system worked together as expected. Mocking was useful because it allowed me to verify interactions without depending on the actual implementations of other components.



Using pytest-cov helped me measure statement and branch coverage. Reaching 100% coverage was a useful result because it showed that all measured statements and branches had been executed during testing. However, I also learned that high coverage does not automatically mean that software is completely correct. The quality of the test cases matters as much as the coverage percentage.



Overall, this assignment helped me practice writing structured tests, identifying edge cases, and interpreting coverage reports. In future projects, I would apply these techniques throughout development instead of waiting until the end to test the application.

