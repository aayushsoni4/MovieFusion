from app.routes import category_bp
from flask import render_template
from app.utils.helper import filter_movies_by_genre


@category_bp.route("/<path:genre_name>")
def category(genre_name):
    genre_name = " ".join(word.capitalize() for word in genre_name.split("-"))
    movies = filter_movies_by_genre(genre_name)
    return render_template("category.html", movies=movies, genre=genre_name)
