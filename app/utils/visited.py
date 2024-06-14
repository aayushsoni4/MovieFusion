from flask_login import current_user
from app.models import UserHistory, UserRating
from datetime import datetime
from logger import logger
from app import db


def add_visited_movie(movie_id):
    """
    Add a movie to the viewing history of the current user, or update the watched_at time if it already exists.

    Args:
        movie_id (int): The ID of the movie to be added to the history.

    Returns:
        bool: True if the movie was successfully added or updated, False otherwise.
    """
    try:
        # Convert movie_id to int
        movie_id = int(movie_id)

        # Check if the movie is already in the user's history
        history_entry = UserHistory.query.filter_by(
            user_id=current_user.id, movie_id=movie_id
        ).first()

        if history_entry:
            # If the entry exists, update the watched_at time
            history_entry.watched_at = datetime.now()
            action = "updated"
        else:
            # If the entry does not exist, create a new one
            new_history_entry = UserHistory(
                user_id=current_user.id,
                movie_id=movie_id,
                watched_at=datetime.now(),
            )
            db.session.add(new_history_entry)
            action = "added"

        # Commit changes to the database
        db.session.commit()

        logger.info(f"Movie {movie_id} {action} in history for user {current_user.id}")
        return True
    except Exception as e:
        # Log any exceptions that occur
        logger.error(
            f"Failed to add or update movie {movie_id} in history for user {current_user.id}: {e}"
        )
        # Rollback the session in case of error
        db.session.rollback()
        return False


def add_movie_rating(movie_id, rating):
    """
    Add or update the rating for a movie by the current user.

    Args:
        movie_id (int): The ID of the movie to be rated.
        rating (int): The rating given by the user (1-5).

    Returns:
        bool: True if the rating was successfully added or updated, False otherwise.
    """
    try:
        # Check if the user has already rated this movie
        user_rating = UserRating.query.filter_by(
            user_id=current_user.id, movie_id=movie_id
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
