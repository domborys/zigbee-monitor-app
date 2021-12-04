from asyncio.streams import StreamReader
from typing import List, Optional
from fastapi import FastAPI, WebSocket, Depends, HTTPException, status, Response, UploadFile, File
from fastapi.params import Cookie
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm, APIKeyCookie

from pydantic import BaseModel
from sqlalchemy.orm import Session
import asyncio, secrets

from sqlalchemy.sql.functions import user
from starlette.requests import Request
from starlette.responses import RedirectResponse
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
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

cookie_sid = APIKeyCookie(name="SID")

async def get_current_session(request: Request, sid: str = Depends(cookie_sid), db : Session = Depends(get_db)) -> dbmodels.UserSession:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    db_session = dbsrv.get_session_and_refresh(db, sid)
    if db_session is None:
        raise credentials_exception
    # check_csrf_token(request)
    return db_session

def check_csrf_token(request: Request):
    csrf_exception =  HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid CSRF token",
    )
    if request.method in ["POST", "PUT", "DELETE", "PATCH"]:
        if not csrf_tokens_equal(request):
            raise csrf_exception

def csrf_tokens_equal(request: Request):
    try:
        cookie_token = request.cookies["XSRF-TOKEN"]
        header_token = request.headers["X-XSRF-TOKEN"]
        return secrets.compare_digest(cookie_token, header_token)
    except KeyError:
        return False

async def get_current_session_ws(websocket: WebSocket, sid: Optional[str] = Cookie(None, alias="SID"), db : Session = Depends(get_db)) -> dbmodels.UserSession:
    if sid is None:
        print("No SID cookie in websocket")
        return None
    db_session = dbsrv.get_session_and_refresh(db, sid)
    if db_session is None:
        print("No valid session in websocket")
        return None
    return db_session

async def get_current_user(user_session: dbmodels.UserSession = Depends(get_current_session)) -> dbmodels.User:
    return user_session.user

async def get_current_active_user(current_user: dbmodels.User = Depends(get_current_user)) -> dbmodels.User:
    if current_user.disabled:
        raise HTTPException(status_code=403, detail="User account disabled")
    return current_user

async def is_valid_user(user_session: dbmodels.UserSession = Depends(get_current_session)):
    current_user: dbmodels.User = user_session.user
    if current_user.disabled:
        raise HTTPException(status_code=403, detail="User account disabled")

async def is_valid_admin(user_session: dbmodels.UserSession = Depends(get_current_session)):
    current_user: dbmodels.User = user_session.user
    if current_user.disabled:
        raise HTTPException(status_code=403, detail="User account disabled")
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Operation not allowed")


@app.get("/")
async def root():
    return RedirectResponse("/static/index.html")

@app.get("/floors", response_model=List[pydmodels.Floor], dependencies=[Depends(is_valid_user)])
def get_all_floors(db: Session = Depends(get_db)):
    return dbsrv.get_all_floors(db)

@app.get("/floors/{floor_id}", response_model=pydmodels.Floor, dependencies=[Depends(is_valid_user)])
def get_floor_by_id(floor_id : int, db: Session = Depends(get_db)):
    floor = dbsrv.get_floor_by_id(db, floor_id)
    if floor is None:
        raise HTTPException(status_code=404, detail="Floor not found")
    return floor

@app.post("/floors", response_model=pydmodels.Floor, dependencies=[Depends(is_valid_user)])
def create_floor(floor: pydmodels.FloorCreate, db: Session = Depends(get_db)):
    return dbsrv.create_floor(db, floor)

@app.put("/floors/{floor_id}", response_model=pydmodels.Floor, dependencies=[Depends(is_valid_user)])
def modify_floor(floor_id: int,floor: pydmodels.FloorCreate, db: Session = Depends(get_db)):
    floor = dbsrv.modify_floor(db, floor_id, floor)
    if floor is None:
        raise HTTPException(status_code=404, detail="Floor not found")
    return floor

