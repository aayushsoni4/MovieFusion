from app.utils import trailer_finder
import googleapiclient
import pickle
import re
import os


def url_slug(title):
    title = re.sub(r"[^\w\s-]", "", title)
    title = title.strip().replace(" ", "-")
    title = re.sub(r"-+", "-", title)
    return title.lower()


def load_movie_data(file_path):
    try:
        with open(file_path, "rb") as f:
            movies = pickle.load(f)
        return movies
    except FileNotFoundError:
        print("Error: File not found.")
        return {}


current_dir = os.path.dirname(os.path.realpath(__file__))
dataset_path = os.path.join(current_dir, "..", "..", "dataset", "movie_api.pkl")

movies = load_movie_data(dataset_path)

title_id = {}
for movie_id, movie_data in movies.items():
    title = movie_data.get("title", "")
    slug_title = url_slug(title)
    title_id[slug_title] = movie_id


def fetch_poster(movie_id):
    try:
        data = movies[movie_id]
        return "http://image.tmdb.org/t/p/w780" + data["poster_path"]
    except KeyError:
        return (
            "https://m.media-amazon.com/images/I/61CHaKs2i1L._AC_UF1000,1000_QL80_.jpg"
        )


def movie_response(movie_id):
    try:
        return movies[movie_id]
    except KeyError:
        return {"error": "Movie not found for the provided ID"}


def backdrop_poster(movie_id):
    try:
        data = movies[movie_id]
        return "http://image.tmdb.org/t/p/w780" + data["backdrop_path"]
    except KeyError:
        return "https://upload.wikimedia.org/wikipedia/commons/d/d1/Image_not_available.png"


def popular_movies(already_watched):
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
    return title_id.get(name)


def get_movie_trailer(movie_id):
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
    return [
        movie
        for movie in movies.values()
        if query.lower() in url_slug(movie.get("title", ""))
    ]
