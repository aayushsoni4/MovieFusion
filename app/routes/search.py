from flask import render_template, redirect, url_for
from flask_login import login_required
from app.routes import search_bp
from app.utils.helper import perform_search


@search_bp.route("/<query>")
@login_required
def search(query):
    search_results = perform_search(query)
    return render_template(
        "search.html", query=(" ".join(query.split("-"))), search_result=search_results
    )
