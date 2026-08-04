# Testing Concepts - Concept Maps

Visual representations of testing relationships and hierarchies.

---

## Concept Map 1: Testing Overview

```
                    SOFTWARE TESTING
                          |
        __________________|__________________
       |                                     |
  STATIC TESTING                      DYNAMIC TESTING
       |                                     |
   (No Execution)                      (Execution Required)
       |                                     |
   - Reviews                            - Unit Testing
   - Inspections                        - Integration Testing
   - Linting                            - System Testing
   - Static Analysis                    - Acceptance Testing
```

---

## Concept Map 2: Testing Types

```
                    TESTING TYPES
                          |
            ______________|______________
           |                             |
    FUNCTIONAL                    NON-FUNCTIONAL
           |                             |
    (What it does)                 (How well it does it)
           |                             |
    ---------------              ------------------
    |             |              |        |       |
  Smoke        Sanity      Performance Security Usability
  Regression   System      Load        Access   UX
  Integration  UAT         Stress      SQL-Inj  A11y
```

---

## Concept Map 3: Testing Levels (The Pyramid)

```
           /\
          /  \        Acceptance Testing
         /____\       (Users validate)
        /      \
       /System  \     System Testing
      /_Testing_\    (Complete system)
     /            \
    /Integration   \  Integration Testing
   /___Testing____\ (Components together)
  /                \
 /   Unit Testing   \ Unit Testing
/___________________\ (Individual functions)

Base = Most tests, Fast, Cheap
Top = Few tests, Slow, Expensive
```

---

## Concept Map 4: Seven Testing Principles

```
SEVEN TESTING PRINCIPLES
        |
        |-- 1. Presence of Defects (Testing shows bugs exist, not absent)
        |
        |-- 2. Exhaustive Testing Impossible (Can't test everything)
        |
        |-- 3. Early Testing (Test from the start)
        |
        |-- 4. Defect Clustering (80/20 rule - most bugs in few modules)
        |
        |-- 5. Pesticide Paradox (Update tests regularly)
        |
        |-- 6. Context Dependent (Different apps, different approaches)
        |
        |-- 7. Absence of Errors Fallacy (Bug-free ≠ Success)
```

---

## Concept Map 5: Testing in SDLC

```
WATERFALL:
Requirements → Design → Code → [Testing] → Deploy

V-MODEL:
Requirements ←→ Acceptance Testing
    ↓                    ↑
Design ←→ System Testing
    ↓                    ↑
Architecture ←→ Integration Testing
    ↓                    ↑
Code ←→ Unit Testing

AGILE:
Plan → Design → Code → Test → Review → Deploy
  ↑______________|______|______|______|______|
         (Iterative - Testing in every sprint)

DEVOPS:
Code → Build → Test → Deploy → Monitor
  ↑______|______|______|______|______|
         (Continuous - Automated testing)
```

---

## Concept Map 6: Testing Workflow

```
                    Write Code
                        ↓
                  Static Testing
                  (Linting, Reviews)
                        ↓
                    Unit Tests
                  (Functions work)
                        ↓
                Integration Tests
               (Modules work together)
                        ↓
                  System Tests
              (Complete system works)
                        ↓
                Acceptance Tests
               (Users validate)
                        ↓
                   Deploy
                        ↓
                   Monitor
             (Production testing)
```

---

## Concept Map 7: Testing Metrics

```
                 TESTING METRICS
                        |
        ________________|________________
       |                |                |
    Coverage        Quality           Efficiency
       |                |                |
   - Code Cov     - Defect Density   - Test Execution Time
   - Req Cov      - Defect Rate      - Automation %
   - Test Cov     - Pass Rate        - Cost per Defect
                  - Critical Bugs    - MTTD / MTTR
```

---

## Exercise: Create Your Own

Create concept maps for:

1. **Testing Tools Landscape**

   - Map out tools for each type of testing
   - Include tools for Python and JavaScript

2. **Your Project Testing Strategy**

   - Draw your project's testing approach
   - Show relationships between test types

3. **Testing Timeline**
   - Map testing activities across your project timeline
   - Show when each testing type occurs

---

## Study Tips

1. **Draw by hand** - Helps memorization
2. **Use colors** - Different colors for different categories
3. **Add examples** - Concrete examples for each node
4. **Connect concepts** - Show relationships, not just hierarchy
5. **Review regularly** - Recreate from memory to test understanding

---

**Visual learning reinforces conceptual understanding!** 🧠
