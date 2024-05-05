from app.routes import main_bp
from flask import render_template, jsonify, session
from flask_login import current_user, login_required
from app.utils.recommendation import recommended_movies
from app.utils.helper import popular_movies, latest_movies, movie_response
from app.utils.visited import add_visited_movie
from logger import logger


@main_bp.route("/")
@login_required
def index():
    """
    Serve the main index page with personalized movie recommendations.

    This route fetches the user's previously visited movies from the session,
    generates recommendations based on the user's history, and displays
    popular and latest movies excluding the ones already watched.

    Returns:
        str: Rendered HTML template for the index page.

    Raises:
        Exception: If an error occurs during fetching or rendering movies.

    Notes:
        - Requires the user to be logged in to access the index page.
        - Logs the request for the index page.
        - Retrieves visited movies from the session and formats them.
        - Retrieves popular and latest movies excluding the visited ones.
        - Generates recommendations based on the user's history.
    """
    try:
        # Log the index page request
        logger.info(f"Index page requested by user: {current_user.username}")

        # Fetch visited movies from the session
        visited_movie_id = session.get("visited_movies", [])
        visited_movie_id = sorted(visited_movie_id, reverse=True, key=lambda x: x[1])

        # Get detailed information for visited movies
        visited_movie = [movie_response(movie_id) for movie_id, _ in visited_movie_id]

        # Get popular and latest movies (excluding visited ones)
        popular_movie = popular_movies(already_watched=visited_movie_id)
        latest_movie = latest_movies(already_watched=visited_movie_id)

        # Extract release year from release date for latest movies
        for movie in latest_movie:
            release_date = movie.get("release_date", "")
            release_year = release_date.split("-")[0] if release_date else ""
            movie["release_year"] = release_year

        # Generate recommendations based on the user's history
        because_you_watch = []
        if visited_movie:
            because_you_watch = recommended_movies(
                visited_movie_id[0][0], already_watched=visited_movie_id
            )

        return render_template(
            "index.html",
            popular_movie=popular_movie,
            latest_movie=latest_movie,
            visited_movie=visited_movie,
            watched_title=visited_movie[0]["title"] if visited_movie else None,
            because_you_watch=because_you_watch,
        )

    except Exception as e:
        error_message = (
            "An error occurred while rendering the index page. Please try again later."
        )
        logger.error(f"{error_message} Error: {str(e)}")
        return render_template("error.html", error_message=error_message), 500


@main_bp.route("/history/<int:movie_id>", methods=["GET"])
def history(movie_id):
    """
    Add a movie to the user's visited history.

    Args:
        movie_id (int): The unique identifier of the movie.

    Returns:
        JSON: Response indicating the movie was added to the history.

    Raises:
        Exception: If an error occurs during the process.

    Notes:
        - Logs the request for adding a movie to history.
        - Adds the movie ID to the visited_movies session list.
    """
    try:
        logger.info(
            f"Movie with ID: {movie_id} was played by user: {current_user.username}"
        )

        add_visited_movie(movie_id)
        return jsonify({"message": "Movie ID added to visited_movies session list"})

    except Exception as e:
        error_message = "An error occurred while processing your request."
        logger.error(f"{error_message} Error: {str(e)}")
        return jsonify({"error": error_message}), 500


@main_bp.route("/history")
def visited_movies():
    """
    Retrieve the list of movies visited by the current user.

    Returns:
        JSON: Response containing the list of visited movies.

    Raises:
        Exception: If an error occurs during retrieval.

    Notes:
        - Logs the request for retrieving visited movies.
        - Retrieves visited movies from the session and formats them.
    """
    try:
        logger.info(f"Visited movies page requested by user: {current_user.username}")
        visited_movie = session.get("visited_movies", [])
        visited_movie = sorted(visited_movie, reverse=True, key=lambda x: x[1])
        return jsonify({"visited_movies": visited_movie})

    except Exception as e:
        error_message = (
            "An error occurred while retrieving visited movies. Please try again later."
        )
        logger.error(f"{error_message} Error: {str(e)}")
        return jsonify({"error": error_message}), 500
