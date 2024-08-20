import pygame
import websockets
import json

from src.client.text import *
from src.client.gamelogic import *
from src.client.networking import *


async def handleEvents(
    event: pygame.event.Event,
    gameState: dict,
    decks: dict,
    texts: GameText,
    biddingSuites: list,
    websocket: websockets.WebSocketClientProtocol,
):

    if event.type == pygame.QUIT:
        return True

    elif event.type == pygame.MOUSEBUTTONDOWN:
        mousePos = pygame.mouse.get_pos()
        for text, highligtedText, rect in texts.biddingNumbers:
            if rect.collidepoint(mousePos):
                pass

        for image, highlighted, rect in biddingSuites:
            if rect.collidepoint(mousePos):
                pass

        if gameState["stage"] == GameStage.PLAYING.value:
            await playCard(decks, websocket, mousePos)

        # temporary
        if gameState["currentPlayer"] == gameState["myId"] and texts.skipBidding[
            2
        ].collidepoint(mousePos):
            await websocket.send(
                json.dumps(
                    {
                        "Type": ReqType.BIDSKIP.value,
                        "Data": {"bid": 7, "trump": "S"},
                    }
                )
            )

    return False
