"""Functions for communication with the coordinator handler."""

import asyncio, json
from asyncio.streams import StreamReader, StreamWriter
from functools import wraps
from typing import Union

from fastapi.exceptions import HTTPException
from starlette.websockets import WebSocket, WebSocketDisconnect
from . import config, pydmodels

class XBeeServerError(Exception):
    """An error raised by the functions in the module whenever the communication with the coordinator handler fails."""
    pass

class MessageParseError(Exception):
    """An error raised when the message received from the coordinator handler is invalid."""
    pass

def unify_exceptions(func):
    """Decorator which catches all the exceptions and re-raises them as :class:`~webserver.xbeesrv.MessageParseError`"""
    @wraps(func)
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
    """Makes a discovery request to the coordinator handler.
    
    Returns:
        ZigBee network discovery results received from the coordinator handler.

    Raises:
        XBeeServerError: when an error occurs while communicating with the coordinator handler.
    """
    request = {"type":"request", "name":"discover"}
    response = await request_response(request)
    return pydmodels.DiscoveryResult.parse_obj(response["data"])

@unify_exceptions
async def send_b64_data(address64 : str, message : str) -> pydmodels.XBeeMessageResult:
    """Makes a request to the coordinator handler to send a message to the given node in the ZigBee network.

    Args:
        address64: 64-bit addres of the node as hexadecimal string.
        message: base64-encoded message to send.
    
    Returns:
        An object describing if the message was successfuly sent.

    Raises:
        XBeeServerError: when an error occurs while communicating with the coordinator handler.
    """
    request = {"type":"request", "name":"send", "data":{"address64":address64, "message":message}}
    response = await request_response(request)
    return pydmodels.XBeeMessageResult(status=response["status"], message=response.get("message"))

@unify_exceptions
async def at_command(
        command_type: str, 
        command: Union[pydmodels.AtCommandGetExecute, pydmodels.AtCommandSet]
    ) -> pydmodels.AtCommandResult:
    """Makes a request to the coordinator handler to send an AT command to a device.
    
    Args:
        command_type: type of the AT command. The allowed names are
            - `get_parameter` to read a parameter value
            - `set_parameter` to set a parameter value
            - `execute_command` to execute a command unrelated to any parameter.
        command: object describing a the command to send.

    Returns:
        An object describing if the AT command was successfuly sent.
        When `command_type` equals get_parameter and the command was successfully sent it also contains the result of the command.

    Raises:
        XBeeServerError: when an error occurs while communicating with the coordinator handler.
    """
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
    return _make_at_command_response(response)

@unify_exceptions
async def wait(time : float) -> pydmodels.XBeeWaitingResult:
    """Makes a request to the coordinator handler to wait for some time. Used for testing purposes.
    
    Args:
        time: time the coordinator should wait. If the time is too long, a timeout may occur.

    Returns:
        An object describing if the request has been successfully executed.

    Raises:
        XBeeServerError: when an error occurs while communicating with the coordinator handler.
    """
    request = {"type":"request", "name":"wait", "data":{"time":time}}
    response = await request_response(request)
    return pydmodels.XBeeWaitingResult(time=time, status=response["status"], message=response.get("message"))

async def request_response(request : dict) -> dict:
    """Makes a request to the coordinator handler and waits for the response.

    Args:
        request: the object which will be sent to the coordinator handler.

    Returns:
        the response of the coordinator handler.

    Raises:
        MessageParseError: when the response from the server is invalid.
        asyncio.TimeoutError: when the time `DEVICE_TIMEOUT` was exceeded.
    
    """
    return await asyncio.wait_for(_request_response_no_timeout(request), timeout=config.DEVICE_TIMEOUT)

async def _request_response_no_timeout(request : dict) -> dict:
    reader, writer = await asyncio.open_connection(
        config.XBEE_IP_ADDRESS, config.XBEE_PORT_REQUEST)
    request_json = _encode_command(request)
    writer.write(request_json)
    await writer.drain()
    response_json = await reader.readline()
    response_dict = _decode_command(response_json)
    writer.close()
    await writer.wait_closed()
    return response_dict
    
def _encode_command(command : dict) -> bytes:
    return (json.dumps(command) + "\n").encode()

def _decode_command(command_bytes : bytes) -> dict:
    try:
        command_str = command_bytes.decode()
        pos = command_str.find('\n')
        if pos == -1:
            raise MessageParseError("The XBee server response was not ended with a newline.")
        command_json = command_str[:pos]
        return json.loads(command_json)
    except Exception as err:
        raise MessageParseError(f"Invalid response from the XBee device server. Root cause: {err}")

def _make_at_command_response(xbee_response) -> pydmodels.AtCommandResult:
    if xbee_response["status"] == "ok":
        return pydmodels.AtCommandResult(status="ok", result=xbee_response["data"]["result"])
    else:
        return pydmodels.AtCommandResult(status="error", error=xbee_response["message"])

class WebsocketMessageSender:
    """Class for receiving notifications from the coordinator handler and sending them to the connected websockets.
    
    Attributes:
        websocket (starlette.websockets.WebSocket): the websocket to which the notifications are sent.
    """

    def __init__(self, websocket : WebSocket):
        """Creates a websocket handler.
        
        Args:
            websocket: the websockets where the messages will be sent.
        """
        self.websocket = websocket

    async def run(self):
        """Starts the sender. The function returns when the socket if closed."""

        await self.websocket.accept()
        self.send_messages_task = asyncio.create_task(self._send_messages())
        await self._receive_messages()

    async def _receive_messages(self):
        try:
            while True:
                await self.websocket.receive_text()
        except WebSocketDisconnect as err:
            self.send_messages_task.cancel()
            print(f"Socket disconnected ({err}).")

    async def _send_messages(self):
        reader, writer = await asyncio.open_connection(
            config.XBEE_IP_ADDRESS, config.XBEE_PORT_NOTIFY)
        try:
            await self._send_messages_loop(reader)
        except asyncio.CancelledError:
            print("Sending task cancelled.")
            raise
        finally:
            writer.close()
            await writer.wait_closed()
            await self._close_websocket()

    async def _send_messages_loop(self, reader : StreamReader):
        while True:
            await self._send_one_message(reader)

    async def _send_one_message(self, reader : StreamReader):
        try:
            response_json = await reader.readline()
            response_dict = _decode_command(response_json)
            websocket_message = {'type':'received', 'address64':response_dict['data']['address64'], 'message':response_dict['data']['message']}
            await self.websocket.send_json(websocket_message)
        except MessageParseError:
            pass
    
    async def _close_websocket(self):
        await self.websocket.close()
        print("Websocket closed by server")

    
