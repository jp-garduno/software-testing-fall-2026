# Homework 5: TaskFlow — White Box Testing

Autor: Aldo Ramon Velazquez Fonseca. Entrega en `students/4Ald0/homework-05/`.

TaskFlow implementa el ciclo de vida de tareas, validación de datos, búsquedas,
persistencia mediante un cliente inyectado y notificaciones por correo y SMS.
El objetivo es comprobar sus decisiones internas con pruebas independientes,
analizar cobertura y verificar fallos sin conectarse a servicios externos.

## Requisitos e instalación

Python **3.11 o posterior**, pytest y pytest-cov. Validado con Python 3.12.14,
pytest 8.4.2, pytest-cov 7.1.0 y coverage.py 7.16.2 en Windows.

Desde la raíz del repositorio:

```powershell
cd students/4Ald0/homework-05
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

En Linux/macOS, la activación es `source .venv/bin/activate`. Todas las
instrucciones siguientes se ejecutan desde `homework-05/` con el entorno activo.
El archivo `pytest.ini` permite importar `src/` también usando `pytest` directamente.

## Pruebas y cobertura

```powershell
pytest -q
pytest tests/test_task_unit.py -v
pytest -v --cov=src --cov-branch --cov-report=term-missing --cov-report=html --cov-report=json:reports/coverage.json
python tools/report_metrics.py
```

Abre `htmlcov/index.html` en un navegador para examinar las líneas cubiertas.
El informe HTML y el JSON completo se regeneran localmente y están ignorados
por Git. Las capturas y el resumen medido sí forman parte de esta entrega.

| Medida | Resultado verificado |
| --- | --- |
| Pruebas unitarias del modelo | 59 casos |
| Pruebas de integración | 19 casos |
| Casos límite | 19 casos |
| Mocking y aislamiento | 15 casos |
| Total | **112 aprobadas**, sin omisiones ni xfail |
| Sentencias/líneas | **187/187, 100%** |
| Ramas | **54/54, 100%** |
| Funciones Python con nombre | **29/29, 100%** |
| Duración reportada por pytest, sin cobertura | **0.75 s** |
| Duración con cobertura, salida detallada y reportes | **2.84 s** |

La duración depende del equipo. Los tiempos anteriores corresponden a las
ejecuciones registradas, no a una garantía de rendimiento. La cobertura de
funciones se deriva de cuerpos con nombre ejecutados en el JSON de coverage.py;
no incluye el cuerpo del módulo ni funciones generadas por `dataclass`.

## Estructura

```text
homework-05/
├── README.md, requirements.txt, pytest.ini, .gitignore
├── src/
│   ├── __init__.py
│   ├── task.py
│   ├── task_service.py
│   ├── task_repository.py
│   └── notification_service.py
├── tests/
│   ├── conftest.py
│   ├── test_task_unit.py
│   ├── test_task_service_integration.py
│   ├── test_coverage_edge_cases.py
│   └── test_mocking.py
├── tools/report_metrics.py
└── reports/
    ├── coverage-analysis.md, analysis-report.md, reflection.md
    ├── coverage-summary.json, test-execution.txt
    └── screenshots/
```

## Funcionalidades y decisiones

- Títulos de 3–100 caracteres, no vacíos; descripción de hasta 500 caracteres.
  Una descripción excesiva se rechaza para respetar el máximo del enunciado.
- Prioridades LOW, MEDIUM, HIGH y URGENT; comparación y orden descendente.
- UUID automático, estado inicial TODO y marcas de creación y actualización.
- Transiciones TODO → IN_PROGRESS → DONE; archivo desde cualquier estado activo.
  ARCHIVED es terminal y no admite ediciones. Archivar y editar otros campos
  requiere operaciones distintas: no se admite `status` en `update_task`.
- Fechas locales sin zona, como los ejemplos del enunciado. La fecha es opcional;
  si se proporciona debe ser estrictamente futura al crearla o reemplazarla.
  Una tarea está vencida cuando su fecha es anterior al reloj y no es DONE ni
  ARCHIVED, según la aclaración acordada. Llegar exactamente al límite no vence
  la tarea. Se puede editar la descripción de una tarea ya vencida.
- Unicidad por título exacto, incluidos los archivados. Las búsquedas parciales
  ignoran mayúsculas; los límites del rango de fechas de vencimiento son inclusivos.
- Borrado lógico mediante archivo y operación explícita de borrado permanente.
  No hay función de restauración. Los errores de persistencia se propagan.
- Notificaciones tras guardar; un fallo de correo o SMS queda registrado y no
  revierte la operación. El envío urgente con SMS es explícito mediante
  `create_task_with_sms`; las alertas de vencimiento urgente usan ambos canales.
- El chequeo periódico se puede invocar mediante `check_overdue_tasks`; el
  programador externo queda fuera de este ejercicio. Cada invocación puede
  volver a notificar tareas vencidas; no hay deduplicación de alertas.

`TaskRepository` recibe un cliente con `save`, `find_by_id`, `find_all` y `delete`.
`NotificationService` recibe un transporte con `send_email` y `send_sms`. Son
fronteras inyectables: esta tarea no incluye una base de datos, credenciales ni
envío real de mensajes. Las pruebas usan mocks con especificación y un almacén
falso en memoria; varias integraciones verifican también el repositorio real
contra ese almacén. Los destinatarios de ejemplo son configurables.

## Evidencia y análisis

- [Análisis de cobertura](reports/coverage-analysis.md)
- [Informe de análisis](reports/analysis-report.md)
- [Reflexión](reports/reflection.md)
- [Salida real de pytest con cobertura](reports/test-execution.txt)
- [Resumen de cobertura medido](reports/coverage-summary.json)
- [Verificación después de corregir la carpeta](reports/path-migration-verification.txt):
  112 pruebas aprobadas y 100% de cobertura de sentencias y ramas desde
  `students/4Ald0/homework-05/` (1.09 s con instrumentación). Las capturas y
  `test-execution.txt` conservan la evidencia original anterior al cambio de ruta.

La entrega requiere una rama y al menos cinco commits convencionales.
Para la calificación posterior, el enunciado solicita un PR hacia `main` con
la etiqueta `homework` y enviar su enlace en Canvas.
