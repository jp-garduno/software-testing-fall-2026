# Part 4: Testing Principles Application

App: **Instagram**

---

## 1. Probar muestra que hay errores, no que no los hay

**Qué significa:** Que las pruebas pasen no quiere decir que la app esté libre de bugs, solo que esos casos concretos que probamos funcionaron bien.

**Cómo aplica en Instagram:** Aunque Instagram tenga un montón de pruebas automáticas, siguen apareciendo bugs en producción (por ejemplo, algo que solo falla en cierto modelo de celular). Por eso también es clave tener buen monitoreo en producción y poder revertir cambios rápido, en lugar de confiar ciegamente en que "si pasaron las pruebas, ya está perfecto".

## 2. Es imposible probar todo

**Qué significa:** Hay tantas combinaciones posibles de celulares, idiomas, conexiones, etc. que no se puede probar absolutamente todo.

**Cómo aplica en Instagram:** Con miles de modelos de celular, más de 100 idiomas y mil situaciones distintas, es imposible cubrirlo todo. Por eso se prioriza: probar primero lo que usa más gente y lo más riesgoso (publicar, mensajes, pagos), y apoyarse en datos reales de errores para saber dónde enfocarse.

## 3. Probar desde el principio

**Qué significa:** Entre más pronto se prueba algo en el desarrollo, más barato sale arreglarlo.

**Cómo aplica en Instagram:** Las pruebas unitarias corren en cada cambio antes de que se junte con el código principal, y los diseños de funciones nuevas se revisan con el equipo de QA antes de siquiera escribir código. Es mucho más barato encontrar un bug en una revisión que después de lanzarlo a mil millones de personas.

## 4. Los errores se agrupan

**Qué significa:** Generalmente unas pocas partes del sistema concentran la mayoría de los bugs.

**Cómo aplica en Instagram:** Partes como el sistema para subir fotos/videos (por toda la variedad de formatos y celulares) o el chat en tiempo real (por todo lo que puede pasar con la conexión) suelen dar más problemas que, digamos, una pantalla simple de "Acerca de". Por eso conviene poner más atención y más pruebas ahí que en partes más simples.

## 5. La paradoja del pesticida

**Qué significa:** Si siempre corres las mismas pruebas, dejan de encontrar cosas nuevas — hay que renovarlas.

**Cómo aplica en Instagram:** No basta con tener siempre las mismas pruebas de regresión para el feed o los mensajes; hay que ir agregando pruebas nuevas, sobre todo basadas en bugs reales que ya pasaron antes, y meter pruebas exploratorias distintas cada cierto tiempo para no quedarse en automático.

## 6. Probar depende del contexto

**Qué significa:** No se prueba igual cualquier tipo de software; depende de qué tipo de app es.

**Cómo aplica en Instagram:** No es lo mismo probar una red social que un sistema de un avión. Aquí tiene más sentido usar A/B testing (porque "funciona bien" a veces también es una decisión de negocio, no solo un sí o no), lanzar cambios poco a poco, y apoyarse mucho en monitoreo real, porque es imposible simular todo el comportamiento real de la gente en un ambiente de pruebas.

## 7. Que no haya errores no significa que el producto sirva

**Qué significa:** Puedes tener algo sin ningún bug y aun así que no le sirva a nadie o no cumpla lo que se necesitaba.

**Cómo aplica en Instagram:** Un nuevo algoritmo de feed puede funcionar perfecto técnicamente y aun así hacer que a la gente le guste menos usar la app. Por eso las pruebas de aceptación en Instagram no solo revisan que "funcione", sino que también midan si a la gente le gusta el resultado con pruebas A/B, porque algo sin bugs pero que nadie quiere usar sigue siendo un fracaso.
