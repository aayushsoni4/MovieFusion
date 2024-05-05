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
    Log in route.

    If user is already authenticated, redirects to the main index page.
    If request method is POST, attempts to log in the user using the provided credentials.
    If successful, redirects to the main index page. Otherwise, displays an error message.
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
                flash("Incorrect username or password. Please try again.", "error")
                logger.warning(
                    f"Login attempt failed for user {username}: incorrect password."
                )
        else:
            flash("Username not found. Please check your credentials.", "error")
            logger.warning(f"Login attempt failed: user {username} not found.")
    return render_template("login.html")


@auth_bp.route("/forgot_password", methods=["POST", "GET"])
def forgot_password():
    """
    Forgot password route.

    Placeholder for future password recovery functionality.
    """
    return "<h1>Forgot Password</h1>"


@auth_bp.route("/register", methods=["POST", "GET"])
def register():
    """
    Register route.

    If user is already authenticated, redirects to the main index page.
    If request method is POST, attempts to register a new user.
    If registration is successful, redirects to the login page with a success message.
    If username or email already exists, displays an error message.
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
    Logout route.

    Logs out the current user and redirects to the login page with a notification message.
    """
    logout_user()
    flash("You have been logged out. See you soon!", "info")
    logger.info("User logged out.")
    return redirect(url_for("auth.login"))
