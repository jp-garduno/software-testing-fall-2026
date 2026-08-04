# Course Resources

This directory contains additional resources, references, and materials to support your learning throughout the semester.

## 📚 Table of Contents

- [Books](#books)
- [Online Courses](#online-courses)
- [Documentation](#documentation)
- [Tools](#tools)
- [Cheat Sheets](#cheat-sheets)
- [Video Channels](#video-channels)
- [Blogs & Articles](#blogs--articles)
- [Practice Platforms](#practice-platforms)
- [Communities](#communities)

---

## 📖 Books

### Essential Reading

1. **"The Art of Software Testing"** by Glenford J. Myers, Corey Sandler, Tom Badgett
   - Classic testing book, covers fundamentals
   - Great for black box testing techniques

2. **"Test Driven Development: By Example"** by Kent Beck
   - The TDD bible
   - Practical examples in Java (concepts apply to any language)

3. **"Clean Code"** by Robert C. Martin
   - Essential for writing testable code
   - Chapter 9 specifically on unit tests

4. **"xUnit Test Patterns"** by Gerard Meszaros
   - Comprehensive guide to test patterns
   - Refactoring and organizing tests

### Recommended Reading

5. **"Growing Object-Oriented Software, Guided by Tests"** by Steve Freeman & Nat Pryce
   - Advanced TDD with mocking
   - Object-oriented design

6. **"Effective Software Testing"** by Maurício Aniche
   - Modern approach to testing
   - Practical examples

7. **"Software Testing"** by Ron Patton
   - Broad overview of testing field
   - Good for beginners

8. **"Agile Testing"** by Lisa Crispin & Janet Gregory
   - Testing in agile environments
   - Whole team approach

---

## 🎓 Online Courses

### Free Courses

1. **[Udacity: Software Testing](https://www.udacity.com/course/software-testing--cs258)**
   - Comprehensive introduction
   - Videos and quizzes

2. **[Test Automation University](https://testautomationu.applitools.com/)**
   - Multiple courses on various tools
   - Selenium, Playwright, API testing

3. **[FreeCodeCamp: Testing JavaScript](https://www.freecodecamp.org/news/testing-javascript/)**
   - JavaScript testing fundamentals
   - Jest and React Testing Library

### Paid Courses (Optional)

4. **Udemy: Various Testing Courses**
   - Often on sale for $10-20
   - Search for specific tools

5. **Pluralsight: Testing Paths**
   - Comprehensive learning paths
   - Free trial available

---

## 📑 Documentation

### Official Documentation

#### Python Testing
- **[pytest](https://docs.pytest.org/)** - Python testing framework
- **[unittest](https://docs.python.org/3/library/unittest.html)** - Built-in Python testing
- **[Coverage.py](https://coverage.readthedocs.io/)** - Code coverage tool
- **[Behave](https://behave.readthedocs.io/)** - BDD framework for Python

#### JavaScript Testing
- **[Jest](https://jestjs.io/)** - JavaScript testing framework
- **[Mocha](https://mochajs.org/)** - Test framework for Node.js
- **[Chai](https://www.chaijs.com/)** - Assertion library

#### Browser Automation
- **[Selenium WebDriver](https://www.selenium.dev/documentation/)** - Browser automation
- **[Playwright](https://playwright.dev/)** - Modern E2E testing
- **[Cypress](https://docs.cypress.io/)** - Alternative E2E tool (not covered in course)

#### Performance Testing
- **[JMeter](https://jmeter.apache.org/usermanual/index.html)** - Load testing tool
- **[Locust](https://docs.locust.io/)** - Python load testing

#### Code Quality
- **[Pylint](https://pylint.readthedocs.io/)** - Python linter
- **[ESLint](https://eslint.org/docs/)** - JavaScript linter
- **[Black](https://black.readthedocs.io/)** - Python formatter
- **[Prettier](https://prettier.io/docs/)** - Code formatter

### Standards & Specifications

- **[ISTQB Syllabus](https://www.istqb.org/)** - International Software Testing Qualifications Board
- **[Conventional Commits](https://www.conventionalcommits.org/)** - Commit message convention
- **[Semantic Versioning](https://semver.org/)** - Version numbering

---

## 🛠️ Tools

### Testing Frameworks

| **Language** | **Tool** | **Type** | **Purpose** |
|--------------|----------|----------|-------------|
| Python | pytest | Unit/Integration | Most popular Python testing framework |
| Python | unittest | Unit/Integration | Built-in Python testing |
| JavaScript | Jest | Unit/Integration | All-in-one testing solution |
| JavaScript | Mocha | Unit/Integration | Flexible test framework |
| Both | Selenium | E2E | Browser automation |
| Both | Playwright | E2E | Modern browser automation |

### Code Quality Tools

- **Linters**: Pylint, ESLint, Flake8
- **Formatters**: Black, Prettier, autopep8
- **Type Checkers**: mypy (Python), TypeScript
- **Pre-commit**: Git hook framework

### Coverage Tools

- **Coverage.py** (Python) - Code coverage
- **Istanbul/NYC** (JavaScript) - Code coverage
- **Codecov** - Coverage reporting service
- **Coveralls** - Coverage tracking

### CI/CD Platforms

- **GitHub Actions** - Integrated with GitHub
- **GitLab CI/CD** - Integrated with GitLab
- **Travis CI** - Popular CI service
- **Jenkins** - Self-hosted CI server

### Performance Testing

- **JMeter** - Load testing (GUI and CLI)
- **Locust** - Python load testing
- **k6** - JavaScript load testing
- **Gatling** - Scala-based load testing

### Additional Tools

- **Postman** - API testing
- **Insomnia** - API client
- **Docker** - Containerization for consistent environments
- **Database Tools**: DBeaver, pgAdmin, MongoDB Compass

---

## 📋 Cheat Sheets

### Git Commands
```bash
# Common commands
git status                 # Check status
git add <file>             # Stage files
git commit -m "message"    # Commit changes
git push                   # Push to remote
git pull                   # Pull from remote
git branch <name>          # Create branch
git checkout <branch>      # Switch branch
git merge <branch>         # Merge branch

# Useful commands
git log --oneline          # View commit history
git diff                   # See changes
git stash                  # Temporarily save changes
git stash pop              # Restore stashed changes
```

### pytest
```bash
# Running tests
pytest                     # Run all tests
pytest test_file.py        # Run specific file
pytest -v                  # Verbose output
pytest -k "pattern"        # Run tests matching pattern
pytest -m "marker"         # Run marked tests
pytest --cov=.             # Run with coverage
pytest -x                  # Stop at first failure
pytest --pdb               # Drop to debugger on failure

# Test structure
@pytest.fixture            # Define fixture
@pytest.mark.parametrize   # Parameterize test
@pytest.mark.skip          # Skip test
@pytest.mark.xfail         # Expected failure
```

### Jest
```bash
# Running tests
npm test                   # Run all tests
npm test -- --watch        # Watch mode
npm test -- --coverage     # With coverage
npm test -- <file>         # Specific file
npm test -- -t "pattern"   # Matching pattern

# Test structure
describe('suite', () => {}) # Test suite
test('case', () => {})      # Test case
it('case', () => {})        # Alias for test
expect(value).toBe()        # Assertion
beforeEach(() => {})        # Setup
afterEach(() => {})         # Teardown
jest.mock()                 # Mock module
```

### Selenium (Python)
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://example.com")

# Locators
driver.find_element(By.ID, "id")
driver.find_element(By.NAME, "name")
driver.find_element(By.CLASS_NAME, "class")
driver.find_element(By.CSS_SELECTOR, "css")
driver.find_element(By.XPATH, "//xpath")

# Actions
element.click()
element.send_keys("text")
element.clear()

# Waits
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "id"))
)

driver.quit()
```

---

## 🎥 Video Channels

### YouTube Channels

1. **freeCodeCamp.org**
   - Comprehensive tutorials
   - Full courses on testing

2. **Traversy Media**
   - Web development and testing
   - Practical examples

3. **The Net Ninja**
   - Testing frameworks
   - TDD tutorials

4. **Test Automation University**
   - Applitools' educational channel
   - Expert instructors

5. **Continuous Delivery**
   - Dave Farley's channel
   - Testing philosophy and practices

6. **Fun Fun Function**
   - JavaScript testing
   - TDD and unit testing

---

## 📝 Blogs & Articles

### Must-Read Articles

1. **[Martin Fowler's Testing Articles](https://martinfowler.com/tags/testing.html)**
   - Testing pyramid
   - Test doubles
   - Continuous integration

2. **[Google Testing Blog](https://testing.googleblog.com/)**
   - Testing at scale
   - Best practices from Google

3. **[Kent Beck on Twitter/X](https://twitter.com/KentBeck)**
   - TDD insights
   - Testing philosophy

4. **[Uncle Bob's Blog](https://blog.cleancoder.com/)**
   - Clean code and testing
   - Professionalism

### Recommended Blogs

- **[Ministry of Testing](https://www.ministryoftesting.com/)**
- **[Software Testing Help](https://www.softwaretestinghelp.com/)**
- **[Guru99 Testing](https://www.guru99.com/software-testing.html)**
- **[Test Automation Patterns](http://testautomationpatterns.org/)**

---

## 🎯 Practice Platforms

### Coding Challenges

1. **[Exercism](https://exercism.org/)**
   - Practice TDD
   - Mentor feedback
   - Python and JavaScript tracks

2. **[Codewars](https://www.codewars.com/)**
   - Kata challenges
   - Test-driven challenges
   - Multiple languages

3. **[LeetCode](https://leetcode.com/)**
   - Algorithm problems
   - Can practice TDD approach

### TDD Katas

- **[Coding Dojo Kata](http://codingdojo.org/kata/)** - Large collection of practice problems
- **[Kata-Log](https://kata-log.rocks/)** - Searchable kata database
- **[Exercism](https://exercism.org/)** - Practice TDD with mentor feedback
- **[Cyber-Dojo](https://cyber-dojo.org/)** - Online TDD practice environment

### Browser Testing Practice

- **[The Internet](https://the-internet.herokuapp.com/)** - Heroku app for practicing automation
- **[UI Test Automation Playground](http://uitestingplayground.com/)** - Various scenarios

---

## 👥 Communities

### Online Forums

1. **[Stack Overflow](https://stackoverflow.com/)**
   - Q&A for specific problems
   - Tags: [testing], [pytest], [jest], [selenium]

2. **[Reddit](https://www.reddit.com/)**
   - r/softwaretesting
   - r/QualityAssurance
   - r/learnprogramming

3. **[Ministry of Testing Club](https://club.ministryoftesting.com/)**
   - Testing community
   - Forum and resources

### Slack Communities

- **[Software Testing Community]()**
- **[Test Automation]()**
- **[Python Testing]()**

### Discord Servers

- Various programming Discord servers with testing channels
- Language-specific communities

---

## 🎓 Certifications (Optional)

For those interested in professional certifications:

1. **ISTQB Foundation Level**
   - Internationally recognized
   - Good for resume
   - Not required for this course

2. **ISTQB Advanced Levels**
   - After foundation
   - Specialized areas

3. **Tool-Specific Certifications**
   - Selenium certification
   - Various vendor certifications

---

## 💡 Tips for Using These Resources

1. **Don't try to consume everything** - This is a curated list for reference
2. **Start with course materials** - External resources supplement, not replace
3. **Practice is key** - Reading/watching isn't enough
4. **Pick resources that match your learning style** - Videos, books, or hands-on
5. **Bookmark useful resources** - You'll return to them often
6. **Share discoveries** - If you find something great, share with the class!

---

## 📌 Quick Links

- [Course README](../README.md)
- [Timeline](../TIMELINE.md)
- [Contributing Guide](../CONTRIBUTING.md)
- [Documentation](../docs/README.md)
- [Module 1: Git](../01-git/README.md)

---

**Happy Learning!** 🚀
