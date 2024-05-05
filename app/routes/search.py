from flask import render_template, redirect, url_for
from flask_login import current_user, login_required
from app.routes import search_bp
from app.utils.helper import perform_search
from logger import logger


@search_bp.route("/<query>")
@login_required
def search(query):
    try:
        logger.info(
            f"Search page requested for query: {query} by user: {current_user.username}"
        )
        search_results = perform_search(query)
        return render_template(
            "search.html",
            query=(" ".join(query.split("-"))),
            search_result=search_results,
        )
    except Exception as e:
        logger.error(f"Error occurred while performing search: {str(e)}")
        return render_template(
            "error.html", error_message="Oops! Something went wrong."
        )
