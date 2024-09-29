from .card import *
from src.common.common import *
from .ui import GameUI
from .deck import *


class Round:
    def __init__(self) -> None:
        self.gameState = self.getDefaultGameState()
        self.decks = {}

    def getDefaultGameState(self) -> dict:
        return {
            "myId": UNDEFINED,
            "currentPlayer": 0,
            "stage": GameStage.WAITING.value,
            "bid": UNDEFINED,
            "trump": TBD,
            "bidder": UNDEFINED,
            "winner": UNDEFINED,
            "champion": UNDEFINED,
            "bidSuit": "",
            "bidRank": UNDEFINED,
            "points": [0, 0],
            "endRound": False,
            "newRound": False,
            "newRoundData": {},
        }

    def clearRoundData(self):
        self.gameState = self.getDefaultGameState()
        self.decks = {}

    def startNewRound(self, ui: GameUI):
        points = self.gameState["points"]
        myId = self.gameState["myId"]
        starterId = self.gameState["newRoundData"]["starterId"]
        points[0] += self.gameState["newRoundData"]["points"][0]
        points[1] += self.gameState["newRoundData"]["points"][1]
        print(points)
        ui.updatePoints(points)
        cards = []
        loadCardImages(
            self.gameState["newRoundData"]["cards"],
            cards,
        )
        self.clearRoundData()
        self.dealCards(cards, myId)
        self.gameState["myId"] = myId
        self.gameState["points"] = points
        self.gameState["stage"] = GameStage.BIDDING.value
        self.gameState["bid"] = UNDEFINED
        self.gameState["trump"] = TBD
        self.gameState["bidder"] = UNDEFINED
        self.gameState["currentPlayer"] = starterId

    def rePositionCards(self):
        for key, deck in self.decks.items():
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

    def dealCards(self, cards: list, myId: int):
        cardReverseVertical, cardReverseHorizontal = loadCardReverseImages()
        self.decks["my"] = Deck()
        self.decks["left"] = Deck()
        self.decks["mate"] = Deck()
        self.decks["right"] = Deck()

        for i in range(4):
            for j in range(13):
                card = cards[j + i * 13]
                if i == myId:
                    card.reverse = cardReverseVertical
                    card.visible = True
                    self.decks["my"].cards.append(card)
                elif i == (myId + 1) % 4:
                    card.reverse = cardReverseHorizontal
                    self.decks["left"].cards.append(card)
                elif i == (myId + 2) % 4:
                    card.reverse = cardReverseVertical
                    self.decks["mate"].cards.append(card)
                elif i == (myId + 3) % 4:
                    card.reverse = cardReverseHorizontal
                    self.decks["right"].cards.append(card)

        for deck in self.decks.values():
            deck.sortDeck()

        self.decks["my"].initialPositions("my")
        self.decks["left"].initialPositions("left")
        self.decks["mate"].initialPositions("mate")
        self.decks["right"].initialPositions("right")
        self.rePositionCards()
