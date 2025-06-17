from flask import Blueprint, render_template, request, jsonify
import pandas as pd
from app.utils.user_processor import process_users

users_bp = Blueprint('users', __name__, url_prefix='/users')

# Load the user metadata once (or move to app startup logic)
user_df = pd.read_csv("data/user_metadata.csv")
USERS_PER_PAGE = 48  # same as the default limit

@users_bp.route("/")
def list_users():
    # Get query parameters
    min_rated = int(request.args.get("min_rated", 0))
    sort_by = request.args.get("sort", "userId")
    sort_order = request.args.get("order", "asc")
    limit = 48
    start = int(request.args.get("start", 0))

    # Process the user data
    users = process_users(
        df=user_df,
        min_rated=min_rated,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit + 1,  # Get one extra to check for more
        start=start
    )

    has_more = len(users) > limit
    users = users[:limit]  # Trim to limit if extra was fetched
    
    return render_template("users.html", users=users,
                           sort_by=sort_by,
                           sort_order=sort_order,
                           min_rated=min_rated,
                           has_more=has_more)


@users_bp.route('/load_more_users')
def load_more_users():
    min_rated = int(request.args.get("min_rated", 0))
    sort_by = request.args.get("sort", "userId")
    sort_order = request.args.get("order", "asc")
    page = int(request.args.get("page", 0))

    start = page * USERS_PER_PAGE
    limit = USERS_PER_PAGE

    users = process_users(
        df=user_df,
        min_rated=min_rated,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit + 1,  # Fetch one extra to check if more exist
        start=start
    )

    has_more = len(users) > limit
    users = users[:limit]

    rendered_cards = render_template("partials/user_cards.html", users=users)
    return jsonify({
        "html": rendered_cards,
        "has_more": has_more
    })