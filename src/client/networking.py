import websockets
import json

from src.client.ui import *
from .round import *


async def handleServerConnection(
    websocket: websockets.WebSocketClientProtocol,
    round: Round,
    ui: GameUI,
    cardPlayAnimations: list,
):
    async for message in websocket:
        data = json.loads(message)
        cards = []

        if data["Type"] == ReqType.CONNECT.value:
            round.gameState["myId"] = data["Data"]

        elif data["Type"] == ReqType.START.value:
            loadCardImages(data["Data"]["cards"], cards)
            round.dealCards(cards, round.gameState["myId"])
            round.gameState["stage"] = GameStage.BIDDING.value
            round.gameState["bid"] = UNDEFINED
            round.gameState["trump"] = TBD
            round.gameState["bidder"] = UNDEFINED
            round.gameState["currentPlayer"] = data["Data"]["starterId"]

        elif data["Type"] == ReqType.BIDDING.value:
            round.gameState["bid"] = data["Data"]["bid"]
            round.gameState["trump"] = data["Data"]["trump"]
            round.gameState["bidder"] = data["Data"]["bidder"]
            round.gameState["bidRank"] = UNDEFINED
            round.gameState["bidSuit"] = TBD
            round.gameState["currentPlayer"] = data["Data"]["currentPlayer"]

        elif data["Type"] == ReqType.GAMESTART.value:
            round.gameState["bid"] = data["Data"]["bid"]
            round.gameState["trump"] = data["Data"]["trump"]
            round.gameState["bidder"] = data["Data"]["bidder"]
            round.gameState["stage"] = GameStage.PLAYING.value
            round.gameState["currentPlayer"] = data["Data"]["currentPlayer"]
            if round.gameState["myId"] == round.gameState["currentPlayer"]:
                round.decks["my"].markPlayableCards(
                    True, "", 0, round.gameState["trump"], False, ""
                )

        elif data["Type"] == ReqType.PLAYTURN.value:
            round.gameState["currentPlayer"] = data["Data"]["currentPlayer"]
            if round.gameState["currentPlayer"] != round.gameState["myId"]:
                round.decks["my"].unMarkMyCards()
            else:
                round.decks["my"].markPlayableCards(
                    data["Data"]["isFirstTurn"],
                    data["Data"]["suit"],
                    data["Data"]["biggestRank"],
                    round.gameState["trump"],
                    data["Data"]["isTrumpPlayed"],
                    data["Data"]["originalSuit"],
                )
            card = None
            for key, deck in round.decks.items():
                card = deck.findCard(data["Data"]["suit"], data["Data"]["rank"])
                if card:
                    deck.cards.remove(card)
                    break
            card.xVel = (WIDTH // 2 - card.rect.center[0]) / 60
            card.yVel = (HEIGHT // 2 - card.rect.center[1]) / 60
            card.frame = 0
            card.rect = card.image.get_rect(center=card.rect.center)

            cardPlayAnimations.append(card)

            round.gameState["winner"] = data["Data"]["winner"]
            round.gameState["champion"] = data["Data"]["champion"]

            if round.gameState["champion"] != UNDEFINED:
                round.gameState["champion"] = data["Data"]["champion"]
                ui.createWinner(round.gameState["champion"])

            round.rePositionCards()

        elif data["Type"] == ReqType.ENDROUND.value:
            round.gameState["currentPlayer"] = data["Data"]["currentPlayer"]
            if round.gameState["currentPlayer"] != round.gameState["myId"]:
                round.decks["my"].unMarkMyCards()
            else:
                round.decks["my"].markPlayableCards(
                    data["Data"]["isFirstTurn"],
                    data["Data"]["suit"],
                    data["Data"]["biggestRank"],
                    round.gameState["trump"],
                    data["Data"]["isTrumpPlayed"],
                    data["Data"]["originalSuit"],
                )
            card = None
            for key, deck in round.decks.items():
                card = deck.findCard(data["Data"]["suit"], data["Data"]["rank"])
                if card:
                    deck.cards.remove(card)
                    break
            card.xVel = (WIDTH // 2 - card.rect.center[0]) / 60
            card.yVel = (HEIGHT // 2 - card.rect.center[1]) / 60
            card.frame = 0
            card.rect = card.image.get_rect(center=card.rect.center)

            cardPlayAnimations.append(card)

            round.gameState["winner"] = data["Data"]["winner"]
            round.gameState["champion"] = data["Data"]["champion"]

            if round.gameState["champion"] != UNDEFINED:
                round.gameState["champion"] = data["Data"]["champion"]
                ui.createWinner(round.gameState["champion"])

            round.rePositionCards()

            round.gameState["endRound"] = True
            round.gameState["newRoundData"] = data["Data"]


async def playCard(
    decks: dict, websocket: websockets.WebSocketClientProtocol, mousePos: tuple
):
    for card in reversed(decks["my"].cards):
        if card.playable and card.rect.collidepoint(mousePos):
            await websocket.send(
                json.dumps(
                    {
                        "Type": ReqType.PLAYCARD.value,
                        "Data": {
                            "suit": card.suit,
                            "rank": card.rank,
                        },
                    }
                )
            )
            break
