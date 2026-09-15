1. Problemas encontrados
   ¿Cuántos problemas detectaron los analizadores de código?
   ¿Qué categorías (estilo, errores, complejidad, etc.)?
   ¿Cuáles fueron los problemas más comunes?
   El linter encontró muchos problemas, en total 8, de los cuales solo 1 fue a propósito (una importación de una clase vacía que nunca se usaría). La mayoría eran nombres de variables que dejé sin usar, importaciones no utilizadas o variables no definidas, lo cual fue un descuido de mi parte. Sin embargo, al querer usar el pre-commit fue donde más problemas tuve, ya que no encontraba la forma de que reconociera que el linter estaba bien configurado, sin importar lo que hiciera, y no lograba pasar esa prueba.

2. Beneficios observados
   ¿Qué problemas detectaron en las pruebas estáticas?
   ¿Se habrían detectado mediante una revisión manual?
   ¿Cuánto tiempo llevó la configuración en comparación con el tiempo que se podría haber ahorrado?
   La verdad es que, como mi mayor problema fue la configuración, en este caso específico no creo haber ganado mucho tiempo. Sin embargo, para evitar llamadas inútiles y que todo esté bien definido, es útil que la herramienta vaya marcando la basura del código para depurar y que después no se convierta en un problema, ya que creo que es lo que más fácilmente pasa desapercibido; Y en mi vida normal, si ahorran mucho tiempo de buscar errores de manera manual o poner a alguien del equipo a revisar el código.

3. Integración
   ¿Cómo integramos esto en el flujo de trabajo del equipo?
   ¿Cuándo debe ejecutarse cada herramienta (IDE, pre-commit, CI)?
   Primero usé pre-commit, que fue la que más trabajo me costó configurar, ya que era la que nunca había usado. Una vez que logré que corriera sin problemas, usé ESLint junto con las herramientas de ESLint para VS Code y Error Lens, para poder ver los problemas desde el mismo IDE y que fuera más sencillo corregirlos.

4. Recomendaciones
   ¿Qué herramientas fueron las más útiles?
   ¿Qué cambiarías de la configuración?
   ¿Lo usarías en proyectos futuros? ¿Por qué?
   Creo que Error Lens y el ESLint de VS Code ayudan a usar este linter de forma mucho más cómoda, y es la opción que terminó usando en mis proyectos, con configuraciones personales o de equipo, para que se ajusten a mis necesidades o a las del equipo, como tener el mismo tipo de declaración de variables, que nos avise de posibles errores o que nos sugiera buenas prácticas. En el caso de pre-commit, me costó mucho más trabajo usarlo, ya que tuve que usar los comandos con python -m, algo que no sabía que se requería para configurarlo correctamente. Por eso es el que me pareció menos útil y más difícil de usar de manera correcta; quizás en el futuro, si vuelvo a usarlo, me resulte más fácil, pero por el momento lo evitaré.
