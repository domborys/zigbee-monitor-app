import asyncio, json, base64
import config

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


