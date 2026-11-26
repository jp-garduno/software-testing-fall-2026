# Mi Portafolio — Git Workflow Practice

Sitio personal simple construido como ejercicio de flujo de trabajo con Git
(ramas, commits y pull requests), para la Homework 1 del curso de Software Testing.

## Descripción

Página de una sola vista con inicio, proyectos y sobre mí, pensada para verse
limpia tanto en escritorio como en móvil.

## Tecnologías usadas

- HTML5
- CSS3 (sin frameworks)
- JavaScript vanilla

## Flujo de trabajo en Git

**Ramas creadas:**
- `feature/initial-structure` — estructura base en HTML
- `feature/add-styling` — hoja de estilos y layout responsivo
- `feature/add-content` — contenido real de las secciones

**Convención de commits:**
Formato `tipo: descripción corta`, usando `feat:`, `fix:`, `docs:` y `style:`
según la naturaleza del cambio.

**Estrategia:**
Cada feature se desarrolló en su propia rama a partir de `main`, con un pull
request por rama antes de mergear.

## Cómo correrlo

Clona el repositorio y abre `index.html` directamente en tu navegador —
no requiere servidor ni dependencias.

```bash
git clone https://github.com/Frijol75/git-workflow-practice.git
cd git-workflow-practice
open index.html
```

## Lecciones aprendidas

Dividir el trabajo en ramas pequeñas y con nombre claro hace que el historial
de commits cuente una historia legible, y evita mezclar cambios sin relación
entre sí.

## Licencia

MIT — ver [LICENSE](./LICENSE).

## Contacto
eduardo.moreno@iteso.mx

> Repositorio de práctica con el historial completo de ramas y PRs:
> https://github.com/Frijol75/git-workflow-practice