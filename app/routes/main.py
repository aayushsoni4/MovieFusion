from flask import render_template, jsonify
from flask_login import current_user, login_required
from app.utils.recommendation import recommended_movies, recommend_movies_based_on_genre
from app.models import UserHistory
from logger import logger
from app.routes import main_bp
from app import db
from app.utils.helper import (
    popular_movies,
    latest_movies,
    movie_response,
    most_watched_genres,
)


@main_bp.route("/")
@login_required
def index():
    """
    Serve the main index page with personalized movie recommendations.

    This route fetches the user's previously visited movies from the database,
    generates recommendations based on the user's history, and displays
    popular and latest movies excluding the ones already watched.

    Returns:
        str: Rendered HTML template for the index page.

    Raises:
        Exception: If an error occurs during fetching or rendering movies.

    Notes:
        - Requires the user to be logged in to access the index page.
        - Logs the request for the index page.
        - Retrieves visited movies from the database for the current user.
        - Retrieves popular and latest movies excluding the visited ones.
        - Generates recommendations based on the user's history.
        - Includes recommendations based on the user's most-watched genres.
    """
    try:
        # Log the index page request
        logger.info(f"Index page requested by user: {current_user.username}")

        # Fetch visited movies from the database, ordered by watched_at
        visited_movie_id = (
            db.session.query(UserHistory.movie_id, UserHistory.watched_at)
            .filter_by(user_id=current_user.id)
            .order_by(UserHistory.watched_at.desc())
            .all()
        )
        logger.debug(f"Visited movies fetched: {len(visited_movie_id)}")

        # Get detailed information for visited movies
        visited_movie = [movie_response(movie_id) for movie_id, _ in visited_movie_id]
        logger.debug(f"Fetched visited movies: {len(visited_movie)}")

        # Get popular movies (excluding visited ones)
        popular_movie = popular_movies(already_watched=visited_movie_id)
        logger.debug(f"Got popular movies: {len(popular_movie)}")

        # Get latest movies (excluding visited ones)
        latest_movie = latest_movies(already_watched=visited_movie_id)
        logger.debug(f"Got latest movies: {len(latest_movie)}")

        # Extract release year from release date for latest movies
        for movie in latest_movie:
            release_date = movie.get("release_date", "")
            release_year = release_date.split("-")[0] if release_date else ""
            movie["release_year"] = release_year
        logger.debug(f"Got latest movies with release year: {len(latest_movie)}")

        # Generate recommendations based on the user's history
        because_you_watch = []
        if visited_movie:
            because_you_watch = recommended_movies(
                visited_movie_id[0][0], already_watched=visited_movie_id
            )
        logger.debug(f"Got recommendations based on history: {len(because_you_watch)}")

        # Recommend movies based on the user's most-watched genres
        most_watched_genres_name = most_watched_genres()
        default_genre = ['Action', 'Comedy']
        if not most_watched_genres_name:
            most_watched_genres_name.extend(default_genre)
        most_watched_genres_movie = [[], []]
        for index, genre in enumerate(most_watched_genres_name[:2]):
            most_watched_genres_movie[index] = recommend_movies_based_on_genre(
                genre, visited_movie_id
            )
        logger.debug(
            f"Got recommendations by genre for {most_watched_genres_name[0]}: {len(most_watched_genres_movie[0])}, for {most_watched_genres_name[1]}: {len(most_watched_genres_movie[1])}"
        )

        return render_template(
            "index.html",
            popular_movie=popular_movie,
            latest_movie=latest_movie,
            visited_movie=visited_movie,
            watched_title=visited_movie[0]["title"] if visited_movie else None,
            because_you_watch=because_you_watch,
            most_watched_genres_name=most_watched_genres_name,
            recommendations_by_genre=most_watched_genres_movie,
        )

    except Exception as e:
        # Handle any errors that occur during rendering
        error_message = (
            "An error occurred while rendering the index page. Please try again later."
        )
        logger.error(f"{error_message} Error: {str(e)}")
        return render_template("error.html", error_message=error_message), 500


@main_bp.route("/history")
@login_required
def visited_movies():
    """
    Retrieve the list of movies visited by the current user.

    Returns:
        JSON: Response containing the list of visited movies.

    Raises:
        Exception: If an error occurs during retrieval.

    Notes:
        - Logs the request for retrieving visited movies.
        - Retrieves visited movies from the database for the current user.
        - Formats the visited movies data for JSON response.
    """
    try:
        # Log the request for visited movies
        logger.info(f"Visited movies page requested by user: {current_user.username}")

        # Fetch visited movies from the database
        visited_movies = (
            db.session.query(UserHistory.movie_id, UserHistory.watched_at)
            .filter_by(user_id=current_user.id)
            .order_by(UserHistory.watched_at.desc())
            .all()
        )
        logger.debug(f"Visited movies fetched: {len(visited_movies)}")

        # Convert visited movies data to JSON format
        visited_movie_list = [
            {
                "movie_id": movie_id,
                "watched_at": watched_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for movie_id, watched_at in visited_movies
        ]
        logger.debug(f"Visited movies JSON response: {len(visited_movie_list)}")

        return jsonify({"visited_movies": visited_movie_list})

    except Exception as e:
        # Handle any errors that occur during retrieval
        error_message = (
            "An error occurred while retrieving visited movies. Please try again later."
        )
        logger.error(f"{error_message} Error: {str(e)}")
        return jsonify({"error": error_message}), 500
