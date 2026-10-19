# Reflection

**¿Qué fue lo más difícil de lograr una cobertura alta?**
Saber qué vale realmente la pena probar y qué no. El Happy path es obvio porque es el que esperamos, pero hay demasiadas variantes y hay que decidir cuáles merecen una prueba. También aprendí que no solo importa tener una cobertura alta, sino por qué se obtiene: para llegar al 100% de ramas tuve que escribir una prueba para un estado que el sistema nunca produce.

**¿En qué se diferencia la caja blanca de la caja negra?**
En la caja negra se prueba lo que el sistema debe hacer según los requisitos, usando solo entradas y salidas, sin ver el código. En la caja blanca se parte de la estructura interna: se revisan ramas, condiciones y dependencias para diseñar pruebas que recorran cada una, incluidos los fallos de servicios externos, que se simulan con mocks. Se complementan: la caja negra confirma que se cumple lo pedido y la caja blanca revisa que no queden rincones del código sin probar.

**¿Usaré la cobertura de código en mis proyectos futuros?**
Sí. Es imposible probarlo todo, así que la cobertura me servirá como guía para ver qué partes me faltan y dónde puede fallar mi código, siempre junto con pruebas que verifiquen resultados y no solo ejecuten líneas.
