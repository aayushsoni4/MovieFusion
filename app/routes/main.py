from app.routes import main_bp
from flask import render_template
from app.utils.helper import popular_movies


@main_bp.route("/")
def index():
    movies = popular_movies()
    for movie in movies:
        release_date = movie.get("release_date", "")
        release_year = release_date.split("-")[0] if release_date else ""
        movie["release_year"] = release_year
    return render_template("index.html", movies=movies)
