# Git Workflow Practice — Laravel Content Page

Proyecto práctico para aplicar un flujo de trabajo con Git y GitHub mediante
ramas de funcionalidad, commits y Pull Requests.

La aplicación se desarrolló con Laravel y presenta una página de contenido
simple, responsive y construida con Blade, Vite y Tailwind CSS.

## Objetivo

Implementar una página de contenido en Laravel siguiendo un flujo de trabajo
basado en ramas `feature/*`.

Cada cambio se desarrolló de manera aislada, se validó localmente y se integró
mediante Pull Requests hacia la rama principal.

## Tecnologías

- PHP 8.5
- Laravel 13
- Blade
- Vite
- Tailwind CSS
- SQLite
- Git y GitHub

## Funcionalidades

- Página principal de contenido disponible en `/`.
- Controlador `ContentController`.
- Renderizado dinámico de tarjetas desde un arreglo de datos.
- Layout Blade reutilizable.
- Estilos responsive mediante Tailwind CSS.
- Configuración de assets con Vite.

## Estructura relevante

```text
app/
└── Http/
    └── Controllers/
        └── ContentController.php

resources/
├── css/
│   └── app.css
├── js/
│   └── app.js
└── views/
    ├── content/
    │   └── index.blade.php
    └── layouts/
        └── app.blade.php

routes/
└── web.php
```

## Ramas implementadas

| Rama | Propósito | Cambios principales |
|---|---|---|
| `feature/initial-structure` | Estructura base de vistas | Creación del layout reutilizable `layouts/app.blade.php` |
| `feature/add-styling` | Estilos de interfaz | Componentes y estilos globales con Tailwind en `resources/css/app.css` |
| `feature/add-content` | Página de contenido | Controlador, ruta y vista de tarjetas de contenido |
| `main` | Rama estable | Integración de las funcionalidades aprobadas |

## Instalación

### Requisitos

Antes de iniciar, se necesita tener instalado:

- PHP 8.5 o compatible con el proyecto.
- Composer.
- Node.js y npm.
- Git.

### Configuración

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/FabianGaxiola/git-workflow-practice-754471.git
   ```

2. Entrar al directorio del proyecto:

   ```bash
   cd git-workflow-practice-754471
   ```

3. Instalar dependencias de PHP:

   ```bash
   composer install
   ```

4. Instalar dependencias de JavaScript:

   ```bash
   npm install
   ```

5. Crear el archivo de configuración local:

   ```bash
   cp .env.example .env
   ```

   En Windows PowerShell:

   ```powershell
   Copy-Item .env.example .env
   ```

6. Generar la clave de la aplicación:

   ```bash
   php artisan key:generate
   ```

7. Ejecutar las migraciones:

   ```bash
   php artisan migrate
   ```

8. Limpiar cachés de Laravel:

   ```bash
   php artisan optimize:clear
   ```

## Ejecución

Iniciar el servidor de Vite para compilar los estilos:

```bash
npm run dev
```

En otra terminal, iniciar Laravel:

```bash
php artisan serve
```

La aplicación estará disponible en:

```text
http://127.0.0.1:8000/
```

Para generar los recursos de producción en lugar de utilizar el servidor de Vite:

```bash
npm run build
```

## Flujo de trabajo Git

El proyecto siguió un enfoque Feature Branch Workflow:

1. La rama `main` se mantiene como la versión estable.
2. Cada cambio se desarrolla en una rama con el prefijo `feature/`.
3. Los cambios se guardan mediante commits descriptivos.
4. Cada rama se publica en GitHub.
5. Se abre un Pull Request hacia `main`.
6. Se revisan los cambios y se ejecutan las validaciones.
7. El Pull Request aprobado se fusiona en `main`.

Ejemplos de commits utilizados:

```text
feat: add base application layout
style: add reusable Tailwind components
feat: add content page
refactor: use shared layout and Tailwind styles
```

## Validación

Se realizaron las siguientes verificaciones locales:

```bash
php artisan optimize:clear
php artisan route:list
npm run build
```

También se verificó manualmente que:

- La ruta principal `/` carga sin errores.
- Laravel resuelve `ContentController@index`.
- La vista encuentra el layout `layouts.app`.
- Vite carga los archivos `resources/css/app.css` y `resources/js/app.js`.
- La interfaz se adapta a pantallas pequeñas y grandes.
- Las tarjetas de contenido se renderizan correctamente.

## Autor

Fabián Gaxiola  
Proyecto académico de práctica de flujo Git con Laravel.
