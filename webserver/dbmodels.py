from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, LargeBinary
from sqlalchemy.orm import relationship

from database import Base

class Floor(Base):
    __tablename__ = "floors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))
    number = Column(Integer)
    image = Column(LargeBinary)
    width = Column(Float)
    height = Column(Float)
    nodes = relationship("Node", back_populates="floor", cascade="all, delete")

class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))
    address64 = Column(String(16))
    x = Column(Float)
    y = Column(Float)
    floor_id = Column(Integer, ForeignKey("floors.id"))
    floor = relationship("Floor", back_populates="nodes")

