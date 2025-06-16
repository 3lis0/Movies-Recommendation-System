from flask import Blueprint, render_template, request
import pandas as pd
from app.utils.movie_processor import process_movies, extract_genres
from flask import jsonify, render_template_string

homepage_bp = Blueprint('homepage', __name__)
movies_df = pd.read_csv("data/new_movies.csv")

# Preprocess genres once
ALL_GENRES = extract_genres(movies_df)

MOVIES_PER_PAGE = 48

@homepage_bp.route('/')
def index():
    genre_filter = request.args.get('genre')
    sort_by = request.args.get('sort', 'vote_average')
    page = int(request.args.get('page', 0))

    start = page * MOVIES_PER_PAGE
    limit = MOVIES_PER_PAGE

    movies = process_movies(movies_df, genre_filter, sort_by, limit + 1, start=start)

    has_more = len(movies) > limit
    movies = movies[:limit]

    return render_template(
        'index.html',
        movies=movies,
        all_genres=ALL_GENRES,
        selected_genre=genre_filter or 'All',
        selected_sort=sort_by,
        current_page=page,
        has_more=has_more
    )

@homepage_bp.route('/load_more_movies')
def load_more_movies():
    genre_filter = request.args.get('genre')
    sort_by = request.args.get('sort', 'vote_average')
    page = int(request.args.get('page', 0))

    start = page * MOVIES_PER_PAGE
    limit = MOVIES_PER_PAGE

    movies = process_movies(movies_df, genre_filter, sort_by, limit + 1, start=start)
    has_more = len(movies) > limit
    movies = movies[:limit]

    rendered_cards = render_template('partials/movie_cards.html', movies=movies)
    return jsonify({
        "html": rendered_cards,
        "has_more": has_more
    })