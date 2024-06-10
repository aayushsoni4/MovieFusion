from flask import render_template, redirect, url_for
from flask_login import current_user, login_required
from app.routes import search_bp
from app.utils.helper import perform_search
from logger import logger


@search_bp.route("/<query>")
@login_required
def search(query):
    """
    Render the search results page for the specified query.

    Args:
        query (str): The search query extracted from the URL path.

    Returns:
        str: Rendered HTML template for the search results page.

    Raises:
        Exception: If an error occurs during search or rendering.

    Notes:
        - Requires the user to be logged in to access the search page.
        - Logs the request for the search page.
        - Performs a search based on the query.
        - Renders the 'search.html' template with search results.
    """
    try:
        # Log the search page request
        logger.info(
            f"Search page requested for query: {query} by user: {current_user.username}"
        )

        # Perform search based on the query
        search_results = perform_search(query)

        # Render the search results page
        return render_template(
            "search.html",
            query=(" ".join(query.split("-"))),
            search_result=search_results,
        )
    except Exception as e:
        # Log the error and display an error message
        logger.error(f"Error occurred while performing search: {str(e)}")
        return render_template(
            "error.html", error_message="Oops! Something went wrong."
        )
