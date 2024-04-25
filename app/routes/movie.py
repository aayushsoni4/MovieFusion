from flask import render_template
from app.routes import movie_bp


@movie_bp.route("/<path:movie_name>")
def movie(movie_name):
    original_movie_name = movie_name.replace("-", " ")
    return render_template("movie.html", movie_name=original_movie_name)
