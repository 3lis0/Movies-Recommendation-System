from flask import Blueprint, render_template, request, abort, redirect, url_for
from app.utils.movie_processor import get_movie_details, get_minimal_movie_cards
from app.utils.ratings import get_user_rating
from app.recommender.recommender import get_recommended_ids, recommend_similar_movies
from flask_login import current_user,login_required
from app.models import Rating
from app import db
import pandas as pd
from datetime import datetime

movie_bp = Blueprint('movie', __name__)
movies_df = pd.read_csv("data/new_movies.csv")

@movie_bp.route('/movie/<int:movie_id>')
def movie_page(movie_id):
    top_n = int(request.args.get("top_n", 6))
    user_rating = None
    if current_user.is_authenticated:
        user_rating = get_user_rating(current_user.id, movie_id)
    movie = get_movie_details(movie_id, movies_df)
    if not movie:
        abort(404)
    recommended_ids,_ = recommend_similar_movies(movie_id, top_n, 2)
    recommendations = get_minimal_movie_cards(recommended_ids, movies_df)

    return render_template("movie.html", movie=movie, recommendations=recommendations, top_n=top_n, user_rating=user_rating, message = 'You may also like')

@movie_bp.route("/movie/<int:movie_id>/rate", methods=["POST"])
@login_required
def rate_movie(movie_id):
    rating_value = int(request.form.get("rating", 0))
    now = datetime.utcnow()

    rating = Rating.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
    if rating:
        rating.rating = rating_value
        rating.timestamp = now  # update timestamp
    else:
        rating = Rating(
            user_id=current_user.id,
            movie_id=movie_id,
            rating=rating_value,
            timestamp=now  # insert timestamp
        )
        db.session.add(rating)

    db.session.commit()
    return redirect(url_for("movie.movie_page", movie_id=movie_id))

