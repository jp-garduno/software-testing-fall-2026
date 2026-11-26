import os
import json
import logging
import random
from urllib import error, parse, request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

GENRES_MAP = {
    "accion": "28",
    "acción": "28",
    "aventura": "12",
    "aventuras": "12",
    "animacion": "16",
    "animación": "16",
    "comedia": "35",
    "crimen": "80",
    "documental": "99",
    "drama": "18",
    "familia": "10751",
    "familiar": "10751",
    "fantasia": "14",
    "fantasía": "14",
    "historia": "36",
    "terror": "27",
    "miedo": "27",
    "musica": "10402",
    "música": "10402",
    "misterio": "9648",
    "romance": "10749",
    "romantica": "10749",
    "ciencia ficcion": "878",
    "ciencia ficción": "878",
    "pelicula de tv": "10770",
    "suspenso": "53",
    "thriller": "53",
    "guerra": "10752",
    "belica": "10752",
    "western": "37",
    "vaqueros": "37",
}


def get_movie_of_the_day():
    url = "https://api.themoviedb.org/3/movie/popular"

    query_params = {"language": "es-MX", "page": "1"}

    querystring = parse.urlencode(query_params)
    full_url = f"{url}?{querystring}"

    token = os.environ.get("TMDB_TOKEN")

    req = request.Request(full_url)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/json")

    try:
        with request.urlopen(req) as response:
            if response.getcode() == 200:
                data = json.loads(response.read().decode())
                results = data.get("results", [])

                if results:
                    return results[0]
                else:
                    return "no_movies_found"

    except error.URLError as e:
        logger.error(f"API Error: {e}")
        return "api_error"

    return "api_error"


#
def get_movie_list(handler_input):
    base_url = "https://api.themoviedb.org/3/discover/movie"

    attr = handler_input.attributes_manager.persistent_attributes
    saved_genres = attr.get("lista_generos")

    logger.info(f"Generos recuperados de la DB: {saved_genres}")

    if not saved_genres:
        return "first_time"

    genres_ids = []
    for genre_name in saved_genres:
        clean_name = str(genre_name).lower().strip()
        if clean_name in GENRES_MAP:
            genres_ids.append(GENRES_MAP[clean_name])
        else:
            logger.warning(f"Genero '{clean_name}' no encontrado en el Mapa.")

    if not genres_ids:
        return "no_valid_ids_found"

    joined_ids = "|".join(genres_ids)

    query_params = {
        "language": "es-MX",
        "page": "1",
        "with_genres": joined_ids,
        "sort_by": "popularity.desc",
    }

    querystring = parse.urlencode(query_params)
    full_url = f"{base_url}?{querystring}"

    token = os.environ.get("TMDB_TOKEN")

    req = request.Request(full_url)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/json")

    try:
        with request.urlopen(req) as response:
            if response.getcode() == 200:
                data = json.loads(response.read().decode())
                results = data.get("results", [])

                if results:
                    return results
                else:
                    return "no_movies_found"

    except error.URLError as e:
        logger.error(f"API Error: {e}")
        return "api_error"

    return "api_error"


def get_next_movie_response(handler_input):
    session_attr = handler_input.attributes_manager.session_attributes

    movie_queue = session_attr.get("movie_queue", [])
    current_index = session_attr.get("movie_index", 0)

    logger.info(
        f"SOLICITANDO SIGUIENTE. Cola: {len(movie_queue)} peliculas. Indice actual: {current_index}"
    )

    if not movie_queue:
        return (
            "No tengo una lista activa de recomendaciones. Pídeme que te recomiende una película primero.",
            "¿Qué te gustaría hacer?",
        )

    new_index = current_index + 1

    if new_index < len(movie_queue):
        session_attr["movie_index"] = new_index
        handler_input.attributes_manager.session_attributes = session_attr

        movie = movie_queue[new_index]
        title = movie.get("title", "Pelicula sin titulo")
        overview = movie.get("overview", "Sin descripción")

        speak_output = (
            f"Aquí tienes otra: {title}. {overview}. ¿Quieres ver otra opción?"
        )
        reprompt = "¿Te doy otra opción?"
    else:
        speak_output = "Ya no tengo más recomendaciones en esta lista. ¿Quieres buscar por otro género?"
        reprompt = "¿Quieres buscar otro género?"
        session_attr["movie_queue"] = []

    return speak_output, reprompt


#
def spin_the_wheel(handler_input):
    results = get_movie_list(handler_input)

    wheel_list = []
    for i in range(6):
        wheel_list.append(results[i])

    num = random.randint(0, 5)
    movie = wheel_list[num]

    return movie
