from app.models import Rating

def get_user_rating(user_id, movie_id):
    rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    return rating.rating if rating else None
