from datetime import datetime, timedelta
from typing import List
from sqlalchemy.orm import Session
import dbmodels, pydmodels
from fastapi import File, UploadFile, HTTPException
from passlib.context import CryptContext
import secrets
import config
from pwdcontext import pwd_context

def get_floor_by_id(db: Session, floor_id: int):
    return db.query(dbmodels.Floor).filter(dbmodels.Floor.id == floor_id).first()

def get_all_floors(db: Session):
    return db.query(dbmodels.Floor).order_by(dbmodels.Floor.number.desc()).all()

def create_floor(db: Session, floor: pydmodels.FloorCreate):
    #db_floor = dbmodels.Floor(**floor.dict())
    db_floor = dbmodels.Floor(name=floor.name, number=floor.number, width=floor.width, height=floor.height)
    for node in floor.nodes:
        #db_node = dbmodels.Node(name=node.name, address64=node.address64, x=node.x, y=node.y)
        db_node = make_db_node(node)
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
        db_node = modify_db_node(node, db_node)
        # db_node.name = node.name
        # db_node.address64 = node.address64
        # db_node.x = node.x
        # db_node.y = node.y

def add_nodes_in_floor(floor: pydmodels.Floor, db_floor: dbmodels.Floor):
    for node in floor.nodes:
        if node.id is None:
            #db_node = dbmodels.Node(name=node.name, address64=node.address64, x=node.x, y=node.y)
            db_node = make_db_node(node)
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

def make_db_node(node: pydmodels.Node) -> dbmodels.Node:
    db_node = dbmodels.Node(name=node.name, address64=node.address64, x=node.x, y=node.y)
    for rc in node.reading_configs:
        db_rc = make_db_rc(rc)
        db_node.reading_configs.append(db_rc)
    return db_node

def modify_db_node(node: pydmodels.Node, db_node: dbmodels.Node):
    db_node.name = node.name
    db_node.address64 = node.address64
    db_node.x = node.x
    db_node.y = node.y
    delete_rcs_in_node(node, db_node)
    update_rcs_in_node(node, db_node)
    add_rcs_in_node(node, db_node)

def delete_rcs_in_node(node: pydmodels.Node, db_node: dbmodels.Node):
    node_rc_ids = [rc.id for rc in node.reading_configs]
    db_node.reading_configs[:] = [rc for rc in db_node.reading_configs if rc.id in node_rc_ids]

def update_rcs_in_node(node: pydmodels.Node, db_node: dbmodels.Node):
    for db_rc in db_node.reading_configs:
        rc = next(rc for rc in node.reading_configs if rc.id == db_rc.id)
        update_db_rc(rc, db_rc)

def add_rcs_in_node(node: pydmodels.Node, db_node: dbmodels.Node):
    for rc in node.reading_configs:
        if rc.id is None:
            db_rc = make_db_rc(rc)
            db_node.reading_configs.append(db_rc)


def make_db_rc(rc: pydmodels.ReadingConfigInNode) -> dbmodels.ReadingConfig:
    db_rc = dbmodels.ReadingConfig(
        name = rc.name,
        mode = rc.mode,
        refresh_period = rc.refresh_period,
        message_prefix = rc.message_prefix,
        message_to_send = rc.message_to_send,
        at_command = rc.at_command,
        at_command_data = rc.at_command_data,
        at_command_result_format = rc.at_command_result_format
    )
    return db_rc

def update_db_rc(rc: pydmodels.ReadingConfigInNode, db_rc: dbmodels.ReadingConfig):
    db_rc.name = rc.name
    db_rc.mode = rc.mode
    db_rc.refresh_period = rc.refresh_period
    db_rc.message_prefix = rc.message_prefix
    db_rc.message_to_send = rc.message_to_send
    db_rc.at_command = rc.at_command
    db_rc.at_command_data = rc.at_command_data
    db_rc.at_command_result_format = rc.at_command_result_format

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

def change_password(db: Session, password_change: pydmodels.PasswordChange, username: str):
    db_user = get_user_by_username(db, username)
    if not pwd_context.verify(password_change.old_password, db_user.password_hash):
        raise HTTPException(status_code=403, detail="Incorrect old password")
    db_user.password_hash = pwd_context.hash(password_change.new_password)
    db.commit()
    db.refresh(db_user)
    return db_user
    

def authenticate_user(db: Session, username: str, password: str):
    db_user = get_user_by_username(db, username)
    if db_user is None:
        return None
    if not pwd_context.verify(password, db_user.password_hash):
        return None
    delete_expired_user_sessions(db)
    user_session = start_user_session(db, db_user)
    return user_session

def get_all_user_sessions(db: Session) -> List[dbmodels.UserSession]:
    return db.query(dbmodels.UserSession).all()

def start_user_session(db: Session, db_user: dbmodels.User) -> dbmodels.UserSession:
    session_id = secrets.token_urlsafe(32)
    time_now = datetime.now()
    user_session = dbmodels.UserSession(session_id=session_id, user_id=db_user.id, time_started=time_now, time_last_activity=time_now)
    db.add(user_session)
    db.commit()
    db.refresh(user_session)
    return user_session

def end_user_session(db: Session, session_id: str):
    user_session = db.query(dbmodels.UserSession).filter(dbmodels.UserSession.session_id == session_id).first()
    db.delete(user_session)
    db.commit()

def end_all_user_sessions(db: Session, db_user: dbmodels.User):
    del db_user.sessions[:]
    db.commit()

def delete_expired_user_sessions(db: Session):
    time_newest_expired = datetime.now() - timedelta(seconds=config.SESSION_IDLE_TIME)
    db.query(dbmodels.UserSession).filter(dbmodels.UserSession.time_last_activity < time_newest_expired).delete()
    db.commit()

def delete_all_user_sessions(db: Session):
    db.query(dbmodels.UserSession).delete()
    db.commit()

def get_session_by_session_id(db: Session, session_id: str):
    return db.query(dbmodels.UserSession).filter(dbmodels.UserSession.session_id == session_id).first()

def get_session_and_refresh(db: Session, session_id: str):
    user_session = get_session_by_session_id(db, session_id)
    if user_session is None:
        return None
    time_now = datetime.now()
    if time_now - user_session.time_last_activity > timedelta(seconds=config.SESSION_IDLE_TIME):
        db.delete(user_session)
        db.commit()
        return None
    user_session.time_last_activity = time_now
    db.commit()
    db.refresh(user_session)
    return user_session




