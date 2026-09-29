# Reflexión sobre el Flujo de Trabajo en Git

## Retos Enfrentados
El principal reto durante esta práctica fue mantener la disciplina de no cometer cambios directamente en la rama `main`. Al principio, es tentador simplemente guardar el archivo y hacer el commit, pero forzarme a crear una rama específica como `feature/add-styling` me ayudó a pensar en los cambios como "paquetes lógicos" de trabajo. Otro reto menor fue recordar los prefijos correctos para los mensajes de commit, especialmente diferenciar entre cuándo usar `style` y cuándo usar `refactor`.

## Comandos más útiles
El comando que encontré más valioso fue `git checkout -b <nombre-rama>` porque simplifica la creación y el cambio de rama en un solo paso. Además, `git status` fue fundamental; me acostumbre a ejecutarlo antes de cada `git add` para asegurarme de que no estaba incluyendo archivos no deseados por accidente. Finalmente, `git log --oneline` me dio mucha claridad visual sobre cómo iba construyendo mi historial.

## Aplicación para proyectos en equipo
Este flujo de trabajo será vital para nuestro proyecto en equipo. Al trabajar todos sobre ramas `feature/` aisladas, evitaremos pisarnos el código unos a otros. Además, la regla de crear Pull Requests y requerir una revisión antes del merge garantizará que el código de `main` siempre sea estable. Los mensajes descriptivos de commit nos ahorrarán mucho tiempo cuando alguien necesite saber por qué se hizo un cambio específico.

## Evidencia
Puedes consultar mi repositorio de práctica, con las ramas, pull requests y el historial completo de commits aquí:
https://github.com/LuisCacho-py/git-workflow-practice
