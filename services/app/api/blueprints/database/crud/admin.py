from ..schema.user import UserCreate
from sqlalchemy.orm import Session
from ..models.user import User
from ..schema.user import (
    GetUser, GetUsers
)


def create_admin(admin_data: UserCreate, session: Session):
    hashed_password = User.hash_password(admin_data.password)
    user = User(
        first_name=admin_data.first_name,
        last_name=admin_data.last_name,
        email_address=admin_data.email_address,
        password=hashed_password,
        role='admin'
    )
    with session() as db:
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def get_admin_by_email(session: Session, email: str):
    with session() as db:
        user = db.query(User).filter(User.email_address == email, User.role == 'admin').first()
    return user

def get_admin(session: Session, admin_data: GetUser):
    with session() as db:
        user = db.query(User).filter(User.id == admin_data.user_id, User.role == 'admin').first()
    return user

def get_admins(session: Session, admin_data: GetUsers):
    with session() as db:
        users = db.query(User).filter(User.role == 'admin').offset(admin_data.offset).limit(admin_data.limit).all()
    return users