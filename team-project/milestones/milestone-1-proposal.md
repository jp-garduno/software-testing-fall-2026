# Milestone 1: Project Proposal

**Due**: End of Week 4  
**Points**: 10 (10% of project grade)  
**Focus**: Planning and team formation

---

## 🎯 Objectives

- Form team and assign roles
- Choose project idea
- Define scope and requirements
- Plan development timeline
- Get instructor approval

---

## 📋 Deliverables

Submit a **Project Proposal Document** (PDF or Markdown) containing:

### 1. Team Information (10 points)

**Team Name**: Creative team name

**Team Members** (4-5 students):

| Name         | Student ID | Email             | Role              |
| ------------ | ---------- | ----------------- | ----------------- |
| Member 1     | 12345678   | member1@email.com | Project Manager   |
| Member 2     | 12345679   | member2@email.com | Backend Lead      |
| Member 3     | 12345680   | member3@email.com | Frontend Lead     |
| Member 4     | 12345681   | member4@email.com | QA Lead           |
| Member 5 (?) | 12345682   | member5@email.com | DevOps (optional) |

**Role Descriptions**:

For each role, describe responsibilities (2-3 sentences each):

- **Project Manager**: Coordinate team, manage timeline, facilitate meetings
- **Backend Lead**: API development, database design, integration tests
- **Frontend Lead**: UI implementation, E2E tests, user experience
- **QA Lead**: Test strategy, automation, coverage monitoring, performance tests
- **DevOps** (if 5 members): CI/CD, deployment, environment config

---

### 2. Project Selection (15 points)

**Selected Project**: [Choose from provided options or propose custom]

**Why This Project?**

Explain why your team chose this project (1 paragraph):

- Team interest/passion
- Relevant to career goals
- Good fit for team skills
- Testing opportunities

**Project Description** (2-3 paragraphs):

- What problem does it solve?
- Who are the users?
- What are the key features?
- What makes it interesting?

---

### 3. Requirements Specification (25 points)

#### 3.1 Functional Requirements

List 10-15 main functional requirements:

**User Management**:

- [ ] FR-1: Users can register with email/password
- [ ] FR-2: Users can log in and log out
- [ ] FR-3: Users can reset password

**Core Features** (example for e-commerce):

- [ ] FR-4: Users can browse product catalog
- [ ] FR-5: Users can search products by keyword
- [ ] FR-6: Users can add items to shopping cart
- [ ] FR-7: Users can checkout and place orders
- [ ] FR-8: Users can view order history

**Admin Features**:

- [ ] FR-9: Admins can manage products (CRUD)
- [ ] FR-10: Admins can view all orders
- [ ] FR-11: Admins can update order status

_Add more based on your project_

#### 3.2 Non-Functional Requirements

**Performance**:

- Response time < 2 seconds for page loads
- Support 100 concurrent users
- Database queries < 500ms

**Security**:

- Password hashing (bcrypt)
- Input validation and sanitization
- Protected admin routes

**Usability**:

- Responsive design (mobile-friendly)
- Intuitive navigation
- Clear error messages

**Testing** (Critical for this course):

- 80%+ code coverage
- All test types implemented (unit, integration, E2E, performance)
- CI/CD with automated tests

---

### 4. Technology Stack (15 points)

#### 4.1 Backend

**Language**: Python 3.11+ or Node.js/TypeScript 22+

**Framework**: Flask / FastAPI / Django OR Express / NestJS

**Database**: SQLite / PostgreSQL / MongoDB

**Authentication**: JWT / Sessions

**API**: REST (or GraphQL)

#### 4.2 Frontend

**Framework**: React / Vue / Vanilla JS+HTML+CSS

**Styling**: Tailwind / Bootstrap / Custom CSS

**State Management**: Context API / Redux / Vuex (if needed)

#### 4.3 Testing & Tools

**Python Testing**:

- pytest (unit/integration)
- pytest-cov (coverage)
- Selenium / Playwright (E2E)
- Behave (BDD)
- JMeter (performance)

**JavaScript Testing**:

- Jest (unit/integration)
- Playwright / Cypress (E2E)
- Cucumber (BDD)
- JMeter (performance)

**Code Quality**:

- Black / isort / Pylint (Python)
- ESLint / Prettier (JavaScript)
- Pre-commit hooks
- GitHub Actions (CI/CD)

