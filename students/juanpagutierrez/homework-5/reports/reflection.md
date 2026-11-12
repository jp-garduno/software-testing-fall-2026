# Reflexión - Tarea 5

## ¿Qué fue lo más difícil de alcanzar una cobertura alta?

Las sentencias fueron fáciles; las ramas no. Tras las suites de integración y
mocks, coverage.py aún reportaba once ramas parciales: filtros siempre
verdaderos y manejadores de errores inalcanzables con entradas normales.
Cubrirlas exigió entradas poco obvias, como una tarea sin fecha dentro de un
rango o un SMS de exactamente 160 caracteres, y mocks con `side_effect` para
forzar fallas. El otro reto fue el tiempo: tuve que hacer el reloj inyectable
para que las pruebas de tareas vencidas fueran deterministas.

## ¿En qué se diferencian las pruebas de caja blanca de las de caja negra?

La caja negra diseña casos desde la especificación y no sabe si recorrió todos
los caminos de la implementación. La caja blanca los diseña desde el código:
cada `if`, ciclo y `except` es algo que alcanzar. Se complementan. La especificación me dijo *qué* debía hacer TaskFlow, y el
reporte de cobertura me dijo *qué partes de mi implementación* nunca se habían
ejecutado. Ninguna de las dos por sí sola habría encontrado el límite inclusivo
del rango de fechas.

## ¿Vas a usar cobertura de código en proyectos futuros?

Sí, como diagnóstico y no como meta: correré cobertura de ramas en CI y
revisaré las líneas faltantes y parciales, sin obsesionarme con el 100%. Esta tarea también
me enseñó que una línea cubierta puede estar mal, como lo demuestra la
condición de carrera de títulos duplicados, así que la cobertura va a
acompañar a la revisión de código y a las pruebas de contrato, no a
reemplazarlas.
