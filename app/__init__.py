from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config


db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.utils.helper import url_slug

    app.jinja_env.filters["url_slug"] = url_slug

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for("auth.login"))

    from app.routes import auth_bp, main_bp, movie_bp, category_bp, search_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(movie_bp, url_prefix="/movie")
    app.register_blueprint(category_bp, url_prefix="/category")
    app.register_blueprint(search_bp, url_prefix="/search")
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User

        return User.query.get(int(user_id))

    return app