#### 4.4 Development Tools

- **Version Control**: Git + GitHub
- **Editor**: VS Code / PyCharm / WebStorm
- **Collaboration**: Slack / Discord / Teams
- **Project Management**: GitHub Projects / Trello

**Justification** (1-2 paragraphs):

Explain why you chose this stack:

- Team familiarity
- Course requirements
- Project needs
- Learning goals

---

### 5. Project Architecture (20 points)

#### 5.1 High-Level Architecture Diagram

Create a diagram showing:

- Frontend (browser/client)
- Backend (API server)
- Database
- External services (if any)
- Communication flow

Use draw.io, Lucidchart, or ASCII art.

Example:

```
┌─────────────┐          ┌─────────────┐          ┌─────────────┐
│   Browser   │  HTTP    │   Backend   │   SQL    │  Database   │
│  (React)    │ ◄──────► │   (Flask)   │ ◄──────► │ (PostgreSQL)│
└─────────────┘  JSON    └─────────────┘          └─────────────┘
```

#### 5.2 Database Schema (Draft)

Provide initial database design:

**Tables**:

1. **Users**

   - id (PK)
   - email (unique)
   - password_hash
   - role (user/admin)
   - created_at

2. **Products** (example for e-commerce)

   - id (PK)
   - name
   - description
   - price
   - stock
   - image_url

3. **Orders**
   - id (PK)
   - user_id (FK)
   - total_amount
   - status (pending/completed/cancelled)
   - created_at

_Add more tables based on your project_

Include ER diagram if possible.

---

### 6. Development Plan (10 points)

#### 6.1 Milestone Breakdown

Show how your features map to course milestones:

**M2 (Week 6 - Foundation)**:

- Set up Git repository
- Basic project structure
- Pre-commit hooks
- User registration/login backend

**M3 (Week 8 - Black Box)**:

- Complete core features
- Test plan for all features
- 20+ test cases documented

**M4 (Week 10 - White Box)**:

- Unit tests for all modules
- 80%+ coverage
- Integration tests for API

**M5 (Week 12 - TDD)**:

- New feature (e.g., shopping cart) using TDD
- Document TDD process

**M6 (Week 14 - System)**:

- E2E tests with Selenium/Playwright
- BDD scenarios in Gherkin

**M7 (Week 16 - Final)**:

- Performance tests with JMeter
- Final polish and documentation
- Presentation

#### 6.2 Timeline

| Week | Tasks                                         | Owner(s)      |
| ---- | --------------------------------------------- | ------------- |
| 4    | Proposal, repo setup                          | All           |
| 5    | Database design, API skeleton                 | Backend       |
| 5-6  | Authentication, basic UI                      | Backend + UI  |
| 6    | Pre-commit hooks, CI/CD                       | DevOps        |
| 7-8  | Core features, test plan                      | All           |
| 9-10 | Unit tests, integration tests                 | QA + Devs     |
| 11   | Exam 2 prep week (lighter project work)       | -             |
| 12   | TDD feature implementation                    | All (pair)    |
| 13   | E2E test automation                           | QA + Frontend |
| 14   | System tests, BDD scenarios                   | QA            |
| 15   | Performance tests, final docs                 | All           |
| 16   | Presentation prep, demo polish, final touches | All           |

---

### 7. Risk Assessment (5 points)

Identify potential risks and mitigation strategies:

| Risk                           | Impact | Probability | Mitigation                         |
| ------------------------------ | ------ | ----------- | ---------------------------------- |
| Team member drops course       | High   | Low         | Clear role documentation, backups  |
| Technology learning curve      | Medium | Medium      | Start simple, iterate              |
| Scope creep                    | Medium | High        | Stick to proposal, no new features |
| Testing takes longer than plan | Medium | Medium      | Start testing early, automate      |
| Merge conflicts                | Low    | High        | Regular syncs, clear branching     |
| CI/CD pipeline issues          | Low    | Medium      | Set up early, test thoroughly      |
| Missed milestone deadline      | High   | Low         | Weekly check-ins, buffer time      |

Add 3-5 project-specific risks.

---

## 📤 Submission Instructions

### 1. Create GitHub Repository

```bash
# One team member creates repo
gh repo create team-project-fall-2026 --public --clone
cd team-project-fall-2026

# Add team members as collaborators
gh repo invite <teammate-username>
```

