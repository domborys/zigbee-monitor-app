from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import FastAPI, WebSocket, Depends, HTTPException, status, Response, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from pydantic import BaseModel
from sqlalchemy.orm import Session
import asyncio
import xbeesrv, config, dbmodels, pydmodels, dbsrv
from database import SessionLocal, engine

SECRET_KEY = "be6bae19960dae668c63c7259f1621f73760ea3c47bffeaa2bdc2c16e8969e31"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

dbmodels.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def decode_token(db : Session, token : str) -> dbmodels.User:
    db_user = dbsrv.get_user_by_username(db, token)
    return db_user

async def get_current_user(token: str = Depends(oauth2_scheme), db : Session = Depends(get_db)) -> dbmodels.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    db_user = dbsrv.get_user_by_username(db, username)
    if db_user is None:
        raise credentials_exception
    return db_user

async def get_current_active_user(current_user: dbmodels.User = Depends(get_current_user)) -> dbmodels.User:
    if current_user.disabled:
        raise HTTPException(status_code=403, detail="User account disabled")
    return current_user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

origins = [
    'http://localhost:8080',
    'http://localhost:8000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageToXBee(BaseModel):
    address64 : str
    text: str

class XBeeWaiting(BaseModel):
    time : float

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/floors", response_model=List[pydmodels.Floor])
def get_all_floors(db: Session = Depends(get_db)):
    return dbsrv.get_all_floors(db)

@app.get("/floors/{floor_id}", response_model=pydmodels.Floor)
def get_floor_by_id(floor_id : int, db: Session = Depends(get_db)):
    floor = dbsrv.get_floor_by_id(db, floor_id)
    if floor is None:
        raise HTTPException(status_code=404, detail="Floor not found")
    return floor

@app.post("/floors", response_model=pydmodels.Floor)
def create_floor(floor: pydmodels.FloorCreate, db: Session = Depends(get_db)):
    return dbsrv.create_floor(db, floor)

@app.put("/floors/{floor_id}", response_model=pydmodels.Floor)
def modify_floor(floor_id: int,floor: pydmodels.FloorCreate, db: Session = Depends(get_db)):
    floor = dbsrv.modify_floor(db, floor_id, floor)
    if floor is None:
        raise HTTPException(status_code=404, detail="Floor not found")
    return floor

@app.delete("/floors/{floor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_floor(floor_id : int, db: Session = Depends(get_db)):
    existed_before = dbsrv.delete_floor(db, floor_id)
    if not existed_before:
        raise HTTPException(status_code=404, detail="Floor not found")

@app.get("/floors/{floor_id}/image", response_class=Response)
def get_floor_by_id(floor_id : int, db: Session = Depends(get_db)):
    db_floor = dbsrv.get_floor_by_id(db, floor_id)
    if db_floor is None:
        raise HTTPException(status_code=404, detail="Floor not found")
    if db_floor.image is None:
        raise HTTPException(status_code=404, detail="Floor image not found")
    return Response(content=db_floor.image, media_type=db_floor.image_media_type)

@app.put("/floors/{floor_id}/image", response_class=Response, status_code=status.HTTP_204_NO_CONTENT)
async def get_floor_by_id(floor_id : int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    await dbsrv.set_floor_image(db, floor_id, file)
    

@app.get("/nodes/{node_id}", response_model=pydmodels.Node)
def get_node_by_id(node_id: int, db: Session = Depends(get_db)):
    node = dbsrv.get_node_by_id(db, node_id)
    if node is None:
        raise HTTPException(status_code=404, detail="Node not found")
    return node

@app.post("/nodes", response_model=pydmodels.Node)
def create_node(node: pydmodels.NodeCreate, db: Session = Depends(get_db)):
    return dbsrv.create_node(db, node)

@app.get("/users", response_model=List[pydmodels.User])
def get_users(db: Session = Depends(get_db)):
    return dbsrv.get_all_users(db)

@app.get("/users/me", response_model=pydmodels.User)
async def get_user_me(current_user: dbmodels.User = Depends(get_current_active_user)):
    return current_user

@app.get("/user/{user_id}", response_model=pydmodels.User)
def get_users(user_id: int, db: Session = Depends(get_db)):
    return dbsrv.get_user_by_id(db, user_id)

@app.post("/user", response_model=pydmodels.User)
def create_user(user: pydmodels.UserCreate, db: Session = Depends(get_db)):
    return dbsrv.create_user(db, user)



@app.put("/user/{user_id}", response_model=pydmodels.User)
def modify_user(user_id: int, user: pydmodels.UserModify, db: Session = Depends(get_db)):
    db_user = dbsrv.modify_user(db, user_id, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User")
    return db_user

@app.delete("/user/{user_id}", response_class=Response,  status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    existed_before = dbsrv.delete_user(db, user_id)
    if not existed_before:
        raise HTTPException(status_code=404, detail="User not found")

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = dbsrv.authenticate_user(db, form_data.username, form_data.password)
    if db_user is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/network-discovery")
async def discover_network():
    return await xbeesrv.discover_network()

@app.post("/xbee-message")
async def send_message(message : MessageToXBee):
    return await xbeesrv.send_text_data(address64=message.address64, text=message.text)

@app.post("/xbee-wait")
async def send_message(waiting : XBeeWaiting):
    return await xbeesrv.wait(waiting.time)

@app.websocket("/message-socket")
async def message_websocket(websocket : WebSocket):
    async def websocket_receive(websocket : WebSocket):
        while True:
            request = await websocket.receive_json()
            await xbeesrv.send_b64_data(address64=request['address64'], message=request['message'])
    await websocket.accept()
    asyncio.create_task(websocket_receive(websocket))
    reader, writer = await asyncio.open_connection(
        config.XBEE_IP_ADDRESS, config.XBEE_PORT_NOTIFY)
    while True:
        response_json = await reader.readline()
        response_dict = xbeesrv.decode_command(response_json)
        websocket_message = {'type':'received', 'address64':response_dict['data']['address64'], 'message':response_dict['data']['message']}
        await websocket.send_json(websocket_message)
