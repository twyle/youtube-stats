from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base
import datetime as dt
import jwt
from flask import current_app
from jwt import ExpiredSignatureError, InvalidTokenError

from ....extensions.extensions import bcrypt


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email_address: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    registration_date: Mapped[datetime] = mapped_column(default_factory=datetime.utcnow)
    role: Mapped[str] = mapped_column(default='user')
    activated: Mapped[bool] = mapped_column(default=False)
    
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def encode_auth_token(user_id: int):
        try:
            payload = {
                "exp": dt.datetime.utcnow() + dt.timedelta(days=0, hours=2),
                "iat": dt.datetime.utcnow(),
                "sub": user_id,
            }
            return jwt.encode(payload, current_app.config.get("SECRET_KEY"), algorithm="HS256")
        except Exception as e:
            return e

    @staticmethod
    def generate_admin_token(admin_id: int):
        try:
            payload = {
                "exp": dt.datetime.utcnow() + dt.timedelta(days=7, hours=0),
                "iat": dt.datetime.utcnow(),
                "sub": admin_id,
            }
            return jwt.encode(payload, current_app.config.get("SECRET_KEY"), algorithm="HS256")
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token: str):
        try:
            payload = jwt.decode(auth_token, current_app.config.get("SECRET_KEY"), algorithms="HS256")
            return payload["sub"]
        except (ExpiredSignatureError, InvalidTokenError) as e:
            raise e
        
    def generate_password_reset_token(self):
        try:
            payload = {
                "exp": dt.datetime.utcnow() + dt.timedelta(days=7, hours=0),
                "iat": dt.datetime.utcnow(),
                "sub": self.email_address,
            }
            return jwt.encode(payload, current_app.config.get("SECRET_KEY"), algorithm="HS256")
        except Exception as e:
            return e
     
    @staticmethod   
    def decode_password_token(auth_token: str):
        try:
            payload = jwt.decode(auth_token, current_app.config.get("SECRET_KEY"), algorithms="HS256")
            return payload["sub"]
        except (ExpiredSignatureError, InvalidTokenError) as e:
            raise e