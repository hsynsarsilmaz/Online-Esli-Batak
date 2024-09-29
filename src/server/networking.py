import websockets
import json

from src.common.common import *
from src.server.game import Game


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


async def connectClient(websocket: websockets.WebSocketServerProtocol, game: Game):
    myId = len(game.connectedClients)
    game.connectedClients.append(websocket)
    printPlayers(game.connectedClients)

    await websocket.send(json.dumps({"Type": ReqType.CONNECT.value, "Data": myId}))

    if myId == 3:
        print("All players connected, starting game...")
        await broadcast(
            {
                "Type": ReqType.START.value,
                "Data": {"cards": game.cards, "starterId": game.bidding.starter},
            },
            game.connectedClients,
        )

    return myId
