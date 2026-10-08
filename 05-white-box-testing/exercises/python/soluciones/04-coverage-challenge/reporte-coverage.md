# Reporte de cobertura

## Resultado

Comando ejecutado desde este directorio:

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=order_processor --cov-report=term-missing --cov-branch test_order_processor.py
```

- Pruebas: **57 pasaron**.
- Cobertura de sentencias: **128/128 (100%)**.
- Cobertura de ramas: **67/68 (98,5%)**.
- Cobertura total reportada: **99%**.

## Rama pendiente

Coverage marca como parcial la rama `122->130` de `order_processor.py`, correspondiente al `elif len(zip_code) == 10` cuando la condición es falsa.

Con entradas normales, esa rama no es alcanzable: la condición previa solo permite continuar si el ZIP tiene longitud 5 o 10. Si la longitud es 5, el primer `if` de validación del ZIP se ejecuta y el `elif` no se evalúa; si es 10, el `elif` resulta verdadero. Otras longitudes salen antes con error. Por tanto, no es posible cubrir la evaluación falsa de ese `elif` mediante una entrada normal sin cambiar el código proporcionado o recurrir a instrumentación artificial.

La lógica del código de producción se mantuvo sin cambios; las pruebas adicionales están en `test_order_processor.py`.
