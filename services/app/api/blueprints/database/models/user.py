from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email_address: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    registration_date: Mapped[datetime] = mapped_column(default_factory=datetime.utcnow)