from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    """
    User model representing user data in the database.

    Attributes:
        id (int): Primary key for the user.
        username (str): Username of the user (unique, nullable=False).
        password_hash (str): Hashed password of the user (nullable=False).
        email (str): Email address of the user (unique, nullable=False).
        is_activated (bool): Flag indicating if the user account is activated (default=False).

    Methods:
        get_id(): Get the user ID.
        is_authenticated(): Check if the user is authenticated.
        is_active(): Check if the user account is active.
        is_anonymous(): Check if the user is anonymous.
        __repr__(): String representation of the User object.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    is_activated = db.Column(db.Boolean, default=False)

    def get_id(self):
        """Get the user ID."""
        return self.id

    def is_authenticated(self):
        """Check if the user is authenticated."""
        return True

    def is_active(self):
        """Check if the user account is active."""
        return self.is_activated

    def __repr__(self):
        """String representation of the User object."""
        return "<User {}>".format(self.username)
