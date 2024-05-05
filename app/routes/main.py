from app.routes import main_bp
from flask import render_template, jsonify, session, redirect, url_for
from flask_login import current_user, login_required
from app.utils.recommendation import recommended_movies
from app.utils.helper import popular_movies, latest_movies, movie_response
from app.utils.visited import add_visited_movie


@main_bp.route("/")
@login_required
def index():
    visited_movie_id = session.get("visited_movies", [])
    visited_movie_id = sorted(visited_movie_id, reverse=True, key=lambda x: x[1])
    visited_movie = []
    for movie_id, _ in visited_movie_id:
        visited_movie.append(movie_response(movie_id))

    popular_movie = popular_movies(already_watched=visited_movie_id)
    latest_movie = latest_movies(already_watched=visited_movie_id)

    for movie in latest_movie:
        release_date = movie.get("release_date", "")
        release_year = release_date.split("-")[0] if release_date else ""
        movie["release_year"] = release_year

    because_you_watch = []
    if len(visited_movie) > 0:
        because_you_watch = recommended_movies(
            visited_movie_id[0][0], already_watched=visited_movie_id
        )

    return render_template(
        "index.html",
        popular_movie=popular_movie,
        latest_movie=latest_movie,
        visited_movie=visited_movie,
        watched_title=visited_movie[0]["title"] if len(visited_movie) > 0 else None,
        because_you_watch=because_you_watch,
    )


@main_bp.route("/history/<int:movie_id>", methods=["GET"])
def history(movie_id):
    add_visited_movie(movie_id)
    return jsonify({"message": "Movie ID added to visited_movies session list"})


@main_bp.route("/history")
def visited_movies():
    visited_movie = session.get("visited_movies", [])
    visited_movie = sorted(visited_movie, reverse=True, key=lambda x: x[1])
    return jsonify({"message": visited_movie})
