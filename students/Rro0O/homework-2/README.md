# Homework 2: Testing Concepts Analysis — Instagram

**Estudiante:** Rro0O

## De qué va esto

Elegí **Instagram** como app para esta tarea porque tiene un poco de todo: mensajes en tiempo real, algoritmos que deciden qué te muestran, fotos y videos pesados, pagos, y millones de personas usándola a la vez. Eso hace que se puedan aplicar prácticamente todos los tipos y niveles de pruebas que vimos en clase, así que es un buen caso para practicar.

## Contenido

| Archivo | De qué trata |
|------|-------------|
| [part1-application-analysis.md](part1-application-analysis.md) | Qué es Instagram, quién la usa, sus funciones principales y qué es lo más crítico que no puede fallar. |
| [part2-testing-types.md](part2-testing-types.md) | 10 tipos de pruebas (funcionales y no funcionales) con ejemplos y qué tan urgentes son. |
| [part3-testing-levels.md](part3-testing-levels.md) | Estrategia para pruebas unitarias, de integración, de sistema y de aceptación. |
| [part4-testing-principles.md](part4-testing-principles.md) | Los 7 principios de testing aplicados a Instagram, explicados sencillo. |
| [part5-risk-analysis.md](part5-risk-analysis.md) | Matriz con 8 riesgos y en qué orden conviene probar cada cosa. |

## Resumen de la idea general

La estrategia se basa en **priorizar por riesgo**: como es imposible probar absolutamente todo en una app tan grande, el esfuerzo se enfoca primero en lo que más duele si falla — seguridad, privacidad, pagos y que se puedan subir fotos/videos sin problema — sin dejar de tener pruebas automáticas en todos los niveles (desde funciones chiquitas hasta la app completa) y buen monitoreo una vez que ya está en producción.
