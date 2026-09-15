# Homework 3: Static Testing Setup

**Student**: David Valdez (`davidvaldezm`)
**Project**: Personal Budget Tracker
**Language**: Python 3.11+

## Descripción

Biblioteca de finanzas personales que registra gastos, calcula saldos y agrupa
totales por categoría. Usa `Decimal` para conservar precisión monetaria y JSON
validado para guardar y recuperar presupuestos. Se eligió la opción B de la tarea:
crear un proyecto sencillo con problemas iniciales intencionales y corregibles.

## Instalación

Desde la raíz del repositorio del curso:

```sh
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r students/davidvaldezm/homework-3/requirements.txt
python -m pre_commit install --config students/davidvaldezm/homework-3/.pre-commit-config.yaml
python -m pre_commit run --all-files --config students/davidvaldezm/homework-3/.pre-commit-config.yaml
```

Mantener activo el entorno al hacer commits: los hooks locales usan
`language: system` y las versiones fijadas en `requirements.txt`. La configuración
filtra las rutas de esta entrega y su workflow. La instalación selecciona estos
hooks para este clon; para volver a los del curso, ejecutar
`python -m pre_commit install --config .pre-commit-config.yaml` desde la raíz.

## Ejecutar el proyecto

```sh
cd students/davidvaldezm/homework-3
python -c "from src.storage import load_budget; budget = load_budget('example.json'); print('Remaining:', budget.remaining())"
```

Resultado esperado: `Remaining: 87.70`.

## Pre-commit hooks configurados

- `trailing-whitespace`: elimina espacios al final.
- `end-of-file-fixer`: asegura un único salto de línea final.
- `check-yaml`: valida sintaxis YAML.
- `check-json`: valida sintaxis JSON.
- `check-added-large-files`: rechaza archivos superiores a 500 KB.
- `black`: aplica formato de 88 columnas.
- `isort`: ordena imports con perfil Black.
- `pylint`: analiza fuente y pruebas, sin desactivar categorías.
- `bandit`: analiza seguridad en `src/`; las pruebas usan asserts legítimos.

## Pruebas y análisis

Desde el directorio de la entrega, con el entorno activo:

```sh
python -m pytest
python -m pylint --rcfile=.pylintrc src test_budget.py
python -m black --check .
python -m isort --check-only .
python -m bandit -r src
```

Validación local: 27 pruebas, 100% de cobertura de líneas y ramas, Pylint 10/10,
Bandit sin hallazgos. Pytest exige al menos 90% de cobertura.
Los resultados están en `reports/`; el análisis y las correcciones en `REPORT.md`.

## Historial y CI

El commit inicial `1731f8d` conserva los problemas; `3876130` añade la configuración
con la que se capturó `reports/pylint-before.txt`. Las correcciones están en
`33719db`. Para reproducir el análisis inicial, usar un worktree separado en
`3876130` y ejecutar Pylint con el comando anterior. Ese análisis debe fallar.

El workflow `.github/workflows/static-testing-davidvaldezm.yml` ejecuta los mismos
hooks y pruebas en Python 3.11, en pushes de esta rama y PRs que cambien la entrega.
Es el único archivo fuera de la carpeta del alumno, ubicación requerida por
GitHub Actions. Consulta `STYLE_GUIDE.md` para las reglas del equipo.
