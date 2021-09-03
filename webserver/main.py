from typing import List
from fastapi import FastAPI, WebSocket, Depends, HTTPException, status, Response, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.orm import Session
import asyncio
import xbeesrv, config, dbmodels, pydmodels, dbsrv
from database import SessionLocal, engine

dbmodels.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

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
