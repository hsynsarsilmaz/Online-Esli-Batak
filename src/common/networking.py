import enum
import json
import websockets

IP = "localhost"
PORT = 7777
URI = f"ws://{IP}:{PORT}"


class ReqType(enum.Enum):
    CONNECT = 0
    DISCONNECT = 1
    START = 2
    BIDSKIP = 3
    GAMESTART = 4
    PLAYCARD = 5
    PLAYTURN = 6


async def sendRequest(websocket: websockets.WebSocketClientProtocol, request: dict):
    await websocket.send(json.dumps(request))
