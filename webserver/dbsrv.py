from sqlalchemy.orm import Session
import dbmodels, pydmodels
from fastapi import File, UploadFile, HTTPException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_floor_by_id(db: Session, floor_id: int):
    return db.query(dbmodels.Floor).filter(dbmodels.Floor.id == floor_id).first()

def get_all_floors(db: Session):
    return db.query(dbmodels.Floor).order_by(dbmodels.Floor.number.desc()).all()

def create_floor(db: Session, floor: pydmodels.FloorCreate):
    #db_floor = dbmodels.Floor(**floor.dict())
    db_floor = dbmodels.Floor(name=floor.name, number=floor.number, width=floor.width, height=floor.height)
    for node in floor.nodes:
        db_node = dbmodels.Node(name=node.name, address64=node.address64, x=node.x, y=node.y)
        db_floor.nodes.append(db_node)
    db.add(db_floor)
    db.commit()
    db.refresh(db_floor)
    return db_floor

def modify_floor(db: Session, floor_id:int, floor: pydmodels.Floor):
    db_floor = db.query(dbmodels.Floor).get(floor_id)
    if db_floor is None:
        return None
    db_floor.name = floor.name
    db_floor.number = floor.number
    db_floor.width = floor.width
    db_floor.height = floor.height
    delete_nodes_in_floor(floor, db_floor)
    update_nodes_in_floor(floor, db_floor)
    add_nodes_in_floor(floor, db_floor)
    db.commit()
    db.refresh(db_floor)
    return db_floor

def delete_nodes_in_floor(floor: pydmodels.Floor, db_floor: dbmodels.Floor):
    floor_node_ids = [n.id for n in floor.nodes]
    db_floor.nodes[:] = [n for n in db_floor.nodes if n.id in floor_node_ids]

def update_nodes_in_floor(floor: pydmodels.Floor, db_floor: dbmodels.Floor):
    for db_node in db_floor.nodes:
        node = next(n for n in floor.nodes if n.id == db_node.id)
        db_node.name = node.name
        db_node.address64 = node.address64
        db_node.x = node.x
        db_node.y = node.y

def add_nodes_in_floor(floor: pydmodels.Floor, db_floor: dbmodels.Floor):
    for node in floor.nodes:
        if node.id is None:
            db_node = dbmodels.Node(name=node.name, address64=node.address64, x=node.x, y=node.y)
            db_floor.nodes.append(db_node)

def delete_floor(db: Session, floor_id: int):
    db_floor = db.query(dbmodels.Floor).get(floor_id)
    if db_floor is None:
        return False
    db.delete(db_floor)
    db.commit()
    return True

async def set_floor_image(db: Session, floor_id: int, file: UploadFile):
    contents = await file.read()
    db_floor = db.query(dbmodels.Floor).get(floor_id)
    if db_floor is None:
        raise HTTPException(status_code=404, detail="Floor not found")
    db_floor.image = contents
    db_floor.image_media_type = file.content_type
    db.commit()
    db.refresh(db_floor)

def get_node_by_id(db: Session, node_id: int):
    return db.query(dbmodels.Node).filter(dbmodels.Node.id == node_id).first()

def create_node(db: Session, node: pydmodels.NodeCreate):
    db_node = dbmodels.Node(**node.dict())
    db.add(db_node)
    db.commit()
    db.refresh(db_node)
    return db_node

def get_all_users(db: Session):
    return db.query(dbmodels.User).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(dbmodels.User).filter(dbmodels.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(dbmodels.User).filter(dbmodels.User.username == username).first()

def create_user(db: Session, user: pydmodels.UserCreate):
    db_user = dbmodels.User(username=user.username, role=user.role, disabled=user.disabled)
    db_user.password_hash = pwd_context.hash(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def modify_user(db: Session, user_id: int, user: pydmodels.UserModify):
    db_user = db.query(dbmodels.User).get(user_id)
    if db_user is None:
        return None
    db_user.username = user.username
    db_user.role = user.role
    db_user.disabled = user.disabled
    if user.password is not None:
        db_user.password_hash = pwd_context.hash(user.password)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(dbmodels.User).get(user_id)
    if db_user is None:
        return False
    db.delete(db_user)
    db.commit()
    return True

def authenticate_user(db: Session, username: str, password: str):
    db_user = get_user_by_username(db, username)
    if db_user is None:
        return None
    if not pwd_context.verify(password, db_user.password_hash):
        return None
    return db_user



