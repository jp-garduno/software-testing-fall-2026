# Contributing

Conventions used in this project.

## Branches

`<type>/<username>/<short-description>` — for example
`feature/gilbertoanayam17/add-styling`.

| Type        | Use                                       |
| ----------- | ----------------------------------------- |
| `feat/`     | new feature                               |
| `fix/`      | bug fix                                   |
| `docs/`     | documentation only                        |
| `refactor/` | restructuring with no change in behaviour |
| `chore/`    | maintenance                               |

Branches are created from the integration branch, kept short-lived, and deleted after the pull request is merged.

## Commits

Conventional Commits, imperative mood, no trailing period:

```
<type>(<scope>): <subject>

- more details (optional)
```

One logical change per commit. Run `git status` and `git diff` before staging.

## Pull requests

1. Push the branch and open a PR against the integration branch.
2. Title: same format as a commit subject.
3. Description: fill in the repository template (`.github/PULL_REQUEST_TEMPLATE.md`) what changed, why it was needed, and how it was tested. Never leave the template empty.
4. Merge with "Rebase and merge" so the individual commits stay in the history.
5. Delete the branch after merging.
