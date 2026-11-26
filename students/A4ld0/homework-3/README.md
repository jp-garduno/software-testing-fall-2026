# Homework 3: Static Testing Setup

**Student**: Aldo Ramon Velazquez Fonseca (A4ld0)
**Project**: Study Task Planner
**Language**: Python 3.11+

## Description

Gestor de tareas de estudio por consola. Permite crear tareas con prioridad,
completarlas, consultar pendientes y resumir el progreso; conserva los datos en
JSON y rechaza registros inválidos antes de modificarlos.

## Setup Instructions

Desde la raíz del repositorio, crea y activa un entorno virtual:

```powershell
python -m venv students/A4ld0/homework-3/.venv
./students/A4ld0/homework-3/.venv/Scripts/Activate.ps1
python -m pip install -r students/A4ld0/homework-3/requirements.txt
```

En Linux/macOS, activa el mismo entorno con
`source students/A4ld0/homework-3/.venv/bin/activate`.

Instala los hooks y revisa los archivos versionados, desde la raíz del repositorio:

```shell
python -m pre_commit install --config students/A4ld0/homework-3/.pre-commit-config.yaml
python -m pre_commit run --all-files --config students/A4ld0/homework-3/.pre-commit-config.yaml
```

Esta configuración utiliza rutas relativas a la raíz de Git. Su filtro limita
los hooks a esta entrega. La instalación es local a cada clon y requiere acceso
a Internet la primera vez para descargar los entornos aislados. Los archivos
nuevos deben agregarse a Git para aparecer en `--all-files`.

Ejecuta el proyecto desde su directorio:

```shell
cd students/A4ld0/homework-3
python -m src.cli add "Repasar análisis estático" --priority 1
python -m src.cli add "Preparar reporte"
python -m src.cli list --pending
python -m src.cli done 1
python -m src.cli summary
```

El archivo `tasks.json` se crea en el directorio actual y está ignorado por Git.
Puedes consultar datos de ejemplo sin crear tareas:

```shell
python -m src.cli --file examples/tasks.json list
```

## Pre-commit Hooks Configured

- `trailing-whitespace`: elimina espacios al final de línea.
- `end-of-file-fixer`: asegura un salto de línea final.
- `check-yaml`: valida YAML.
- `check-json`: valida JSON.
- `check-added-large-files`: rechaza archivos superiores a 500 KB.
- `black`: aplica formato uniforme.
- `isort`: ordena imports con el perfil compatible con Black.
- `pylint`: revisa errores, convenciones y complejidad.
- `bandit`: busca patrones de seguridad problemáticos.

## Linting

Desde `students/A4ld0/homework-3/`, con el entorno virtual activo:

```shell
python -m pylint --rcfile=.pylintrc src
python -m black --check src
python -m isort --check-only src
python -m bandit -r src
```

Para aplicar formato: `python -m black src` y `python -m isort src`.
No se deshabilitan categorías de Pylint; Black, isort y Pylint comparten un
límite de 88 columnas. Las versiones principales de las herramientas están
fijadas en `requirements.txt` y coinciden con las revisiones de los hooks.

## Resultados y evidencia

- [Reporte de análisis y correcciones](REPORT.md).
- [Pylint inicial](reports/pylint-before.txt): 8 avisos, 9.29/10.
- [Pylint final](reports/pylint-after.txt): 0 avisos, 10.00/10.
- [Bandit](reports/bandit.json): 0 hallazgos.
- [Verificación local](reports/verification.md).
- Los JSON de Pylint permiten contar y comparar los diagnósticos.

El código inicial está conservado en el commit `3890861`. Para volver a analizarlo,
usa un checkout separado de ese commit y proporciona la configuración del commit
`26d5f8e`; evita sobrescribir las correcciones locales.

## Estado de entrega local

Se prepararon los archivos y se ejecutaron los analizadores individualmente.
Quedan pendientes instalar y ejecutar los hooks completos, verificar un commit
con el hook activo y publicar el Pull Request
con etiqueta `homework`. No se ha solicitado ni obtenido calificación automática.
El historial contiene cinco commits con formato Conventional Commits. La rama
permanece local por decisión del estudiante.

Los dos commits que completan el historial son:

- `fix: resolve linting issues in task planner`
- `docs: add static analysis report and setup instructions`

El título preparado para el PR es
`Homework 3: Static Testing Setup - Aldo Ramon Velazquez Fonseca`, con base `main`,
rama `codex/homework-3-A4ld0` y etiqueta `homework`.

## Referencias

- [Instrucciones de la tarea](../../../03-static-testing/homework/homework-3.md).
- [Uso y configuración de pre-commit](https://pre-commit.com/).
- [Ejecución de Pylint](https://pylint.readthedocs.io/en/stable/user_guide/usage/run.html).
