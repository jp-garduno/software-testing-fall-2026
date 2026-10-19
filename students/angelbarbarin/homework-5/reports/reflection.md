# Reflection – Homework 5

## What was most challenging about achieving high coverage?

Lo más difícil no fue escribir más pruebas, sino entender por qué algunas líneas no se ejecutaban. El servicio
de notificaciones tenía 32% de cobertura porque en las pruebas de integración lo reemplacé completo por un mock.
Tuve que mover el mock un nivel más abajo (a los clientes de correo y SMS) para que su lógica real corriera.
También fue complicado probar tareas vencidas, porque el modelo no deja crear fechas en el pasado; lo resolví
pasando la hora actual como parámetro y congelando el reloj en una prueba.

## How does white box testing differ from black box testing?

En la tarea 4 diseñé las pruebas a partir de la especificación, sin ver el código: particiones, valores límite,
tablas de decisión. Aquí partí del código: cada `if` y cada `except` es una ruta que necesita una prueba, y el
reporte de cobertura me dice exactamente cuál me falta. La caja negra encuentra requisitos mal implementados; la
caja blanca encuentra código que nunca se ejecutó. Se complementan: una suite con 100% de cobertura igual puede
estar verificando el comportamiento equivocado si no se basa en los requisitos.

## Will you use code coverage in your future projects?

Sí, pero como herramienta de diagnóstico y no como meta. Me sirve para encontrar huecos, sobre todo en manejo
de errores, que es lo que más se olvida probar. Para el proyecto final pondría un mínimo de 80% en el CI y
revisaría el reporte HTML en cada PR, pero sin escribir pruebas solo para subir el porcentaje.
