import pandas as pd

def process_users(df: pd.DataFrame, min_rated=0, sort_by='userId', sort_order='asc', limit=48, start=0):
    df = df.copy()

    # Filter users by minimum rated movies
    if min_rated:
        df = df[df['num_rated_movies'] >= min_rated]

    # Sorting
    valid_sort_keys = ['userId', 'num_rated_movies', 'avg_rating_given']
    if sort_by in valid_sort_keys:
        df = df.sort_values(by=sort_by, ascending=(sort_order == 'asc'))

    # Pagination
    df = df.iloc[start:start + limit]

    # Format into dicts
    users = []
    for _, row in df.iterrows():
        users.append({
            "userId": int(row.userId),
            "num_rated_movies": int(row.num_rated_movies),
            "avg_rating_given": f'{row.avg_rating_given:.2f}'
        })

    return users
