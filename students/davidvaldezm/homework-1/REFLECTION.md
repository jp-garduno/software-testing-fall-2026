# Reflexión — Homework 1

## Retos que enfrenté

El reto principal fue pensar en Git como una herramienta para organizar decisiones y no solamente como un lugar donde guardar archivos. Resulta tentador hacer toda la página y crear un solo commit, pero dividir el trabajo en cambios pequeños facilitó revisar cada modificación. También cuidé que los nombres de ramas y mensajes describieran una intención concreta. Lo más delicado fue mantener la entrega ordenada al integrar estructura, contenido, estilos y documentación.

## Comandos más útiles

Los comandos más útiles fueron `git status`, `git diff` y `git log --oneline`, porque permiten verificar el repositorio antes y después de cada commit. `git switch -c` sirve para crear ramas descriptivas, mientras que `git add <archivo>` selecciona únicamente los cambios de una unidad de trabajo. Finalmente, `git push -u origin <rama>` conecta la rama local con GitHub.

## Estrategia e historial

Organicé el trabajo en tres áreas: estructura, contenido y estilos. La rama final `feat/davidvaldezm/homework-1` conserva más de diez commits convencionales de tipo `feat`, `style`, `docs` y `chore`. Cada uno tiene un propósito verificable, como agregar la navegación, documentar el flujo o adaptar la interfaz para móvil. El pull request final funciona como revisión antes de integrar a `main`.

## Aplicación en el proyecto de equipo

En un proyecto colaborativo partiré de una versión actualizada de `main`, desarrollaré una responsabilidad por rama, haré commits pequeños y abriré un pull request con contexto y pruebas. Antes de aprobar revisaré el diff, los comentarios y los resultados automáticos. Este flujo reduce conflictos, conserva la trazabilidad y permite discutir cambios sin perder una versión estable.
