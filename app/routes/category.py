from app.routes import category_bp
from flask import render_template
from app.utils.helper import filter_movies_by_genre
from flask_login import current_user, login_required
from logger import logger


@category_bp.route("/<path:genre_name>")
@login_required
def category(genre_name):
    """
    Display a list of movies filtered by the specified genre.

    Args:
        genre_name (str): The genre name extracted from the URL path.

    Returns:
        str: Rendered HTML template for the category page.

    Raises:
        Exception: If an error occurs during movie filtering or rendering.

    Notes:
        - The route URL is "/<path:genre_name>", where "genre_name" is a dynamic parameter.
        - The user must be logged in to access this page.
        - The genre name in the URL can contain hyphens, which are converted to spaces and capitalized.

    Example:
        - If the user visits "/action-movies", the genre_name will be "action movies".
        - The function logs the request and filters movies by the specified genre.
        - The filtered movies are passed to the "category.html" template for rendering.
    """
    try:
        # Capitalize each word in the genre name for better readability
        genre_name = " ".join(word.capitalize() for word in genre_name.split("-"))

        # Log the category page request
        logger.info(
            f"Category page requested for genre: {genre_name} by user: {current_user.username}"
        )

        # Filter movies by the specified genre
        movies = filter_movies_by_genre(genre_name)

        # Render the category page template
        return render_template("category.html", movies=movies, genre=genre_name)
    except Exception as e:
        # Log the error and display an error message
        logger.error(f"Error occurred while rendering category page: {str(e)}")
        return render_template(
            "error.html", error_message="Oops! Something went wrong."
        )
