# Library Management System (TDD)

Sistema de gestión de biblioteca desarrollado con Test Driven Development estricto (Red-Green-Refactor) en Python.

## Funcionalidades

- **Core**: libros, miembros, catálogo, préstamos, devoluciones y búsquedas por título y autor.
- **Late Fees**: $1 por día de retraso (14 días de préstamo), con tarifa por categoría.
- **Member Categories**: student (límite 3), faculty (5) y public (2).
- **Borrowing History**: registro de préstamos y devoluciones, reporte por miembro y libro más prestado.

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate      # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecutar los tests

```bash
pytest
```

`pytest.ini` ya incluye cobertura de líneas y ramas, el reporte HTML en `coverage/index.html`, un umbral mínimo del 90% y orden aleatorio de tests (`pytest-randomly`).

## Documentación

- [Estructura del proyecto](docs/structure.md)
- [Proceso TDD (5 ciclos)](docs/tdd-process.md)
- [Reflexión](docs/reflection.md)