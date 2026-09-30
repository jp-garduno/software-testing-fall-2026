# Part 1: Application Selection & Analysis

I chose **Option A**: an application I use regularly.

## Application: Trello

**Purpose**: Trello organises work visually. A **board** is a project, **lists** are the stages of that project, and **cards** are the pieces of work you drag from one stage to the next. What separates it from a normal to-do app is that boards are live: when one member moves a card, everyone else looking at that board sees it move within a second, without refreshing. Trello launched in 2011 and has belonged to Atlassian since 2017.

**Target Users**:

- **Small teams and startups** running sprints, hiring pipelines or content calendars.
- **Individuals** using Trello as a personal to-do system.
- **Large organisations** on paid tiers, where boards sit inside workspaces with admin controls.
- **Third-party developers** building Power-Ups on Trello's public API.

**Key Features**:

1. Boards, lists and cards with drag-and-drop reordering between lists.
2. Card detail: descriptions, checklists, due dates, labels, members and attachments.
3. Real-time sync of every change across all connected clients.
4. Comments, mentions and an activity feed per card and per board.
5. Permissions and visibility settings (private, workspace, public) with member roles.
6. Search and filtering across cards, boards and workspaces.
7. Butler automation: rules and scheduled commands that act on cards on their own.
8. Power-Ups and a public REST API for integrations.
9. Calendar, timeline, table and dashboard views on paid plans.

**Technology Stack** (as publicly described by Trello's engineering team):

- **Frontend**: a single-page web app, originally Backbone.js and progressively moved to React, plus native iOS and Android apps and an Electron desktop app.
- **Backend**: **Node.js** services behind **HAProxy**.
- **Data**: **MongoDB** as the main database, **Redis** for sessions and ephemeral data, **Elasticsearch** for search.
- **Real time**: **WebSockets** push board changes to every connected client.
- **Hosting**: Amazon Web Services.

This stack shapes the strategy directly. WebSocket sync turns concurrency and reconnection into core test targets instead of edge cases, and a separate search index means results can legitimately lag behind the database, so that lag has to be tested as expected behaviour rather than reported as a bug.

**Critical Functions**:

1. **Card creation, editing and movement** - the core write path. A lost card, or a move that silently reverts, destroys trust in the tool as a system of record.
2. **Real-time synchronisation** - two people on the same board must end up in the same state, with no lost update and no phantom card.
3. **Permission enforcement** - a private board must never be readable by a non-member, and that has to hold at the API level, not just in the UI.
4. **Board loading performance** - a board with thousands of cards still has to open and stay responsive.
5. **Butler automation** - rules run with nobody watching, so a faulty rule can modify hundreds of cards before anyone notices.

Alternative views and the dashboard matter commercially, but they can degrade for an afternoon without lasting damage. That distinction drives the priorities in Parts 2 and 5.
