import json
import pandas as pd
from app.utils.image_info import ImageInfo

img = ImageInfo()

def extract_genre_names(genre_json):
    try:
        genres = json.loads(genre_json.replace("'", '"'))
        return [g['name'] for g in genres] if isinstance(genres, list) else []
    except:
        return []

def process_movies(df: pd.DataFrame, genre_filter=None, sort_by='vote_average', limit=20, start=0):
    df = df.copy()
    df['genre_list'] = df['genres'].apply(extract_genre_names)
    df['release_year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year

    if genre_filter and genre_filter != 'All':
        df = df[df['genre_list'].apply(lambda genres: genre_filter in genres)]

    if sort_by in ['vote_average', 'popularity', 'release_year', 'title']:
        df = df.sort_values(by=sort_by, ascending=False if sort_by != 'title' else True)
    df = df.iloc[start:start+limit]

    df = df.head(limit)

    movies = []
    for _, row in df.iterrows():
        movie = {
            "movieId": int(row.movieId),
            "title": row.title,
            "overview": row.overview,
            "genre_list": row.genre_list,
            "release_year": int(row.release_year) if pd.notnull(row.release_year) else None,
            "vote_average": f'{row.vote_average:.1f}',
            "poster_url": img.get_url(img.poster_sizes.w342, row.poster_path) if pd.notnull(row.poster_path) else None
        }
        movies.append(movie)

    return movies

def extract_genres(df):
    all_genres = set()
    for gjson in df['genres'].dropna():
        try:
            genres = json.loads(gjson.replace("'", '"'))
            all_genres.update(g['name'] for g in genres)
        except:
            continue
    return sorted(all_genres)

def get_movie_details(movie_id: int, df) -> dict:
    try:
        row = df[df['movieId'] == movie_id].iloc[0]
    except IndexError:
        return None  # movieId not found

    def parse_genres(g):
        try:
            genres = json.loads(g.replace("'", '"'))
            return [genre['name'] for genre in genres]
        except:
            return []

    return {
        "movieId": int(row.movieId),
        "title": row.title,
        "overview": row.overview,
        "release_date": row.release_date,
        "release_year": int(row.release_date[:4]) if isinstance(row.release_date, str) else None,
        "runtime": int(row.runtime) if not pd.isna(row.runtime) else None,
        "vote_average": f'{row.vote_average:.1f}',
        "vote_count": int(row.vote_count),
        "genres": parse_genres(row.genres),
        "poster_url": img.get_url(img.poster_sizes.w780, row.poster_path) if pd.notnull(row.poster_path) else None,
        "backdrop_url": img.get_url(img.backdrop_sizes.w780, row.backdrop_path) if pd.notnull(row.backdrop_path) else None,
        "tagline": row.tagline if pd.notnull(row.tagline) else None,
        "status": row.status,
        "original_language": row.original_language,
    }
    
def get_minimal_movie_cards(movie_ids: list[int], df) -> list[dict]:
    filtered = df[df['movieId'].isin(movie_ids)]

    def parse_genres(g):
        try:
            genres = json.loads(g.replace("'", '"'))
            return [genre['name'] for genre in genres]
        except:
            return []

    filtered['genre_list'] = filtered['genres'].apply(parse_genres)
    filtered['release_year'] = pd.to_datetime(filtered['release_date'], errors='coerce').dt.year

    movies = []
    for _, row in filtered.iterrows():
        movie = {
            "movieId": int(row.movieId),
            "title": row.title,
            "poster_url": img.get_url(img.poster_sizes.w342, row.poster_path) if pd.notnull(row.poster_path) else None,
            "genre_list": row.genre_list,
            "vote_average": row.vote_average,
            "release_year": int(row.release_year) if pd.notnull(row.release_year) else None,
        }
        movies.append(movie)
    return movies