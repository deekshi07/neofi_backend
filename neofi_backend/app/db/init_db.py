from app.db.session import engine, Base
from app.models import user, event

def init_db():
    Base.metadata.create_all(bind=engine)
