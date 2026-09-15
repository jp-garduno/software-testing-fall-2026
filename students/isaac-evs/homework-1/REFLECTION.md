# Reflection — Homework 1: Git Workflow Practice

## Challenges Faced

The biggest challenge was resisting the urge to just work on one branch and dump everything into a single commit. Splitting the portfolio into logical pieces — structure, styling, content, documentation — meant constantly asking "is this one idea or several?" before committing. I also had to be careful with `git merge --no-ff`, since forgetting the flag would have collapsed my feature branches into fast-forward merges and erased the branch history I wanted to keep visible in the log. Writing commit messages that actually explained the "why" instead of just restating the diff took more thought than I expected.

## Useful Git Commands

- `git checkout -b <branch>` to create and switch to feature branches from a specific starting point.
- `git merge --no-ff <branch>` to preserve merge commits and keep a readable history of feature work.
- `git log --oneline --graph` to visualize how the feature branches merged back into the homework branch.
- `git add <path>` (instead of `git add .`) to stage only the files relevant to the current logical change.
- `git commit --amend --reset-author` to fix commit authorship after realizing my local Git config wasn't set correctly.

## Application to Team Project

For the semester-long team project, I plan to use the same branch-per-feature approach demonstrated here: create a descriptively named branch for each unit of work, keep commits small and scoped, and open a pull request as soon as a feature is ready for review rather than batching multiple features into one large PR. This should make code review faster for teammates and make it much easier to bisect or revert a single feature if something breaks, since each piece of work has its own isolated history instead of being tangled together with unrelated changes.

## Branching and Commit Summary

This submission includes 4 feature branches (`feature/initial-structure`, `feature/add-styling`, `feature/add-content`, `feature/add-documentation`) merged into `feat/isaac-evs/homework-1`, with 11 commits total using `feat`, `fix`, `style`, `chore`, and `docs` types, as documented in the README.
