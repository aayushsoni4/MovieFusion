from flask import render_template, redirect, url_for
from flask_login import current_user
from app.routes import search_bp
from app.utils.helper import perform_search


@search_bp.route("/<query>")
def search(query):
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))

    search_results = perform_search(query)
    return render_template(
        "search.html", query=(" ".join(query.split("-"))), search_result=search_results
    )
