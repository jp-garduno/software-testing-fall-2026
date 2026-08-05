# Team Project

## 🎯 Project Overview

The team project is a semester-long effort where you'll build a complete application with comprehensive testing coverage. This project integrates all concepts from the course and demonstrates your ability to work in a team while applying professional testing practices.

**Weight**: 20% of final grade  
**Team Size**: 4-5 students  
**Duration**: Weeks 4-16 (13 weeks)

---

## 📋 Project Objectives

By completing this project, you will:

- Apply all testing techniques learned in class
- Build a real application from scratch
- Work collaboratively using Git and GitHub
- Practice professional software development workflows
- Create comprehensive test coverage (unit, integration, E2E, performance)
- Document and present your work

---

## 🎯 Learning Goals

### Technical Skills

- Full-stack development (your choice of technologies)
- Test automation at all levels
- CI/CD pipeline integration
- Code quality and coverage measurement
- Performance testing and optimization

### Soft Skills

- Team collaboration
- Project management
- Technical documentation
- Code review practices
- Presentation skills

---

## 📅 Milestones

| **Milestone**              | **Week** | **Deliverable**           | **Points** | **Focus Modules** |
| -------------------------- | -------- | ------------------------- | ---------- | ----------------- |
| **M1: Proposal**           | Week 4   | Project proposal document | 10%        | -                 |
| **M2: Foundation**         | Week 6   | Git setup, static testing | 10%        | Modules 1, 3      |
| **M3: Black Box Tests**    | Week 8   | Test plan with test cases | 15%        | Module 4          |
| **M4: White Box Tests**    | Week 10  | Unit tests with coverage  | 20%        | Module 5          |
| **M5: TDD Feature**        | Week 12  | Feature using TDD         | 15%        | Module 6          |
| **M6: System Tests**       | Week 14  | E2E automated tests       | 15%        | Module 8          |
| **M7: Final Presentation** | Week 16  | Complete project + demo   | 15%        | All modules       |

**Total**: 100% (20% of course grade)

See [Milestones Guide](./milestones/README.md) for detailed requirements.

---

## 💡 Project Ideas

Choose **one** project idea (or propose your own):

### Option 1: E-Commerce Platform

Build an online shopping platform with:

- User authentication and profiles
- Product catalog with search/filter
- Shopping cart and checkout
- Order history and tracking
- Admin dashboard

**Testing Focus**: Payment processing, cart calculations, user flows, load testing for sales events

---

### Option 2: Task Management System

Build a project/task management tool with:

- User accounts and teams
- Project creation and management
- Task assignment and tracking
- Comments and attachments
- Dashboard and reporting

**Testing Focus**: State transitions (task statuses), authorization, concurrent updates, data integrity

---

### Option 3: Social Media Feed

Build a social networking platform with:

- User profiles and connections
- Post creation (text, images)
- Feed algorithm
- Likes, comments, shares
- Notifications

**Testing Focus**: Feed algorithm, real-time updates, media upload, performance under load

---

### Option 4: Online Learning Platform

Build an educational platform with:

- Course catalog
- Video lessons and materials
- Quizzes and assignments
- Progress tracking
- Certificates

**Testing Focus**: Quiz grading logic, progress calculation, video streaming, concurrent users

---

### Option 5: Healthcare Appointment System

Build a medical appointment system with:

- Patient and doctor profiles
- Appointment scheduling
- Medical records (simplified)
- Prescription management
- Notifications and reminders

**Testing Focus**: Scheduling conflicts, data privacy, appointment state machine, load testing

---

### Option 6: Food Delivery Platform

Build a food ordering system with:

- Restaurant listings
- Menu browsing and ordering
- Shopping cart with customizations
- Order tracking
- Delivery driver assignment

**Testing Focus**: Order state machine, pricing calculations, real-time tracking, concurrent orders

---

### Custom Project

Propose your own project idea! Must include:

- Clear scope and requirements
- Multiple user roles
- Complex business logic suitable for testing
- State transitions or workflows
- Approval from instructor required

