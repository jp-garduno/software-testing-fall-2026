# Guía de estilo del equipo

## Código

- Python 3.11 o superior; nombres descriptivos en `snake_case` y clases en `PascalCase`.
- Funciones pequeñas con una responsabilidad y docstrings que describan contratos.
- Black con 88 columnas; isort con `profile = "black"`. No alinear manualmente imports.
- Dinero mediante `Decimal`, conservado como cadena en JSON; nunca redondear silenciosamente.
- Validar entradas en los límites: montos positivos finitos, categorías no vacías y esquema JSON explícito.
- Excepciones concretas; propagar errores de archivos y JSON para que el llamador decida.
- No usar `eval`, deserialización ejecutable ni secretos incluidos en código.
- Revisar advertencias antes de considerar excepciones. Toda supresión futura debe ser local y justificada.

## Pruebas y colaboración

- Nombres `test_*.py`, escenarios de éxito, entradas inválidas y límites exactos.
- Usar `tmp_path` para archivos y comprobar resultados observables.
- Activar el entorno y ejecutar todos los hooks antes de abrir un PR.
- Mantener al menos 90% de cobertura de líneas y ramas combinadas.
- Commits con `feat`, `fix`, `chore`, `test` o `docs`, alcance y descripción concreta.
- En cada PR, explicar el cambio, la evidencia de validación y cualquier limitación.
- CI debe pasar; la revisión humana debe comprobar requisitos y lógica del negocio.
