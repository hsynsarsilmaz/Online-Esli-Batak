import pygame
import websockets

from ..common.networking import *
from ..common.card import *
from ..common.gamelogic import *
from ..common.text import *

from .networking import *
from .rendering import *


async def handleEvents(
    event: pygame.event.Event,
    gameState: dict,
    decks: dict,
    texts: GameText,
    websocket: websockets.WebSocketClientProtocol,
):
    if event.type == pygame.QUIT:
        return True

    elif event.type == pygame.MOUSEBUTTONDOWN:
        mousePos = pygame.mouse.get_pos()
        for text, highligtedText, rect in texts.biddingNumbers:
            if rect.collidepoint(mousePos):
                pass

        for text, highligtedText, rect in texts.biddingSuites:
            if rect.collidepoint(mousePos):
                pass

        if gameState["stage"] == GameStage.PLAYING.value:
            await playCard(decks, websocket, mousePos)

        # temporary
        if gameState["currentPlayer"] == gameState["myId"] and texts.skipBidding[
            2
        ].collidepoint(mousePos):
            await sendRequest(
                websocket,
                {
                    "Type": ReqType.BIDSKIP.value,
                    "Data": {"bid": 7, "trump": "S"},
                },
            )

    return False
