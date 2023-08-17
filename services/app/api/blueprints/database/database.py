from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from sqlalchemy.orm import sessionmaker
import os
from contextlib import contextmanager


class Base(MappedAsDataclass, DeclarativeBase):
    pass

SQLALCHEMY_DATABASE_URI = 'sqlite:///./oryks.db'
engine = create_engine(SQLALCHEMY_DATABASE_URI, 
                       connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def create_all():
    Base.metadata.create_all(bind=engine)

@contextmanager
def get_db():
    try:
        db = Session()
        yield db
    finally:
        db.close()
    
