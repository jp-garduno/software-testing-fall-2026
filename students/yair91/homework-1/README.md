# Portafolio de Emmanuel Arias

Sitio web personal construido para **Homework 1: Git Workflow Practice** del curso de Software Testing, Fall 2026.

El sitio en sí es deliberadamente simple: dos páginas estáticas sin dependencias ni proceso de compilación. Lo que se documenta aquí es el flujo de trabajo con Git que se usó para construirlo, que es el objetivo real de la tarea.

## Tecnologías

- HTML5 semántico
- CSS3 con custom properties y diseño responsive
- JavaScript ES6 sin dependencias
- Git y GitHub

## Estructura

```
students/yair91/homework-1/
├── index.html        Inicio: perfil, experiencia, proyectos y habilidades
├── about.html        Sobre mí, educación y contacto
├── style.css         Tokens de diseño, componentes y breakpoint móvil
├── script.js         Año del footer y enlace de navegación activo
├── CONTRIBUTING.md   Convenciones de ramas, commits y pull requests
├── REFLECTION.md     Reflexión de la tarea
├── LICENSE           MIT
└── .gitignore
```

## Cómo ejecutarlo

No requiere dependencias.

1. Clona el repositorio.
2. Entra a `students/yair91/homework-1/`.
3. Abre `index.html` en un navegador.

También funciona con un servidor local:

```bash
python3 -m http.server 8000
```

Después visita <http://localhost:8000>.

## Flujo de trabajo con Git

La práctica completa se hizo en un repositorio aparte, como sugiere la opción A del enunciado:

**<https://github.com/yair91/git-workflow-practice>**

Ahí están las ramas, los commits y los pull requests reales. Este directorio contiene los entregables finales.

### Estrategia de ramas

`main` se mantiene siempre en estado funcional. Todo cambio entra por una rama de característica y un pull request. Los nombres siguen `tipo/descripción-corta`, en minúsculas y con guiones.

| Rama                        | Propósito                                              | Pull request                                                 |
| --------------------------- | ------------------------------------------------------ | ------------------------------------------------------------ |
| `feature/initial-structure` | Esqueleto HTML de ambas páginas y hoja de estilos base | [#1](https://github.com/yair91/git-workflow-practice/pull/1) |
| `feature/add-styling`       | Tokens de diseño, header, footer y layout responsive   | [#2](https://github.com/yair91/git-workflow-practice/pull/2) |
| `feature/add-content`       | Contenido de las páginas y `script.js`                 | [#3](https://github.com/yair91/git-workflow-practice/pull/3) |
| `feature/update-content`    | Contenido profesional definitivo                       | [#4](https://github.com/yair91/git-workflow-practice/pull/4) |

### Conflicto de merge

`feature/add-content` se creó a partir de `feature/initial-structure` antes de integrar `feature/add-styling`. Las dos ramas agregaron una fila a la misma tabla del README, así que al integrar la segunda Git no pudo decidir:

```
CONFLICT (content): Merge conflict in README.md
<<<<<<< HEAD
| `feature/add-content` | Real copy for the home and about pages, plus script.js |
=======
| `feature/add-styling` | Design tokens, header and footer styling, responsive layout |
>>>>>>> main
```

Se resolvió conservando ambas filas en orden cronológico, dentro de la rama y antes de mergear el pull request, en el commit `fix(readme): resolve branch table conflict by keeping both rows`.

### Convención de commits

Los mensajes siguen [Conventional Commits](https://www.conventionalcommits.org/):

```
<tipo>(<alcance>): <descripción en imperativo, minúsculas>
```

Tipos utilizados: `feat`, `fix`, `docs`, `chore`.

Reglas que seguí:

- Un cambio lógico por commit. Si el mensaje necesita una "y", se parte en dos.
- Nada de mensajes vagos como `update`, `cambios` o `fix`.
- El detalle largo va en la descripción del pull request, no en el commit.

Las convenciones completas están en [CONTRIBUTING.md](CONTRIBUTING.md).

## Licencia

MIT. Ver [LICENSE](LICENSE).
