# Homework 5: TaskFlow — pruebas de caja blanca

**Autor:** David Valdez (`davidvaldezm`)
**Tecnología:** Python 3.11+, pytest y pytest-cov

TaskFlow es un sistema pequeño de gestión de tareas creado para aplicar pruebas de caja blanca. La entrega contiene el modelo de dominio, la capa de servicio y 48 pruebas independientes que cubren decisiones, transiciones, validaciones, errores y colaboraciones entre componentes.

## Objetivos logrados

- Validar títulos, descripciones, prioridades y fechas límite.
- Controlar el ciclo `TODO → IN_PROGRESS → DONE → ARCHIVED`.
- Probar flujos de servicio con repositorio y notificaciones aislados mediante mocks.
- Ejercitar fallas de persistencia y de servicios externos sin red, archivos ni base de datos.
- Obtener 100% de sentencias y líneas, y 99% de cobertura de ramas.

## Instalación

Desde este directorio:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Ejecución

```powershell
# Suite completa
python -m pytest -v

# Cobertura de sentencias y ramas; crea htmlcov/index.html
python -m pytest --cov=src --cov-branch --cov-report=term-missing --cov-report=html
```

La ejecución verificada contiene 48 pruebas y no requiere ningún servicio externo. Los dobles con `Mock(spec=...)` sustituyen las fronteras de persistencia y mensajería.

## Cobertura actual

| Métrica | Resultado | Meta |
| --- | ---: | ---: |
| Sentencias | 100% | >85% |
| Ramas | 99% | >80% |
| Funciones | 100% | >90% |
| Líneas | 100% | >85% |

Consulta el resultado completo en [reports/coverage-analysis.md](reports/coverage-analysis.md) y el análisis reflexivo en [reports/analysis-report.md](reports/analysis-report.md).

## Estructura

```text
src/
  task.py                  # Modelo, validación, ciclo y comparación de prioridad
  task_service.py          # Reglas de negocio y coordinación
  task_repository.py       # Frontera de persistencia
  notification_service.py  # Frontera de mensajería
tests/
  test_task_unit.py                # Pruebas de modelo
  test_task_service_integration.py # Flujos con mocks
  test_mocking.py                  # Aislamiento y dobles
reports/
  coverage-analysis.md
  analysis-report.md
  reflection.md
```

## Automatización

El workflow específico de esta entrega instala dependencias, formatea, analiza estáticamente y ejecuta pytest con cobertura de ramas en Python 3.11 y 3.12. Publica el HTML y los resultados como artefactos de cada pull request.
