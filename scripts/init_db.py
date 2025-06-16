from app import create_app, db
from app.models import User, Rating  # Import all models before create_all

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Database tables created.")
