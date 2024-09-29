from src.common.common import *


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
