import os
from dotenv import load_dotenv

# Load environment variables from .env file
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()


class Config:
    """
    Configuration settings for the Flask application.

    Attributes:
        SECRET_KEY (str): Secret key for protecting against CSRF attacks.
        SQLALCHEMY_DATABASE_URI (str): Database URI for connecting to the SQLite database.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Flag to track modifications in the database.
    """

    SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "movies.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
