"""Module providing SQLAlchemy setup"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from . import config

engine = create_engine(
    config.DATABASE_URL, connect_args={"check_same_thread": False}
)
"""The SQLAlchemy database engine."""

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""A callable generating database sessions."""

Base = declarative_base()
"""A base for all ORM classes."""