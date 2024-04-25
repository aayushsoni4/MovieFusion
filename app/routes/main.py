from app.routes import main_bp
from flask import render_template, url_for, request


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/movie/<movie_name>")
def movie(movie_name):
    return render_template("movie.html", movie_name=movie_name)
