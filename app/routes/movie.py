from flask import render_template, jsonify, session, redirect, url_for
from flask_login import current_user, login_required
from app.routes import movie_bp
from datetime import datetime
from app.utils.helper import movie_response, get_movie_id_by_name, get_movie_trailer
from app.utils.recommendation import recommended_movies
from logger import logger


@movie_bp.route("/<path:movie_name>")
@login_required
def movie(movie_name):
    """
    Render the movie page for the specified movie name.

    Args:
        movie_name (str): The name of the movie extracted from the URL path.

    Returns:
        str: Rendered HTML template for the movie page.

    Raises:
        Exception: If an error occurs during rendering.

    Notes:
        - Requires the user to be logged in to access the movie page.
        - Logs the request for the movie page.
        - Retrieves visited movies from the session.
        - Retrieves detailed information for the specified movie.
        - Formats release date and retrieves trailer for the movie.
        - Renders the 'movie.html' template with movie details and recommended movies.
    """
    try:
        logger.info(
            f"Movie page requested for: {movie_name} by user: {current_user.username}"
        )

        visited_movie_id = session.get("visited_movies", [])
        movie_id = get_movie_id_by_name(movie_name)
        movie = movie_response(movie_id=movie_id)
        movie["release"] = datetime.strptime(
            movie["release_date"], "%Y-%m-%d"
        ).strftime("%d %B %Y")

        movie["trailer"] = get_movie_trailer(movie_id)
        video_id = movie["trailer"].split("v=")[1]

        movie["embed_trailer"] = "https://www.youtube.com/embed/" + f"{video_id}"

        return render_template(
            "movie.html",
            movie=movie,
            recommended_movie=recommended_movies(
                movie_id, already_watched=visited_movie_id
            ),
        )
    except Exception as e:
        logger.error(f"Error occurred while rendering movie page: {str(e)}")
        return render_template(
            "error.html", error_message="Oops! Something went wrong."
        )


@movie_bp.route("/<int:movie_id>")
def movie_detail(movie_id):
    """
    Retrieve details for the specified movie ID.

    Args:
        movie_id (int): The unique identifier of the movie.

    Returns:
        JSON: Response containing the details of the movie.

    Raises:
        Exception: If an error occurs during retrieval.

    Notes:
        - Logs the request for retrieving movie details.
        - Returns a JSON response with movie details.
    """
    try:
        logger.info(
            f"Movie details page requested for ID: {movie_id} by user: {current_user.username}"
        )
        return jsonify(movie_response(movie_id))
    except Exception as e:
        logger.error(f"Error occurred while fetching movie details: {str(e)}")
        return render_template(
            "error.html", error_message="Oops! Something went wrong."
        )
