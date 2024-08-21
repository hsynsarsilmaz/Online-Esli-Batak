import pygame
import websockets
import json

from src.client.ui import *
from src.client.gamelogic import *
from src.client.networking import *


async def handleEvents(
    event: pygame.event.Event,
    gameState: dict,
    decks: dict,
    ui: GameUI,
    websocket: websockets.WebSocketClientProtocol,
):

    if event.type == pygame.QUIT:
        return True

    elif event.type == pygame.MOUSEBUTTONDOWN:
        mousePos = pygame.mouse.get_pos()

        if gameState["currentPlayer"] == gameState["myId"]:
            if ui.passBidding.rect.collidepoint(mousePos):
                if gameState["bid"] != UNDEFINED:
                    await websocket.send(
                        json.dumps(
                            {
                                "Type": ReqType.MAKEBID.value,
                                "Data": {"bid": UNDEFINED, "trump": TBD},
                            }
                        )
                    )

            if ui.makeBidding.rect.collidepoint(mousePos):
                await websocket.send(
                    json.dumps(
                        {
                            "Type": ReqType.MAKEBID.value,
                            "Data": {
                                "bid": gameState["bidRank"],
                                "trump": gameState["bidSuit"][0],
                            },
                        }
                    )
                )

            for text in ui.biddingNumbers:
                if (
                    text.rect.collidepoint(mousePos)
                    and int(text.value) > gameState["bid"]
                ):
                    gameState["bidRank"] = int(text.value)

            for image in ui.biddingSuits:
                if image.rect.collidepoint(mousePos):
                    gameState["bidSuit"] = image.value

        if gameState["stage"] == GameStage.PLAYING.value:
            await playCard(decks, websocket, mousePos)

    return False
