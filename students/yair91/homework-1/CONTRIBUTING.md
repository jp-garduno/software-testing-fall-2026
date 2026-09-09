# Contributing

This repository follows a simplified GitHub Flow. `main` is always in a
working state; every change arrives through a feature branch and a pull
request.

## Branching

Branch names use a `type/short-description` format, lowercase, dashes instead
of spaces:

| Prefix     | Used for                     |
| ---------- | ---------------------------- |
| `feature/` | New functionality or content |
| `fix/`     | Corrections to existing work |
| `docs/`    | Documentation-only changes   |

Examples: `feature/add-styling`, `fix/typo-in-readme`, `docs/update-workflow`.

Every branch is created from an up-to-date `main`:

```bash
git checkout main
git pull origin main
git checkout -b feature/my-change
```

## Commits

Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>
```

Types used here: `feat`, `fix`, `docs`, `style`, `refactor`, `chore`.

Rules:

- One logical change per commit. If the message needs an "and", split it.
- Description in the imperative mood, lowercase, no trailing period.
- No vague messages such as `update`, `fix stuff` or `changes`.

## Pull Requests

1. Push the branch: `git push -u origin feature/my-change`
2. Open a PR against `main`.
3. Fill in what changed, why, and how it was verified.
4. Merge once the description is complete, then delete the branch.

## Releases

Stable states of `main` are tagged with annotated tags following semantic
versioning:

```bash
git tag -a v1.0.0 -m "first complete version of the portfolio"
git push origin v1.0.0
```
