from app.db.session import SessionLocal
from fastapi import Depends
from app.models.user import User  # adjust import if needed

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user():
    # mock function or real token decoding logic
    return User(id=1, username="testuser")  # Replace with real logic
