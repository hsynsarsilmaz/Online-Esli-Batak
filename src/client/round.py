from .card import *
from src.common.common import *
from .ui import GameUI
from .deck import dealCards


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
        dealCards(cards, self.decks, myId)
        self.gameState["myId"] = myId
        self.gameState["points"] = points
        self.gameState["stage"] = GameStage.BIDDING.value
        self.gameState["bid"] = UNDEFINED
        self.gameState["trump"] = TBD
        self.gameState["bidder"] = UNDEFINED
        self.gameState["currentPlayer"] = starterId
