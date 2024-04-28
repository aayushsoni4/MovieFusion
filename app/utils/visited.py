from flask import session
from datetime import datetime


def add_visited_movie(movie_id):
    visited_movies = session.get("visited_movies", [])
    for i, movie in enumerate(visited_movies):
        if movie[0] == movie_id:
            visited_movies[i] = (movie_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            break
    else:
        visited_movies.append((movie_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    session["visited_movies"] = visited_movies
