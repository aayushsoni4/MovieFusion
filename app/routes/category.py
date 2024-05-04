from app.routes import category_bp
from flask import render_template, redirect, url_for
from app.utils.helper import filter_movies_by_genre
from flask_login import current_user


@category_bp.route("/<path:genre_name>")
def category(genre_name):
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))

    genre_name = " ".join(word.capitalize() for word in genre_name.split("-"))
    movies = filter_movies_by_genre(genre_name)
    return render_template("category.html", movies=movies, genre=genre_name)
