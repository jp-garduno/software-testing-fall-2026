# Reflexión - Homework 1: Git Workflow Practice

## Retos enfrentados

El mayor reto fue mantener la disciplina de hacer commits pequeños y enfocados en lugar de acumular varios cambios en uno solo. Al principio es tentador terminar toda una rama y hacer un único commit gigante, pero eso hace que el historial sea menos útil. También tuve que corregir un mensaje de commit a medio camino porque no reflejaba correctamente lo que hacía el cambio, lo cual reforzó la importancia de revisar el mensaje antes de confirmar.

## Comandos de Git más útiles

- `git checkout -b <rama>` para crear y cambiar a una nueva feature branch desde `main`.
- `git add <archivo>` (en vez de `git add .`) para revisar exactamente qué se va a incluir en cada commit.
- `git commit -m "tipo: descripción"` siguiendo la convención de commits.
- `git log --oneline` para revisar rápidamente el historial de una rama.
- `git push origin <rama>` seguido de `gh pr create` para abrir el pull request desde la terminal.

## Aplicación en el proyecto de equipo

Pienso aplicar exactamente este mismo flujo en el proyecto de equipo: ramas con nombres descriptivos por funcionalidad, commits pequeños y bien etiquetados, y pull requests con descripción clara de qué cambió y por qué. Esto facilita que otros miembros del equipo revisen el código sin tener que adivinar el propósito de cada cambio, y reduce el riesgo de conflictos grandes al fusionar.

## Documentación de ramas y commits

Se crearon 3 feature branches (`feature/initial-structure`, `feature/add-styling`, `feature/add-content`), con un total de 10 commits siguiendo la convención `tipo: descripción`, fusionadas mediante 3 pull requests en https://github.com/juanpagutierrez/software-testing-fall-2026. El detalle completo está documentado en el README.md de esta entrega.
