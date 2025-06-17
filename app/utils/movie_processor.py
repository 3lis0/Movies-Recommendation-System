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

def process_movies(df: pd.DataFrame, genre_filter=None, sort_by='vote_average', order = 'asc', limit=20, start=0):
    df = df.copy()
    df['genre_list'] = df['genres'].apply(extract_genre_names)
    df['release_year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year

    if genre_filter and genre_filter != 'All':
        df = df[df['genre_list'].apply(lambda genres: genre_filter in genres)]

    if sort_by in ['vote_average', 'popularity', 'release_year', 'title']:
        df = df.sort_values(by=sort_by, ascending=(order == 'asc'))
    df = df.iloc[start:start+limit]

    df = df.head(limit)

    movies = []
    for _, row in df.iterrows():
        movie = {
            "movieId": int(row.movieId),
            "title": row.title if row.title else 'Title Unavailable',
            "overview": row.overview if row.overview else '',
            "genre_list": row.genre_list[0:min(3,len(row.genre_list))] if row.genre_list else [],
            "release_year": int(row.release_year) if pd.notnull(row.release_year) else None,
            "vote_average": f'{row.vote_average:.1f}' if row.vote_average else 'N/A',
            "poster_url": img.get_url(img.poster_sizes.w342, row.poster_path)
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
        "title": row.title if row.title else 'Title Unavailable',
        "overview": row.overview if row.overview else '',
        "release_date": row.release_date if pd.notnull(row.release_date) else None,
        "release_year": int(row.release_date[:4]) if isinstance(row.release_date, str) else None,
        "runtime": int(row.runtime) if not pd.isna(row.runtime) else None,
        "vote_average": f'{row.vote_average:.1f}' if row.vote_average and str(row.vote_average)!='nan' else 'N/A',
        "vote_count": int(row.vote_count) if row.vote_count and str(row.vote_count)!='nan' else 'N/A',
        "genres": parse_genres(row.genres),
        "poster_url": img.get_url(img.poster_sizes.w780, row.poster_path),
        "backdrop_url": img.get_url(img.backdrop_sizes.w780, row.backdrop_path, True),
        "tagline": row.tagline if pd.notnull(row.tagline) else None,
        "status": row.status if row.status else '',
        "original_language": row.original_language if row.original_language else '',
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
            "title": row.title if row.title else 'Title Unavailable',
            "poster_url": img.get_url(img.poster_sizes.w342, row.poster_path),
            "genre_list": row.genre_list,
            "vote_average": f'{row.vote_average:.1f}' if pd.notnull(row.vote_average) else "N/A",
            "release_year": int(row.release_year) if pd.notnull(row.release_year) else None,
        }
        movies.append(movie)
    return movies

def process_user_ratings(user_id: int, ratings_df: pd.DataFrame, movies_df: pd.DataFrame,
                         start: int = 0, limit: int = 20):
    # Filter for user
    user_ratings = ratings_df[ratings_df['userId'] == user_id].copy()

    # Sort by timestamp (latest first)
    user_ratings = user_ratings.sort_values(by="timestamp", ascending=False)

    # Join with movie data
    merged = user_ratings.merge(
        movies_df,
        how='left',
        left_on='movieId',
        right_on='movieId'
    )

    # Slice the desired page
    sliced = merged.iloc[start:start + limit + 1]  # +1 for has_more logic

    results = []
    for _, row in sliced.iterrows():
        results.append({
            "movieId": int(row.movieId),
            "title": row.title if row.title else 'Title Unavailable',
            "poster_url": img.get_url(img.poster_sizes.w154, row.poster_path),
            "user_rating": int(row.rating*2) if row.rating else 'N/A',
            "vote_average": f'{row.vote_average:.1f}' if pd.notnull(row.vote_average) else "N/A"
        })

    has_more = len(sliced) > limit
    return results[:limit], has_more