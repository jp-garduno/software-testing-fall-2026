"""Tests for src/helpers/api.py.

Run from the homework-3 directory with:
    python -m pytest test_api.py -v
or:
    python -m unittest test_api.py -v
"""
import json
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Make src/ importable regardless of where pytest is invoked from.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from helpers.api import (  # noqa: E402  pylint: disable=wrong-import-position
    GENRES_MAP,
    get_movie_list,
    get_next_movie_response,
    spin_the_wheel,
)


class TestGenresMap(unittest.TestCase):
    """GENRES_MAP is static data used to translate Spanish genre names
    into TMDB genre IDs. These tests protect against typos when the
    dict is edited in the future."""

    def test_accented_and_unaccented_accion_map_to_same_id(self):
        self.assertEqual(GENRES_MAP["accion"], GENRES_MAP["acción"])

    def test_terror_and_miedo_map_to_same_id(self):
        self.assertEqual(GENRES_MAP["terror"], GENRES_MAP["miedo"])

    def test_thriller_and_suspenso_map_to_same_id(self):
        self.assertEqual(GENRES_MAP["thriller"], GENRES_MAP["suspenso"])

    def test_all_genre_ids_are_numeric_strings(self):
        for genre, genre_id in GENRES_MAP.items():
            with self.subTest(genre=genre):
                self.assertTrue(
                    genre_id.isdigit(),
                    f"Genre id for '{genre}' should be a numeric string",
                )


class TestGetNextMovieResponse(unittest.TestCase):
    """get_next_movie_response only touches handler_input.attributes_manager
    .session_attributes, so it can be tested fully with a MagicMock instead
    of a real Alexa HandlerInput."""

    @staticmethod
    def _make_handler_input(session_attributes):
        handler_input = MagicMock()
        handler_input.attributes_manager.session_attributes = session_attributes
        return handler_input

    def test_no_queue_returns_prompt_to_request_recommendation(self):
        handler_input = self._make_handler_input({})

        speak_output, reprompt = get_next_movie_response(handler_input)

        self.assertIn("recomiende", speak_output)
        self.assertTrue(reprompt)

    def test_advances_to_next_movie_in_queue(self):
        queue = [
            {"title": "Movie A", "overview": "Overview A"},
            {"title": "Movie B", "overview": "Overview B"},
        ]
        handler_input = self._make_handler_input(
            {"movie_queue": queue, "movie_index": 0}
        )

        speak_output, _ = get_next_movie_response(handler_input)

        self.assertIn("Movie B", speak_output)
        self.assertIn("Overview B", speak_output)
        self.assertEqual(
            handler_input.attributes_manager.session_attributes["movie_index"], 1
        )

    def test_reaching_end_of_queue_clears_it_and_warns_user(self):
        queue = [{"title": "Only Movie", "overview": "Overview"}]
        handler_input = self._make_handler_input(
            {"movie_queue": queue, "movie_index": 0}
        )

        speak_output, _ = get_next_movie_response(handler_input)

        self.assertIn("no tengo más recomendaciones", speak_output.lower())
        self.assertEqual(
            handler_input.attributes_manager.session_attributes["movie_queue"], []
        )


class TestGetMovieList(unittest.TestCase):
    """get_movie_list depends on TMDB over the network, so the network
    call itself is mocked out; only our own logic (genre lookup, error
    handling) is under test."""

    @staticmethod
    def _make_handler_input(saved_genres):
        handler_input = MagicMock()
        handler_input.attributes_manager.persistent_attributes = {
            "lista_generos": saved_genres
        }
        return handler_input

    def test_returns_first_time_when_no_genres_saved(self):
        handler_input = self._make_handler_input(None)

        result = get_movie_list(handler_input)

        self.assertEqual(result, "first_time")

    def test_returns_no_valid_ids_found_for_unknown_genres(self):
        handler_input = self._make_handler_input(["genero_inventado"])

        result = get_movie_list(handler_input)

        self.assertEqual(result, "no_valid_ids_found")

    @patch("helpers.api.request.urlopen")
    def test_returns_results_on_successful_response(self, mock_urlopen):
        fake_response = MagicMock()
        fake_response.getcode.return_value = 200
        fake_response.read.return_value = json.dumps(
            {"results": [{"title": "Some Movie"}]}
        ).encode()
        mock_urlopen.return_value.__enter__.return_value = fake_response

        handler_input = self._make_handler_input(["comedia"])
        result = get_movie_list(handler_input)

        self.assertEqual(result, [{"title": "Some Movie"}])


class TestSpinTheWheel(unittest.TestCase):
    """spin_the_wheel relies on get_movie_list and random.randint, both
    mocked here so the test is deterministic."""

    @patch("helpers.api.get_movie_list")
    @patch("helpers.api.random.randint")
    def test_picks_movie_at_random_index_from_first_six_results(
        self, mock_randint, mock_get_movie_list
    ):
        mock_get_movie_list.return_value = [
            {"title": f"Movie {i}"} for i in range(6)
        ]
        mock_randint.return_value = 3

        movie = spin_the_wheel(MagicMock())

        self.assertEqual(movie, {"title": "Movie 3"})


if __name__ == "__main__":
    unittest.main()
