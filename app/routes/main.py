from app.routes import main_bp
from flask import render_template
from app.utils.helper import popular_movies, latest_movies


@main_bp.route("/")
def index():
    popular_movie = popular_movies()
    latest_movie = latest_movies()

    for movie in popular_movie:
        release_date = movie.get("release_date", "")
        release_year = release_date.split("-")[0] if release_date else ""
        movie["release_year"] = release_year
    
    for movie in latest_movie:
        release_date = movie.get("release_date", "")
        release_year = release_date.split("-")[0] if release_date else ""
        movie["release_year"] = release_year

    return render_template("index.html", popular_movie=popular_movie, latest_movie=latest_movie)