---

## 📋 Technical Requirements

### Application Requirements

1. **Functionality**:

   - At least 5 major features
   - Multiple user roles (admin, regular user, etc.)
   - CRUD operations (Create, Read, Update, Delete)
   - Data persistence (database)
   - Authentication and authorization

2. **Technology Stack** (Your Choice):

   - **Backend**: Python (Flask/FastAPI/Django) or Node.js/TypeScript (Express/NestJS)
   - **Frontend**: React, Vue, or vanilla JavaScript/HTML/CSS
   - **Database**: SQLite, PostgreSQL, MongoDB, or similar
   - **Other**: Any additional libraries/frameworks as needed

3. **Code Quality**:
   - Clean, readable code
   - Consistent style (linting enforced)
   - Modular architecture
   - Proper error handling
   - Environment configuration

### Testing Requirements

Your project must include **all** of these:

1. **Static Testing** (Module 3):

   - Pre-commit hooks configured
   - Linting (Pylint/ESLint)
   - Conventional commits
   - `.pre-commit-config.yaml`

2. **Black Box Testing** (Module 4):

   - Test plan document
   - Test cases using EP, BVA, Decision Tables
   - At least 20 documented test cases

3. **Unit Tests** (Module 5):

   - Individual function/method tests
   - At least 80% code coverage
   - Coverage reports generated

4. **Integration Tests** (Module 5):

   - Module interaction tests
   - API endpoint tests
   - Database integration tests
   - Mocking external dependencies

5. **TDD Feature** (Module 6):

   - At least one feature developed using TDD
   - Documented Red-Green-Refactor cycles
   - Git history showing test-first commits

6. **Data-Driven Tests** (Module 7):

   - Parameterized tests
   - External test data (CSV/JSON)

7. **System/E2E Tests** (Module 8):

   - BDD feature files (Gherkin)
   - Selenium or Playwright tests
   - Page Object Model implementation
   - At least 5 E2E scenarios

8. **Performance Tests** (Module 9):
   - JMeter test plan
   - Load testing results
   - Performance report with recommendations

### Documentation Requirements

1. **README.md**:

   - Project description
   - Features list
   - Setup instructions
   - Running tests
   - Team members and roles

2. **Testing Documentation**:

   - Test strategy document
   - Test plan
   - Coverage reports
   - Performance test results

3. **Architecture Documentation**:

   - System architecture diagram
   - Database schema
   - API documentation

4. **User Guide**:
   - How to use the application
   - Screenshots

---

## 👥 Team Structure

### Team Formation (Week 4)

- Teams of 4-5 students
- Self-organized or instructor-assigned
- Submit team roster with roles

### Recommended Roles

Roles can overlap, but ensure clear responsibilities:

1. **Project Manager**:

   - Coordinates team activities
   - Manages milestones and deadlines
   - Facilitates communication

2. **Backend Lead**:

   - API development
   - Database design
   - Integration testing

3. **Frontend Lead**:

   - UI implementation
   - E2E testing
   - User experience

4. **QA Lead**:

   - Test strategy
   - Test automation
   - Coverage monitoring
   - Performance testing

5. **DevOps/Tools** (if 5 members):
   - CI/CD setup
   - Deployment
   - Environment configuration

**Note**: In 4-person teams, combine roles strategically.

---

## 🔄 Workflow Requirements

### Git Workflow

1. **Repository**:

   - Create GitHub repository
   - Add all team members
   - Set up branch protection

2. **Branching Strategy**:

   - `main` branch: production-ready code
   - `develop` branch: integration branch
   - Feature branches: `feature/feature-name`
   - Bugfix branches: `fix/bug-description`

3. **Pull Requests**:

   - All changes via pull requests
   - At least one team member review
   - PR template (provided)
   - Conventional commit messages

4. **CI/CD** (Bonus):
   - GitHub Actions or similar
   - Automated testing
   - Code quality checks

### Collaboration Practices

