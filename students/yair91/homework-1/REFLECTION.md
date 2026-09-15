# Reflexión — Homework 1

## Retos que enfrenté

Lo difícil no fue Git, fue quitarme la maña de trabajar directo en `main` cuando el proyecto es mío y nadie más lo va a tocar. En el trabajo siempre ramifico, pero ahí el flujo ya está armado y nomás lo sigo. Aquí me tocó pensarlo desde cero: qué va en cada rama, qué merece su propio commit. Lo más incómodo fue el conflicto de merge. Saqué `feature/add-content` de `feature/initial-structure` antes de integrar `feature/add-styling`, y las dos acabaron agregando una fila a la misma tabla del README. Provocarlo a propósito salió mejor que evitarlo, porque me tocó resolverlo sin prisa y entendiendo qué estaba pasando.

## Comandos más útiles

El que más usé fue `git log --oneline --graph --all`, porque te deja ver la forma del historial en lugar de andarla imaginando. `git status` y `git diff --staged` antes de cada commit, para no meter cosas que no iban. `git checkout -b <rama> <base>`, para dejar claro de dónde sale cada rama, que fue justo lo que causó el conflicto y también lo que me lo explicó. Y `git merge main` dentro de la rama antes de abrir el PR, para arreglar el conflicto en mi máquina y no en la página de GitHub.

## Historial y estrategia de ramas

Todo está en <https://github.com/yair91/git-workflow-practice>: cuatro ramas, catorce commits y cuatro pull requests con su descripción, ya mergeados a `main`.

## Aplicación en el proyecto de equipo

Salir siempre de un `main` actualizado, una cosa por rama, y dejar el PR bien explicado para que quien lo revise no tenga que preguntarme nada. Y resolver los conflictos en local antes de pedir revisión: eso es lo que me llevo de esta tarea.
