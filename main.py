from fastapi import Depends, FastAPI,Request
from sqlalchemy.orm import Session
import os
from contextlib import asynccontextmanager
from database.db import get_db
from database.models import User
from schemas.user import UserCreate, UserResponse
from routes.login import login_router

from exceptions import UserAlreadyExistsError

import logging
from core.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()

    logger = logging.getLogger(__name__)
    logger.info("Application starting")

    yield

    logger.info("Application shutting down")


app = FastAPI(
    title="My API",
    lifespan=lifespan,
)


@app.get("/")
def home():
    return {"message": "API is running"}


@app.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


app.include_router(login_router)