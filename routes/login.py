from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from database.models import User
from schemas.user import UserCreate, UserResponse
from exceptions import UserAlreadyExistsError

login_router = APIRouter()


@login_router.post("/users", response_model=UserResponse)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise UserAlreadyExistsError("Email already registered")

    user = User(email=user_data.email)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user