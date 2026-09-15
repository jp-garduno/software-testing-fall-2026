# Reflexión — Homework 1: Git Workflow Practice

## ¿Qué retos enfrenté?

Lo que más se me dificultó al principio fue la falta de práctica trabajando con
branches en Git. Aunque ya había usado comandos básicos antes, no tenía tan
claro el flujo completo de crear una rama, hacer commits ahí, subirla,
abrir un pull request y regresar a `main` actualizado antes de empezar la
siguiente rama. Al principio me generaba dudas saber en qué rama estaba
parado y si mis cambios iban a afectar el trabajo de mis compañeros o del
repositorio del curso.

Sin embargo, conforme fui repitiendo el mismo proceso varias veces (crear
rama → hacer cambios → commit → push → PR → merge → actualizar main), le fui
agarrando el modo, y en general la práctica resultó más sencilla de lo que
esperaba. No me tomó tanto tiempo una vez que entendí la lógica detrás del
flujo.

## ¿Qué comandos me resultaron más útiles?

El comando que más usé y que más se me facilitó fue `git add .`, porque me
permite agregar todos los archivos modificados de una sola vez en lugar de
tener que ir añadiendo cada archivo por separado con su nombre. También usé
mucho `git status` para confirmar en qué rama estaba y qué cambios tenía
pendientes antes de comitear, y `git checkout` para moverme entre ramas.

## ¿Cómo aplicaré este flujo en el proyecto de equipo?

Pienso aplicar esta misma lógica de ramas por feature en el proyecto de
equipo: en lugar de que todos trabajemos directo sobre `main`, cada quien
puede crear su propia rama para la parte que le toque, hacer commits
pequeños y descriptivos conforme avanza, y abrir un pull request para que el
resto del equipo revise los cambios antes de integrarlos. Esto debería
ayudarnos a evitar conflictos grandes, mantener un historial claro de quién
hizo qué, y detectar errores antes de que lleguen a la versión final del
proyecto.