import asyncio
import websockets
import sys
import json
from src.common.common import *
from src.server.game import *

games = []


async def handleClient(websocket: websockets.WebSocketServerProtocol, path: str):
    myId = await games[0].connectClient(websocket)

    try:
        async for message in websocket:
            data = json.loads(message)

            if data["Type"] == ReqType.MAKEBID.value:
                await games[0].processBid(myId, data)

            if data["Type"] == ReqType.PLAYCARD.value:
                await games[0].playTurn(myId, data)

    except websockets.ConnectionClosed:
        print("Client disconnected")

    except Exception as e:
        print(f"An error occurred:\n{e}")

    finally:
        games[0].connectedClients[myId] = None


async def main():
    games.append(Game())
    server = None
    try:
        server = await websockets.serve(handleClient, IP, PORT)
        print("Online Eşli Batak Server has started...")
        print(f"Server ip address: {IP}\nPort: {PORT}\n")
        games[0].printPlayers()
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
