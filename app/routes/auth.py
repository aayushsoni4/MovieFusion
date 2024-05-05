import logging
from app.routes import auth_bp
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from logger import logger
from app import db


@auth_bp.route("/login", methods=["POST", "GET"])
def login():
    """
    Handle the login process for a user.

    GET: Serve the login page.
    POST: Authenticate the user and redirect to the index page if successful,
    otherwise, flash an error message and re-render the login page.

    Returns:
        On GET: Rendered 'login.html' template.
        On POST: Redirect to 'main.index' if login is successful, otherwise
        render 'login.html' with an error message.

    Notes:
        - This route is accessible only to non-authenticated users.
        - Logs successful and failed login attempts.
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()
        if user:
            if check_password_hash(user.password_hash, password):
                login_user(user)
                logger.info(f"User {username} logged in successfully.")
                return redirect(url_for("main.index"))
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
    Serve the forgot password page.

    This is a placeholder route for future implementation of password recovery functionality.

    Returns:
        A simple HTML string with a message.
    """
    return "<h1>Forgot Password</h1>"


@auth_bp.route("/register", methods=["POST", "GET"])
def register():
    """
    Handle the registration process for a new user.

    GET: Serve the registration page.
    POST: Create a new user account and redirect to the login page if successful,
    otherwise, flash an error message and re-render the registration page.

    Returns:
        On GET: Rendered 'register.html' template.
        On POST: Redirect to 'auth.login' if registration is successful, otherwise
        render 'register.html' with an error message.

    Notes:
        - This route is accessible only to non-authenticated users.
        - Checks for existing usernames and emails to avoid duplicates.
        - Logs successful user registration.
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
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
            hashed_password = generate_password_hash(password)
            new_user = User(
                username=username, email=email, password_hash=hashed_password
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful. You can now log in.", "success")
            logger.info(f"User {username} registered successfully.")
            return redirect(url_for("auth.login"))
    return render_template("register.html")


@auth_bp.route("/logout")
@login_required
def logout():
    """
    Log out the current user and redirect to the login page.

    Returns:
        Redirect to 'auth.login' after logging out the user.

    Notes:
        - This route is accessible only to authenticated users.
        - Logs user logout.
    """
    logout_user()
    flash("You have been logged out. See you soon!", "info")
    logger.info("User logged out.")
    return redirect(url_for("auth.login"))
