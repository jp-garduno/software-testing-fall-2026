# Portfolio Personal - Git Workflow Practice

## Descripción del Proyecto
Página web de portafolio personal desarrollada para la asignatura de Pruebas de Software. El objetivo principal de este proyecto es poner en práctica el flujo de trabajo estándar de Git y GitHub, incluyendo estrategias de ramificación (*Feature Branch Workflow*), convenciones de commits y gestión de Pull Requests.

## Tecnologías Utilizadas
* **HTML5:** Estructura semántica de la página.
* **CSS3:** Hoja de estilos y diseño responsivo.
* **Git & GitHub:** Control de versiones y gestión del flujo de trabajo.

## Documentación del Flujo de Trabajo en Git

### Estrategia de Ramas (Branching Strategy)
Se utilizó la estrategia **Feature Branch Workflow**. Toda característica o cambio se desarrolló en una rama independiente creada a partir de la rama de trabajo base:
* `feature/initial-structure`: Creación del maquetado y estructura HTML base.
* `feature/add-content`: Inclusión del stack tecnológico, proyectos reales y documentación.
* `feature/add-styling`: Diseño de la hoja de estilos CSS y reglas de diseño responsivo.

### Convención de Mensajes de Commit
Se siguió el estándar de **Conventional Commits**:
* `feat:` Nuevas características agregadas a la aplicación.
* `style:` Cambios visuales o de formato CSS sin alterar la funcionalidad.
* `docs:` Creación o modificación de documentación (`README.md`, `REFLECTION.md`).
* `refactor:` Reorganización, limpieza o formateo de código.

## Instrucciones de Instalación y Ejecución
1. Clonar el repositorio del curso:
   git clone [https://github.com/ITESO-Software-Testing/software-testing-fall-2026.git](https://github.com/ITESO-Software-Testing/software-testing-fall-2026.git)

2. Navegar a la carpeta personal del proyecto:
   cd software-testing-fall-2026/students/DiegoGom05/homework-1/

3. Abrir el archivo `index.html` en tu navegador de preferencia.

## Cosas aprendidas de Git
Aprendí a manejar el flujo de trabajo de las ramas por cada feature y luego hacerle merge con la rama principal.