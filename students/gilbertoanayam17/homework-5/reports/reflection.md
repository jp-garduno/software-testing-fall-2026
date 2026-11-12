# Reflection

## What was most challenging about achieving high coverage?

Lo difícil no fue subir el número, sino que el número significara algo. Llegar al 88% fue rápido con unos cuantos flujos completos; después, cada punto costó una prueba dirigida a una rama concreta. Lo que más me costó fue el tiempo: para probar si una tarea está vencida tuve que sacar el reloj del modelo y reemplazarlo en las pruebas, porque con la hora real el caso de "vence justo ahora" no se puede repetir. También me desconcertó encontrar un archivo con 100% de ramas en el que un error en el límite de HTTP 400 pasaba sin que ninguna prueba fallara.

## How does white box testing differ from black box testing?

En la tarea 4 diseñé los casos solo a partir de la especificación, sin ver el código. Aquí el código me dijo qué faltaba: el reporte señalaba líneas y ramas exactas, como la de actualizar una tarea sin cambiarle el título, que ninguna prueba había tomado. La caja negra me sirvió para encontrar huecos en los requisitos; la caja blanca, para encontrar huecos en mis propias pruebas. Creo que se complementan: los valores límite, una técnica de caja negra, fueron los que detectaron los mutantes que cambiaban un `<` por un `<=`.

## Will you use code coverage in your future projects?

Sí, pero como piso y no como meta. Pondría un mínimo de 80% en CI para que el código nuevo no entre sin pruebas, y usaría `term-missing` para decidir qué probar después. Lo que no haría es escribir pruebas solo para llegar al 100%: la única línea que dejé sin cubrir la dejé así a propósito, y está documentada.
