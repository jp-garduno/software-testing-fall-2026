# recomendacion.py
import random

# =========================
# Patrón Strategy
# =========================


class RecomendacionStrategy:
    """Interfaz para estrategias de recomendación"""

    def recomendar(self, generos=None):
        raise NotImplementedError("Debes implementar el método 'recomendar'")


# --- Estrategia por género ---
class PorGeneroStrategy(RecomendacionStrategy):
    def recomendar(self, generos=None):
        # Aquí iría la lógica de API o filtrado según los géneros
        if not generos:
            return "No tienes géneros registrados. Prueba agregando algunos."
        return f"Recomendación según tus géneros: {random.choice(generos)}"


# --- Estrategia aleatoria ---
class AleatoriaStrategy(RecomendacionStrategy):
    def recomendar(self, generos=None):
        # Lógica de recomendación completamente aleatoria
        peliculas = ["Peli A", "Peli B", "Peli C", "Peli D"]
        return f"Recomendación aleatoria: {random.choice(peliculas)}"


# --- Estrategia recomendación del día ---
class DelDiaStrategy(RecomendacionStrategy):
    def recomendar(self, generos=None):
        # Lógica de recomendación del día, por ejemplo usando API
        return "Recomendación del día: ¡No te pierdas Inception!"


# --- Contexto ---
class Recomendador:
    def __init__(self, strategy: RecomendacionStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: RecomendacionStrategy):
        self._strategy = strategy

    def recomendar(self, generos=None):
        return self._strategy.recomendar(generos)
