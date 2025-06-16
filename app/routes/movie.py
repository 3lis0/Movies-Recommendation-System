from flask import Blueprint, render_template, request, abort
from app.utils.movie_processor import get_movie_details, get_minimal_movie_cards
from app.recommender.random_recommender import get_recommended_ids
import pandas as pd

movie_bp = Blueprint('movie', __name__)
movies_df = pd.read_csv("data/new_movies.csv")

@movie_bp.route('/movie/<int:movie_id>')
def movie_page(movie_id):
    top_n = int(request.args.get("top_n", 6))

    movie = get_movie_details(movie_id, movies_df)
    if not movie:
        abort(404)

    recommended_ids = get_recommended_ids(movie_id, movies_df, top_n)
    recommendations = get_minimal_movie_cards(recommended_ids, movies_df)

    return render_template("movie.html", movie=movie, recommendations=recommendations, top_n=top_n)
