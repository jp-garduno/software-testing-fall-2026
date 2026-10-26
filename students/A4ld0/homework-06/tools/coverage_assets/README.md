# Activo de coverage.py revisado

`coverage_html.js` deriva del activo distribuido en coverage.py 7.16.2, versión
fijada en requirements.txt. Conserva su licencia Apache 2.0 y sus avisos de autoría,
incluidos en LICENSE.txt y NOTICE.txt. Las modificaciones locales están identificadas
en la cabecera del archivo.

Se corrigieron las 50 observaciones del ESLint del curso: declaraciones var,
variables globales accidentales, argumento sin uso, comparación no estricta,
punto y coma innecesario, bloques catch vacíos y el bucle de búsqueda sin condición.
No se deshabilitaron reglas ni se excluyó el archivo del análisis.

`tools/check_quality.py` genera el HTML y después llama a `report_assets.py`.
Este copia el activo revisado, calcula un nombre basado en su contenido, actualiza
las referencias de las páginas HTML y elimina los activos antiguos del reporte.
Así se conserva la corrección al regenerar y se evita reutilizar una copia antigua
del navegador. Al actualizar coverage.py debe revisarse también este derivado.
