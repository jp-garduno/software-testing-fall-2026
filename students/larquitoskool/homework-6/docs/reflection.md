# TDD Reflection

**1. Design Impact**: TDD drastically influenced my design. Instead of creating a massive Library class that did everything, TDD forced me to distribute responsibilities. The Book handles its copies, the Member handles its limits, and the Library just orchestrates them. This made the API much cleaner.

**2. Challenges**: The most difficult part of test-first development was predicting the exact edge cases before writing the code. Thinking about what exceptions should be raised (like borrowing an unavailable book) before the logic existed felt unnatural at first.

**3. Benefits**: The biggest advantage was the absolute confidence during refactoring. When I changed the Member categories to use a dictionary, the tests instantly confirmed I hadn't broken the borrowing limits.

**4. Comparison**: Compared to test-after, TDD prevents "testing bias" (writing tests just to pass the code you already wrote). It ensures every line of production code is actually necessary to satisfy a requirement.

**5. Future Use**: I will definitely use TDD for complex business logic, financial calculations, and core domain models. However, I might skip strict TDD for rapid UI prototyping where the design changes too fast.

**6. Learning**: I was surprised by how much time TDD actually saves in the debugging phase. Finding bugs in a massive test-after suite is painful, but in TDD, if a test fails, you know the bug is in the exact 3 lines of code you just wrote.