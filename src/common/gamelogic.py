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


class Deck:
    def __init__(self):
        self.cards = []

    def createDeck(self, cards: list):
        self.cards = cards


def dealCards(cards: list, decks: dict, myId: int):
    myId -= 1
    cardReverseVertical, cardReverseHorizontal = loadCardReverseImages()
    decks["my"] = Deck()
    decks["left"] = Deck()
    decks["mate"] = Deck()
    decks["right"] = Deck()

    for i in range(4):
        for j in range(13):
            c = cards[j + i * 13]
            if i == myId:
                c.xPos = 317 + j * 70
                c.yPos = 668
                c.visible = True
                c.reverse = cardReverseVertical
                decks["my"].cards.append(c)
            elif i == (myId + 1) % 4:
                c.xPos = 68
                c.yPos = 88 + j * 50
                c.reverse = cardReverseHorizontal
                decks["left"].cards.append(c)
            elif i == (myId + 2) % 4:
                c.xPos = 317 + j * 70
                c.yPos = 50
                c.reverse = cardReverseVertical
                decks["mate"].cards.append(c)
            elif i == (myId + 3) % 4:
                c.xPos = 1350
                c.yPos = 88 + j * 50
                c.reverse = cardReverseHorizontal
                decks["right"].cards.append(c)
