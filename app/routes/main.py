from app.routes import main_bp
from flask import render_template
from app.utils.helper import popular_movies


@main_bp.route("/")
def index():
    movies = popular_movies()
    return render_template("index.html", movies=movies)
