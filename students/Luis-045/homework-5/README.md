# Homework 5: White Box Testing - TaskFlow

TaskFlow es el sistema de administracion de tareas de la tarea 5. Se desarrollara en Python con pytest, pytest-cov y unittest.mock.

Esta primera etapa prepara la configuracion y las dependencias. La implementacion, las pruebas y las metricas de cobertura se incorporaran durante las siguientes etapas del desarrollo.

## Requisitos

- Python 3.11 o posterior, con el lanzador `py` disponible en Windows.
- PowerShell.
- Git.

## Instalacion en Windows

Ejecutar desde `students/Luis-045/homework-5/`:

```powershell
py -3 --version
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest --version
```

La primera orden debe mostrar Python 3.11 o posterior. Usar directamente el ejecutable del entorno evita tener que activar scripts de PowerShell.

Las dependencias incluyen pytest, pytest-cov y las herramientas de formato y revision black, isort y pylint. Las pruebas usaran unittest.mock, que forma parte de la biblioteca estandar.

## Ejecucion prevista de las pruebas

Una vez implementados `src/` y `tests/`, ejecutar desde esta carpeta:

```powershell
.\.venv\Scripts\pytest.exe -v
.\.venv\Scripts\pytest.exe -v --cov=src --cov-branch --cov-report=term-missing --cov-report=html --cov-report=json
```

El ejecutable `pytest.exe` tambien permitira comprobar las importaciones mediante el comando de consola que utiliza el evaluador. `pytest.ini` limita el descubrimiento a `tests/` y agrega las rutas de importacion requeridas por el enunciado.

Los reportes generados y el entorno virtual estan excluidos de Git. Las capturas reales de la ejecucion y de la cobertura se guardaran en `reports/screenshots/`.

## Autor

Luis-045 - Software Testing Fall 2026.
