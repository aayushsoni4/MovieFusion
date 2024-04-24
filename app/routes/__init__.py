from flask import Blueprint

auth_bp = Blueprint("auth", __name__)
main_bp = Blueprint("main", __name__)

from . import auth, main
