import enum
import json
import websockets

IP = "localhost"
PORT = 8765
URI = f"ws://{IP}:{PORT}"

#create an enum  for request types
class ReqType(enum.Enum):
    CONNECT = 0
    DISCONNECT = 1
    START = 2

async def sendRequest(websocket : websockets.WebSocketClientProtocol, request : dict):
    await websocket.send(json.dumps(request))