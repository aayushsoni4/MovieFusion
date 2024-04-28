from app.routes import main_bp
from flask import render_template, jsonify, session
from app.utils.helper import popular_movies, latest_movies
from app.utils.visited import add_visited_movie


@main_bp.route("/")
def index():
    popular_movie = popular_movies()
    latest_movie = latest_movies()

    for movie in latest_movie:
        release_date = movie.get("release_date", "")
        release_year = release_date.split("-")[0] if release_date else ""
        movie["release_year"] = release_year

    return render_template(
        "index.html", popular_movie=popular_movie, latest_movie=latest_movie
    )


@main_bp.route("/history/<int:movie_id>", methods=["GET"])
def history(movie_id):
    add_visited_movie(movie_id)
    return jsonify({"message": "Movie ID added to visited_movies session list"})


@main_bp.route("/history")
def visited_movies():
    visited_movie = session.get("visited_movies", [])
    return jsonify({"message": visited_movie})
