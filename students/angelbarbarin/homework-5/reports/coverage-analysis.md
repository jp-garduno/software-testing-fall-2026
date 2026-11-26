# Coverage Analysis – TaskFlow

Herramienta: `pytest` + `pytest-cov` (coverage.py) con medición de ramas (`--cov-branch`).

```bash
pytest -v --cov=src --cov-branch --cov-report=term-missing --cov-report=html
```

## Coverage Summary

| Metric             | Threshold | Achieved | Status  |
| ------------------ | --------- | -------- | ------- |
| Statement Coverage | 80%       | 100%     | ✅ Pass |
| Branch Coverage    | 80%       | 100%     | ✅ Pass |
| Function Coverage  | 80%       | 100%     | ✅ Pass |
| Line Coverage      | 80%       | 100%     | ✅ Pass |

- 293 sentencias, 96 ramas, 40 funciones/métodos en `src/`; 0 sentencias y 0 ramas sin cubrir.
- En Python, coverage.py mide sentencias por línea, así que *statement* y *line coverage* son la misma cifra.
- *Function coverage* = funciones con al menos una línea ejecutada (40 de 40), calculado a partir de `coverage json`.
- 135 pruebas, todas pasan. La suite completa tarda ~0.3 s sin cobertura y <1 s con cobertura.

## Coverage by File

| File                    | Statements | Branches | Functions | Lines |
| ----------------------- | ---------- | -------- | --------- | ----- |
| task.py                 | 100% (122) | 100% (50) | 100% (14) | 100% |
| task_service.py         | 100% (76)  | 100% (20) | 100% (11) | 100% |
| task_repository.py      | 100% (52)  | 100% (16) | 100% (7)  | 100% |
| notification_service.py | 100% (43)  | 100% (10) | 100% (8)  | 100% |

## How Coverage Goals Were Achieved

### Initial Coverage: 87% (combinado sentencias + ramas)

La primera medición se hizo solo con las pruebas unitarias del modelo y las de integración del servicio
(84 pruebas). Ver `screenshots/coverage-initial.png`.

| File                    | Statements | Branches | Missing |
| ----------------------- | ---------- | -------- | ------- |
| task.py                 | 100%       | 100%     | –       |
| task_service.py         | 100%       | 100%     | –       |
| task_repository.py      | 79%        | 81%      | manejo de errores de BD y 3 ramas de `search()` |
| notification_service.py | 40%        | 0%       | casi todo: validaciones, reintentos, mensajes |
| **Total**               | **87.4%**  | **86.5%** |        |

El reporte dejó claro por qué: las pruebas de integración usan un `Mock(spec=NotificationService)`, así que el
código real del servicio de notificaciones **nunca se ejecutaba**. Igual con el repositorio: el `FakeDatabase`
nunca falla, así que los `except` que traducen errores a `RepositoryError` quedaban sin ejecutar.

### Strategy Applied

1. **Probar `NotificationService` real con los *gateways* simulados** (`email_client` y `sms_client` como `Mock`).
   Así se ejecuta la lógica propia (validación de correo/teléfono, truncado de SMS, reintentos) y solo se simula
   la red. Cobertura del archivo: 32% → 100%.
2. **Inyectar fallas con `side_effect`** en una base de datos simulada para cubrir los cuatro `except` del
   repositorio, verificando además que la causa original se conserva (`__cause__`).
3. **Valores límite en el filtro de fechas** (rango inclusivo, rango invertido, tareas sin fecha) y el filtro de
   título en blanco: cubrió las 3 ramas parciales de `search()`. Repositorio: 79% → 100%.
4. **Reintentos**: éxito tras 2 fallas, rendición tras `max_retries + 1` intentos y `max_retries=0`.

### Final Coverage: 100%

51 pruebas nuevas (`test_coverage_edge_cases.py` y `test_mocking.py`) dirigidas a las líneas que el reporte
marcaba como faltantes. Ver `screenshots/coverage-summary.png` y `screenshots/coverage-html-report.png`.

## Untested Code Paths

No quedan líneas ni ramas sin ejecutar. Pero 100% de cobertura de ramas **no** significa que todo esté probado;
estas son las rutas que la métrica no ve y por qué se dejaron así:

### task_repository.py – `search()`: combinaciones de filtros

**Code**:

```python
if status is not None: ...
if priority is not None: ...
if due_after is not None: ...
if due_before is not None: ...
if title_contains and title_contains.strip(): ...
```

**Reason**: son 5 decisiones independientes, es decir 2⁵ = 32 caminos. La cobertura de ramas se cumple con
cada filtro encendido y apagado; las pruebas cubren cada filtro solo, sin filtros, y todos juntos, pero no las 32
combinaciones (cobertura de caminos). Como los filtros se combinan con `all(...)` y no dependen entre sí, el
riesgo de que una combinación concreta falle es bajo.

**Risk**: Low

### task_repository.py – condiciones compuestas dentro de lambdas

**Code**:

```python
predicates.append(lambda task: task.due_date is not None and task.due_date >= due_after)
```

**Reason**: coverage.py marca la línea como cubierta aunque solo se evalúe una de las dos condiciones; no mide
*condition coverage*. Se revisó a mano: hay pruebas con tareas sin fecha (`False` en la primera condición) y con
fechas dentro y fuera del rango (ambos valores de la segunda).

**Risk**: Very Low

### Adaptadores reales de base de datos, correo y SMS

**Reason**: `database`, `email_client` y `sms_client` son dependencias externas. La tarea pide simularlas, así
que no existe una implementación real que medir. El riesgo es que el mock no se comporte como el cliente real
(por ejemplo, que el cliente real devuelva un código en lugar de lanzar excepción). Se mitiga con
`Mock(spec=...)`, que falla si se llama un método que la clase real no tiene, y debería cubrirse con pruebas de
sistema contra un servidor SMTP/BD de prueba.

**Risk**: Medium – es la principal limitación de una suite basada en mocks.

### Revisión periódica de tareas vencidas

**Reason**: la regla “check for overdue tasks periodically” se implementa como `check_overdue_tasks(now)`, que
es lo que llamaría un programador de tareas (cron, scheduler). El programador en sí no es parte del sistema.

**Risk**: Low

### Contenido de los logs

**Reason**: cuando falla una notificación se ejecuta `logger.warning(...)` (está cubierto), pero ninguna
prueba verifica el texto del log; sí se verifica el contador `failed_notifications`.

**Risk**: Very Low – solo diagnóstico.

## Screenshots

| Archivo | Contenido |
| ------- | --------- |
| `screenshots/test-execution.png` | Salida de `pytest -v` con las 135 pruebas |
| `screenshots/coverage-summary.png` | Tabla de cobertura final en terminal |
| `screenshots/coverage-initial.png` | Primera medición (87%) – tendencia de cobertura |
| `screenshots/coverage-html-report.png` | Índice del reporte HTML |
| `screenshots/coverage-html-task-service.png` | Detalle HTML de `task_service.py` con líneas cubiertas |
