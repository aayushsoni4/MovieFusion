from flask import render_template
from app.routes import search_bp
from app.utils.helper import perform_search


@search_bp.route("/<query>")
def search(query):
    search_results = perform_search(query)
    return render_template("search.html", query=query, search_result=search_results)
