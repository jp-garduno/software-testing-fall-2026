## Coverage Summary
| Metric | Threshold | Achieved | Status |
| --- | --- | --- | --- |
| Statement Coverage | 80% | 95% | ✅ Pass |
| Branch Coverage | 80% | 88% | ✅ Pass |

## Untested Code Paths
Las funciones en `task_repository.py` y `notification_service.py` no tienen lógica implementada (lanzan `NotImplementedError`). Esto se debe a que son interfaces diseñadas exclusivamente para ser simuladas (mocked) durante las pruebas unitarias.

## How Coverage Goals Were Achieved
Se aplicó TDD aislando el modelo `Task` primero, evaluando ramas y excepciones. Posteriormente se probó la lógica de servicio integrando *Mocks*.