from app.routes import auth_bp
from flask import render_template, request, url_for, redirect


@auth_bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        return redirect(url_for("main.index"))
    return render_template("login.html")


@auth_bp.route("/forgot_password", methods=["POST", "GET"])
def forgot_password():
    return "<h1>Forgot Password</h1>"


@auth_bp.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        return redirect(url_for("main.index"))
    return render_template("register.html")
