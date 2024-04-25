from flask import render_template, jsonify
from app.routes import movie_bp
from datetime import datetime
from app.utils.helper import movie_response, get_movie_id_by_name, get_movie_trailer
from app.utils.recommendation import recommended_movies


@movie_bp.route("/<path:movie_name>")
def movie(movie_name):
    movie_id = get_movie_id_by_name(movie_name)
    movie = movie_response(movie_id=movie_id)
    movie["release"] = datetime.strptime(movie["release_date"], "%Y-%m-%d").strftime(
        "%d %B %Y"
    )
    movie["trailer"] = get_movie_trailer(movie_id)
    return render_template(
        "movie.html", movie=movie, recommended_movie=recommended_movies(movie_id)
    )


@movie_bp.route("/<int:movie_id>")
def movie_detail(movie_id):
    return jsonify(movie_response(movie_id))
