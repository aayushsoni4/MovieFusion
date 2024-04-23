import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "movies.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
