import random

from src.common.common import *
from src.server.networking import *

TBD = ""


class Turn:
    def __init__(self):
        self.number = 0
        self.originalSuit = TBD
        self.turnSuit = TBD
        self.lastRank = 0
        self.biggestRank = 0
        self.trump = TBD
        self.isTrumpPlayed = False
        self.currentPlayer = 0
        self.playedCount = 0
        self.winner = UNDEFINED

    def play(self, suit: str, rank: int, player: int):
        if self.winner == UNDEFINED:
            # print(f"First card played by player {player + 1}")
            self.winner = player
            self.biggestRank = rank
            self.originalSuit = suit
            self.turnSuit = suit
        else:
            # print(
            #     f"Player {player + 1} played {rank} of {suit}, trump is {self.trump}, last suit is {self.turnSuit}"
            # )
            if suit == self.trump and self.turnSuit != self.trump:
                self.winner = player
                self.turnSuit = self.trump
                self.isTrumpPlayed = True
                self.biggestRank = rank
            elif suit == self.turnSuit and rank > self.biggestRank:
                self.winner = player
                self.biggestRank = rank

        self.lastRank = rank
        self.currentPlayer = (player + 1) % 4
        self.playedCount += 1

    def endTurn(self):
        self.playedCount = 0
        self.number += 1
        self.currentPlayer = self.winner
        self.winner = UNDEFINED


class Bidding:
    def __init__(self):
        self.currentPlayer = 0
        self.bidder = UNDEFINED
        self.bid = UNDEFINED
        self.trump = TBD
        self.biddablePlayers = [True, True, True, True]

    def makeBid(self, bid: int, trump: str, bidder: int):
        self.bid = bid
        self.trump = trump
        self.bidder = bidder
        self.currentPlayer = (bidder + 1) % 4

    def passBid(self, player: int):
        self.biddablePlayers[player] = False
        self.currentPlayer = (self.currentPlayer + 1) % 4
        while not self.biddablePlayers[self.currentPlayer]:
            self.currentPlayer = (self.currentPlayer + 1) % 4

    def isBiddingEnded(self):
        return sum(self.biddablePlayers) == 1


def dealCards(cards: list):
    suits = ["H", "S", "D", "C"]
    ranks = [int(n) for n in range(2, 15)]
    for suit in suits:
        for rank in ranks:
            cards.append((suit, rank))
    random.shuffle(cards)


async def processBid(
    myId: int, connectedClients: list, bidding: Bidding, data: dict, turn: Turn
):
    if data["Data"]["bid"] == UNDEFINED:
        bidding.passBid(myId)
    else:
        bidding.makeBid(data["Data"]["bid"], data["Data"]["trump"], myId)

    if bidding.isBiddingEnded():
        turn.trump = bidding.trump
        request = ReqType.GAMESTART.value
    else:
        request = ReqType.BIDDING.value

    print(bidding.bidder)

    await broadcast(
        {
            "Type": request,
            "Data": {
                "bid": bidding.bid,
                "trump": bidding.trump,
                "bidder": bidding.bidder,
                "currentPlayer": (
                    bidding.currentPlayer
                    if request == ReqType.BIDDING.value
                    else bidding.bidder
                ),
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
                "suit": turn.turnSuit,
                "rank": turn.lastRank,
                "biggestRank": turn.biggestRank,
                "originalSuit": turn.originalSuit,
                "isTrumpPlayed": turn.isTrumpPlayed,
                "currentPlayer": turn.currentPlayer,
                "winner": winner,
                "champion": champion,
                "isFirstTurn": turn.playedCount == 0,
            },
        },
        connectedClients,
    )
