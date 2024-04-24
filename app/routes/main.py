from app.routes import main_bp


@main_bp.route("/")
def index():
    return "<h1>Hello, World!</h1>"
