import random

from src.common.common import *
from src.server.networking import *

TBD = ""


class Turn:
    def __init__(self):
        self.number = 0
        self.lastSuit = TBD
        self.lastRank = 0
        self.biggestRank = 0
        self.trump = TBD
        self.isTrumpPlayed = False
        self.currentPlayer = 0
        self.playedCount = 0
        self.winner = UNDEFINED

    def play(self, suit: str, rank: int, player: int):
        if self.winner == UNDEFINED:
            self.winner = player
            self.biggestRank = rank
        else:
            if suit == self.trump and self.lastSuit != self.trump:
                self.winner = player
                self.lastSuit = self.trump
                self.isTrumpPlayed = True
                self.biggestRank = rank
            elif suit == self.lastSuit and rank > self.biggestRank:
                self.winner = player
                self.biggestRank = rank

        self.lastSuit = suit
        self.lastRank = rank
        self.currentPlayer = (player + 1) % 4
        self.playedCount += 1

    def endTurn(self):
        self.playedCount = 0
        self.number += 1
        self.currentPlayer = self.winner
        self.winner = UNDEFINED
        self.trump = TBD
        self.biggestRank = 0


def dealCards(cards: list):
    suits = ["H", "S", "D", "C"]
    ranks = [int(n) for n in range(2, 15)]
    for suit in suits:
        for rank in ranks:
            cards.append((suit, rank))
    random.shuffle(cards)


async def skipBid(myId: int, connectedClients: list, turn: Turn, data: dict):
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
        },
        connectedClients,
    )


async def playTurn(
    myId: int, connectedClients: list, turn: Turn, data: dict, points: list
):
    winner = UNDEFINED
    champion = UNDEFINED
    turn.play(data["Data"]["suit"], data["Data"]["rank"], myId)
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
                "biggestRank": turn.biggestRank,
                "isTrumpPlayed": turn.isTrumpPlayed,
                "currentPlayer": turn.currentPlayer,
                "winner": winner,
                "champion": champion,
                "isFirstTurn": turn.playedCount == 0,
            },
        },
        connectedClients,
    )
