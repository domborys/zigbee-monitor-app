from typing import List
from pydantic import BaseModel

class NodeBase(BaseModel):
    name: str
    address64: str
    x: float
    y: float
    floor_id: int

class NodeCreate(NodeBase):
    pass

class Node(NodeBase):
    id: int

    class Config:
        orm_mode = True


class FloorBase(BaseModel):
    name : str
    number: int
    width: float
    height: float

class FloorCreate(FloorBase):
    pass

class Floor(FloorBase):
    id: int
#    nodes: List[Node] = [] 
    class Config:
        orm_mode = True

