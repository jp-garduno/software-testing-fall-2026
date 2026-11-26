# Reporte de pruebas y cobertura

## Resumen

| Métrica                       |       Resultado |
| ----------------------------- | --------------: |
| Pruebas ejecutadas            |              32 |
| Pruebas aprobadas             |              32 |
| Pruebas fallidas              |               0 |
| Cobertura total de sentencias |            100% |
| Cobertura total de ramas      | 100% (14 de 14) |

## Cobertura por archivo

| Archivo                | Sentencias | No cubiertas |  Ramas | Parciales | Cobertura |
| ---------------------- | ---------: | -----------: | -----: | --------: | --------: |
| `email_service.py`     |         11 |            0 |      2 |         0 |      100% |
| `user_repository.py`   |         16 |            0 |      2 |         0 |      100% |
| `user_service.py`      |         38 |            0 |     10 |         0 |      100% |
| `test_user_service.py` |        176 |            0 |      0 |         0 |      100% |
| **Total**              |    **241** |        **0** | **14** |     **0** |  **100%** |

La cobertura indicada para los módulos de implementación (`email_service.py`,
`user_repository.py` y `user_service.py`) también es del 100% en sentencias y
ramas.

## Alcance probado

- Registro exitoso, validación de datos, contraseña corta y correo duplicado.
- Fallos de base de datos y errores de correo no bloqueantes durante el registro.
- Inicio de sesión exitoso, usuario inexistente, contraseña incorrecta y fallos
  de base de datos.
- Envío de correo, dirección inválida y errores del servicio externo.
- Búsqueda de usuario por ID, incluidos usuario inexistente y fallo de base de
  datos.
- Operaciones del repositorio y del servicio de correo.
- Flujos de integración de registro e inicio de sesión después del registro.

## Cómo ejecutar las pruebas

Los siguientes pasos no dependen de rutas locales. Se asume que Python está
instalado y disponible como `python` en la terminal. En algunas plataformas
puede ser necesario usar `python3` en su lugar.

1. Abre una terminal y cambia al directorio de esta solución:

   ```sh
   cd 05-white-box-testing/exercises/python/soluciones/03-user-service
   ```

2. (Recomendado) Crea y activa un entorno virtual:

   ```sh
   python -m venv .venv
   ```

   En Windows (PowerShell):

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   En macOS o Linux:

   ```sh
   source .venv/bin/activate
   ```

3. Instala las dependencias de prueba:

   ```sh
   python -m pip install pytest pytest-cov
   ```

4. Ejecuta las pruebas y genera el reporte de cobertura:

   ```sh
   python -m pytest test_user_service.py --cov=. --cov-branch --cov-report=term-missing
   ```

**Resultado registrado:** `32 passed`; cobertura de sentencias y ramas:
`100%`. La cifra corresponde a la ejecución validada para este reporte; los
pasos anteriores permiten repetirla en otro entorno.
