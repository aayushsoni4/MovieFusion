from app.utils.helper import movie_response
from flask_login import current_user
from app.models import UserHistory
from collections import defaultdict
from app import db
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
similarity_score_dataset_path = os.path.join(
    current_dir, "..", "..", "models", "similarity_scores.pkl"
)

# Load similarity models
features_similarity = load_model(features_similarity_dataset_path)
items_similarity = load_model(items_similarity_dataset_path)
similarity_score = load_model(similarity_score_dataset_path)


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


def recommend_movies_based_on_genre(target_genre_name, already_watched):
    """
    Recommend movies based on the target genre, excluding those already watched.

    Args:
        target_genre_name (str): The name of the target genre.
        already_watched (list): A list of tuples containing movie IDs and their corresponding similarity scores.

    Returns:
        list: A list of recommended movie IDs.
    """
    visited_movie_ids = (
        db.session.query(UserHistory.movie_id, UserHistory.watched_at)
        .filter_by(user_id=current_user.id)
        .order_by(UserHistory.watched_at.desc())
        .all()
    )
    visited_movie_ids_genre = []
    # Filter visited movie IDs by genre
    for movie_id, _ in visited_movie_ids:
        movie = movie_response(movie_id)
        for genre in movie.get('genres', []):
            if genre['name'] == target_genre_name:
                visited_movie_ids_genre.append(movie_id)

    recommendation_scores = defaultdict(list)

    # Calculate average similarity scores for recommended movies
    for movie_id in visited_movie_ids_genre:
        recommendations = similarity_score.get(movie_id, None)
        for recommended_movie_id, sim_score in recommendations:
            recommendation_scores[recommended_movie_id].append(sim_score)

    average_scores = {
        movie_id: sum(scores) / len(scores)
        for movie_id, scores in recommendation_scores.items()
    }

    sorted_recommendations = sorted(
        average_scores.items(), key=lambda x: x[1], reverse=True
    )

    recommended_movies = []
    already_watched_ids = [watched_id for watched_id, _ in already_watched]
    for movie_id, _ in sorted_recommendations:
        if movie_id not in already_watched_ids:
            movie_data = movie_response(movie_id)
            if movie_data:
                for genre in movie_data.get('genres', []):
                    if genre['name'] == target_genre_name:
                        recommended_movies.append(movie_data)
            if len(recommended_movies) == 20:
                break

    return recommended_movies
