# Tarea 6: sistema de biblioteca con TDD

Entrega de A4ld0 en el repositorio del curso. Implementación en Python, en memoria,
con Book, Member y Library. Funciones avanzadas: multas, filtros e historial.

## Instalación y pruebas

Requiere Python 3.12 o posterior. Desde esta carpeta:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe tools/check_quality.py
```

Si `python` abre la tienda de Windows, usa la ruta de tu intérprete instalado.
En macOS/Linux, sustituye `.venv\Scripts\python.exe` por `.venv/bin/python`.
