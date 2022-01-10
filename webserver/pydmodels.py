"""Module with Pydantic models for the API requests and responses."""

from typing import List, Optional
from pydantic import BaseModel

class ReadingConfigBase(BaseModel):
    """Base class for ReadingConfig objects."""

    name: str
    """Name of the reading."""

    mode: str
    """The mode of obtaining the reading."""

    refresh_period: Optional[float]
    """The period in which the reading is refreshed."""

    message_prefix: Optional[str]
    """Prefix of the message containing the reading value."""

    message_to_send: Optional[str]
    """The message which will be sent to the device in order to obtain the reading value."""

    at_command: Optional[str]
    """The AT command which will be used for obtaining the reading value."""

    at_command_data: Optional[str]
    """Data for the AT command which will be used for obtaining the reading value."""

    at_command_result_format: Optional[str]
    """Format of the AT command result"""

class ReadingConfigInNode(ReadingConfigBase):
    """ReadingConfig as a part of a Node object."""

    id: Optional[int]
    """Id in the system."""

    node_id: Optional[int]
    """Id of the node the ReadingConfig belongs to."""

    class Config:
        orm_mode = True


class NodeBase(BaseModel):
    """Base class for all Node objects. Node objects describe ZigBee network nodes."""

    name: str
    """Node name."""

    address64: str
    """64-bit address of the node as a hexadecimal string."""

    x: float
    """x coordinate of the node on the map."""

    y: float
    """y coordinate of the node on the map."""

    reading_configs: List[ReadingConfigInNode] = []
    """The readings related to the node."""
    

class NodeCreate(NodeBase):
    """Node schema used when adding a new node to the system."""

    floor_id: int
    """Id of the floor the node belongs to."""

class Node(NodeBase):
    """Node schema used for reading and modyfying the node."""

    id: int
    """Node id."""

    floor_id: int
    """Id of the floor the node belongs to."""

    class Config:
        orm_mode = True

class NodeInFloor(NodeBase):
    """Node schema when the node is part of a Floor object."""

    id: Optional[int]
    """Node id."""

    floor_id: Optional[int]
    """Id of the floor the node belongs to."""

    class Config:
        orm_mode = True


class FloorBase(BaseModel):
    """Base class for a map (floor)."""

    name : str
    """Name of the map."""

    number: int
    """The number used for sorting maps. If the maps are building floors, the number may be equal to floor number."""

    width: float
    """The width of the map."""

    height: float
    """The height of the map."""

    nodes: List[NodeInFloor] = [] 
    """Nodes present on the map."""

class FloorCreate(FloorBase):
    """A schema used for creating nodes."""
    pass

class Floor(FloorBase):
    """A schema used for reading and modifying of the node."""

    id: int
    """Node id."""

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    """Base class for users of the system."""

    username: str
    """User's username."""

    role: str
    """Role of the user. Can be either "user" or "admin"."""

    disabled: bool
    """True if the user is disabled."""

class UserCreate(UserBase):
    """A schema used for adding users to the system."""

    password: str
    """User password in plain text."""

class UserModify(UserBase):
    """A schema used for modifying users in the system."""

    password: Optional[str]
    """New password of the user. Value None means that the password should not be changed."""

class User(UserBase):
    """A schema used for reading users in the system."""

    id: int
    """User's id."""

    class Config:
        orm_mode = True

class PasswordChange(BaseModel):
    """Schema used for changing the password of the user which is currently logged in."""

    old_password: str
    """Old password in plain text."""

    new_password: str
    """New password in plain text."""

class AtCommandBase(BaseModel):
    """Base class for schemas used to send AT commands to the devices in the XBee network."""

    address64: str
    """64-bit address of the device."""

    at_command: str
    """AT command name (2 characters)."""

    apply_changes: bool = True
    """If the changes should be applied."""

class AtCommandSet(AtCommandBase):
    """Schema for AT command which sets a parameter."""

    value: str
    """New parameter value."""

class AtCommandGetExecute(AtCommandBase):
    """Schema for AT command which gets a parameter or executes a command unrelated to any parameter."""

    value: Optional[str]
    """AT command value."""

class AtCommandWithType(AtCommandBase):
    """AT command with the type of the command."""

    command_type: str
    """Type of the command. Allowed values:
    - `get_parameter` to read a parameter value
    - `set_parameter` to set a parameter value
    - `execute_command` to execute a command unrelated to any parameter.
    """

    value: Optional[str]
    """AT command value."""

class AtCommandResult(BaseModel):
    """Schema of the result of AT command request."""

    status: str
    """Describes if the command was successfully sent. Possible values: `error` and `ok`."""

    result: Optional[str]
    """Result of the command. Present if the command was of type get_parameter and `status` is `ok`."""

    error: Optional[str]
    """Error message. Present if `status` is `error`."""

class MessageToXBee(BaseModel):
    """Schema for sending messages to an XBee device."""

    address64 : str
    """64-bit address of the device."""

    message: str
    """Base64-encoded message to send."""

class XBeeWaiting(BaseModel):
    """Schema for sending messages a request to wait for the coordinator handler. Used for testing purposes."""

    time : float
    """The time to wait."""

class XBeeWaitingResult(BaseModel):
    """Schema of the result the waiting request."""

    status : str
    """Describes if the command was successfully executed. Possible values: `error` and `ok`."""

    time : float
    """Time the coordinator handler was supposed to wait."""

    message: Optional[str]
    """Error message. Present if `status` is `error`."""

class DeviceInDiscoveryResult(BaseModel):
    """A device in the list of discovered devices."""

    address64 : str
    """64-bit address of the device."""

    address16 : str
    """16-bit address of the device."""

    id : str
    """Node id of the device (NI parameter)."""

    role : str
    """Role of the device in the network."""

class DiscoveryResult(BaseModel):
    """Schema for the result of discovery request."""

    devices : List[DeviceInDiscoveryResult]
    """List of discovered devices."""

class XBeeMessageResult(BaseModel):
    """Result of a request to send a message to an XBee device."""

    status: str
    """Describes if the message was successfully executed. Possible values: `error` and `ok`."""

    message: Optional[str]
    """Error message. Present if `status` is `error`."""

class UserSession(BaseModel):
    """Schema describing a user's session."""

    id: str
    """Session ID (token)"""

    user_id: Optional[str]
    """User id."""

    class Config:
        orm_mode = True
