# Portafolio de David Valdez

Sitio web personal creado para **Homework 1: Git Workflow Practice**. El proyecto presenta mi perfil, habilidades y una selección de ejercicios académicos. Su objetivo principal es demostrar un flujo de trabajo ordenado con Git y GitHub.

## Tecnologías

- HTML5 semántico
- CSS3 con diseño responsive
- JavaScript sin dependencias
- Git y GitHub

La tipografía de títulos es Archivo Narrow, distribuida bajo la SIL Open Font License y alojada localmente en `fonts/`.

## Ejecutar el proyecto

No se requieren dependencias ni proceso de compilación.

1. Clona el repositorio.
2. Entra a `students/davidvaldezm/homework-1/`.
3. Abre `index.html` en un navegador moderno.

También se puede iniciar un servidor local:

```bash
python -m http.server 8000
```

Después visita `http://localhost:8000`.

## Flujo de trabajo con Git

La entrega final usa la rama `feat/davidvaldezm/homework-1`. El desarrollo se dividió en tres líneas de trabajo descriptivas:

- `feature/initial-structure`: estructura HTML y navegación.
- `feature/add-content`: perfil, proyectos y contacto.
- `feature/add-styling`: sistema visual y adaptación responsive.

Cada cambio se desarrolló de forma incremental y se integró en la rama de entrega después de revisar el diff. Los pull requests se usan como punto de revisión antes de integrar trabajo en `main`.

## Convención de commits

Los mensajes siguen Conventional Commits:

```text
<tipo>: <descripción breve en imperativo>
```

Tipos utilizados:

- `feat:` para funcionalidades o contenido nuevo.
- `style:` para presentación visual sin cambiar la lógica.
- `docs:` para documentación.
- `chore:` para archivos de mantenimiento.

Los commits representan unidades lógicas pequeñas; se evitaron mensajes vagos como “update” o “changes”.

## Accesibilidad y pruebas manuales

- Navegación por teclado y enlace para saltar al contenido.
- Estados de foco visibles.
- HTML semántico y etiquetas ARIA únicamente donde aportan contexto.
- Contraste legible y compatibilidad con `prefers-reduced-motion`.
- Revisión en vista de escritorio y móvil.

## Estructura

```text
homework-1/
├── index.html
├── styles.css
├── script.js
├── README.md
├── REFLECTION.md
├── CONTRIBUTING.md
└── .gitignore
```

## Autor

David Valdez — [@davidvaldezm](https://github.com/davidvaldezm)
