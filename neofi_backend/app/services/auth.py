from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, Token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

class AuthService:

    def register(self, user: UserCreate, db: Session) -> Token:
        existing = db.query(User).filter(User.email == user.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed_password = pwd_context.hash(user.password)
        db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return self._create_token(db_user)

    def login(self, user: UserLogin, db: Session) -> Token:
        db_user = db.query(User).filter(User.email == user.email).first()
        if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return self._create_token(db_user)

    def _create_token(self, user: User) -> Token:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {"sub": user.email, "exp": expire}
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return Token(access_token=token)
