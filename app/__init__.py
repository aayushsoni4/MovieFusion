from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config


db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.utils.helper import url_slug

    app.jinja_env.filters["url_slug"] = url_slug

    db.init_app(app)
    from app.routes import auth_bp, main_bp, movie_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(movie_bp, url_prefix="/movie")
    app.register_blueprint(main_bp)

    return app
