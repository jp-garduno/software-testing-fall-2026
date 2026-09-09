# Guía de contribución

## Preparar una mejora

1. Actualiza `main` con `git pull --ff-only`.
2. Crea una rama descriptiva, por ejemplo `feature/improve-project-copy`.
3. Mantén cada rama enfocada en una sola responsabilidad.

## Commits

Usa el formato `<tipo>: <descripción>` y revisa los cambios con `git diff --staged` antes de confirmar. Evita combinar correcciones, contenido y estilos que puedan revisarse por separado.

## Pull requests

El título debe resumir el resultado. La descripción debe incluir qué cambió, por qué era necesario y cómo se verificó. Antes de solicitar revisión:

- abre `index.html` y prueba los enlaces;
- revisa las vistas de escritorio y móvil;
- navega la página únicamente con teclado;
- confirma que no existan archivos locales o temporales en el diff.

Los comentarios de revisión se resuelven con nuevos commits para conservar la trazabilidad.
