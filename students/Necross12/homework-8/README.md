# Homework 8: End-to-End Test Automation

Comparación de prubas usando selenum vs Playwright 

## Ejercicios extras (bonus)

- **A (Capturas de pantalla)**
- **C (Metricas de rendimiento)**


## Prerrequisitos

- Node.js 22+

## Instalación

```bash
npm i
```

## Comandos

```bash
    npm test # selenium + jest con cobertura (es lo que corre el CI)
    npm run test:all # selenium, playwright y cucumber
    npm run test:selenium # selenium
    npm run test:playwright # playwright
    npm run test:bdd # cucumber
    npm run perf # métricas de rendimiento (bonus C), ver PERFORMANCE.md
```

Selenium y Cucumber corren en modo headless (sin ventana) para que funcionen en CI. Para ver el navegador en PowerShell:

```powershell
$env:HEADLESS='false'; npm run test:selenium
```

## Estructura del proyecto

Se hizo todo en js por comodidad

``` bash
homework-8/
├── features/
│   ├── todo.feature
│   └── step_definitions/
│       └── todoSteps.js
├── performance/
│   ├── measure.js
│   └── results.json
├── playwright/
│   ├── pages/
│   │   └── TodoPage.js
│   └── tests/
│       ├── TodoCrud.test.js
│       └── TodoFilter.test.js
├── screenshots/
│    └── (capturas de ejecución)
├── selenium/
│   ├── pages/
│   │   └── TodoPage.js
│   └── tests/
│       ├── TodoCrud.test.js
│       └── TodoFilter.test.js
├── .gitignore
├── COMPARISON_REPORT.md
├── cucumber.js
├── package.json
├── PERFORMANCE.md
├── playwright.config.js 
├── README.md
```

## Autor

Diego Orozco Mólgora - Software Testing Fall 2026
