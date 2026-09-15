# Part 2: Testing Types Classification

Testing **types** describe what we test - functionality, performance, security and the other quality attributes - while testing **levels** describe where in the system we test. Nine types are covered below: the five required by the assignment, plus four that a real-time web and mobile product cannot skip.

Priorities use the scale Critical / High / Medium / Low.

---

## Test Type: Functional Testing

**Category**: Functional

**Purpose**: Check that Trello's features behave the way the requirements say they should, starting with the card write path that the rest of the product is built on.

**Examples**:

1. Dragging a card from "To Do" to "Doing" keeps the new list and position after a page reload.
2. Setting a due date on a card produces the reminder notification at the configured time.
3. Archiving a card removes it from the board but keeps it retrievable from the archive.

**Priority**: Critical

**Justification**: These are the mission-critical functions from Part 1. If a card move does not persist, Trello stops being a reliable system of record.

---

## Test Type: Regression Testing

**Category**: Functional

**Purpose**: Confirm that existing behaviour still works after a change. Trello ships continuously and most of the product is reachable from any board, so an unrelated change can easily break the card detail view or the activity feed.

**Examples**:

1. After a change to the card detail modal, checklists, labels, attachments and comments all still save.
2. After a refactor of the permission layer, the private-board access suite is re-run in full.
3. After a Power-Up API change, boards using the most popular Power-Ups still load.

**Priority**: Critical

**Justification**: The write path and the permission layer are where defects cluster, and both are touched constantly, so an undetected regression is both likely and expensive.

---

## Test Type: Smoke Testing

**Category**: Functional

**Purpose**: A broad but shallow check after every build that the basics work, before anyone spends time on deeper testing.

**Examples**:

1. A user can log in and the board list loads.
2. A board opens and renders its lists and cards.
3. A new card appears immediately for a second connected client.

**Priority**: High

**Justification**: It is cheap and it protects the rest of the pipeline. With several builds a day, catching a broken build early saves more time than the suite costs.

---

## Test Type: Performance Testing

**Category**: Non-Functional

**Purpose**: Make sure boards load and stay responsive at realistic size and load, and that the WebSocket layer holds up with many simultaneous viewers.

**Examples**:

1. **Load**: a board with 5,000 cards across 20 lists opens in under 3 seconds and scrolls without dropped frames.
2. **Stress**: the WebSocket service is pushed past its rated connection count to find the breaking point and confirm it degrades gracefully.
3. **Spike**: 200 members opening the same board within a minute - the Monday-morning pattern - does not delay updates for everyone else.
4. **Endurance**: a board left open for 8 hours shows no memory growth and no loss of real-time updates.

**Priority**: High

**Justification**: Slow boards are the most common reason teams abandon the tool, and the biggest boards belong to the paying customers.

---

## Test Type: Security Testing

**Category**: Non-Functional

**Purpose**: Find vulnerabilities before attackers do. Trello boards routinely hold confidential material - hiring pipelines, roadmaps, credentials pasted into cards - so unauthorised access is the highest-impact failure the product has.

**Examples**:

1. A non-member cannot read a private board by requesting its board ID through the public API.
2. Revoking a member's access immediately closes their existing WebSocket subscription to that board.
3. A card description containing a script tag renders as text instead of executing (XSS).
4. An uploaded attachment cannot be served in a way that runs code in the application's origin.

**Priority**: Critical

**Justification**: A permission leak exposes company data with no rollback, and it is easy to introduce because access has to be enforced on the API and the WebSocket channel, not only in the UI.

---

## Test Type: Usability Testing

**Category**: Non-Functional

**Purpose**: Measure how easily a new user understands the board metaphor and finishes everyday tasks, and how well drag-and-drop actually works on a touch screen.

**Examples**:

1. A first-time user creates a board, adds three lists and moves a card between them, unaided, in under 3 minutes.
2. On a phone, dragging a card between lists works on the first attempt for at least 8 of 10 participants.
3. Users find the board's visibility setting without being told where it lives.

**Priority**: High

**Justification**: Trello competes on simplicity - it is why people pick it over heavier tools - so a usability defect attacks the product's main differentiator.

---

## Test Type: Compatibility Testing

**Category**: Non-Functional

**Purpose**: Verify Trello works on the browsers, operating systems, devices and screen sizes its users actually have, including the Electron desktop app.

**Examples**:

1. Board rendering and drag-and-drop behave the same on current Chrome, Firefox, Safari and Edge.
2. The mobile apps work on the oldest supported iOS and Android versions as well as the newest.
3. The board view stays usable on a small phone, a tablet in landscape and an ultrawide monitor.

**Priority**: High

**Justification**: Companies standardise on browsers the team may not use daily, and drag-and-drop is exactly the interaction most sensitive to browser and input differences.

---

## Test Type: Accessibility Testing

**Category**: Non-Functional

**Purpose**: Make sure people using screen readers or keyboard-only navigation can work with the product, which also matters commercially because enterprise buyers ask for accessibility compliance.

**Examples**:

1. A card can be moved between lists using only the keyboard, with no mouse drag.
2. Screen readers announce card titles, list names and the result of a move.
3. Label colours meet WCAG 2.1 AA contrast and are not the only way to tell labels apart.

**Priority**: Medium

**Justification**: It affects a smaller share of users and rarely causes data loss, but drag-and-drop is hostile to assistive technology by nature, so it needs deliberate testing instead of assumed coverage.

---

## Test Type: Reliability and Recovery Testing

**Category**: Non-Functional

**Purpose**: Verify that Trello survives lost connections, concurrent edits and offline use, and comes back into a correct state instead of a divergent one.

**Examples**:

1. Dropping the WebSocket for 60 seconds and reconnecting resyncs the board to the correct state without duplicating cards.
2. Two users drag the same card to different lists at the same moment; both clients end up on one agreed position.
3. Edits made offline in the mobile app are queued and applied on reconnect, with conflicts resolved rather than silently dropped.

**Priority**: Critical

**Justification**: Real-time sync is Trello's defining feature and these are ordinary conditions - dropped Wi-Fi and two people touching one card happen daily. A failure here causes silent data loss, the hardest kind of defect for users to notice and for support to reproduce.

---

## Summary

| Test Type                | Category       | Priority |
| ------------------------ | -------------- | -------- |
| Functional               | Functional     | Critical |
| Regression               | Functional     | Critical |
| Smoke                    | Functional     | High     |
| Performance              | Non-Functional | High     |
| Security                 | Non-Functional | Critical |
| Usability                | Non-Functional | High     |
| Compatibility            | Non-Functional | High     |
| Accessibility            | Non-Functional | Medium   |
| Reliability and Recovery | Non-Functional | Critical |
