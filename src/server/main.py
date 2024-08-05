import asyncio
import websockets
import json

from ..common.networking import * 

async def handle_client(websocket: websockets.WebSocketServerProtocol, path: str):
    message = json.dumps({"Test": "Hello, client!"})
    await websocket.send(message)
    print("Sent message to client:", message)
    data = await websocket.recv()
    print("Received from client:", data)

async def main():
    async with websockets.serve(handle_client, IP, PORT):
        print(f"Server started on ws://{IP}:{PORT}")
        await asyncio.Future() 

if __name__ == "__main__":
    asyncio.run(main())
