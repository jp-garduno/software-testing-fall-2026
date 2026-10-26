# Homework 6: Library Management System

- **Alumno:** Luis-045
- **Módulo:** 6 — Test Driven Development
- **Rama:** `feat/Luis-045/homework-6`

Implementación en Python del núcleo de libros, miembros y biblioteca. Incluye las tres funciones avanzadas seleccionadas: multas por retraso, búsquedas con filtros e historial de préstamos.

Toda la entrega se encuentra en esta carpeta, hermana de `homework-5`.


## Preparación en PowerShell

Requiere Python 3.11 o superior. La ruta del ejemplo corresponde al Python 3.13.9 utilizado en este equipo; ajústala si tu instalación está en otra ubicación. Los comandos usan directamente el entorno, sin requerir activación.

```powershell
Set-Location "C:\Users\luisf\OneDrive\Documentos\pruebas\software-testing-fall-2026\students\Luis-045\homework-6"
& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Dependencias de pruebas: pytest, pytest-cov y coverage. Black, isort y Pylint permiten repetir las comprobaciones de calidad.
