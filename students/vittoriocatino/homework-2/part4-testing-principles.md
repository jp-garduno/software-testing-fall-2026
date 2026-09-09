# Part 4: Testing Principles Application

## 1. Testing Shows Presence of Defects, Not Their Absence
**Application to FoodHub**: Passing checkout tests raises confidence but cannot prove unusual payment and network combinations are defect-free.
**Impact on Strategy**: Report residual risk; monitor production payments and cancellations; explore high-risk paths.

## 2. Exhaustive Testing Is Impossible
**Application to FoodHub**: Every restaurant, cart, address, promotion, device, and event combination cannot be tested.
**Impact on Strategy**: Use risk selection, boundaries, equivalence classes, and pairwise device coverage; prioritize P0 money and privacy paths.

## 3. Early Testing
**Application to FoodHub**: Ambiguous fees or cancellation rules become costly after implementation.
**Impact on Strategy**: Review stories, API contracts, calculations, and designs before coding; define examples during refinement.

## 4. Defect Clustering
**Application to FoodHub**: Checkout, promotions, payment webhooks, and status synchronization are complex change hot spots.
**Impact on Strategy**: Use incidents and code churn to target regression, review, and exploratory effort.

## 5. Pesticide Paradox
**Application to FoodHub**: Repeating the same happy-path order stops revealing new risks.
**Impact on Strategy**: Refresh data with unusual modifiers and network errors; convert production defects into regression tests; add mutation and exploratory testing.

## 6. Testing Is Context Dependent
**Application to FoodHub**: A money-moving, time-sensitive marketplace needs resilience, privacy, and operational tests unlike a static site.
**Impact on Strategy**: Use payment sandboxes, peak demand, restaurant schedules, courier events, and stricter gates for critical changes.

## 7. Absence-of-Errors Fallacy
**Application to FoodHub**: Technically correct checkout can still fail if its fees or delivery expectations confuse users.
**Impact on Strategy**: Validate comprehension and business outcomes with users and analytics; treat inaccessible or misleading experiences as defects.
