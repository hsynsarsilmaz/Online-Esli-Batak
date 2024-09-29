from src.common.common import *


class Game:
    def __init__(self):
        self.connectedClients = []
        self.turn = Turn()
        self.bidding = Bidding(0)
        self.cards = []
        self.points = [0, 0]


class Turn:
    def __init__(self):
        self.reset()

    def play(self, suit: str, rank: int, player: int):
        if self.winner == UNDEFINED:
            self.winner = player
            self.biggestRank = rank
            self.originalSuit = suit
            self.turnSuit = suit
        else:
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

    def reset(self):
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


class Bidding:

    def __init__(self, starter: int):
        self.reset(starter)

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

    def reset(self, starter: int):
        self.starter = starter
        self.currentPlayer = starter
        self.bidder = UNDEFINED
        self.bid = UNDEFINED
        self.trump = TBD
        self.biddablePlayers = [True, True, True, True]
