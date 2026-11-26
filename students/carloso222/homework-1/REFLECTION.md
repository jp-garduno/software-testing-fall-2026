# Reflexión - Tarea 1: Flujo de Trabajo con Git

## Desafíos enfrentados

Esta práctica en particular me resultó sumamente sencilla, ya que el semestre pasado llevé la materia de Técnicas de Integración del Código, donde profundizamos bastante en Git: ramas, estrategias de merge, resolución de conflictos, y buenas prácticas de commits. Gracias a eso, ya tenía bastante interiorizados los conceptos y el flujo de trabajo que pedía esta tarea.

Aun así, fue muy útil repasar y poner en práctica de nuevo esos conceptos, sobre todo porque al no usar Git a diario es fácil olvidar detalles pequeños. Por ejemplo, en un momento intenté hacer `git commit` después de modificar un archivo, pero olvidé ejecutar `git add` primero, lo que provocó el error "changes not staged for commit". Fue un buen recordatorio de que Git no incluye automáticamente los cambios en un commit: primero hay que "prepararlos" explícitamente. También me sirvió como repaso mantener la disciplina de correr `git pull` en `main` antes de crear cada rama nueva, para partir siempre de la versión más actualizada del código.

## Comandos de Git más útiles

Los comandos que más utilicé y que considero esenciales fueron `git status`, que me permitió ver en todo momento qué archivos estaban modificados, preparados o sin seguimiento; `git checkout -b` para crear y cambiar de rama en un solo paso; y `git add` junto con `git commit -m` para preparar y guardar cambios con mensajes descriptivos. `git push -u origin <rama>` también fue clave para subir cada rama nueva y poder abrir un Pull Request en GitHub.

## Aplicación en el proyecto en equipo

Este flujo de trabajo —crear una rama por funcionalidad, hacer commits pequeños y descriptivos, y fusionar mediante Pull Requests— es exactamente lo que planeo aplicar en el proyecto en equipo. Permite que varias personas trabajen en paralelo sin pisarse el trabajo entre sí, facilita la revisión de código antes de integrar cambios a `main`, y deja un historial claro de qué se hizo y por qué. En un equipo, además, planeo usar los Pull Requests no solo para fusionar código, sino como espacio de retroalimentación entre compañeros antes de aprobar los cambios.

link al repo
https://github.com/carloso222/git-workflow-practice.git
