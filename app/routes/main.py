from app.routes import main_bp
from flask import render_template


@main_bp.route("/")
def index():
    return render_template("index.html")
