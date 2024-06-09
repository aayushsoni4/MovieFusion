import os
from datetime import timedelta
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

    # Email Configuration
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT"))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
