from src.common.common import *


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
