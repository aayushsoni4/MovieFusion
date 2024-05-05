from app.routes import category_bp
from flask import render_template
from app.utils.helper import filter_movies_by_genre
from flask_login import current_user, login_required
from logger import logger


@category_bp.route("/<path:genre_name>")
@login_required
def category(genre_name):
    try:
        genre_name = " ".join(word.capitalize() for word in genre_name.split("-"))
        logger.info(
            f"Category page requested for genre: {genre_name} by user: {current_user.username}"
        )
        movies = filter_movies_by_genre(genre_name)
        return render_template("category.html", movies=movies, genre=genre_name)
    except Exception as e:
        logger.error(f"Error occurred while rendering category page: {str(e)}")
        return render_template(
            "error.html", error_message="Oops! Something went wrong."
        )
