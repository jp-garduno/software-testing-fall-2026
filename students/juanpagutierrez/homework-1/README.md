# Portafolio Personal - Juan Pablo Gutierrez

## Descripción del Proyecto

Sitio de portafolio personal simple, construido como práctica del flujo de trabajo de Git para Homework 1 (Módulo 1: Git Fundamentals). El objetivo no es la complejidad del sitio, sino demostrar un uso correcto de ramas, commits y pull requests.

## Tecnologías Usadas

- HTML5
- CSS3
- JavaScript (vanilla)

## Documentación del Flujo de Trabajo con Git

### Estrategia de ramas

Todo el trabajo se hizo con feature branches creadas desde `main`, cada una enfocada en una sola responsabilidad, fusionada de vuelta a `main` mediante un Pull Request en GitHub.

Ramas creadas:

| Rama | Propósito |
|------|-----------|
| `feature/initial-structure` | Estructura base de archivos y HTML |
| `feature/add-styling` | Estilos CSS (reset, tipografía, header/nav) |
| `feature/add-content` | Contenido real (about, proyectos, contacto) y script del footer |

Práctica completa (ramas, commits y PRs) realizada en el fork: https://github.com/juanpagutierrez/software-testing-fall-2026

- PR #1 - feat: initial portfolio structure: https://github.com/juanpagutierrez/software-testing-fall-2026/pull/1
- PR #2 - feat: add styling for header and base layout: https://github.com/juanpagutierrez/software-testing-fall-2026/pull/2
- PR #3 - feat: add real content to portfolio: https://github.com/juanpagutierrez/software-testing-fall-2026/pull/3

### Convención de commits

Se usó el formato `<tipo>: <descripción corta>`, con estos tipos:

- `feat:` nueva funcionalidad
- `fix:` corrección de errores
- `style:` cambios de formato sin afectar funcionalidad
- `docs:` cambios de documentación

Ejemplos reales usados en este proyecto:

```
feat: add initial index.html skeleton
feat: add header and navigation styling
style: fix indentation to 4 spaces for consistency
fix: correct typo in about section heading
```

## Instrucciones de Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/jp-garduno/software-testing-fall-2026.git
   ```
2. Abre `students/juanpagutierrez/homework-1/index.html` directamente en tu navegador. No requiere build ni dependencias.

## Lecciones Aprendidas

Trabajar con ramas pequeñas y enfocadas hace que los pull requests sean mucho más fáciles de revisar, y escribir el mensaje del commit antes de confirmar ayuda a mantener cada cambio como una unidad lógica.
