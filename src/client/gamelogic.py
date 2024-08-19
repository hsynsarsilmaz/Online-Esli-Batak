from .card import *
from src.common.common import *

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

    def checkPlayable(self, playableCards: list) -> bool:
        if len(playableCards) > 0:
            for playableCard in playableCards:
                playableCard.playable = True
            return True

        return False

    def firstCard(self, trump: str, isFirst: bool, isTrumpPlayed: bool):
        # Until a player is obligated to play trump card, trump card can't be played as the first card
        # After a player played trump card, every card can be played as first card
        if isFirst:
            if isTrumpPlayed:
                for card in self.cards:
                    card.playable = True
            else:
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

    def sameSuitCards(
        self,
        suit: str,
        trump: str,
        biggestRank: int,
        playableCards: list,
        originalSuit: str,
    ) -> bool:
        # If the suit of the game changed to trump but player has a card of the original suit, they must play it
        if suit == trump:
            for card in self.cards:
                if card.suit == originalSuit:
                    playableCards.append(card)

        if self.checkPlayable(playableCards):
            return True

        # If the player has a card that greater than biggest played card, they must play it
        for card in self.cards:
            if card.suit == suit and card.rank > biggestRank:
                playableCards.append(card)

        if self.checkPlayable(playableCards):
            return True

        # If the player doesn't have a card that greater than biggest played card, they can play any card of the same suit
        for card in self.cards:
            if card.suit == suit:
                playableCards.append(card)

        if self.checkPlayable(playableCards):
            return True

        return False

    def obligatedTrump(self, trump: str, playableCards: list) -> bool:
        # If the player doesn't have any cards of the same suit, they can play a trump card
        # This will effectively change the suit to trump
        for card in self.cards:
            if card.suit == trump:
                playableCards.append(card)

        if self.checkPlayable(playableCards):
            return True

    def markPlayableCards(
        self,
        isFirst: bool,
        suit: str,
        biggestRank: int,
        trump: str,
        isTrumpPlayed: bool,
        originalSuit: str,
    ):
        if len(self.cards) == 0:
            return

        if isFirst:
            self.firstCard(trump, isFirst, isTrumpPlayed)
            return

        playableCards = []

        if self.sameSuitCards(suit, trump, biggestRank, playableCards, originalSuit):
            return

        # This case is only when last card is not trump and the player has trump cards
        if suit != trump and self.obligatedTrump(trump, playableCards):
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
