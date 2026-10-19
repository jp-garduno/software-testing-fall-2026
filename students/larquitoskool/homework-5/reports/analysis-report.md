# White Box Testing & Coverage Analysis Report

## Coverage Metrics Achievement
Logré superar el 80% de cobertura enfocándome en el modelo principal primero y diseñando pruebas para cada límite de las variables de negocio y las bifurcaciones `if/else`. 

## Challenges Encountered
Fue difícil manejar el tiempo del sistema en las pruebas de `is_overdue()`, y controlar las transiciones de estado requirió mucha atención a los límites de la matriz de transiciones.

## Benefits of Mocking
Mockear el repositorio y el servicio de notificaciones me permitió validar que las llamadas se hacían en el orden correcto sin necesidad de tener una base de datos real configurada.

## Trade-offs Between Coverage and Test Quality
Llegar al 100% no es realista porque hay excepciones en la capa de infraestructura (redes) que solo pueden validarse eficazmente mediante pruebas E2E.

## Lessons Learned
Aprendí que el testing de caja blanca no se trata de ejecutar líneas a lo loco, sino de probar el flujo y el control de datos sistemáticamente.