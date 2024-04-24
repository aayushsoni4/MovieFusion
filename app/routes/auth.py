from app.routes import auth_bp


@auth_bp.route("/login")
def login():
    return "<h1>Login</h1>"
