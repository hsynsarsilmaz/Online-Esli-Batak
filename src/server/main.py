import asyncio
import websockets
import json
import sys

from ..common.networking import * 

connectedClients = []
for i in range(4):
    connectedClients.append({
        "socket" : None,
        "id" : i + 1
    })
clientCounter = 0

async def handleClient(websocket: websockets.WebSocketServerProtocol, path: str):
    myId = clientCounter
    saveClient(websocket)
    printPlayers()

    if(myId == 3):
        print("All players connected, starting game...")
        await broadcast({"Type" : ReqType.START.value, "Data" : None})
    
    try:
        async for data in websocket:
            print("Received from client:", data)
    
    except websockets.ConnectionClosed:
        print("Client disconnected")

    except Exception as e:
        print(f"An error occurred:\n{e}")

    finally:
        connectedClients[myId]["socket"] = None

async def broadcast(request : dict):
    for player in connectedClients:
        if player["socket"] != None:
            await sendRequest(player["socket"], request)


def saveClient(websocket):
    global clientCounter
    connectedClients[clientCounter]["socket"] = websocket
    clientCounter += 1

def printPlayers():
    print("Players:")
    for player in connectedClients:
        if player["socket"] == None:
            print(f"Player {player['id']}: Waiting for connection")
        else:
            print(f"Player {player['id']}: Connected")
    print()


async def main():
    try:
        async with websockets.serve(handleClient, IP, PORT):
            print("Online Eşli Batak Server has started...")
            print(f"Server ip address: {IP}\nPort: {PORT}\n")
            printPlayers()
            await asyncio.Future() 
    except Exception as e:
        print(f"An error occurred, closing server:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
