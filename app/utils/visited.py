from flask_login import current_user
from app.models import UserHistory, UserRating
from datetime import datetime
from logger import logger
from app import db


def add_visited_movie(movie_id):
    """
    Adds a movie to the currently logged-in user's viewing history in the database.

    Args:
        movie_id (int): The ID of the movie to be added.

    Returns:
        bool: True if the movie was successfully added to the history, False otherwise.
    """
    try:
        # Create a new UserHistory record
        new_history_entry = UserHistory(
            user_id=current_user.id,
            movie_id=int(float(movie_id)),
            watched_at=datetime.now(),
        )

        # Add to the database and commit changes
        db.session.add(new_history_entry)
        db.session.commit()

        logger.info(f"Movie {movie_id} added to history for user {current_user.id}")
        return True
    except Exception as e:
        # Log any exceptions that occur
        logger.error(
            f"Failed to add movie {movie_id} to history for user {current_user.id}: {e}"
        )
        # Rollback the session in case of error
        db.session.rollback()
        return False


def add_movie_rating(movie_id, rating):
    """
    Adds or updates the rating for a movie by the currently logged-in user.

    Args:
        movie_id (int): The ID of the movie to be rated.
        rating (int): The rating given by the user (1-5).

    Returns:
        bool: True if the rating was successfully added or updated, False otherwise.
    """
    try:
        # Check if the user has already rated this movie
        user_rating = UserRating.query.filter_by(
            user_id=current_user.id, movie_id=int(float(movie_id))
        ).first()

        if user_rating:
            # Update the existing rating
            user_rating.rating = rating
            user_rating.rated_at = datetime.now()
        else:
            # Create a new rating entry
            user_rating = UserRating(
                user_id=current_user.id,
                movie_id=movie_id,
                rating=rating,
                rated_at=datetime.now(),
            )
            db.session.add(user_rating)

        # Commit the changes to the database
        db.session.commit()

        logger.info(
            f"Rating {rating} added for movie {movie_id} by user {current_user.id}"
        )
        return True
    except Exception as e:
        # Log any exceptions that occur
        logger.error(
            f"Failed to add rating for movie {movie_id} by user {current_user.id}: {e}"
        )
        # Rollback the session in case of error
        db.session.rollback()
        return False
