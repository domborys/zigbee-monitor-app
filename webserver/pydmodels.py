from typing import List, Optional
from pydantic import BaseModel

class NodeBase(BaseModel):
    name: str
    address64: str
    x: float
    y: float
    

class NodeCreate(NodeBase):
    floor_id: int

class Node(NodeBase):
    id: int
    floor_id: int
    class Config:
        orm_mode = True

class NodeInFloor(NodeBase):
    id: Optional[int]
    floor_id: Optional[int]
    class Config:
        orm_mode = True


class FloorBase(BaseModel):
    name : str
    number: int
    width: float
    height: float
    nodes: List[NodeInFloor] = [] 

class FloorCreate(FloorBase):
    pass

class Floor(FloorBase):
    id: int
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    role: str
    disabled: bool

class UserCreate(UserBase):
    password: str

class UserModify(UserBase):
    password: Optional[str]

class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True

class AtCommandBase(BaseModel):
    address64: str
    at_command: str
    apply_changes: bool = True

class AtCommandSet(AtCommandBase):
    value: str

class AtCommandGetExecute(AtCommandBase):
    value: Optional[str]

class AtCommandWithType(AtCommandBase):
    command_type: str
    value: Optional[str]

class AtCommandResult(BaseModel):
    status: str
    result: Optional[str]
    error: Optional[str]
