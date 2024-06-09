from app.routes import auth_bp
from flask import render_template, session, request, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from logger import logger
from app import db
from app.utils.verification import (
    add_user,
    send_otp,
    otp,
    activate_user,
    generate_token,
)


@auth_bp.route("/login", methods=["POST", "GET"])
def login():
    """
    Handle the login process for a user.

    GET: Serve the login page.
    POST: Authenticate the user and redirect to the index page if successful,
    otherwise, flash an error message and re-render the login page or OTP validation page if user is not activated.

    Returns:
        On GET: Rendered 'login.html' template.
        On POST: Redirect to 'main.index' if login is successful, otherwise
        render 'login.html' with an error message, or 'validate_user.html' if user is not activated.

    Notes:
        - This route is accessible only to non-authenticated users.
        - Logs successful and failed login attempts.
    """
    # Redirect to index if user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Query user by username or email
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()

        if user:
            # Check if the provided password matches the stored hash
            if check_password_hash(user.password_hash, password):
                if user.is_activated:
                    login_user(user)
                    logger.info(f"User {username} logged in successfully.")
                    return redirect(url_for("main.index"))
                else:
                    # If account is not activated, send OTP for validation
                    session["email"] = user.email
                    send_otp(session.get("email"))
                    flash("Account not activated. Please verify your email.", "info")
                    return redirect(url_for("auth.validate_user"))
            else:
                flash("Incorrect password. Please try again.", "error")
                logger.warning(
                    f"Login attempt failed for user {username}: incorrect password."
                )
        else:
            flash("User not found. Please check your credentials.", "error")
            logger.warning(f"Login attempt failed: user {username} not found.")

    return render_template("login.html")


@auth_bp.route("/forgot_password", methods=["POST", "GET"])
def forgot_password():
    """
    Placeholder for forgot password functionality.

    GET/POST: Currently, returns a simple message.

    Returns:
        A simple HTML message indicating the placeholder.
    """
    return "<h1>Forgot Password</h1>"


@auth_bp.route("/resend_otp", methods=["GET"])
def resend_otp():
    """
    Handle OTP resend requests.

    GET: Resend OTP to the email stored in session.

    Returns:
        Redirects to 'main.profile' if user is authenticated.
        Redirects to 'auth.validate_user' if OTP is resent successfully.
        Redirects to 'auth.register' if email sending fails or session email is not found.
        Flashes appropriate messages based on success or failure of the OTP resend process.

    Notes:
        - If OTP resend fails, the user is deleted from the database.
    """
    # Redirect to profile if user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for("main.profile"))

    # Retrieve the user's email from the session
    email = session.get("email")

    if email is None:
        flash("Error! Please register again.", "error")
        return redirect(url_for("auth.register"))

    # Attempt to resend the OTP
    if send_otp(email):
        flash("New OTP sent successfully.", "info")
        return redirect(url_for("auth.validate_user"))
    else:
        flash("Error resending OTP. Please try again later.", "error")

        # Delete the user from the database if email sending fails
        user = User.query.filter_by(email=email).first()
        if user:
            db.session.delete(user)
            db.session.commit()

        # Redirect to the registration page in case of failure
        return redirect(url_for("auth.register"))


@auth_bp.route("/register", methods=["POST", "GET"])
def register():
    """
    Handle user registration requests.

    GET: Render the registration page.
    POST: Register a new user if username and email are unique.

    Returns:
        On GET: Rendered 'register.html' template.
        On POST: Redirect to 'auth.validate_user' if registration is successful, otherwise
        render 'register.html' with an error message.

    Notes:
        - This route is accessible only to non-authenticated users.
        - Checks for existing username or email before registering a new user.
        - Sends an OTP to the registered email for account activation.
        - Logs successful and failed registration attempts.
    """
    # Redirect to index if user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Check if username or email already exists
        existing_user_username = User.query.filter_by(username=username).first()
        existing_user_email = User.query.filter_by(email=email).first()

        if existing_user_username:
            flash("Username already exists. Please choose another.", "error")
            logger.warning(
                f"Registration attempt failed: username {username} already exists."
            )
            return redirect(url_for("auth.register"))
        elif existing_user_email:
            flash("Email already exists. Please choose another.", "error")
            logger.warning(
                f"Registration attempt failed: email {email} already exists."
            )
            return redirect(url_for("auth.register"))
        else:
            # Hash the password and attempt to add the user to the database
            hashed_password = generate_password_hash(password)
            if add_user(username, email, hashed_password):
                session["email"] = email
                if send_otp(email):
                    flash("OTP sent successfully.", "info")
                    return redirect(url_for("auth.validate_user"))
                else:
                    flash("Error sending OTP. Please try again later.", "error")
                    return redirect(url_for("auth.register"))
            else:
                flash("Registration failed.", "error")
                return redirect(url_for("auth.register"))

    return render_template("register.html")


@auth_bp.route("/validate_user", methods=["POST", "GET"])
def validate_user():
    """
    Handle user validation via OTP.

    GET: Render the OTP validation page.
    POST: Validate the OTP entered by the user.

    Returns:
        On GET: Rendered 'validate_user.html' template.
        On POST: Redirect to 'main.index' if OTP validation is successful, otherwise
        re-render 'validate_user.html' with an error message.

    Notes:
        - This route is accessible only to non-authenticated users.
        - Verifies the OTP entered by the user against the current OTP.
        - Activates the user account if OTP validation is successful.
        - Logs successful and failed OTP validation attempts.
    """
    # Redirect to profile if user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for("main.profile"))

    if request.method == "POST":
        otp_entered = request.form.get("otp")
        email = session.get("email")

        # Get the current OTP using the TOTP generator
        current_otp = otp.now()

        if otp_entered == current_otp:
            if activate_user(email):
                user = User.query.filter_by(email=email).first()
                login_user(user)
                session.pop("email", None)
                return redirect(url_for("main.index"))
            else:
                flash("Error activating user.", "error")
                return redirect(url_for("auth.validate_user"))
        else:
            flash("Invalid OTP.", "error")
            return redirect(url_for("auth.validate_user"))

    return render_template("validate_user.html")


@auth_bp.route("/logout")
@login_required
def logout():
    """
    Log the user out and redirect to the login page.

    Returns:
        Redirect to 'auth.login' with a flash message indicating successful logout.

    Notes:
        - This route is accessible only to authenticated users.
        - Logs the logout event.
    """
    logout_user()
    flash("You have been logged out. See you soon!", "info")
    logger.info("User logged out.")
    return redirect(url_for("auth.login"))
