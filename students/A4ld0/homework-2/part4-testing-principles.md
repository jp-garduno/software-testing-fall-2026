# Parte 4: Aplicación de los siete principios

## 1. Testing Shows Presence of Defects

**Application to TikTok**: Que una cuenta ajena no pueda abrir un video privado en diez casos no demuestra que ninguna combinación de caché, sesión o enlace permita hacerlo. Un fallo confirma un defecto; los casos aprobados solo aportan evidencia sobre las condiciones evaluadas.

**Impact on Strategy**: Priorizar privacidad y autenticación; documentar configuraciones cubiertas y riesgos residuales. Complementar las pruebas con monitoreo de errores y reportes después de liberar, sin confundir monitoreo con una garantía de calidad.

## 2. Exhaustive Testing is Impossible

**Application to TikTok**: Existen demasiadas combinaciones de videos, dispositivos, redes, idiomas, cuentas y relaciones entre usuarios para probarlas todas.

**Impact on Strategy**: Usar particiones de equivalencia para archivos válidos e inválidos, valores límite para tamaños y combinaciones por pares para dispositivos y redes. Probar de forma explícita todas las reglas críticas de autorización, aunque no sean seleccionadas por la técnica combinatoria.

## 3. Early Testing

**Application to TikTok**: Una especificación ambigua sobre quién puede ver una publicación puede producir diferencias entre pantalla, API y almacenamiento.

**Impact on Strategy**: Revisar reglas de audiencia y criterios de aceptación antes de desarrollar. Preparar una tabla de permisos y ejemplos de rechazo durante el diseño; después incorporar pruebas unitarias y de contrato en los primeros cambios.

## 4. Defect Clustering

**Application to TikTok**: Publicación y privacidad combinan estados, permisos y dependencias, por lo que son candidatos iniciales a concentrar defectos. Sin historial real no se puede afirmar que efectivamente sean los módulos más defectuosos.

**Impact on Strategy**: Registrar defectos por módulo, gravedad y recurrencia. Si los datos muestran concentración en cargas interrumpidas, aumentar los casos de reintento y concurrencia allí, manteniendo comprobaciones esenciales en otros módulos.

## 5. Pesticide Paradox

**Application to TikTok**: Repetir siempre el mismo video, cuenta y conexión puede dejar de descubrir problemas con formatos distintos o cambios rápidos de audiencia.

**Impact on Strategy**: Conservar la regresión útil y renovar los datos y escenarios en cada ciclo. Añadir videos de distintas características, secuencias de cambios de permisos y sesiones exploratorias basadas en defectos recientes.

## 6. Testing is Context Dependent

**Application to TikTok**: Una plataforma audiovisual móvil necesita evaluar continuidad de reproducción, consumo de recursos, interacción social y privacidad. Las prioridades también cambian entre un espectador con red inestable y un creador que publica contenido.

**Impact on Strategy**: Combinar pruebas de red y dispositivos con controles de audiencia y accesibilidad. Definir resultados esperados según la configuración y elegibilidad de las cuentas de prueba; no asumir que todas disponen de las mismas opciones.

## 7. Absence-of-Errors Fallacy

**Application to TikTok**: Un feed puede responder rápidamente y no presentar errores técnicos, pero seguir siendo poco útil si el usuario no encuentra contenido de su interés. Una opción de privacidad puede funcionar y aun así ser incomprensible.

**Impact on Strategy**: Validar necesidades mediante aceptación con usuarios representativos. Medir finalización de tareas y comprensión de audiencia; recoger percepción de relevancia del feed. No usar únicamente cobertura de código, ausencia de crashes o tiempo de uso como evidencia de satisfacción.
