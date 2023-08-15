from ..schema.user import UserCreate
from http import HTTPStatus
from sqlalchemy.orm import Session
from ....extensions.extensions import bcrypt
from ..models.user import User
from ..schema.user import User as UserSchema
from ..schema.user import GetUser, GetUsers
from typing import Optional


def create_user(user_data: UserCreate, session: Session):
    hashed_password = bcrypt.generate_password_hash(user_data.password)
    user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email_address=user_data.email_address,
        password=hashed_password
    )
    with session() as db:
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def get_user_by_email(session: Session, email: str):
    with session() as db:
        user = db.query(User).filter(User.email_address == email).first()
    return user

def get_user(session: Session, user_data: GetUser):
    with session() as db:
        user = db.query(User).filter(User.id == user_data.user_id).first()
    return user

def get_users(session: Session, user_data: GetUsers):
    with session() as db:
        users = db.query(User).offset(user_data.offset).limit(user_data.limit).all()
    return users

def delete_user(session: Session, user_data: GetUser):
    with session() as db:
        user = db.query(User).filter(User.id == user_data.user_id).first()
        db.delete(user)
        db.commit()
        
    return user