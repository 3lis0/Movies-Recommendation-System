import random

def get_recommended_ids(movie_id: int, df, top_n: int = 10) -> list[int]:
    #random.seed(movie_id)  # to make recommendations consistent per movie
    valid_movies = df[
        (df['movieId'] != movie_id) & 
        (df['poster_path'].notna())
    ]['movieId'].tolist()

    if top_n > len(valid_movies):
        top_n = len(valid_movies)

    return random.sample(valid_movies, top_n)
