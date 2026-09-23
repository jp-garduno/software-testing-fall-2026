# Correcciones de linting — Homework 3

Detalle de los problemas corregidos, con la herramienta que los detectó, la
ubicación, la explicación y el código antes y después. El análisis general está
en [`REPORT.md`](REPORT.md).

### 1. `W0102` dangerous-default-value — `src/cotizador.py:14`

Lista mutable como valor por defecto; el bug descrito arriba.

```python
# Antes
def agregar_item(self, sku, cantidad, carrito=[]):
```
```python
# Después
def agregar_item(self, sku, cantidad, carrito=None):
    if carrito is None:
        carrito = []
```

### 2. `W0102` dangerous-default-value — `src/catalogo.py:18`

La misma falla, con la lista global del catálogo: cualquier modificación al
catálogo de una instancia contaminaba a todas las demás.

```python
# Antes
def __init__(self, productos=PRODUCTOS):
    self.productos = productos
```
```python
# Después
def __init__(self, productos=None):
    self.productos = list(PRODUCTOS) if productos is None else productos
```

### 3. `C0121` singleton-comparison ×4 — `catalogo.py:36`, `cotizador.py:10,20`, `validaciones.py:2`

`== None` compara por valor e invoca `__eq__`, que una clase puede sobrescribir
para devolver cualquier cosa. `is None` compara identidad y no se puede falsear.

```python
if producto == None:      # antes
if producto is None:      # después
```

### 4. `W0702` bare-except — `src/validaciones.py:12`

Un `except:` a secas captura también `KeyboardInterrupt` y `SystemExit`: el
programa deja de responder a Ctrl+C y los errores de programación se disfrazan de
"cantidad inválida".

```python
try:
    cantidad = int(cantidad)
except:                              # antes
except (TypeError, ValueError):      # después
```

### 5. `C0103` invalid-name — `src/catalogo.py:21`

`ObtenerProducto` estaba en PascalCase, que en Python nombra clases, no métodos.
Se renombró a `obtener_producto` y se actualizaron las llamadas y las pruebas.

### 6. `W1514` + `R1732` — `src/catalogo.py:41`

`open()` sin `encoding` usa el del sistema: el mismo archivo se escribe distinto
en Windows y en Linux. Sin `with`, el archivo queda abierto si algo falla.

```python
f = open(ruta, "w")                                   # antes
f.write(json.dumps(self.productos)); f.close()
```
```python
with open(ruta, "w", encoding="utf-8") as archivo:    # después
    json.dump(self.productos, archivo, ensure_ascii=False, indent=2)
```

### 7. `W0612` + `C0209` — `src/validaciones.py:20`

Una variable `mensaje` construida con formato `%` y nunca usada: código muerto
que alguien tendría que leer y mantener. Se eliminó.

### 8. `W0611` unused-import ×2 — `src/catalogo.py:2,3`

`os` y `List` importados sin usar. Imports muertos hacen creer que un módulo
depende de cosas de las que no depende.

### 9. `E0015` unrecognized-option — `.pylintrc`

pylint encontró un error en su propia configuración: la opción
`suggestion-mode` no existe en esta versión. Vale la pena destacarlo: sin ese
aviso, el archivo habría seguido ahí con una línea inerte que nadie revisa.

