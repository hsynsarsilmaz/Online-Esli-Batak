import websockets
import json

from src.client.ui import *
from src.client.gamelogic import *


async def handleServerConnection(
    websocket: websockets.WebSocketClientProtocol,
    decks: dict,
    gameState: dict,
    ui: GameUI,
    cardPlayAnimations: list,
):
    async for message in websocket:
        data = json.loads(message)
        cards = []

        if data["Type"] == ReqType.CONNECT.value:
            gameState["myId"] = data["Data"]

        elif data["Type"] == ReqType.START.value:
            loadCardImages(data["Data"]["cards"], cards)
            dealCards(cards, decks, gameState["myId"])
            gameState["stage"] = GameStage.BIDDING.value
            gameState["bid"] = UNDEFINED
            gameState["trump"] = TBD
            gameState["bidder"] = UNDEFINED
            gameState["currentPlayer"] = data["Data"]["starterId"]

        elif data["Type"] == ReqType.GAMESTART.value:
            gameState["bid"] = data["Data"]["bid"]
            gameState["trump"] = data["Data"]["trump"]
            gameState["bidder"] = data["Data"]["bidder"]
            gameState["stage"] = GameStage.PLAYING.value
            if gameState["myId"] == gameState["currentPlayer"]:
                decks["my"].markPlayableCards(
                    True, "", 0, gameState["trump"], False, ""
                )

        elif data["Type"] == ReqType.PLAYTURN.value:
            gameState["currentPlayer"] = data["Data"]["currentPlayer"]
            if gameState["currentPlayer"] != gameState["myId"]:
                decks["my"].unMarkMyCards()
            else:
                decks["my"].markPlayableCards(
                    data["Data"]["isFirstTurn"],
                    data["Data"]["suit"],
                    data["Data"]["biggestRank"],
                    gameState["trump"],
                    data["Data"]["isTrumpPlayed"],
                    data["Data"]["originalSuit"],
                )
            card = None
            for key, deck in decks.items():
                card = deck.findCard(data["Data"]["suit"], data["Data"]["rank"])
                if card:
                    deck.cards.remove(card)
                    break
            # move the card to center
            card.xVel = (WIDTH // 2 - card.rect.center[0]) / 60
            card.yVel = (HEIGHT // 2 - card.rect.center[1]) / 60
            card.frame = 0
            card.rect = card.image.get_rect(center=card.rect.center)

            cardPlayAnimations.append(card)

            gameState["winner"] = data["Data"]["winner"]
            gameState["champion"] = data["Data"]["champion"]

            if gameState["champion"] != UNDEFINED:
                gameState["champion"] = data["Data"]["champion"]
                ui.createWinner(gameState["champion"])

            rePositionCards(decks)


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
