## 1. Testing Shows Presence of Defects (Not Absence)

**Application to Canvas**:
Aunque probemos exhaustivamente el módulo de calificaciones y exámenes,
pasar todas las pruebas no garantiza que Canvas esté libre de errores;
solo confirma que no encontramos defectos con las pruebas que
diseñamos. Puede haber errores en combinaciones que no contemplamos,
como un alumno con doble inscripción en el mismo curso.

**Impact on Strategy**:

- Priorizar pruebas en áreas de alto riesgo (calificaciones, exámenes, roles).
- Mantener canales de reporte de bugs por parte de usuarios reales tras el lanzamiento.

---

## 2. Exhaustive Testing is Impossible

**Application to Canvas**:
Sería imposible probar todas las combinaciones posibles de navegador,
dispositivo, tipo de archivo, rol de usuario y condición de red en
Canvas. No se puede probar cada combinación de tamaño de archivo x tipo
x navegador x conexión.

**Impact on Strategy**:

- Usar análisis de riesgo para priorizar qué combinaciones probar (ej. los navegadores más usados por la escuela).
- Aceptar que no se puede cubrir el 100% de los escenarios posibles.

---

## 3. Early Testing

**Application to Canvas**:
Detectar un error en la lógica de cálculo de promedios durante el
diseño es mucho más barato que descubrirlo después de que cientos de
boletas ya se generaron mal al fin de semestre.

**Impact on Strategy**:

- Incluir revisiones de requisitos y pruebas unitarias desde las primeras etapas de desarrollo del módulo de calificaciones.
- No dejar las pruebas solo para el final del ciclo de desarrollo.

---

## 4. Defect Clustering

**Application to Canvas**:
Es probable que la mayoría de los defectos se concentren en los módulos
más complejos, como el motor de calificación automática de exámenes o
el sistema de permisos por rol, más que en pantallas simples como el
calendario.

**Impact on Strategy**:

- Dedicar más tiempo y casos de prueba a esos módulos de alto riesgo.
- No repartir el esfuerzo de prueba de forma pareja entre todas las funciones.

---

## 5. Pesticide Paradox

**Application to Canvas**:
Si el equipo de QA repite exactamente las mismas pruebas de entrega de
tareas en cada ciclo, eventualmente dejarán de encontrar nuevos
errores, no porque el sistema sea perfecto, sino porque esas pruebas ya
"inmunizaron" esa parte del código.

**Impact on Strategy**:

- Revisar y actualizar periódicamente los casos de prueba.
- Agregar escenarios nuevos (nuevos tipos de archivo, nuevos navegadores) en vez de solo repetir el mismo set.

---

## 6. Testing is Context Dependent

**Application to Canvas**:
Probar Canvas para una universidad grande con miles de alumnos
concurrentes requiere mucho más énfasis en pruebas de rendimiento y
carga que probar una implementación pequeña para una escuela con 200
alumnos, donde la usabilidad y la claridad pueden pesar más.

**Impact on Strategy**:

- Ajustar la profundidad de cada tipo de prueba (performance, seguridad, usabilidad) según el tamaño y necesidades reales de la institución que use Canvas.

---

## 7. Absence-of-Errors Fallacy

**Application to Canvas**:
Que un módulo de exámenes pase todas sus pruebas y no tenga bugs
reportados no significa que sea útil. Si el diseño de la interfaz
confunde a los alumnos y les hace perder tiempo respondiendo, el
sistema sigue siendo defectuoso desde la perspectiva del usuario,
aunque "funcione" técnicamente.

**Impact on Strategy**:

- No basta con pruebas funcionales sin errores.
- Validar contra los objetivos reales del usuario (usabilidad, satisfacción) para asegurar que el sistema realmente sirve para lo que fue diseñado.
