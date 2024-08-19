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
        self.initPos = 0
        self.interval = 0
        self.fixedPos = 0
        self.factor = 0

    def createDeck(self, cards: list):
        self.cards = cards

    def initialPositions(self, key: str):
        hInverval = 70
        vInterval = 50
        hMargin = 50
        vMargin = 100
        hInitPos = (WIDTH - ((12 * hInverval + CARD_WIDTH))) // 2
        vInitPos = (HEIGHT - ((12 * vInterval + CARD_HEIGHT))) // 2
        hFactor = (WIDTH // 2 - hInitPos) // 12
        vFactor = (HEIGHT // 2 - vInitPos) // 12

        if key == "my":
            self.initPos = hInitPos
            self.interval = hInverval
            self.fixedPos = HEIGHT - hMargin - CARD_HEIGHT // 2
            self.factor = hFactor
            for card in self.cards:
                card.rect = card.image.get_rect()
        elif key == "left":
            self.initPos = vInitPos
            self.interval = vInterval
            self.fixedPos = vMargin + CARD_HEIGHT // 2
            self.factor = vFactor
            for card in self.cards:
                card.rect = card.reverse.get_rect()
        elif key == "mate":
            self.initPos = hInitPos
            self.interval = hInverval
            self.fixedPos = hMargin + CARD_HEIGHT // 2
            self.factor = hFactor
            for card in self.cards:
                card.rect = card.reverse.get_rect()

        elif key == "right":
            self.initPos = vInitPos
            self.interval = vInterval
            self.fixedPos = WIDTH - vMargin - CARD_HEIGHT // 2
            self.factor = vFactor
            for card in self.cards:
                card.rect = card.reverse.get_rect()

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

    decks["my"].initialPositions("my")
    decks["left"].initialPositions("left")
    decks["mate"].initialPositions("mate")
    decks["right"].initialPositions("right")
    rePositionCards(decks)


def rePositionCards(decks: dict):
    for key, deck in decks.items():
        played = 13 - len(deck.cards)
        if key == "my":
            for i, card in enumerate(deck.cards):
                card.rect.midleft = (
                    deck.initPos + i * deck.interval + played * deck.factor,
                    deck.fixedPos,
                )
        elif key == "left":
            for i, card in enumerate(deck.cards):
                card.rect.midtop = (
                    deck.fixedPos,
                    deck.initPos + i * deck.interval + played * deck.factor,
                )
        elif key == "mate":
            for i, card in enumerate(deck.cards):
                card.rect.midleft = (
                    deck.initPos + i * deck.interval + played * deck.factor,
                    deck.fixedPos,
                )
        elif key == "right":
            for i, card in enumerate(deck.cards):
                card.rect.midtop = (
                    deck.fixedPos,
                    deck.initPos + i * deck.interval + played * deck.factor,
                )


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
