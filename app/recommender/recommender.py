import random
import pandas as pd
import pickle
import numpy as np
import torch
import json
from app.recommender.factorization_model.factorization_machine import FactorizationMachineModel
from lightfm import LightFM
import joblib
from scipy.sparse import coo_matrix
from scipy.sparse import load_npz


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

def lightFM_recommendations(user_id: int, top_n: int):
    # === Load model and mappings ===
    model = joblib.load("app/recommender/lightFM_model/lightfm_model.pkl")
    user_id_map = joblib.load("app/recommender/lightFM_model/user_id_map.pkl")
    item_id_map = joblib.load("app/recommender/lightFM_model/item_id_map.pkl")
    inv_item_id_map = {v: k for k, v in item_id_map.items()}

    # === Load interactions and ratings ===
    interactions = load_npz("app/recommender/lightFM_model/interactions.npz")
    ratings_df = pd.read_csv("data/ratings.csv")
    ratings_df = ratings_df[ratings_df['rating'] > 6]

    # === Fallback if user is unknown ===
    if user_id not in user_id_map:
        print(f"[WARN] User {user_id} not found. Finding similar user...")

        # Try finding a user who rated the same movies
        user_movies = ratings_df[ratings_df['userId'] == user_id]['movieId'].tolist()
        if not user_movies:
            print("[INFO] Cold start user. Recommending global top-N.")
            user_idx = 0  # fallback to user 0
        else:
            # Find user with max overlap
            known_users = ratings_df['userId'].unique()
            overlap_scores = {}

            for uid in known_users:
                other_movies = set(ratings_df[ratings_df['userId'] == uid]['movieId'])
                overlap = len(set(user_movies) & other_movies)
                if overlap > 0:
                    overlap_scores[uid] = overlap

            if not overlap_scores:
                user_idx = 0
            else:
                most_similar_user = max(overlap_scores, key=overlap_scores.get)
                user_idx = user_id_map[most_similar_user]
                print(f"[INFO] Using similar user {most_similar_user} instead.")
    else:
        user_idx = user_id_map[user_id]

    # === Predict scores ===
    scores = model.predict(user_ids=user_idx, item_ids=np.arange(len(item_id_map)))

    # Mask already-interacted items
    known_items = interactions.tocsr()[user_idx].indices
    scores[known_items] = -np.inf

    # Top-N results
    top_indices = np.argsort(-scores)[:top_n]
    top_scores = scores[top_indices]
    top_movie_ids = [inv_item_id_map[idx] for idx in top_indices]

    return top_movie_ids, top_scores.tolist()

import numpy as np
import joblib
from sklearn.metrics.pairwise import cosine_similarity
import random

def recommend_similar_movies(movie_id, top_n=10, randomness_factor=2):
    # === Load features and mappings ===
    final_features = np.load("app/recommender/cosine_similarity/final_features.npy")
    movie_id_to_index = joblib.load("app/recommender/cosine_similarity/movie_id_to_index.pkl")
    index_to_movie_id = joblib.load("app/recommender/cosine_similarity/index_to_movie_id.pkl")

    if movie_id not in movie_id_to_index:
        raise ValueError("Movie ID not found in the dataset.")

    idx = movie_id_to_index[movie_id]
    movie_vector = final_features[idx].reshape(1, -1)

    # === Compute cosine similarity with all movies ===
    sim_scores = cosine_similarity(movie_vector, final_features)[0]

    # Get top (top_n * randomness_factor) indices, excluding self
    pool_size = top_n * randomness_factor
    top_pool_indices = sim_scores.argsort()[::-1]
    top_pool_indices = [i for i in top_pool_indices if i != idx][:pool_size]

    # Randomly select top_n
    selected_indices = random.sample(top_pool_indices, top_n)

    # Extract IDs and scores
    similar_movie_ids = [index_to_movie_id[i] for i in selected_indices]
    similar_scores = [round(sim_scores[i], 4) for i in selected_indices]

    # Sort by similarity descending
    sorted_pairs = sorted(zip(similar_movie_ids, similar_scores), key=lambda x: -x[1])
    sorted_movie_ids, sorted_scores = zip(*sorted_pairs)

    return list(sorted_movie_ids), list(sorted_scores)

