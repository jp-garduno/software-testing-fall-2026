# Team Project Milestones

This directory contains detailed requirements for all 7 project milestones throughout the semester.

## 📅 Milestone Timeline

| Milestone | Week    | Due Date       | Focus              | Points |
| --------- | ------- | -------------- | ------------------ | ------ |
| M1        | Week 4  | End of Week 4  | Project Proposal   | 10%    |
| M2        | Week 6  | End of Week 6  | Foundation & Setup | 10%    |
| M3        | Week 8  | End of Week 8  | Black Box Testing  | 15%    |
| M4        | Week 10 | End of Week 10 | White Box Testing  | 20%    |
| M5        | Week 12 | End of Week 12 | TDD Feature        | 15%    |
| M6        | Week 14 | End of Week 14 | System Testing     | 15%    |
| M7        | Week 16 | End of Week 16 | Final Presentation | 15%    |

**Total**: 100 points (= 20% of course grade)

---

## 📋 Milestone Details

### [Milestone 1: Project Proposal](./milestone-1-proposal.md)

**Week 4 | 10 points**

Submit a comprehensive project proposal including:

- Team composition and roles
- Project idea selection
- High-level requirements
- Technology stack
- Timeline and milestones

**Goal**: Establish clear project scope and team structure.

---

### [Milestone 2: Foundation & Setup](./milestone-2-foundation.md)

**Week 6 | 10 points**

Set up project infrastructure:

- Git repository with branch protection
- Development environment
- Pre-commit hooks and linting
- CI/CD pipeline (basic)
- Project structure

**Modules Applied**: Git (1), Static Testing (3)

---

### [Milestone 3: Black Box Testing](./milestone-3-black-box.md)

**Week 8 | 15 points**

Create comprehensive test plan:

- Test strategy document
- 20+ test cases using EP, BVA, Decision Tables
- State transition diagrams
- Traceability matrix

**Module Applied**: Black Box Testing (4)

---

### [Milestone 4: White Box Testing](./milestone-4-white-box.md)

**Week 10 | 20 points**

Implement automated testing:

- Unit tests (80%+ coverage)
- Integration tests
- Mocking strategy
- Coverage reports
- Bug fixes based on tests

**Module Applied**: White Box Testing (5)

---

### [Milestone 5: TDD Feature](./milestone-5-tdd.md)

**Week 12 | 15 points**

Develop new feature using TDD:

- Feature specification
- Test-first implementation
- Red-Green-Refactor cycles documented
- Git history showing TDD workflow
- Retrospective

**Module Applied**: TDD (6)

---

### [Milestone 6: System Testing](./milestone-6-system-testing.md)

**Week 14 | 15 points**

End-to-end test automation:

- BDD feature files (Gherkin)
- Selenium or Playwright tests
- Page Object Model implementation
- 5+ E2E scenarios
- Test execution report

**Module Applied**: System Testing (8)

---

### [Milestone 7: Final Presentation](./milestone-7-final.md)

**Week 16 | 15 points**

Complete project delivery:

- Performance testing with JMeter
- Final documentation
- Deployed application (or demo)
- Team presentation (10-15 min)
- Project report

**Modules Applied**: All modules + Performance Testing (9)

---

## 📤 Submission Format

For all milestones:

1. **GitHub Repository**: All work must be in your team repository
2. **Pull Request**: Create PR for each milestone (e.g., `milestone-3-black-box`)
3. **Documentation**: Include required docs in `/docs/milestones/M#/` folder
4. **Canvas Submission**: Submit GitHub repository URL + PR link

### Repository Structure

```
your-team-project/
├── docs/
│   └── milestones/
│       ├── M1/          # Milestone 1 deliverables
│       ├── M2/
│       ├── M3/
│       └── ...
├── src/                 # Application code
├── tests/               # All test suites
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   └── performance/
├── .pre-commit-config.yaml
├── .github/
│   └── workflows/
└── README.md
```

---

## 🎯 Grading Criteria

### Common Criteria (All Milestones)

- **Completeness** (40%): All required deliverables present
- **Quality** (40%): Work meets professional standards
- **Documentation** (10%): Clear, well-written docs
- **Timeliness** (10%): Submitted on time

### Milestone-Specific Criteria

See individual milestone files for detailed rubrics.

---

## ⏰ Late Submission Policy

- **On time**: Full credit
- **1-3 days late**: -10% per day
- **4-7 days late**: -50%
- **> 7 days late**: No credit

**Exception**: Instructor approval for documented emergencies.

---

## 🔄 Revision Policy

Milestones can be revised for partial credit recovery:

- **M1-M5**: Can revise within 1 week for up to 50% of lost points
- **M6-M7**: No revisions (final deliverables)

Revisions must address all feedback and be submitted as new PR.

---

## 🆘 Getting Help

- **Office Hours**: Weekly office hours for milestone questions
- **Team Consultations**: Schedule 30-min team meetings with instructor
- **GitHub Issues**: Use issues for milestone-specific questions
- **Peer Learning**: Review other teams' work (without copying)

---

## ✅ Success Tips

1. **Start early** - Each milestone builds on the previous
2. **Communicate** - Keep team and instructor informed
3. **Iterate** - Don't wait for perfection, improve continuously
4. **Document** - Write docs as you work, not at the end
5. **Review feedback** - Apply instructor feedback to future milestones
6. **Test often** - Don't leave testing to the last minute
7. **Commit regularly** - Show incremental progress

---

## 📊 Milestone Tracking

Use this checklist to track your progress:

- [ ] M1: Project Proposal (Week 4)
- [ ] M2: Foundation & Setup (Week 6)
- [ ] M3: Black Box Testing (Week 8)
- [ ] M4: White Box Testing (Week 10)
- [ ] M5: TDD Feature (Week 12)
- [ ] M6: System Testing (Week 14)
- [ ] M7: Final Presentation (Week 16)

---

**Remember**: The team project integrates everything you learn. Each milestone is a chance to demonstrate mastery of that module's concepts while building toward a complete, tested application. 🚀
