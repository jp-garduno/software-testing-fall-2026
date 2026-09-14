"""Tests for src/helpers/recomendacion.py.

Run from the homework-3 directory with:
    python -m pytest test_recomendacion.py -v
or:
    python -m unittest test_recomendacion.py -v
"""
import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


from helpers.recomendacion import (  # noqa: E402  pylint: disable=wrong-import-position
    AleatoriaStrategy,
    DelDiaStrategy,
    PorGeneroStrategy,
    Recomendador,
    RecomendacionStrategy,
)

class TestRecomendacionStrategyBase(unittest.TestCase):
    """The base class is an interface: calling recomendar() directly
    should fail loudly rather than silently doing nothing."""

    def test_base_strategy_raises_not_implemented(self):
        strategy = RecomendacionStrategy()
        with self.assertRaises(NotImplementedError):
            strategy.recomendar()


class TestPorGeneroStrategy(unittest.TestCase):
    def test_returns_fallback_message_when_no_genres_given(self):
        strategy = PorGeneroStrategy()

        result = strategy.recomendar(generos=None)

        self.assertIn("No tienes géneros registrados", result)

    def test_returns_fallback_message_for_empty_list(self):
        strategy = PorGeneroStrategy()

        result = strategy.recomendar(generos=[])

        self.assertIn("No tienes géneros registrados", result)

    @patch("helpers.recomendacion.random.choice")
    def test_recommends_based_on_one_of_the_given_genres(self, mock_choice):
        mock_choice.return_value = "comedia"
        strategy = PorGeneroStrategy()

        result = strategy.recomendar(generos=["comedia", "drama"])

        mock_choice.assert_called_once_with(["comedia", "drama"])
        self.assertIn("comedia", result)


class TestAleatoriaStrategy(unittest.TestCase):
    @patch("helpers.recomendacion.random.choice")
    def test_returns_one_of_the_hardcoded_movies(self, mock_choice):
        mock_choice.return_value = "Peli B"
        strategy = AleatoriaStrategy()

        result = strategy.recomendar()

        self.assertIn("Peli B", result)

    def test_ignores_genres_argument_and_still_returns_a_recommendation(self):
        strategy = AleatoriaStrategy()

        result = strategy.recomendar(generos=["terror"])

        self.assertTrue(result.startswith("Recomendación aleatoria:"))


class TestDelDiaStrategy(unittest.TestCase):
    def test_returns_fixed_movie_of_the_day_message(self):
        strategy = DelDiaStrategy()

        result = strategy.recomendar()

        self.assertIn("Inception", result)


class TestRecomendador(unittest.TestCase):
    """Recomendador is the Strategy 'context': it should defer entirely
    to whichever strategy is currently set."""

    def test_delegates_to_initial_strategy(self):
        recomendador = Recomendador(DelDiaStrategy())

        result = recomendador.recomendar()

        self.assertIn("Inception", result)

    def test_set_strategy_switches_behavior(self):
        recomendador = Recomendador(DelDiaStrategy())
        recomendador.set_strategy(AleatoriaStrategy())

        result = recomendador.recomendar()

        self.assertTrue(result.startswith("Recomendación aleatoria:"))

    @patch("helpers.recomendacion.random.choice")
    def test_passes_generos_through_to_strategy(self, mock_choice):
        mock_choice.return_value = "accion"
        recomendador = Recomendador(PorGeneroStrategy())

        result = recomendador.recomendar(generos=["accion", "drama"])

        mock_choice.assert_called_once_with(["accion", "drama"])
        self.assertIn("accion", result)


if __name__ == "__main__":
    unittest.main()
