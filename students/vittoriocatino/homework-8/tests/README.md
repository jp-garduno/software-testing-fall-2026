# Entradas de la suite de sistema

La configuración `pytest.ini` descubre las suites en sus carpetas de framework,
como pide el enunciado. Este índice permite localizar las pruebas desde la
carpeta convencional `tests/` sin duplicar su ejecución ni sus implementaciones.

| Suite | CRUD / edición | Filtros | Ejecución |
|---|---|---|---|
| Selenium | `../selenium/tests/test_todo_crud.py` | `../selenium/tests/test_todo_filter.py` | `python -m pytest selenium/tests -q` |
| Playwright | `../playwright/tests/test_todo_crud.py` | `../playwright/tests/test_todo_filter.py` | `python -m pytest playwright/tests -q` |
| BDD | `../features/todo.feature` | Scenario Outline con All/Active/Completed | `python -m behave features` |

Los comandos se ejecutan desde la raíz de `homework-8/`. El runner conjunto
es `python scripts/run_all.py`; publica resultados reales en `reports/` y
capturas en `screenshots/`. La prueba de cancelación es una falla conocida
estricta en ambos frameworks; los detalles están en `DEFECTS.md`.
