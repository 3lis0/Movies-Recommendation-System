from flask import Blueprint, render_template, request, jsonify
from app.utils.movie_processor import process_user_ratings, get_minimal_movie_cards
import pandas as pd
from app.recommender.recommender import SVD_reccomendation, FM_recommendations, lightFM_recommendations

user_bp = Blueprint("user", __name__, url_prefix="/user")
user_df = pd.read_csv('data/user_metadata.csv')
movies_df = pd.read_csv('data/new_movies.csv')
ratings_df = pd.read_csv('data/ratings.csv')

@user_bp.route("/<int:user_id>")
def user_profile(user_id):
    # Pagination params
    page = int(request.args.get("page", 0))
    limit = 20
    start = page * limit

    # Get metadata (you should already have this loaded at app level)
    user_info = user_df[user_df['userId'] == user_id].squeeze()
    username = f"User #{user_id}"
    num_ratings = int(user_info["num_rated_movies"])
    avg_rating = round(user_info["avg_rating_given"], 2)
    top_n = int(request.args.get("top_n", 6))
    recommended_ids, _ = lightFM_recommendations(user_id, top_n)
    recommendations = get_minimal_movie_cards(recommended_ids, movies_df)

    # Get ratings for this page
    ratings, has_more = process_user_ratings(
        user_id=user_id,
        ratings_df=ratings_df,
        movies_df=movies_df,
        start=start,
        limit=limit
    )
    return render_template(
        "user.html",
        user_id=user_id,
        username=username,
        num_ratings=num_ratings,
        avg_rating=avg_rating,
        ratings=ratings,
        has_more=has_more,
        recommendations=recommendations,
        top_n=top_n,
        message = 'Recommendations for this user'
    )
    
@user_bp.route("/<int:user_id>/load_more")
def load_more_ratings(user_id):
    page = int(request.args.get("page", 0))
    limit = 20
    start = page * limit

    ratings, has_more = process_user_ratings(
        user_id=user_id,
        ratings_df=ratings_df,
        movies_df=movies_df,
        start=start,
        limit=limit
    )

    rendered = render_template("partials/user_ratings_rows.html", ratings=ratings)
    return jsonify({
        "html": rendered,
        "has_more": has_more
    })

