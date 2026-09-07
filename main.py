from fastapi import Depends, FastAPI,Request
from sqlalchemy.orm import Session
import os
from fastapi.responses import JSONResponse
from database.db import engine
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database.db import get_db
from database.models import User
from schemas.user import UserCreate, UserResponse
from routes.login import login_router
from routes.health import router as health_router
from sqlalchemy import text

from exceptions import UserAlreadyExistsError

import logging
from core.logging import setup_logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting")

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        logger.info("Database connection: OK")

    except Exception:
        logger.exception("Database connection: FAILED")
        raise

    yield

    logger.info("Application shutting down")

app = FastAPI(
    title="My API",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "API is running"}

@app.exception_handler(UserAlreadyExistsError)
async def user_already_exists_handler(
    request: Request,
    exc: UserAlreadyExistsError,
):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )

@app.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


app.include_router(login_router)
app.include_router(health_router)

