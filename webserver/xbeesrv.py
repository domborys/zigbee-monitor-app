import asyncio, json
from asyncio.streams import StreamReader, StreamWriter
from typing import Union

from fastapi.exceptions import HTTPException
from starlette.websockets import WebSocket, WebSocketDisconnect
from . import config, pydmodels

class XBeeServerError(Exception):
    pass

class MessageParseError(Exception):
    pass

def unify_exceptions(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except XBeeServerError as err:
            raise err
        except Exception as err:
            raise XBeeServerError(err)
    return wrapper

@unify_exceptions
async def discover_network() -> pydmodels.DiscoveryResult:
    request = {"type":"request", "name":"discover"}
    response = await request_response(request)
    return pydmodels.DiscoveryResult.parse_obj(response["data"])

@unify_exceptions
async def send_b64_data(address64 : str, message : str) -> pydmodels.XBeeMessageResult:
    request = {"type":"request", "name":"send", "data":{"address64":address64, "message":message}}
    response = await request_response(request)
    return pydmodels.XBeeMessageResult(status=response["status"], message=response.get("message"))

@unify_exceptions
async def at_command(
        command_type: str, 
        command: Union[pydmodels.AtCommandGetExecute, pydmodels.AtCommandSet]
    ) -> pydmodels.AtCommandResult:
    valid_command_types = ["get_parameter", "set_parameter", "execute_command"]
    if command_type not in valid_command_types:
        raise HTTPException(status_code=400, detail=f"Invalid command_type ({command_type})")
    request = {"type":"request", "name":command_type, "data":{
        "address64":command.address64,
        "at_command": command.at_command,
        "value": command.value,
        "apply_changes": command.apply_changes
    }}
    response = await request_response(request)
    return make_at_command_response(response)

@unify_exceptions
async def wait(time : float) -> pydmodels.XBeeWaitingResult:
    request = {"type":"request", "name":"wait", "data":{"time":time}}
    response = await request_response(request)
    return pydmodels.XBeeWaitingResult(time=time, status=response["status"], message=response.get("message"))

async def request_response(request : dict) -> dict:
    return await asyncio.wait_for(request_response_no_timeout(request), timeout=config.DEVICE_TIMEOUT)

async def request_response_no_timeout(request : dict) -> dict:
    reader, writer = await asyncio.open_connection(
        config.XBEE_IP_ADDRESS, config.XBEE_PORT_REQUEST)
    request_json = encode_command(request)
    writer.write(request_json)
    await writer.drain()
    response_json = await reader.readline()
    response_dict = decode_command(response_json)
    writer.close()
    await writer.wait_closed()
    return response_dict
    
def encode_command(command : dict) -> bytes:
    return (json.dumps(command) + "\n").encode()

def decode_command(command_bytes : bytes) -> dict:
    try:
        command_str = command_bytes.decode()
        pos = command_str.find('\n')
        if pos == -1:
            raise MessageParseError("The XBee server response was not ended with a newline.")
        command_json = command_str[:pos]
        return json.loads(command_json)
    except Exception as err:
        raise MessageParseError(f"Invalid response from the XBee device server. Root cause: {err}")

def make_at_command_response(xbee_response) -> pydmodels.AtCommandResult:
    if xbee_response["status"] == "ok":
        return pydmodels.AtCommandResult(status="ok", result=xbee_response["data"]["result"])
    else:
        return pydmodels.AtCommandResult(status="error", error=xbee_response["message"])

class WebsocketMessageSender:
    def __init__(self, websocket : WebSocket):
        self.websocket = websocket

    async def run(self):
        await self.websocket.accept()
        self.send_messages_task = asyncio.create_task(self.send_messages())
        await self.receive_messages()

    async def receive_messages(self):
        try:
            while True:
                await self.websocket.receive_text()
        except WebSocketDisconnect as err:
            self.send_messages_task.cancel()
            print(f"Socket disconnected ({err}).")

    async def send_messages(self):
        reader, writer = await asyncio.open_connection(
            config.XBEE_IP_ADDRESS, config.XBEE_PORT_NOTIFY)
        try:
            await self.send_messages_loop(reader)
        except asyncio.CancelledError:
            print("Sending task cancelled.")
            raise
        finally:
            writer.close()
            await writer.wait_closed()
            await self.close_websocket()

    async def send_messages_loop(self, reader : StreamReader):
        while True:
            await self.send_one_message(reader)

    async def send_one_message(self, reader : StreamReader):
        try:
            response_json = await reader.readline()
            response_dict = decode_command(response_json)
            websocket_message = {'type':'received', 'address64':response_dict['data']['address64'], 'message':response_dict['data']['message']}
            await self.websocket.send_json(websocket_message)
        except MessageParseError:
            pass
    
    async def close_websocket(self):
        await self.websocket.close()
        print("Websocket closed by server")

    
