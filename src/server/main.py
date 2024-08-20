import asyncio
import websockets
import sys
import json
from src.common.common import *

from src.server.networking import *
from src.server.gamelogic import *

connectedClients = []
turn = Turn()
cards = []
points = [0, 0]


async def handleClient(websocket: websockets.WebSocketServerProtocol, path: str):
    myId = await connectClient(websocket, connectedClients, cards)

    try:
        async for message in websocket:
            data = json.loads(message)

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
    server = None
    try:
        server = await websockets.serve(handleClient, IP, PORT)
        print("Online Eşli Batak Server has started...")
        print(f"Server ip address: {IP}\nPort: {PORT}\n")
        printPlayers(connectedClients)
        await asyncio.Future()
    except Exception as e:
        print(f"An error occurred, closing server:\n{e}")
    finally:
        if server:
            server.close()
            await server.wait_closed()
            print("Server closed.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server closed by user.")
    except Exception as e:
        print(f"An error occurred:\n{e}")
        sys.exit(1)
