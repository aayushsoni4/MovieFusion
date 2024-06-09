from datetime import datetime
from app import db


class UserHistory(db.Model):
    """
    UserHistory model representing the history of movies watched by users.

    Attributes:
        id (int): Primary key for the history record.
        user_id (int): Foreign key referencing the User who watched the movie.
        movie_id (int): ID of the movie watched.
        watched_at (datetime): Timestamp when the movie was watched.
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)
    watched_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("history", lazy=True))

    def __repr__(self):
        """String representation of the UserHistory object."""
        return f"<UserHistory user_id={self.user_id} movie_id={self.movie_id} watched_at={self.watched_at}>"
