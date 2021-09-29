import asyncio, json, base64
from typing import Union

from fastapi.exceptions import HTTPException
import config, pydmodels

class XBeeServerError(Exception):
    pass

async def discover_network():
    request = {"type":"request", "name":"discover"}
    response = await request_response(request)
    return response["data"]

async def send_text_data(address64 : str, text : str, output_encoding : str = 'utf-8'):
    message = base64.b64encode(text.encode(output_encoding)).decode()
    request = {"type":"request", "name":"send", "data":{"address64":address64, "message":message}}
    response = await request_response(request)
    return response

async def send_b64_data(address64 : str, message : str):
    request = {"type":"request", "name":"send", "data":{"address64":address64, "message":message}}
    response = await request_response(request)
    return response

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

async def wait(time : float):
    request = {"type":"request", "name":"wait", "data":{"time":time}}
    return await request_response(request)

async def request_response(request : dict) -> dict:
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
            raise XBeeServerError("The XBee server response was not ended with a newline.")
        command_json = command_str[:pos]
        return json.loads(command_json)
    except Exception as err:
        raise XBeeServerError(f"Invalid response from the XBee device server. Root cause: {err}")

def make_at_command_response(xbee_response) -> pydmodels.AtCommandResult:
    if xbee_response["status"] == "ok":
        return pydmodels.AtCommandResult(status="ok", result=xbee_response["data"]["result"])
    else:
        return pydmodels.AtCommandResult(status="error", error=xbee_response["message"])


