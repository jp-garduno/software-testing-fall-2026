# Reflection: Homework 1

## What challenges did I face?

The portfolio was the easy part, Git was where I got a little stuck.

My first commit was already wrong: I saved the `.gitignore` one level above the submission folder, committed and pushed before noticing. My first tought was to amend and force push, but the commit was already published, so I moved the file with `git mv` and recorded the correction as its own `fix:` commit. Rewriting published history would have been faster and dishonest. The same rule cost me a typo later: a commit message went out as "documententation" and it stays, because a cosmetic fix is not worth rewriting what others may have already pulled.

Merging surprised me too. This repository has merge commits disabled, and squashing would have collapsed each branch into a single commit, erasing exactly what the assignment is about, so I rebased. Then `git branch -d` refused to delete them, because rebasing rewrites the SHAs, so `-D` was the answer.

## Which Git commands were most useful?

`git status` before every `git add` and `git diff` before every commit: between them they caught a stray backup file and a navigation link pointing to a section id that did not exist. `git mv` kept a rename visible as a rename.

## How will I apply this in the team project?

Short-lived branches and one pull request per unit of work, but mostly this: `git commit --amend` is for commits nobody has seen yet. Once something is pushed, the honest fix is another commit. In a team that difference decides whether I break everyone else's history.

## Commit history and branching strategy

- Submission branch: `feat/gilbertoanayam17/homework-1`, created from `main`
- Feature branches: `initial-structure`, `add-styling`, `add-content`; fix branch: `nav-and-title-typos` (all prefixed `<type>/gilbertoanayam17/`)
- Conventional Commits (`feat`, `fix`, `docs`, `style`, `refactor`, `chore`) merged through 4 pull requests plus this final one.