@app.delete("/floors/{floor_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(is_valid_user)])
def delete_floor(floor_id : int, db: Session = Depends(get_db)):
    existed_before = dbsrv.delete_floor(db, floor_id)
    if not existed_before:
        raise HTTPException(status_code=404, detail="Floor not found")

@app.get("/floors/{floor_id}/image", response_class=Response, dependencies=[Depends(is_valid_user)])
def get_floor_by_id(floor_id : int, db: Session = Depends(get_db)):
    db_floor = dbsrv.get_floor_by_id(db, floor_id)
    if db_floor is None:
        raise HTTPException(status_code=404, detail="Floor not found")
    if db_floor.image is None:
        raise HTTPException(status_code=404, detail="Floor image not found")
    return Response(content=db_floor.image, media_type=db_floor.image_media_type)

@app.put("/floors/{floor_id}/image", response_class=Response, status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(is_valid_user)])
async def get_floor_by_id(floor_id : int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    await dbsrv.set_floor_image(db, floor_id, file)
    

@app.get("/nodes/{node_id}", response_model=pydmodels.Node, dependencies=[Depends(is_valid_user)])
def get_node_by_id(node_id: int, db: Session = Depends(get_db)):
    node = dbsrv.get_node_by_id(db, node_id)
    if node is None:
        raise HTTPException(status_code=404, detail="Node not found")
    return node

@app.post("/nodes", response_model=pydmodels.Node, dependencies=[Depends(is_valid_user)])
def create_node(node: pydmodels.NodeCreate, db: Session = Depends(get_db)):
    return dbsrv.create_node(db, node)

@app.get("/users", response_model=List[pydmodels.User], dependencies=[Depends(is_valid_admin)])
def get_users(db: Session = Depends(get_db)):
    return dbsrv.get_all_users(db)

@app.get("/users/me", response_model=pydmodels.User)
async def get_user_me(current_user: dbmodels.User = Depends(get_current_active_user)):
    return current_user

@app.get("/user/{user_id}", response_model=pydmodels.User, dependencies=[Depends(is_valid_admin)])
def get_users(user_id: int, db: Session = Depends(get_db)):
    return dbsrv.get_user_by_id(db, user_id)

@app.post("/users", response_model=pydmodels.User, dependencies=[Depends(is_valid_admin)])
def create_user(user: pydmodels.UserCreate, db: Session = Depends(get_db)):
    return dbsrv.create_user(db, user)

@app.put("/users/{user_id}", response_model=pydmodels.User, dependencies=[Depends(is_valid_admin)])
def modify_user(user_id: int, user: pydmodels.UserModify, db: Session = Depends(get_db)):
    db_user = dbsrv.modify_user(db, user_id, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User")
    return db_user

@app.delete("/users/{user_id}", response_class=Response,  status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(is_valid_admin)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    existed_before = dbsrv.delete_user(db, user_id)
    if not existed_before:
        raise HTTPException(status_code=404, detail="User not found")

@app.post("/password-change", response_model=pydmodels.User)
def change_password(password_change: pydmodels.PasswordChange, db: Session = Depends(get_db), current_user: dbmodels.User = Depends(get_current_active_user)):
    return dbsrv.change_password(db, password_change, current_user.username)

#TODO Remove
@app.post("/token")
async def login_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_session = dbsrv.authenticate_user(db, form_data.username, form_data.password)
    if db_session is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return {"access_token": db_session.session_id, "token_type": "bearer"}

@app.post("/login")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db), response_class=Response,  status_code=status.HTTP_204_NO_CONTENT):
    db_session = dbsrv.authenticate_user(db, form_data.username, form_data.password)
    if db_session is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    response.set_cookie("SID", db_session.session_id, httponly=True)
    response.set_cookie("XSRF-TOKEN", secrets.token_urlsafe(32))

@app.post("/logout", response_class=Response,  status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response, db: Session = Depends(get_db), user_session: dbmodels.UserSession = Depends(get_current_session)):
    response.delete_cookie("SID")
    dbsrv.end_user_session(db, user_session.session_id)

@app.post("/logout-all", response_class=Response,  status_code=status.HTTP_204_NO_CONTENT)
def logout_all(response: Response, db: Session = Depends(get_db), user_session: dbmodels.UserSession = Depends(get_current_session)):
    response.delete_cookie("SID")
    dbsrv.end_all_user_sessions(db, user_session.user)

@app.get("/user-sessions", response_model=List[pydmodels.UserSession], dependencies=[Depends(is_valid_admin)])
def get_users(db: Session = Depends(get_db)):
    return dbsrv.get_all_user_sessions(db)

@app.delete("/user-sessions", response_class=Response,  status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(is_valid_admin)])
def get_users(db: Session = Depends(get_db)):
    dbsrv.delete_all_user_sessions(db)

@app.exception_handler(xbeesrv.XBeeServerError)
def handle_xbee_error(request: Request, err: xbeesrv.XBeeServerError):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Error with XBee device connection {err}"},
    )

@app.get("/network-discovery", response_model=pydmodels.DiscoveryResult, dependencies=[Depends(is_valid_user)])
async def discover_network():
    return await xbeesrv.discover_network()

@app.post("/xbee-message", response_model=pydmodels.XBeeMessageResult, dependencies=[Depends(is_valid_user)])
async def send_message(message : pydmodels.MessageToXBee):
    return await xbeesrv.send_b64_data(address64=message.address64, message=message.message)

@app.post("/xbee-wait", response_model=pydmodels.XBeeWaitingResult, dependencies=[Depends(is_valid_user)])
async def send_message(waiting : pydmodels.XBeeWaiting):
    return await xbeesrv.wait(waiting.time)

@app.post("/xbee-get-parameter", response_model=pydmodels.AtCommandResult, dependencies=[Depends(is_valid_user)])
async def get_parameter(command_data : pydmodels.AtCommandGetExecute):
    return await xbeesrv.at_command("get_parameter", command_data)

@app.post("/xbee-set-parameter", response_model=pydmodels.AtCommandResult, dependencies=[Depends(is_valid_user)])
async def set_parameter(command_data : pydmodels.AtCommandSet):
    return await xbeesrv.at_command("set_parameter", command_data)

@app.post("/xbee-execute-command", response_model=pydmodels.AtCommandResult, dependencies=[Depends(is_valid_user)])
async def execute_command(command_data : pydmodels.AtCommandGetExecute):
    return await xbeesrv.at_command("execute_command", command_data)

@app.post("/xbee-at-command", response_model=pydmodels.AtCommandResult, dependencies=[Depends(is_valid_user)])
async def execute_command(command_data : pydmodels.AtCommandWithType):
    return await xbeesrv.at_command(command_data.command_type, command_data)

@app.websocket("/message-socket")
async def message_websocket(websocket : WebSocket, user_session : Optional[dbmodels.UserSession] = Depends(get_current_session_ws)):
    if user_session is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    sender = xbeesrv.WebsocketMessageSender(websocket)
    await sender.run()