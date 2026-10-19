# Homework 5: White Box Testing - TaskFlow

TaskFlow implementa el modelo y la lógica de negocio de un administrador de tareas. Esta entrega aplica pruebas de caja blanca, cobertura de sentencias y ramas, integración entre componentes y aislamiento de dependencias externas.

Las pruebas usan el modelo y el servicio reales. El repositorio y el envío de correo y SMS se sustituyen por mocks, stubs o un fake en memoria; no se necesita una base de datos ni credenciales externas.

## Objetivos y resultados

- Probar las validaciones, las transiciones de estado, las prioridades y los vencimientos.
- Verificar flujos completos y fallos de persistencia y notificaciones.
- Superar el 80% de cobertura requerido, con aserciones sobre resultados e interacciones.
- Documentar las métricas, sus límites y las decisiones de implementación.

Resultado verificado con Python 3.13.9: **124 casos aprobados, sin pruebas omitidas ni xfail**. La ejecución sin cobertura tomó **0.38 segundos** en el equipo de desarrollo; la duración depende del equipo y del instrumentado de cobertura.

| Métrica | Resultado |
| --- | --- |
| Sentencias | 100%: 196/196 |
| Ramas | 100%: 66/66 |
| Funciones implementadas | 100%: 20/20 |
| Pylint, configuración del evaluador | 10.00/10 en `src/` y `tests/` |

La cobertura de funciones se calcula a partir de los datos por función de `coverage.json`; no aparece como columna del resumen de terminal. El detalle está en [el análisis de cobertura](reports/coverage-analysis.md).

## Requisitos

- Python 3.11 o posterior, con el lanzador `py` disponible en Windows.
- PowerShell.
- Git.

## Instalación en Windows

Todos los comandos siguientes se ejecutan desde `students/Luis-045/homework-5/` dentro del repositorio de la clase:

```powershell
py -3 --version
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest --version
```

La primera orden debe mostrar Python 3.11 o posterior. Usar directamente el ejecutable del entorno evita tener que activar scripts de PowerShell. `requirements.txt` fija las versiones verificadas de las herramientas; quien ya las instaló durante la preparación no necesita reinstalarlas.

`unittest.mock`, `datetime`, `dataclasses` y las demás dependencias del código de producción pertenecen a la biblioteca estándar.

## Ejecutar las pruebas

Ejecutar toda la suite o solamente las pruebas unitarias:

```powershell
.\.venv\Scripts\pytest.exe -v
.\.venv\Scripts\pytest.exe tests/test_task_unit.py -v
```

Con un entorno ya activado también se puede usar `pytest -v`. `pytest.ini` define `testpaths = tests` y `pythonpath = . src`, de modo que el comando de consola del evaluador encuentra el código.

| Archivo de pruebas | Funciones de prueba | Casos ejecutados |
| --- | --- | --- |
| `test_task_unit.py` | 20 | 52 |
| `test_task_service_integration.py` | 29 | 34 |
| `test_mocking.py` | 12 | 14 |
| `test_coverage_edge_cases.py` | 13 | 24 |
| **Total** | **74** | **124** |

La parametrización cubre, entre otros casos, las 16 combinaciones de estados. Las fixtures se crean de nuevo para cada prueba; el reloj se controla sin `sleep` ni dependencia entre pruebas.

## Generar cobertura y capturas

```powershell
.\.venv\Scripts\pytest.exe -v --cov=src --cov-branch --cov-report=term-missing --cov-report=html --cov-report=json
Start-Process .\htmlcov\index.html
```

El comando mide únicamente `src/`, produce la tabla de terminal, `coverage.json` y un reporte navegable en `htmlcov/`. Los archivos generados y `.venv/` están excluidos de Git.

Las capturas reales se incorporan manualmente en `reports/screenshots/`:

- `test-execution.png`: salida de `pytest.exe -q` con todos los casos aprobados.
- `coverage-summary.png`: tabla de cobertura de la terminal.
- `coverage-html-report.png`: reporte HTML abierto en el navegador, mostrando el detalle de un archivo.

