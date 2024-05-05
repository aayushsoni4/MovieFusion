from flask import render_template, jsonify, session, redirect, url_for
from flask_login import login_required
from app.routes import movie_bp
from datetime import datetime
from app.utils.helper import movie_response, get_movie_id_by_name, get_movie_trailer
from app.utils.recommendation import recommended_movies


@movie_bp.route("/<path:movie_name>")
@login_required
def movie(movie_name):
    visited_movie_id = session.get("visited_movies", [])

    movie_id = get_movie_id_by_name(movie_name)
    movie = movie_response(movie_id=movie_id)
    movie["release"] = datetime.strptime(movie["release_date"], "%Y-%m-%d").strftime(
        "%d %B %Y"
    )

    movie["trailer"] = get_movie_trailer(movie_id)
    video_id = movie["trailer"].split("v=")[1]

    movie["embed_trailer"] = (
        "https://www.youtube.com/embed/" + f"{video_id}" + "?si=uxBB_OOhszRSE_CN"
    )
    return render_template(
        "movie.html",
        movie=movie,
        recommended_movie=recommended_movies(
            movie_id, already_watched=visited_movie_id
        ),
    )


@movie_bp.route("/<int:movie_id>")
def movie_detail(movie_id):
    return jsonify(movie_response(movie_id))