- Weekly team meetings (document in repo)
- Code reviews for all PRs
- Issue tracking for tasks and bugs
- Regular commits (not everything in one commit)
- Fair distribution of work

---

## 📤 Deliverables

### For Each Milestone

See [Milestones Guide](./milestones/README.md) for specific requirements.

### Final Submission (Milestone 7, Week 16)

1. **GitHub Repository**:

   - Complete source code
   - All test suites
   - Documentation
   - README with setup instructions

2. **Live Demo** (optional):

   - Deployed application
   - Or local demo during presentation

3. **Presentation** (10-15 minutes):

   - Project overview
   - Demo of key features
   - Testing strategy and results
   - Lessons learned
   - Q&A

4. **Project Report** (PDF):
   - Executive summary
   - Technical architecture
   - Testing strategy and results
   - Coverage reports
   - Performance results
   - Challenges and solutions
   - Team contributions
   - Appendices (screenshots, diagrams)

---

## 🎯 Grading Rubric

### Overall Project Grading (20% of course grade)

| **Category**            | **Weight** | **Description**                                         |
| ----------------------- | ---------- | ------------------------------------------------------- |
| **Milestones**          | 40%        | Timely submission and quality of milestone deliverables |
| **Application Quality** | 20%        | Functionality, code quality, user experience            |
| **Testing Coverage**    | 30%        | Completeness and quality of all testing types           |
| **Documentation**       | 10%        | Clarity, completeness, professionalism                  |
| **Presentation**        | 10%        | Demo, explanation, Q&A performance                      |
| **Collaboration**       | 10%        | Git workflow, code reviews, equal contributions         |

**Total**: 120% (20% bonus points available)

### Individual Grading

- 80% of project grade is team-based
- 20% is based on individual contribution:
  - Commit history
  - Code reviews
  - Peer evaluation
  - Meeting participation

---

## 💡 Tips for Success

### Project Management

1. **Start early** - Don't wait for deadlines
2. **Meet regularly** - Weekly team syncs minimum
3. **Use project board** - GitHub Projects or Trello
4. **Track progress** - Milestones and issues
5. **Communicate** - Keep team and instructor informed

### Development

1. **Simple first** - Get basic features working, then enhance
2. **Test continuously** - Don't leave testing to the end
3. **Review code** - Catch issues early
4. **Document as you go** - Don't wait until final week
5. **Version control discipline** - Commit often, meaningful messages

### Testing

1. **Integrate early** - Set up testing from the start
2. **Automate** - Manual testing doesn't scale
3. **Measure coverage** - Track and improve
4. **Real scenarios** - Test realistic use cases
5. **Performance matters** - Don't ignore it

### Common Pitfalls

- ❌ Scope creep - Keep it manageable
- ❌ One person doing everything - Distribute work
- ❌ No testing until the end - Test from day one
- ❌ Poor communication - Stay in sync
- ❌ Waiting for perfect code - Iterate and improve

---

## 📚 Resources

- [Project Templates](./templates/) - Starter files and templates
- [Milestone Guidelines](./milestones/) - Detailed milestone requirements (M1-M7)
- [Development Guidelines](./guidelines/) - Git workflow, code review, testing best practices

---

## 🆘 Getting Help

- **Office Hours**: Weekly office hours available
- **Team Consultations**: Schedule 1-on-1 team meetings with instructor
- **GitHub Discussions**: Ask questions, share knowledge
- **Peer Review**: Learn from other teams (without copying)

---

## ✅ Getting Started Checklist

Week 4 - Project Kickoff:

- [ ] Form team of 4-5 students
- [ ] Assign team roles
- [ ] Choose project idea
- [ ] Create GitHub repository
- [ ] Set up communication channel (Slack, Discord, etc.)
- [ ] Schedule first team meeting
- [ ] Read all milestone requirements
- [ ] Submit Milestone 1: Project Proposal

---

**Good luck with your team project!** This is your chance to build something real and showcase everything you've learned. Make it count! 🚀
