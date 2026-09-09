Durante esta tarea practiqué el flujo completo de trabajo con Git y GitHub mientras creaba un portafolio personal sencillo. Uno de los principales desafíos fue entender cuándo los cambios estaban realmente disponibles para realizar un commit. Por ejemplo, mientras trabajaba en la rama de estilos, intenté agregar styles.css antes de que el archivo se hubiera creado correctamente. Git mostró un error de pathspec y posteriormente indicó nothing to commit, working tree clean. Esto me ayudó a comprender que Git solo crea commits cuando existen cambios reales en los archivos.

Los comandos que me resultaron más útiles fueron git status, git add, git commit, git checkout, git pull y git push. En particular, git status fue importante porque me permitió verificar qué archivos habían cambiado antes de crear cada commit.

Para el proyecto utilicé ramas independientes, como feature/initial-structure, feature/add-styling y feature/add-content. Realicé commits pequeños con mensajes descriptivos en lugar de incluir todos los cambios en un solo commit. También utilicé pull requests para integrar las funcionalidades terminadas en la rama principal.

Considero que este flujo de trabajo será útil en el proyecto de equipo porque cada integrante podrá trabajar en una funcionalidad diferente sin modificar directamente la versión principal. Además, los pull requests ofrecen la oportunidad de revisar los cambios antes de integrarlos.

https://github.com/angelbarbarin2/git-workflow-practice.git
