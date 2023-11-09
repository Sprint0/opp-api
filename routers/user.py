from fastapi import APIRouter, Depends, HTTPException
from datetime import timedelta, datetime
from starlette import status
from pydantic import BaseModel
from models.models import Users
from db.database import SessionLocal
from typing import Annotated, Any
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


router = APIRouter(prefix='/users', tags=['users'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class UserCreate(BaseModel):
    email: str
    username: str
    first_name: str
    surname: str
    password: str
    is_active: bool
    phone_number: str


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user_create: UserCreate):
    create_user_model = Users(
        email=user_create.email,
        username=user_create.username,
        first_name=user_create.first_name,
        surname=user_create.surname,
        hashed_password=bcrypt_context.hash(user_create.password),
        is_active=True,
        phone_number=user_create.phone_number
    )

    db.add(create_user_model)
    db.commit()











