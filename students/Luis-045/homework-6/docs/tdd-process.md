# Proceso TDD

Se documentan cinco ciclos ejecutados durante el desarrollo, con los commits y las salidas reales de cada fase. Los fragmentos muestran el código de ese momento; el código final incorpora validaciones y formato posteriores.

Comando utilizado desde la carpeta de la entrega: `.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider`.

Se agregó un caso por paso. Las pruebas de regresión que ya pasaban se registraron como GREEN, sin atribuirles un fallo inexistente. Los tiempos corresponden a cada ejecución y pueden variar entre equipos.


## Ciclo 1. Validación del ISBN

### RED

Commit: `7b4fe64`. La longitud correcta no bastaba: el ISBN con una letra era aceptado.

```python
def test_book_rejects_an_isbn_containing_letters():
    with pytest.raises(ValueError, match="ISBN"):
        Book("123456789X", "Dune", "Frank Herbert")
```

Resultado real: `1 failed, 3 passed in 0.06s`.


### GREEN

Commit: `5b65e35`. Implementación mínima que hizo pasar el caso:

```python
if len(isbn) not in (10, 13) or not isbn.isdigit():
    raise ValueError("ISBN must contain 10 or 13 digits")
```

Resultado real: `4 passed in 0.01s`.
