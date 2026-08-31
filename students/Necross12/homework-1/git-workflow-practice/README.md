# git-workflow-practice

## Flujo de trabajo de Git

### Estrategia de ramificación
Similar a lo visto en clase, usé la estrategia de tener varias ramas, una por cada función global significativa, alimentándolas con varios commits, tratando de subir cambios solo cuando hubo algo significativo relacionado con la función de la rama. Por ejemplo, una rama con solo el contenido que se va a renderizar en el proyecto, y un commit por cada uno de los 3 archivos que le corresponden. Así, si se necesita buscar un cambio en específico dentro del contenido, es más fácil rastrearlo.

### Ramas creadas
* main
* feature/añadir-contenido
* feature/añadir-estilo
* feature/estructura-inicial
* docs/añadir-documentación

### Convención de mensajes de confirmación
Para el nombre de las ramas use:
* feature/
* docs/

Para el nombre de los commits use:
* feat:
* fix:
* docs:
* style:
* chore: 

Más el nombre de la rama o una descripción breve del commit, tratando de ser lo más descriptivo posible.

## Instrucciones de configuración

git clone https://github.com/Necross12/git-workflow-practice.git
npm i
npm start


## Lecciones aprendidas sobre Git
La verdad, cuando cursé la materia de Integración de Software nunca vi nada de esto; solo vimos el uso básico de Git, cómo crear y eliminar ramas, y cómo revisar y actualizar el progreso del proyecto (add, commit, status, pull, push). Nunca vimos la documentación más formal ni la manera correcta de trabajar con ramas, ya que solo se nos enseñó que podían crearse y fusionarse. Más que necesitar una forma correcta de usarlas, todo dependía de cómo se sintiera el equipo en el momento. Por lo tanto, esta parte más centrada en la documentación, por así decirlo, sería nueva para mí.

## Imagen
<img width="445" height="770" alt="Captura de pantalla 2026-08-26 120657" src="https://github.com/user-attachments/assets/dbdd98a5-2139-49da-a2d7-f1714806a853" />
<img width="1917" height="537" alt="image" src="https://github.com/user-attachments/assets/d45ebaaa-c80c-42ff-9b1b-35f0ee0a0071" />
<img width="1536" height="590" alt="image" src="https://github.com/user-attachments/assets/c0bfecc7-ee9d-4e20-bc06-36922f185676" />

