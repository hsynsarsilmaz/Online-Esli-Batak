import enum

from ..common.card import *


class GameStage(enum.Enum):
    WAITING = 0
    BIDDING = 1
    PLAYING = 2
    END = 3


# Constants
WIDTH, HEIGHT = 1600, 900
FPS = 60
BGCOLOR = (2, 100, 42)
SUIT_ORDER = {"H": 0, "S": 1, "D": 2, "C": 3}


class Deck:
    def __init__(self):
        self.cards = []

    def createDeck(self, cards: list):
        self.cards = cards

    def sortDeck(self):
        self.cards.sort(key=lambda x: (SUIT_ORDER[x.suit], x.rank))

    def findCard(self, suit: str, rank: int):
        for card in self.cards:
            if card.suit == suit and card.rank == rank:
                return card
        return None


def dealCards(cards: list, decks: dict, myId: int):
    cardReverseVertical, cardReverseHorizontal = loadCardReverseImages()
    decks["my"] = Deck()
    decks["left"] = Deck()
    decks["mate"] = Deck()
    decks["right"] = Deck()

    for i in range(4):
        for j in range(13):
            c = cards[j + i * 13]
            if i == myId:
                c.reverse = cardReverseVertical
                c.visible = True
                decks["my"].cards.append(c)
            elif i == (myId + 1) % 4:
                c.reverse = cardReverseHorizontal
                decks["left"].cards.append(c)
            elif i == (myId + 2) % 4:
                c.reverse = cardReverseVertical
                decks["mate"].cards.append(c)
            elif i == (myId + 3) % 4:
                c.reverse = cardReverseHorizontal
                decks["right"].cards.append(c)

    for deck in decks.values():
        deck.sortDeck()

    rePositionCards(decks)


def rePositionCards(decks: dict):
    for key, deck in decks.items():
        if key == "my":
            for i, card in enumerate(deck.cards):
                card.rect.topleft = (317 + i * 70, 668)
        elif key == "left":
            for i, card in enumerate(deck.cards):
                card.rect.topleft = (68, 88 + i * 50)
        elif key == "mate":
            for i, card in enumerate(deck.cards):
                card.rect.topleft = (317 + i * 70, 50)
        elif key == "right":
            for i, card in enumerate(deck.cards):
                card.rect.topleft = (1350, 88 + i * 50)


class Turn:
    def __init__(self):
        self.number = 0
        self.lastCard = None
        self.currentPlayer = 0
        self.playedCount = 0
        self.winner = -1

    def playTurn(self, suit: str, rank: int, player: int):
        self.lastCard = {"suit": suit, "rank": rank}
        self.currentPlayer = (player + 1) % 4
        self.playedCount += 1
        if self.winner == -1:
            self.winner = player

        return self.lastCard, self.currentPlayer
