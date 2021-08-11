from sqlalchemy.orm import Session
import dbmodels, pydmodels

def get_floor_by_id(db: Session, floor_id: int):
    return db.query(dbmodels.Floor).filter(dbmodels.Floor.id == floor_id).first()

def get_all_floors(db: Session):
    return db.query(dbmodels.Floor).order_by(dbmodels.Floor.number).all()

def create_floor(db: Session, floor: pydmodels.FloorCreate):
    db_floor = dbmodels.Floor(**floor.dict())
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
    db.commit()
    db.refresh(db_floor)
    return db_floor

def delete_floor(db: Session, floor_id: int):
    db_floor = db.query(dbmodels.Floor).get(floor_id)
    if db_floor is None:
        return False
    db.delete(db_floor)
    db.commit()
    return True

def get_node_by_id(db: Session, node_id: int):
    return db.query(dbmodels.Node).filter(dbmodels.Node.id == node_id).first()

def create_node(db: Session, node: pydmodels.NodeCreate):
    db_node = dbmodels.Node(**node.dict())
    db.add(db_node)
    db.commit()
    db.refresh(db_node)
    return db_node

