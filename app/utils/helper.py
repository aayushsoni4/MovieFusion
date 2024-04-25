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
        return None


def backdrop_poster(movie_id):
    try:
        data = movies[movie_id]
        return "http://image.tmdb.org/t/p/w780" + data["backdrop_path"]
    except KeyError:
        return "https://upload.wikimedia.org/wikipedia/commons/d/d1/Image_not_available.png"
