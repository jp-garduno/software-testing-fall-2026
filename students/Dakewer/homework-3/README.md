# Homework 3: Static Testing Setup

**Student**: David Eduardo Páez Aguilar
**Project**: Movie Picker (Alexa Skill)
**Language**: Python

## Description

Movie Picker es una skill de Alexa que recomienda películas a los usuarios según sus géneros favoritos, o mediante recomendaciones aleatorias / del día. Usa el patrón Strategy para las distintas formas de recomendar, y persiste los géneros favoritos del usuario en DynamoDB. El proyecto original vive en [github.com/Pardosito/movie-picker](https://github.com/Pardosito/movie-picker).

## Setup Instructions

1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Instalar los hooks de pre-commit:
   ```bash
   pre-commit install
   ```
   (si `pre-commit` no se reconoce como comando, usar `python -m pre_commit install`)
3. Correr el proyecto: este es el código de una Alexa Skill (AWS Lambda), por lo que no se "ejecuta" localmente de forma independiente — se despliega como función Lambda y se invoca a través del Alexa Developer Console o del ASK CLI. Para revisar el código y correr los checks estáticos y los tests, ubicarse en esta carpeta (`homework-3/`) y usar los comandos de las secciones siguientes.

## Pre-commit Hooks Configured

- `trailing-whitespace`
- `end-of-file-fixer`
- `check-yaml`
- `check-json`
- `check-added-large-files`
- `black`
- `isort`
- `pylint`

## Testing

Correr todos los tests desde esta carpeta (`homework-3/`):

```bash
python -m pytest -v
```

O individualmente:

```bash
python -m pytest test_api.py -v
python -m pytest test_recomendacion.py -v
python -m pytest test_utils.py -v
```

Los tests usan `unittest.mock` para simular las llamadas a la API de TMDB y al `handler_input` de Alexa, por lo que no requieren conexión a internet ni credenciales reales para ejecutarse.

Para correr los checks de pre-commit sobre todo el código:

```bash
pre-commit run --all-files
```