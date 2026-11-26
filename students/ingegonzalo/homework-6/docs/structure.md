# Library Management System (TDD)

```
library-management-system/
├── README.md
├── requirements.txt
├── pytest.ini
├── .gitignore
├── .github/
│   └── workflows/
│       └── tests.yml
├── src/
│   ├── __init__.py
│   ├── book.py
│   ├── member.py
│   ├── library.py
│   ├── late_fees.py
│   └── history.py
├── tests/
│   ├── __init__.py
│   ├── test_book.py
│   ├── test_member.py
│   ├── test_library.py
│   └── test_late_fees.py
├── docs/
│   ├── structure.md
│   ├── tdd-process.md
│   └── reflection.md
└── coverage/            # reporte HTML generado por pytest-cov
```

## Responsabilidad de cada módulo

| Archivo | Responsabilidad |
|---------|-----------------|
| `src/book.py` | Libro: validación de ISBN y título, control de copias |
| `src/member.py` | Miembro: límite de préstamos, categorías y multas acumuladas |
| `src/library.py` | Catálogo, miembros, préstamos, devoluciones, búsquedas e historial |
| `src/late_fees.py` | Cálculo de fecha de vencimiento y multa por retraso |
| `src/history.py` | `HistoryEntry` y constantes `BORROW` / `RETURN` |