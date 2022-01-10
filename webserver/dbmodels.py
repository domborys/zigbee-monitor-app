"""Module defining ORM models used by SQLAlchemy"""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime

from .database import Base

class Floor(Base):
    """A single map in the system."""

    __tablename__ = "floors"

    id = Column(Integer, primary_key=True, index=True)
    """Id in the system (primary key)."""

    name = Column(String(256))
    """Name of the map."""

    number = Column(Integer)
    """The number used for sorting maps. If the maps are building floors, the number may be equal to floor number."""

    image = Column(LargeBinary)
    """Map image file."""

    image_media_type = Column(String(256))
    """Media type of the image file."""

    width = Column(Float)
    """The width of the map."""

    height = Column(Float)
    """The height of the map."""

    nodes = relationship("Node", back_populates="floor", cascade="all, delete-orphan")
    """Nodes present on the map."""

class Node(Base):
    """A node of ZigBee network."""

    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, index=True)
    """Id in the system (primary key)."""

    name = Column(String(256))
    """Node name."""

    address64 = Column(String(16))
    """64-bit address of the node as a hexadecimal string."""

    x = Column(Float)
    """x coordinate of the node on the map."""

    y = Column(Float)
    """y coordinate of the node on the map."""

    floor_id = Column(Integer, ForeignKey("floors.id"))
    """id of the map on which the node is placed."""

    floor = relationship("Floor", back_populates="nodes")
    """The map on which the node is placed."""

    reading_configs = relationship("ReadingConfig", back_populates="node", cascade="all, delete-orphan")
    """The readings related to the node."""

class ReadingConfig(Base):
    """Configuration of a reading provided by a node."""

    __tablename__ = "reading_configs"

    id = Column(Integer, primary_key=True, index=True)
    """Id in the system (primary key)."""

    name = Column(String(64))
    """Name of the reading."""

    mode = Column(String(8))
    """The mode of obtaining the reading."""

    refresh_period = Column(Float)
    """The period in which the reading is refreshed."""

    message_prefix = Column(String(256))
    """Prefix of the message containing the reading value."""

    message_to_send = Column(String(256))
    """The message which will be sent to the device in order to obtain the reading value."""

    at_command = Column(String(2))
    """The AT command which will be used for obtaining the reading value."""

    at_command_data = Column(String(256))
    """Data for the AT command which will be used for obtaining the reading value."""

    at_command_result_format = Column(String(8))
    """Format of the AT command result"""

    node_id = Column(Integer, ForeignKey("nodes.id"))
    """Id of the node which provides the reading."""

    node = relationship("Node", back_populates="reading_configs")
    """The node which provides the reading."""

class User(Base):
    """A user of the system"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    """User id in the system (primary key)."""

    username = Column(String(64))
    """User's username."""

    password_hash = Column(String(128))
    """Hash of user's password"""

    role = Column(String(32))
    """Role of the user. Can be either "user" or "admin"."""

    disabled = Column(Boolean)
    """True if the user is disabled."""

    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    """Sessions of the user."""

class UserSession(Base):
    """User session.
    
    Session is created when the user logs in and deleted when user logs out or does not make any requests in specified time.
    """

    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    """Id of the session in the database (primary key)."""

    session_id = Column(String(43), index = True, unique=True)
    """Session id used by the user for authorization."""

    user_id = Column(Integer, ForeignKey("users.id"))
    """Id of the user to whom the session belongs."""

    user = relationship(User, back_populates="sessions")
    """The user to whom the session belongs."""

    time_started = Column(DateTime)
    """Time when the session was started."""

    time_last_activity = Column(DateTime)
    """Time of the last activity of the user in the session."""



