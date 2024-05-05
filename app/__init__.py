from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from logger import logger

# Initialize Flask extensions
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_class=Config):
    """
    Create and configure the Flask application.

    Args:
        config_class (class): Configuration class for the Flask application.

    Returns:
        Flask: Initialized Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register custom Jinja filter for URL slugs
    from app.utils.helper import url_slug

    app.jinja_env.filters["url_slug"] = url_slug

    # Initialize Flask extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Handle unauthorized access
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for("auth.login"))

    # Register blueprints for different routes
    from app.routes import auth_bp, main_bp, movie_bp, category_bp, search_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(movie_bp, url_prefix="/movie")
    app.register_blueprint(category_bp, url_prefix="/category")
    app.register_blueprint(search_bp, url_prefix="/search")
    app.register_blueprint(main_bp)

    # Create database tables
    with app.app_context():
        db.create_all()

    # Load user for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User

        return User.query.get(int(user_id))

    logger.info("Flask application initialized successfully.")
    return app
