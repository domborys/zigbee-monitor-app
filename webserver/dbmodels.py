from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP, DateTime

from database import Base

class Floor(Base):
    __tablename__ = "floors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))
    number = Column(Integer)
    image = Column(LargeBinary)
    image_media_type = Column(String(256))
    width = Column(Float)
    height = Column(Float)
    nodes = relationship("Node", back_populates="floor", cascade="all, delete-orphan")

class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))
    address64 = Column(String(16))
    x = Column(Float)
    y = Column(Float)
    floor_id = Column(Integer, ForeignKey("floors.id"))
    floor = relationship("Floor", back_populates="nodes")
    reading_configs = relationship("ReadingConfig", back_populates="node", cascade="all, delete-orphan")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64))
    password_hash = Column(String(128))
    role = Column(String(32))
    disabled = Column(Boolean)
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")

class ReadingConfig(Base):
    __tablename__ = "reading_configs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64))
    mode = Column(String(8))
    refresh_period = Column(Float)
    message_prefix = Column(String(256))
    message_to_send = Column(String(256))
    at_command = Column(String(2))
    at_command_data = Column(String(256))
    at_command_result_format = Column(String(8))
    node_id = Column(Integer, ForeignKey("nodes.id"))
    node = relationship("Node", back_populates="reading_configs")

class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(43), index = True, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(User, back_populates="sessions")
    time_started = Column(DateTime)
    time_last_activity = Column(DateTime)


