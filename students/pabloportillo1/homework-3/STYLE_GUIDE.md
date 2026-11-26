# Team Style Guide — Python

A short, enforceable style guide. Every rule here is checked by a tool; nothing in this document
relies on a reviewer remembering it.

## 1. Formatting is not a discussion

Black owns formatting, line length 120. isort owns import order, `black` profile. Neither is
configurable per developer, and neither belongs in a code review comment. If you disagree with an
output, take it up with the tool's maintainers, not with your teammate.

## 2. CI runs exactly what pre-commit runs

The pull request gate and the local hook use the same `.pre-commit-config.yaml`. If the two ever
drift, developers stop trusting local hooks and start passing `--no-verify`, and the whole setup
is worthless.

## 3. Disable rules narrowly, never in bulk

A rule that does not fit gets disabled **inline at the one site**, with a reason:

```python
value = compute()  # pylint: disable=invalid-name  # matches the NEWS2 spec notation
```

Adding a code to the `disable =` list in `.pylintrc` requires review, because it silences the rule
for everyone forever. A 10/10 score obtained by switching rules off measures nothing.

## 4. Naming

`snake_case` for functions, variables and arguments. `PascalCase` for classes. `UPPER_SNAKE` for
module constants. One name per domain concept across every layer — if the database column is
`systolic_bp`, the Python field is not `sbp` and the UI label is not `systolicPressure`.

## 5. Docstrings

Every module, public class and public function has a docstring that says what the caller gets, not
what the code does line by line. Private helpers may skip it when the name is honest.

## 6. Comments

Default to none. A comment must record something the code cannot express — a clinical rule, a
security decision, a gotcha. Never restate the line above it.

## 7. Guard clauses over nesting

Return early. `else` after `return` or `raise` is flagged by Pylint (`R1705` / `R1720`) and should
be flattened.

## 8. Identity for singletons

`is None`, never `== None`. Same for `True` and `False`.

## 9. Never a mutable default argument

`def f(items=[])` shares one list across all calls. Use `None` and build inside the function.
Pylint `W0102` catches this, and it has caused real defects in this codebase.

## 10. Conventional commits

`<type>(<scope>): <description>` in the imperative, lowercase. Types: `feat`, `fix`, `docs`,
`style`, `refactor`, `test`, `chore`. Enforced at `commit-msg` stage.
