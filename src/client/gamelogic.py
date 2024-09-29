from .card import *
from src.common.common import *
from .ui import GameUI
from .deck import dealCards


def getDefaultGameState() -> dict:
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


def clearRoundData(gameState: dict, decks: list):
    gameState.update(getDefaultGameState())
    decks.clear()


def startNewRound(gameState: dict, decks: list, ui: GameUI):
    points = gameState["points"]
    myId = gameState["myId"]
    starterId = gameState["newRoundData"]["starterId"]
    points[0] += gameState["newRoundData"]["points"][0]
    points[1] += gameState["newRoundData"]["points"][1]
    print(points)
    ui.updatePoints(points)
    cards = []
    loadCardImages(
        gameState["newRoundData"]["cards"],
        cards,
    )
    clearRoundData(gameState, decks)
    dealCards(cards, decks, myId)
    gameState["myId"] = myId
    gameState["points"] = points
    gameState["stage"] = GameStage.BIDDING.value
    gameState["bid"] = UNDEFINED
    gameState["trump"] = TBD
    gameState["bidder"] = UNDEFINED
    gameState["currentPlayer"] = starterId
