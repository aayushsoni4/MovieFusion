from app.routes import auth_bp


@auth_bp.route("/login")
def login():
    return "<h1>Login</h1>"


@auth_bp.route("/forgot_password")
def forgot_password():
    return "<h1>Forgot Password</h1>"


@auth_bp.route("/register")
def register():
    return "<h1>Register</h1>"
