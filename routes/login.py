from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from database.models import User
from schemas.user import UserCreate, UserResponse
login_router = APIRouter()

@login_router.post("/users", response_model=UserResponse)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user = User(email=user_data.email)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


