import asyncio
import websockets
import sys
import json
from src.common.common import *
from src.server.networking import *
from src.server.game import *

games = []


async def handleClient(websocket: websockets.WebSocketServerProtocol, path: str):
    myId = await connectClient(websocket, games[0])

    try:
        async for message in websocket:
            data = json.loads(message)

            if data["Type"] == ReqType.MAKEBID.value:
                await processBid(myId, games[0], data)

            if data["Type"] == ReqType.PLAYCARD.value:
                await playTurn(myId, games[0], data)

    except websockets.ConnectionClosed:
        print("Client disconnected")

    except Exception as e:
        print(f"An error occurred:\n{e}")

    finally:
        games[0].connectedClients[myId] = None


async def main():
    games.append(Game())
    dealCards(games[0].cards)
    server = None
    try:
        server = await websockets.serve(handleClient, IP, PORT)
        print("Online Eşli Batak Server has started...")
        print(f"Server ip address: {IP}\nPort: {PORT}\n")
        printPlayers(games[0].connectedClients)
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
