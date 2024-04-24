from app.routes import main_bp
from flask import render_template, url_for


@main_bp.route("/")
def index():
    title = "MovieFusion"
    return render_template("index.html", title=title)
