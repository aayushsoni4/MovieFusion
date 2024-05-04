from app.routes import auth_bp
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db


@auth_bp.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("main.index"))
        else:
            flash("Invalid username or password.", "error")
    return render_template("login.html")


@auth_bp.route("/forgot_password", methods=["POST", "GET"])
def forgot_password():
    return "<h1>Forgot Password</h1>"


@auth_bp.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        if existing_user:
            flash("Username or email already exists.", "error")
            return redirect(url_for("auth.register"))
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(
                username=username, email=email, password_hash=hashed_password
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful. You can now log in.", "success")
            return redirect(url_for("auth.login"))
    return render_template("register.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
