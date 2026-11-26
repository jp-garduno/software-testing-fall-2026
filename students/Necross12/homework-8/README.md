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
    npm test # todo
    npm run test:selenium # selenium 
    npm run test:playwright # playwright
    npm run test:bdd # cucumber
    npm run perf # métricas de rendimiento (bonus C), ver PERFORMANCE.md
```

```bash
npm run test:selenium
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
