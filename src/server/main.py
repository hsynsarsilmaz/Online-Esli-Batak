import asyncio
import websockets
import sys
import random

from ..common.networking import *
from ..common.card import *
from ..common.gamelogic import *

connectedClients = []
for i in range(4):
    connectedClients.append({"socket": None, "id": i + 1})
clientCounter = 0
turn = Turn()
cards = []
points = [0, 0]


def dealCards():
    global cards
    suits = ["H", "S", "D", "C"]
    ranks = [int(n) for n in range(2, 15)]
    for suit in suits:
        for rank in ranks:
            cards.append((suit, rank))
    random.shuffle(cards)


async def handleClient(websocket: websockets.WebSocketServerProtocol, path: str):
    myId = clientCounter
    saveClient(websocket)
    printPlayers()

    await sendRequest(websocket, {"Type": ReqType.CONNECT.value, "Data": myId})

    if myId == 3:
        print("All players connected, starting game...")
        await broadcast({"Type": ReqType.START.value, "Data": cards})

    try:
        async for message in websocket:
            data = json.loads(message)

            if data["Type"] == ReqType.BIDSKIP.value:
                print(f"Player {myId + 1} skipped bidding")
                turn.trump = data["Data"]["trump"]
                await broadcast(
                    {
                        "Type": ReqType.GAMESTART.value,
                        "Data": {
                            "bid": data["Data"]["bid"],
                            "trump": data["Data"]["trump"],
                            "bidder": myId,
                        },
                    }
                )

            if data["Type"] == ReqType.PLAYCARD.value:
                winner = -1
                champion = -1
                turn.playTurn(data["Data"]["suit"], data["Data"]["rank"], myId)
                if turn.playedCount == 4:
                    winner = turn.winner
                    if winner == 0 or winner == 2:
                        points[0] += 1
                    else:
                        points[1] += 1
                    turn.endTurn()
                    if turn.number == 13:
                        if points[0] > points[1]:
                            champion = 0
                        else:
                            champion = 1

                await broadcast(
                    {
                        "Type": ReqType.PLAYTURN.value,
                        "Data": {
                            "suit": turn.lastSuit,
                            "rank": turn.lastRank,
                            "currentPlayer": turn.currentPlayer,
                            "winner": winner,
                            "champion": champion,
                            "isFirstTurn": turn.playedCount == 0,
                        },
                    }
                )

    except websockets.ConnectionClosed:
        print("Client disconnected")

    except Exception as e:
        print(f"An error occurred:\n{e}")

    finally:
        connectedClients[myId]["socket"] = None


async def broadcast(request: dict):
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
    dealCards()
    # test
    turn.number = 12
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
