import asyncio
import websockets
import sys
import json
from ..common.common import *

from .networking import *
from .gamelogic import *

connectedClients = []
turn = Turn()
cards = []
points = [0, 0]


async def handleClient(websocket: websockets.WebSocketServerProtocol, path: str):
    myId = await connectClient(websocket, connectedClients, cards)

    try:
        async for message in websocket:
            data = json.loads(message)

            # Temporary
            if data["Type"] == ReqType.BIDSKIP.value:
                await skipBid(myId, connectedClients, turn, data)

            if data["Type"] == ReqType.PLAYCARD.value:
                await playTurn(myId, connectedClients, turn, data, points)

    except websockets.ConnectionClosed:
        print("Client disconnected")

    except Exception as e:
        print(f"An error occurred:\n{e}")

    finally:
        connectedClients[myId] = None


async def main():
    dealCards(cards)
    try:
        async with websockets.serve(handleClient, IP, PORT):
            print("Online Eşli Batak Server has started...")
            print(f"Server ip address: {IP}\nPort: {PORT}\n")
            printPlayers(connectedClients)
            await asyncio.Future()
    except Exception as e:
        print(f"An error occurred, closing server:\n{e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
