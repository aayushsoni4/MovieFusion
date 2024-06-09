from datetime import datetime
from app import db


class UserRating(db.Model):
    """
    UserRating model representing the ratings given by users to movies.

    Attributes:
        id (int): Primary key for the rating record.
        user_id (int): Foreign key referencing the User who rated the movie.
        movie_id (int): ID of the movie rated.
        rating (int): Rating given by the user (1-5).
        rated_at (datetime): Timestamp when the movie was rated.
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    rated_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("ratings", lazy=True))

    def __repr__(self):
        """String representation of the UserRating object."""
        return f"<UserRating user_id={self.user_id} movie_id={self.movie_id} rating={self.rating} rated_at={self.rated_at}>"