Las capturas están pendientes de incorporación por el autor; no se reemplazan con imágenes fabricadas ni se incluyen los reportes HTML generados en el commit.

## Estructura

```text
homework-5/
├── README.md
├── requirements.txt
├── pytest.ini
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── task.py
│   ├── task_repository.py
│   ├── notification_service.py
│   └── task_service.py
├── tests/
│   ├── conftest.py
│   ├── test_task_unit.py
│   ├── test_task_service_integration.py
│   ├── test_mocking.py
│   └── test_coverage_edge_cases.py
└── reports/
    ├── coverage-analysis.md
    ├── analysis-report.md
    ├── reflection.md
    └── screenshots/
```

`task.py` contiene el modelo, las enumeraciones, las validaciones y las reglas de tiempo y estados. `task_service.py` coordina los casos de uso. `TaskRepository` y `NotificationService` son contratos `Protocol` para adaptadores externos; el fake en memoria vive únicamente en `tests/conftest.py`.

## Funcionalidades y decisiones

- `create_task`: valida el título, la descripción, la prioridad y la fecha, comprueba la unicidad y guarda antes de notificar.
- `update_task`: acepta título, descripción, prioridad, fecha y estado; valida todos los cambios sobre una copia antes de guardar.
- `update_task_status`: permite `TODO → IN_PROGRESS → DONE` y el archivo desde cualquiera de esos estados.
- `delete_task`: marca como `ARCHIVED`, conserva el registro y evita la eliminación física. Las tareas archivadas no pueden modificarse ni restaurarse.
- `search_tasks`: combina estado, prioridad, título parcial sin distinguir mayúsculas y un intervalo inclusivo de fechas de vencimiento. Sin filtros devuelve todos los registros, incluidos los archivados; con fechas excluye los registros sin vencimiento.
- `check_overdue_tasks`: evalúa todo el lote con una sola hora del servicio y avisa sobre tareas vencidas que no estén terminadas ni archivadas. Puede invocarse periódicamente desde un llamador; la entrega no incorpora un proceso en segundo plano.

El título conserva su contenido y requiere entre 3 y 100 caracteres, sin aceptar cadenas en blanco. La unicidad es exacta y distingue mayúsculas, conforme al contrato de búsqueda por título; los títulos archivados siguen reservados. La descripción admite hasta 500 caracteres; `None` se normaliza a una cadena vacía y los valores mayores se rechazan. La fecha es opcional, pero, al crearla o cambiarla, debe ser estrictamente futura. Las fechas sin zona se interpretan como UTC y las demás se convierten a UTC.

El servicio conserva la identidad y la fecha de creación al actualizar, y modifica `updated_at`. Archivar y cambiar otros campos en la misma operación es inválido. Un error de persistencia se propaga sin emitir un aviso de éxito; un `NotificationError` se registra y no deshace una operación guardada. Los adaptadores deben traducir sus fallos a `RepositoryError` o `NotificationError`, respectivamente.

Las notificaciones de correo usan el destinatario de ejemplo del enunciado. Si se configura `phone_number` en el servicio, las tareas `URGENT` también generan SMS. Cada canal se maneja por separado. Las comprobaciones repetidas de vencimientos pueden volver a notificar: no se implementan reintentos ni deduplicación de avisos.

## Formato y revisión

```powershell
.\.venv\Scripts\python.exe -m black --check src tests
.\.venv\Scripts\python.exe -m isort --check-only --profile black src tests
.\.venv\Scripts\python.exe -m pylint --rcfile=../../../.github/grading/pylintrc src tests
```

Se usa la configuración compartida de Pylint únicamente para lectura. Las dos excepciones locales documentadas corresponden a los atributos exigidos del modelo y a los cinco filtros independientes del servicio.

## Entrega

Rama: `feat/Luis-045/homework-5`. Todos los cambios de contenido pertenecen a esta carpeta. El PR debe apuntar a `main`, usar el título `Homework 5: White Box Testing - Luis-045` y llevar la etiqueta `homework` para activar la calificación. La referencia para Canvas es la URL del PR.

## Autor

Luis-045 - Software Testing Fall 2026.
