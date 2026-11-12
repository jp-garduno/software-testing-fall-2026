# Reporte de Pruebas de Caja Blanca y Análisis de Cobertura

## Resumen Ejecutivo

Las 142 pruebas de TaskFlow alcanzan 100% de cobertura de sentencias y ramas
en unos 0.3 segundos, gracias sobre todo a decisiones de diseño previas.

## Logro de las Métricas de Cobertura

Medí la cobertura después de cada suite. Las pruebas unitarias dieron 50%:
`Task` quedó cubierto, pero los otros módulos apenas. La integración subió a
76% y los mocks a 90%. El último 10% salió de la columna `BrPart` (ramas
parciales), que señaló condiciones, como los filtros por rango de fechas,
evaluadas en un solo sentido.

Lo más efectivo fueron los valores límite (títulos de 2, 3, 100 y 101
caracteres; una fecha igual a "ahora") y una tabla parametrizada de
transiciones. Lo más difícil fueron los bloques `except` de la base de datos y
los proveedores, inalcanzables desde el camino feliz.

## Retos para Alcanzar las Metas de Cobertura

El primer obstáculo fue el tiempo. `is_overdue` depende de `datetime.now()`,
así que las pruebas cerca de un límite podían fallar al azar. Agregué `now` a
`Task` y `clock` a `TaskService` y fijé todas las pruebas a un instante.

El segundo obstáculo fueron los stubs con `NotImplementedError` del repositorio
de ejemplo. Código que solo lanza excepciones no se cubre de forma útil, así que
`TaskRepository` tiene lógica real sobre un cliente `database` y solo se simula
el cliente.

Los rendimientos fueron decrecientes: el último 10% requirió 46 pruebas, un
tercio de la suite, para 21 sentencias y 11 ramas parciales.

## Beneficios de Simular Dependencias Externas

Los mocks permiten provocar fallas a voluntad. Un `side_effect` simula una
caída de la base de datos o un timeout de SMTP, y así demostré dos reglas: si
falla el guardado no se notifica, y si falla la notificación no se revierte el
guardado. Con `attach_mock` verifiqué que el guardado ocurre antes del correo.

Sin mocks, la suite necesitaría una base de datos y un servidor de correo,
tardaría segundos y no reproduciría caídas de forma confiable. Pero tienen un
costo. Un mock solo refleja mi suposición
sobre una interfaz. `Mock(spec=...)` ayudó al rechazar métodos que no existen,
y el repositorio falso detectó errores de estado que los stubs por llamada no
podían, como que al renombrar una tarea se liberara el título anterior.

## Balance entre Cobertura y Calidad de las Pruebas

El 100% fue barato porque el código es pequeño y diseñado para probarse; en un
sistema grande no lo perseguiría. Todas las pruebas validan
un resultado, pero algunas de casos borde, como verificar que `repr` contenga el
título, están más motivadas por la cobertura que por el riesgo. Mientras tanto,
la condición de carrera de títulos duplicados está totalmente "cubierta" y aun
así falla bajo concurrencia. La cobertura muestra qué código se ejecutó, no si
el comportamiento es correcto. Lo equilibré exigiendo que cada prueba validara
algo que un usuario notaría.

## Lecciones Aprendidas sobre Pruebas de Caja Blanca

Me sorprendió cuánto influyeron las pruebas en el diseño: la inyección de
dependencias, el reloj inyectable y un tipo de error por capa existen porque
hacían alcanzables las ramas. La próxima vez agregaría el reloj desde el
inicio. En proyectos futuros voy a usar la cobertura de ramas, en particular
la lista de ramas parciales, como un mapa de lo que falta probar y no como una
meta, y la voy a complementar con pruebas de contrato para todo lo que simule.

## Conclusión

La cobertura mostró con precisión qué quedó sin ejecutar; los riesgos restantes
(drivers reales, concurrencia, zonas horarias) no aparecen en ningún porcentaje.
