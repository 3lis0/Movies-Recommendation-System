import random
import pandas as pd
import pickle
import numpy as np
import torch
import json
from app.recommender.factorization_model.factorization_machine import FactorizationMachineModel


def get_recommended_ids(movie_id: int, top_n: int = 10) -> list[int]:
    df = pd.read_csv('data/new_movies.csv')
    valid_movies = df[(df['movieId'] != movie_id)]['movieId'].tolist()

    if top_n > len(valid_movies):
        top_n = len(valid_movies)

    return random.sample(valid_movies, top_n)

def SVD_reccomendation(user_id: int, top_n: int = 10) -> list[int]:
    with open("app/recommender/svd_model.pkl", "rb") as f:
        model = pickle.load(f)
        ratings_df = pd.read_csv('data/ratings.csv')
        all_movie_ids = ratings_df['movieId'].unique()
        rated_movie_ids = ratings_df[ratings_df['userId'] == user_id]['movieId'].values
        unrated_movie_ids = [mid for mid in all_movie_ids if mid not in rated_movie_ids]
        predictions = [
            model.predict(str(user_id), str(movie_id))
            for movie_id in unrated_movie_ids
        ]
        recommended_movies = sorted(predictions, key=lambda x: x.est, reverse=True)[:top_n]
        movie_ids = [int(pred.iid) for pred in recommended_movies]
        predicted_ratings = [int(pred.est) for pred in recommended_movies]
        return movie_ids,predicted_ratings


def _load_recommender_assets():
    # Load encoders
    user_enc = pickle.load(open("app/recommender/factorization_model/user_enc.pkl", "rb"))
    movie_enc = pickle.load(open("app/recommender/factorization_model/movie_enc.pkl", "rb"))

    # Load data
    ratings_df = pd.read_csv("data/ratings.csv")
    movies_df = pd.read_csv("data/movies_feature_engineered.csv")

    # Load features
    with open("app/recommender/factorization_model/cont_features.json", "r") as f:
        cont_features = json.load(f)

    # Define model shape
    num_users = len(user_enc.classes_)
    num_movies = len(movie_enc.classes_)
    num_cont_features = len(cont_features)

    model = FactorizationMachineModel(num_users, num_movies, num_cont_features)
    model.load_state_dict(torch.load("app/recommender/factorization_model/fm_model.pt", map_location="cpu"))

    return model, user_enc, movie_enc, ratings_df, movies_df, cont_features


def FM_recommendations(user_id: int, top_n: int = 10):
    """
    Get top-N movie recommendations for a given user using a trained FM model.

    Args:
        user_id (int): Original user ID.
        top_n (int): Number of movies to recommend.

    Returns:
        Tuple[List[int], List[float]]: Movie IDs and predicted ratings.
    """

    # Load everything needed
    model, user_enc, movie_enc, ratings_df, movies_df, cont_features = _load_recommender_assets()

    model.eval()
    device = next(model.parameters()).device

    # Encode user
    user_idx = user_enc.transform([user_id])[0]

    # Get unrated movies
    rated_movie_ids = ratings_df[ratings_df['userId'] == user_id]['movieId'].values
    all_movie_ids = ratings_df['movieId'].unique()
    unrated_movie_ids = [mid for mid in all_movie_ids if mid not in rated_movie_ids]
    movie_indices = movie_enc.transform(unrated_movie_ids)

    # Create input
    X_cat = np.array([[user_idx, midx] for midx in movie_indices])
    X_cont = movies_df.set_index('movieId').loc[unrated_movie_ids][cont_features].values.astype('float32')

    # Predict
    X_cat_tensor = torch.tensor(X_cat, dtype=torch.long).to(device)
    X_cont_tensor = torch.tensor(X_cont, dtype=torch.float).to(device)

    with torch.no_grad():
        preds = model(X_cat_tensor, X_cont_tensor).cpu().numpy()

    top_idx = preds.argsort()[::-1][:top_n]
    top_movie_ids = [unrated_movie_ids[i] for i in top_idx]
    top_scores = preds[top_idx].tolist()

    return top_movie_ids, top_scores


