# Homework 1 Reflection

One of the main challenges I faced during this assignment was understanding how feature branches, pull requests, and merge strategies affect Git history. I expected every commit from my feature branches to appear individually in my homework branch, but after using Squash and Merge I learned that GitHub combines those commits into a single commit in the destination branch. This helped me understand the difference between feature-branch history and the final branch history.

The Git commands I found most useful were `git checkout -b`, `git status`, `git add`, `git commit`, `git push`, and `git pull`. I also used `git log --oneline` and `git rev-list --count` to verify my commit history before submission.

In a team project, I would use feature branches to keep changes isolated, create pull requests for review, and avoid modifying the shared main branch directly. Clear branch names and meaningful commit messages would make collaboration and debugging easier.

## Branching Strategy

I created these feature branches:

- `feature/Luis-045/initial-structure`
- `feature/Luis-045/add-styling`
- `feature/Luis-045/add-content`

Each branch was merged into `feat/Luis-045/homework-1` through a pull request. The final homework branch will be submitted to `main`.

## Pull Requests

- PR #40 - Add initial portfolio structure
- PR #46 - Add portfolio styling
- PR #47 - Add portfolio content and documentation

## Commit History

My development commits included:

- `feat: create initial portfolio structure`
- `feat: add portfolio page sections`
- `docs: add initial project README`
- `style: add base portfolio styling`
- `style: improve navigation styling`
- `style: enhance section layout and responsiveness`
- `feat: add about me content`
- `feat: add projects content`
- `feat: add contact information`
- `docs: document Git workflow and setup instructions`