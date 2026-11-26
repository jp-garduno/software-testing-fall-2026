# Reflexión breve

Lo más retador fue convertir reglas escritas en lenguaje natural en resultados
únicos cuando varias condiciones fallan al mismo tiempo. Por ejemplo, una
transferencia puede provenir de una cuenta congelada, superar el límite diario
y además no tener fondos. Para evitar que la prueba dependiera de una decisión
implícita, documenté una prioridad de validación y construí la tabla con todas
las combinaciones. También fue importante distinguir “saldo mayor que el
umbral” de “saldo mayor o igual”, porque un centavo cambia el cobro de la cuota.

Aprendí que las técnicas de caja negra no compiten entre ellas. Las particiones
reducen un dominio grande a categorías manejables; los valores frontera atacan
los lugares donde suelen aparecer errores; las tablas de decisión exponen
interacciones; y las transiciones comprueban que el historial del sistema sea
coherente. El solapamiento entre técnicas resulta útil cuando protege una regla
financiera crítica desde más de una perspectiva.

Mi confianza en el modelo entregado es alta dentro del alcance definido: las 73
pruebas pasan y alcanzan 100% de líneas y ramas. Sin embargo, ese número no
significa que un banco real esté completamente probado. Faltarían autenticación,
seguridad, persistencia, concurrencia, zonas horarias, integración con otras
instituciones y pruebas de rendimiento. La mayor ganancia del ejercicio fue
entender que la calidad depende tanto de hacer visibles los supuestos como de
ejecutar casos automáticamente.
