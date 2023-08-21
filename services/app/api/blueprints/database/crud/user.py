from ..schema.user import UserCreate
from http import HTTPStatus
from sqlalchemy.orm import Session
from ....extensions.extensions import bcrypt
from ..models.user import User
from ..schema.user import User as UserSchema
from ..schema.user import (
    GetUser, GetUsers, ActivateUser, LoginUser, RequestPasswordReset, PasswordReset
)
from typing import Optional
from jwt import ExpiredSignatureError, InvalidTokenError


def create_user(user_data: UserCreate, session: Session):
    hashed_password = User.hash_password(user_data.password)
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


def user_account_active(session: Session, user_data: GetUser):
    with session() as db:
        user: User = db.query(User).filter(User.id == user_data.user_id).first()
    return user.activated


def activate_user_account(session: Session, activation_data: ActivateUser):
    with session() as db:
        user: User = db.query(User).filter(User.id == activation_data.user_id).first()
        if user.id == User.decode_auth_token(activation_data.activation_token):
            user.activated = True
            db.commit()
            return True
    raise InvalidTokenError('Invalid or Expired token.')


def loggin_user(session: Session, login_data: LoginUser):
    with session() as db:
        user: User = db.query(User).filter(User.email_address == login_data.email_address).first()
        if user and user.check_password(login_data.password):
            return True
    raise ValueError('Invalid email address and or password.')


def generate_password_reset_token(session: Session, reset_password_request: RequestPasswordReset):
    with session() as db:
        user: User = db.query(User).filter(User.email_address == reset_password_request.email_address).first()
    resp = {
        'user_id': user.id,
        'email_address': user.email_address,
        'password_reset_token': user.generate_password_reset_token()
    }
    return resp


def password_repeated(session: Session, password_reset: PasswordReset):
    with session() as db:
        user: User = db.query(User).filter(User.email_address == password_reset.email_address).first()
    return user.check_password(password_reset.password)


def reset_password(session: Session, password_reset: PasswordReset):
    with session() as db:
        user: User = db.query(User).filter(User.email_address == password_reset.email_address).first()
        email_address = user.decode_password_token(password_reset.password_reset_token)
        if email_address == user.email_address:
            user.password = user.hash_password(password_reset.password)
            db.commit()
            return True