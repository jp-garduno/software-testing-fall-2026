# Test Execution Report

## Command

```bash
python -m pytest -v --cov=src --cov-branch --cov-report=term-missing --cov-report=html
```

## Verified Result

```text
42 passed in 0.11s

Name                          Stmts   Miss Branch BrPart  Cover
src/notification_service.py       5      0      0      0   100%
src/task.py                      54      0     20      0   100%
src/task_repository.py           13      0      0      0   100%
src/task_service.py              77      1     38      1    98%
TOTAL                           149      1     58      1    99%
```

The HTML coverage output is generated into `htmlcov/` by the command above and is intentionally excluded from version control because it is reproducible build output.
