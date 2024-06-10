from app.utils.helper import movie_response
import pickle
import os


def load_model(file_path):
    """
    Load a similarity model from a pickle file.

    Args:
        file_path (str): The path to the pickle file.

    Returns:
        dict: A similarity model loaded from the pickle file.
        If the file is not found, returns an empty dictionary.
    """
    try:
        with open(file_path, "rb") as f:
            similarity = pickle.load(f)
        return similarity
    except FileNotFoundError:
        print("Error: File not found.")
        return {}


# Set the paths to the model files
current_dir = os.path.dirname(os.path.realpath(__file__))
features_similarity_dataset_path = os.path.join(
    current_dir, "..", "..", "models", "features_similarity.pkl"
)
items_similarity_dataset_path = os.path.join(
    current_dir, "..", "..", "models", "items_similarity.pkl"
)

# Load similarity models
features_similarity = load_model(features_similarity_dataset_path)
items_similarity = load_model(items_similarity_dataset_path)


def recommended_movies(movie_id, already_watched):
    """
    Generate recommended movies based on a similarity model.

    Args:
        movie_id (int): The ID of the movie for which recommendations are generated.
        already_watched (list): A list of tuples containing already watched movie IDs and timestamps.

    Returns:
        list: A list of recommended movies.
    """
    recommended_movie = features_similarity.get(movie_id, [])
    already_watched_ids = [watched_id for watched_id, _ in already_watched]
    recommended_movie = [
        id for id in recommended_movie if id not in already_watched_ids
    ][:12]
    movies = [movie_response(int(float(movie_id))) for movie_id in recommended_movie]
    return movies
