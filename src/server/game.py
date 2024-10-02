import random
import websockets
import json

from src.common.common import *
from src.server.turn import Turn
from src.server.bidding import Bidding


class Game:
    def __init__(self):
        self.connectedClients = []
        self.turn = Turn()
        self.turn.number = 11
        self.bidding = Bidding(0)
        self.cards = []
        self.points = [0, 0]
        self.dealCards()

    async def processBid(self, myId: int, data: dict):
        if data["Data"]["bid"] == UNDEFINED:
            self.bidding.passBid(myId)
        else:
            self.bidding.makeBid(data["Data"]["bid"], data["Data"]["trump"], myId)

        if self.bidding.isBiddingEnded():
            self.turn.trump = self.bidding.trump
            request = ReqType.GAMESTART.value
        else:
            request = ReqType.BIDDING.value

        await self.broadcast(
            {
                "Type": request,
                "Data": {
                    "bid": self.bidding.bid,
                    "trump": self.bidding.trump,
                    "bidder": self.bidding.bidder,
                    "currentPlayer": (
                        self.bidding.currentPlayer
                        if request == ReqType.BIDDING.value
                        else self.bidding.bidder
                    ),
                },
            }
        )

    async def playTurn(self, myId: int, data: dict):
        if data["Data"]["playedForMate"] == True:
            myId = (myId + 2) % 4
        winner = UNDEFINED
        champion = UNDEFINED
        self.turn.play(data["Data"]["suit"], data["Data"]["rank"], myId)
        if self.turn.playedCount == 4:
            winner = self.turn.winner
            if winner == 0 or winner == 2:
                self.points[0] += 1
            else:
                self.points[1] += 1
            self.turn.endTurn()
            if self.turn.number == 13:
                if self.bidding.bidder == 0 or self.bidding.bidder == 2:
                    if self.points[0] < self.bidding.bid:
                        self.points[0] = -self.bidding.bid
                    if self.points[1] < 2:
                        self.points[1] = -self.bidding.bid
                else:
                    if self.points[0] < 2:
                        self.points[0] = -self.bidding.bid
                    if self.points[1] < self.bidding.bid:
                        self.points[1] = -self.bidding.bid

                starter = self.bidding.starter + 1 % 4
                self.bidding.reset(starter)
                self.dealCards()

                await self.broadcast(
                    {
                        "Type": ReqType.ENDROUND.value,
                        "Data": {
                            "suit": self.turn.turnSuit,
                            "rank": self.turn.lastRank,
                            "biggestRank": self.turn.biggestRank,
                            "originalSuit": self.turn.originalSuit,
                            "isTrumpPlayed": self.turn.isTrumpPlayed,
                            "currentPlayer": self.turn.currentPlayer,
                            "winner": winner,
                            "champion": champion,
                            "isFirstTurn": self.turn.playedCount == 0,
                            "points": self.points,
                            "cards": self.cards,
                            "starterId": self.bidding.starter,
                        },
                    }
                )

                self.turn.reset()

                return

        await self.broadcast(
            {
                "Type": ReqType.PLAYTURN.value,
                "Data": {
                    "suit": self.turn.turnSuit,
                    "rank": self.turn.lastRank,
                    "biggestRank": self.turn.biggestRank,
                    "originalSuit": self.turn.originalSuit,
                    "isTrumpPlayed": self.turn.isTrumpPlayed,
                    "currentPlayer": self.turn.currentPlayer,
                    "winner": winner,
                    "champion": champion,
                    "isFirstTurn": self.turn.playedCount == 0,
                },
            }
        )

    def dealCards(self):
        self.cards.clear()
        suits = ["H", "S", "D", "C"]
        ranks = [int(n) for n in range(2, 15)]
        for suit in suits:
            for rank in ranks:
                self.cards.append((suit, rank))
        random.shuffle(self.cards)

    async def connectClient(self, websocket: websockets.WebSocketServerProtocol):
        myId = len(self.connectedClients)
        self.connectedClients.append(websocket)
        self.printPlayers()

        await websocket.send(json.dumps({"Type": ReqType.CONNECT.value, "Data": myId}))

        if myId == 3:
            print("All players connected, starting game...")
            await self.broadcast(
                {
                    "Type": ReqType.START.value,
                    "Data": {"cards": self.cards, "starterId": self.bidding.starter},
                }
            )

        return myId

    def printPlayers(self):
        print("Players:")
        connectedCount = len(self.connectedClients)
        for i in range(connectedCount):
            print(f"Player {i + 1}: Connected")
        for i in range(connectedCount, 4):
            print(f"Player {i + 1}: Waiting")
        print()

    async def broadcast(self, request: dict):
        for player in self.connectedClients:
            if player != None:
                await player.send(json.dumps(request))
