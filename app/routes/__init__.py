from flask import Blueprint

auth_bp = Blueprint("auth", __name__)
main_bp = Blueprint("main", __name__)
movie_bp = Blueprint("movie", __name__)
category_bp = Blueprint("category", __name__)
from . import auth, main, movie, category
