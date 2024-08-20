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
                await websocket.send(
                    json.dumps(
                        {
                            "Type": ReqType.BIDSKIP.value,
                            "Data": {"bid": 7, "trump": "S"},
                        }
                    )
                )

            for text in ui.biddingNumbers:
                if text.rect.collidepoint(mousePos):
                    gameState["bidRank"] = text.value

            for image in ui.biddingSuits:
                if image.rect.collidepoint(mousePos):
                    gameState["bidSuit"] = image.value

        if gameState["stage"] == GameStage.PLAYING.value:
            await playCard(decks, websocket, mousePos)

    return False
