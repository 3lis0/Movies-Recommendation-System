import random
import pandas as pd

def get_recommended_ids(movie_id: int, top_n: int = 10) -> list[int]:
    df = pd.read_csv('data/new_movies.csv')
    valid_movies = df[(df['movieId'] != movie_id)]['movieId'].tolist()

    if top_n > len(valid_movies):
        top_n = len(valid_movies)

    return random.sample(valid_movies, top_n)

def get_recommended_ids_for_user(user_id: int, top_n: int = 10) -> list[int]:
    df = pd.read_csv('data/new_movies.csv')
    movies = df['movieId'].tolist()

    if top_n > len(movies):
        top_n = len(movies)

    return random.sample(movies, top_n)
