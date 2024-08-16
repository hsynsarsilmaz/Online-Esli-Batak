from ..common.common import *

from .text import *
from .networking import *
from .rendering import *
from .events import *
from .card import *


SUIT_ORDER = {"H": 0, "S": 1, "D": 2, "C": 3}


class GameStage(enum.Enum):
    WAITING = 0
    BIDDING = 1
    PLAYING = 2
    END = 3


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

    def markPlayableCards(self, isFirst: bool, suit: str, rank: int, trump: str):
        if len(self.cards) == 0:
            return

        # Every card except trumps can be played in first hand
        if isFirst:
            nonTrumpSuitCount = 0
            for card in self.cards:
                if card.suit != trump:
                    nonTrumpSuitCount += 1
            if nonTrumpSuitCount > 0:
                for card in self.cards:
                    if card.suit != trump:
                        card.playable = True
            else:
                for card in self.cards:
                    card.playable = True
            return

        playableCards = []

        # If the player has higher cards of the same suit, they must be played
        for card in self.cards:
            if card.suit == suit and card.rank > rank:
                playableCards.append(card)

        if len(playableCards) > 0:
            for playableCard in playableCards:
                playableCard.playable = True
            return

        # If the player doesn't have higher cards of the same suit, they can play a lesser card of the same suit
        for card in self.cards:
            if card.suit == suit:
                playableCards.append(card)

        if len(playableCards) > 0:
            for playableCard in playableCards:
                playableCard.playable = True
            return

        # If the player doesn't have any cards of the same suit, they can play any trump card
        # This will effectively change the suit to trump
        for card in self.cards:
            if card.suit == trump:
                playableCards.append(card)

        if len(playableCards) > 0:
            for playableCard in playableCards:
                playableCard.playable = True
            return

        # If the player doesn't have any cards of interest they can play any card without effect
        for card in self.cards:
            card.playable = True

    def unMarkMyCards(self):
        for card in self.cards:
            card.playable = False


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


def getDefaultGameState() -> dict:
    return {
        "myId": UNDEFINED,
        "currentPlayer": 0,
        "stage": GameStage.WAITING.value,
        "bid": 0,
        "trump": "",
        "bidder": 0,
        "winner": UNDEFINED,
        "champion": UNDEFINED,
    }
