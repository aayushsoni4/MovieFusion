from app.utils.helper import movie_response
import pickle
import os


def load_model(file_path):
    try:
        with open(file_path, "rb") as f:
            similarity = pickle.load(f)
        return similarity
    except FileNotFoundError:
        print("Error: File not found.")
        return {}


current_dir = os.path.dirname(os.path.realpath(__file__))
features_similarity_dataset_path = os.path.join(
    current_dir, "..", "..", "models", "features_similarity.pkl"
)

features_similarity = load_model(features_similarity_dataset_path)

items_similarity_dataset_path = os.path.join(
    current_dir, "..", "..", "models", "items_similarity.pkl"
)

items_similarity = load_model(items_similarity_dataset_path)


def recommended_movies(movie_id):
    recommended_movie = features_similarity[movie_id][:12]
    movies = [movie_response(int(float(movie_id))) for movie_id in recommended_movie]
    return movies


def because_you_watched(movie_id):
    recommended_movie = items_similarity[movie_id][:10]
    movies = [movie_response(int(float(movie_id))) for movie_id in recommended_movie]
    return movies