### 2. Create Proposal Document

```
team-project-fall-2026/
├── docs/
│   └── milestones/
│       └── M1/
│           ├── proposal.md (or proposal.pdf)
│           └── architecture-diagram.png
├── README.md
└── .gitignore
```

### 3. Submit via Canvas

- **Repository URL**: https://github.com/your-team/team-project-fall-2026
- **Proposal Document**: Direct link to `docs/milestones/M1/proposal.md`
- **Team Members**: All team member names in Canvas submission

### 4. Schedule Approval Meeting (Optional)

If you want early feedback, schedule 15-min meeting with instructor during Week 4.

---

## 🎯 Grading Rubric

| Category                   | Points | Criteria                                             |
| -------------------------- | ------ | ---------------------------------------------------- |
| **Team Information**       | 10     | Complete roster, clear role descriptions             |
| **Project Selection**      | 15     | Appropriate scope, clear description, good rationale |
| **Requirements**           | 25     | Comprehensive functional & non-functional reqs       |
| **Technology Stack**       | 15     | Appropriate choices, well justified                  |
| **Architecture**           | 20     | Clear diagrams, sensible design, database schema     |
| **Development Plan**       | 10     | Realistic timeline, clear milestone mapping          |
| **Risk Assessment**        | 5      | Thoughtful risks, practical mitigation               |
| **Quality & Presentation** | 10     | Professional, well-organized, clear writing          |

**Total**: 110 points (10% bonus built in)

**Deductions**:

- Late submission: -10% per day
- Incomplete sections: -5 points each
- Poor formatting/spelling: -5 points
- Missing diagrams: -10 points

---

## ✅ Checklist

Before submitting, verify:

- [ ] All team members listed with roles
- [ ] Project idea clearly described
- [ ] 10-15 functional requirements listed
- [ ] Non-functional requirements specified
- [ ] Full technology stack documented
- [ ] Architecture diagram included
- [ ] Database schema draft created
- [ ] Development timeline mapped to milestones
- [ ] Risk assessment completed
- [ ] Document professionally formatted
- [ ] GitHub repository created
- [ ] All team members added as collaborators
- [ ] README.md exists in repository
- [ ] Submitted on Canvas with repo link

---

## 💡 Tips for Success

### Proposal Writing

1. **Be specific**: "Users can search" → "Users can search products by name, category, and price range"
2. **Be realistic**: Don't promise features you can't deliver in 12 weeks
3. **Be testable**: Every requirement should be testable
4. **Use professional tone**: This is a technical document

### Team Organization

1. **Meet early**: Don't wait until Week 4 to form teams
2. **Assess skills**: Know each member's strengths
3. **Set expectations**: Discuss availability, work style, communication
4. **Create team agreement**: How will you handle conflicts?

### Scope Management

1. **Start small**: Plan minimum viable product (MVP) first
2. **Add stretch goals**: List "nice to have" features separately
3. **Focus on testing**: This is a testing course - tests are as important as features
4. **Plan for learning time**: New technologies need buffer time

### Common Mistakes

- ❌ Too ambitious scope (build Amazon in 12 weeks)
- ❌ Vague requirements ("make it fast")
- ❌ No thought to testing
- ❌ Unclear team roles
- ❌ Unrealistic timeline
- ❌ No risk planning

---

## 📚 Resources

- [Requirements Template](../templates/requirements-template.md)
- [Team Charter Template](../templates/team-charter.md)

---

## ❓ Frequently Asked Questions

**Q: Can we change our project idea after approval?**  
A: Minor adjustments yes, major changes need instructor approval. Discouraged after Week 6.

**Q: What if we can't form a team of 4-5?**  
A: Contact instructor. Teams of 3 may be allowed with adjusted requirements.

**Q: Can we use a project from another class?**  
A: Only if you write all tests from scratch and it meets course requirements. Discuss with instructor.

**Q: Should we start coding in Week 4?**  
A: Light setup (repo, basic structure) yes. Major coding starts after approval.

**Q: How detailed should the database schema be?**  
A: Draft level is fine. Show main tables and relationships. Can evolve during development.

**Q: What if we're not sure about the technology stack?**  
A: Choose what your team knows best. Can adjust minor dependencies later.

---

**Good luck with your proposal! This is your roadmap for the next 12 weeks. Take time to plan well.** 📝🚀
