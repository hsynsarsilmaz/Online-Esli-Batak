import websockets
import json

from ..common.common import *


async def broadcast(request: dict, connectedClients: list):
    for player in connectedClients:
        if player != None:
            await player.send(json.dumps(request))


def printPlayers(connectedClients: list):
    print("Players:")
    connectedCount = len(connectedClients)
    for i in range(connectedCount):
        print(f"Player {i + 1}: Connected")
    for i in range(connectedCount, 4):
        print(f"Player {i + 1}: Waiting")
    print()


async def connectClient(
    websocket: websockets.WebSocketServerProtocol, connectedClients: list, cards: list
):
    myId = len(connectedClients)
    connectedClients.append(websocket)
    printPlayers(connectedClients)

    await websocket.send(json.dumps({"Type": ReqType.CONNECT.value, "Data": myId}))

    if myId == 3:
        print("All players connected, starting game...")
        await broadcast({"Type": ReqType.START.value, "Data": cards}, connectedClients)

    return myId
