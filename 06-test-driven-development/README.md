# Module 6: Test Driven Development (TDD)

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Understand the TDD philosophy and workflow
- Apply the Red-Green-Refactor cycle
- Write tests before implementation
- Design better code through test-first thinking
- Practice TDD with real examples in Python and JavaScript
- Recognize when TDD is appropriate

## 📚 Theory Materials

### Core TDD Resources

**Recommended Reading Materials**:

1. **Getting Started with TDD**

   - [Kent Beck's "Test Driven Development: By Example"](https://www.oreilly.com/library/view/test-driven-development/0321146530/) - The definitive TDD book
   - [Martin Fowler: TDD Introduction](https://martinfowler.com/bliki/TestDrivenDevelopment.html)
   - [Uncle Bob: The Three Rules of TDD](http://butunclebob.com/ArticleS.UncleBob.TheThreeRulesOfTdd)

2. **Writing Clean Tests**

   - [Clean Code Chapter 9: Unit Tests](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
   - [Test Naming Conventions](https://dzone.com/articles/7-popular-unit-test-naming)
   - [Arrange-Act-Assert Pattern](http://wiki.c2.com/?ArrangeActAssert)

3. **TDD Practice Resources**
   - [Exercism.org TDD Tracks](https://exercism.org/) - Python and JavaScript
   - [Coding Dojo Kata Catalog](http://codingdojo.org/kata/)
   - [Kata-Log.rocks](https://kata-log.rocks/) - Searchable kata collection

### Additional Theory Files

- [01-introduction-to-tdd.md](./theory/01-introduction-to-tdd.md)
- [02-red-green-refactor.md](./theory/02-red-green-refactor.md)
- [03-tdd-best-practices.md](./theory/03-tdd-best-practices.md)
- [04-tdd-anti-patterns.md](./theory/04-tdd-anti-patterns.md)

## 🔄 The TDD Cycle

```
    ┌─────────────┐
    │  RED        │  Write a failing test
    │  (Test)     │  (Test should fail because feature doesn't exist)
    └──────┬──────┘
           │
           ↓
    ┌─────────────┐
    │  GREEN      │  Write minimal code to pass
    │  (Code)     │  (Get the test to pass quickly)
    └──────┬──────┘
           │
           ↓
    ┌─────────────┐
    │  REFACTOR   │  Improve the code
    │  (Improve)  │  (Clean up while tests still pass)
    └──────┬──────┘
           │
           ↓ (Repeat)
```

## 💻 Practical Exercises

### TDD Katas (Classic Exercises)

Both Python and JavaScript implementations:

1. **[FizzBuzz Kata](./exercises/01-fizzbuzz-kata.md)**

   - Classic TDD introduction
   - Simple rules, clear tests

2. **[String Calculator Kata](./exercises/02-string-calculator.md)**

   - Incrementally add features
   - Practice the TDD cycle

3. **[Bowling Game Kata](./exercises/03-bowling-game.md)**

   - More complex scoring logic
   - Multiple test scenarios

4. **[Roman Numerals Kata](./exercises/04-roman-numerals.md)**

   - Conversion algorithms
   - Edge cases and refactoring

5. **[Bank Account Kata](./exercises/05-bank-account.md)**
   - Stateful object testing
   - Transaction history

## 📝 Homework Assignment

**[Homework 6: TDD Feature Development](./homework/homework-6.md)** **Due**: End of Week 11

**Objectives**:

- Develop a complete feature using TDD
- Document your Red-Green-Refactor cycles
- Submit test-first commit history
- Reflect on the TDD experience

## 🎥 Video Resources

- **TDD Introduction** (20 min)
- **Live TDD Demo** (30 min) - Watch a developer practice TDD in real-time
- **Common TDD Mistakes** (15 min)
- **TDD vs Test-After** (10 min)

## 🛠️ Tools

Same as Module 5:

- **Python**: pytest
- **JavaScript**: Jest
- **Coverage**: pytest-cov, Jest --coverage

## 📖 TDD Principles

1. **Write tests first** - Before any production code
2. **Keep tests simple** - One assertion per test when possible
3. **Write minimal code** - Just enough to pass the test
4. **Refactor continuously** - Improve code while tests pass
5. **Run tests frequently** - After every small change
6. **Red-Green-Refactor** - Follow the cycle religiously

## ❓ Common Questions

**Q: Isn't writing tests first slower?**
A: Initially yes, but TDD often results in faster overall development due to fewer bugs and better design.

**Q: Do I need to use TDD for everything?**
A: No. TDD is a tool. Use it when it adds value (complex logic, critical features).

**Q: What if I don't know what tests to write?**
A: Start with the simplest case. The tests will guide your design.

**Q: How is TDD different from just writing tests?**
A: TDD is a design technique. Tests drive the API design and implementation.

## 🎯 Self-Assessment Checklist

- [ ] Understand the Red-Green-Refactor cycle
- [ ] Write failing tests before implementation
- [ ] Write minimal code to pass tests
- [ ] Refactor code while keeping tests green
- [ ] Complete at least 3 TDD katas
- [ ] Develop a feature using TDD from scratch
- [ ] Recognize TDD benefits and limitations

## 🚀 Next Steps

- Complete TDD katas
- Complete [Homework 6](./homework/homework-6.md)
- Prepare for **Exam 2** (Week 11) covering Modules 4-6
- Preview [Module 7: Data Driven Testing](../07-data-driven-testing/README.md)

---

**Remember**: TDD is a discipline - it feels awkward at first, but with practice it becomes natural! 🔄
