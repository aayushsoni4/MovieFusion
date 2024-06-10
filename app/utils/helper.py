from app.utils import trailer_finder
import googleapiclient
import pickle
import re
import os


def url_slug(title):
    """
    Convert a movie title into a URL-friendly slug.

    Args:
        title (str): The original movie title.

    Returns:
        str: The URL-friendly slug.
    """
    title = re.sub(r"[^\w\s-]", "", title)
    title = title.strip().replace(" ", "-")
    title = re.sub(r"-+", "-", title)
    return title.lower()


def load_movie_data(file_path):
    """
    Load movie data from a pickle file.

    Args:
        file_path (str): The path to the pickle file.

    Returns:
        dict: A dictionary of movie data.
        If the file is not found, returns an empty dictionary.
    """
    try:
        with open(file_path, "rb") as f:
            movies = pickle.load(f)
        return movies
    except FileNotFoundError:
        print("Error: File not found.")
        return {}


# Set the path to the movie dataset
current_dir = os.path.dirname(os.path.realpath(__file__))
dataset_path = os.path.join(current_dir, "..", "..", "dataset", "movie_api.pkl")

# Load movie data
movies = load_movie_data(dataset_path)

# Create a dictionary to map URL slugs to movie IDs
title_id = {}
for movie_id, movie_data in movies.items():
    title = movie_data.get("title", "")
    slug_title = url_slug(title)
    title_id[slug_title] = movie_id


def fetch_poster(movie_id):
    """
    Fetch the poster URL for a given movie ID.

    Args:
        movie_id (int): The ID of the movie.

    Returns:
        str: The URL of the movie's poster.
        If the poster is not found, returns a default image URL.
    """
    try:
        data = movies[movie_id]
        return "http://image.tmdb.org/t/p/w780" + data["poster_path"]
    except KeyError:
        return (
            "https://m.media-amazon.com/images/I/61CHaKs2i1L._AC_UF1000,1000_QL80_.jpg"
        )


def movie_response(movie_id):
    """
    Retrieve the movie data for a given movie ID.

    Args:
        movie_id (int): The ID of the movie.

    Returns:
        dict: The movie data.
        If the movie is not found, returns an error message.
    """
    try:
        return movies[movie_id]
    except KeyError:
        return {"error": "Movie not found for the provided ID"}


def backdrop_poster(movie_id):
    """
    Fetch the backdrop poster URL for a given movie ID.

    Args:
        movie_id (int): The ID of the movie.

    Returns:
        str: The URL of the movie's backdrop poster.
        If the backdrop is not found, returns a default image URL.
    """
    try:
        data = movies[movie_id]
        return "http://image.tmdb.org/t/p/w780" + data["backdrop_path"]
    except KeyError:
        return "https://upload.wikimedia.org/wikipedia/commons/d/d1/Image_not_available.png"


def popular_movies(already_watched):
    """
    Retrieve a list of popular movies excluding the ones already watched.

    Args:
        already_watched (list): A list of tuples containing already watched movie IDs and timestamps.

    Returns:
        list: A sorted list of popular movies.
    """
    already_watched_ids = [movie_id for movie_id, _ in already_watched]
    filtered_movies = [
        movie
        for movie in movies.values()
        if movie.get("vote_count", 0) > 10000
        and movie.get("id") not in already_watched_ids
    ]

    sorted_movies = sorted(
        filtered_movies,
        key=lambda x: (x.get("vote_average", 0), x.get("popularity", 0)),
        reverse=True,
    )
    return sorted_movies[:20]


def latest_movies(already_watched):
    """
    Retrieve a list of the latest movies excluding the ones already watched.

    Args:
        already_watched (list): A list of tuples containing already watched movie IDs and timestamps.

    Returns:
        list: A sorted list of the latest movies.
    """
    already_watched_ids = [movie_id for movie_id, _ in already_watched]
    filtered_movies = [
        movie
        for movie in movies.values()
        if movie.get("release_date")
        and movie.get("vote_count", 0) > 5000
        and movie.get("id") not in already_watched_ids
    ]

    sorted_movies = sorted(
        filtered_movies,
        key=lambda x: x.get("release_date", ""),
        reverse=True,
    )
    return sorted_movies[:12]


def get_movie_id_by_name(name):
    """
    Get the movie ID by its name.

    Args:
        name (str): The name of the movie.

    Returns:
        int: The movie ID, or None if not found.
    """
    return title_id.get(name)


def get_movie_trailer(movie_id):
    """
    Fetch the trailer URL for a given movie ID.

    Args:
        movie_id (int): The ID of the movie.

    Returns:
        str: The URL of the movie's trailer.
        If the trailer is not found, returns a default trailer URL.
    """
    data = movie_response(movie_id)
    query = (
        data.get("original_title", data.get("title", "Avatar 2009"))
        + " "
        + str(data["release_date"][:4])
        + " official trailer"
    )
    try:
        video_url = trailer_finder.findYTtrailer(query)
    except (googleapiclient.errors.HttpError, Exception) as e:
        try:
            video_url = trailer_finder.findYTtrailerbs4(query)
        except Exception as e:
            video_url = "https://www.youtube.com/watch?v=5PSNL1qE6VY"
    return video_url


def filter_movies_by_genre(category):
    """
    Filter movies by a specific genre.

    Args:
        category (str): The genre to filter by.

    Returns:
        list: A sorted list of movies in the specified genre.
    """
    filtered_movies = [
        movie
        for movie in movies.values()
        if movie.get("vote_count", 0) > 10000
        and any(genre.get("name") == category for genre in movie.get("genres", []))
    ]

    sorted_movies = sorted(
        filtered_movies,
        key=lambda x: x.get("vote_average", x.get("popularity", 0)),
        reverse=True,
    )
    return sorted_movies[:20]


def perform_search(query):
    """
    Perform a search for movies based on a query.

    Args:
        query (str): The search query.

    Returns:
        list: A list of movies matching the search query.
    """
    return [
        movie
        for movie in movies.values()
        if query.lower() in url_slug(movie.get("title", ""))
    ]
