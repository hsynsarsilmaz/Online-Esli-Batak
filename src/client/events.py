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

    if event.type == pygame.MOUSEBUTTONDOWN:
        mousePos = pygame.mouse.get_pos()

        if gameState["currentPlayer"] == gameState["myId"]:
            await handleBidding(ui, mousePos, gameState, websocket)

        if gameState["stage"] == GameStage.PLAYING.value:
            await playCard(decks, websocket, mousePos)

    return False


async def handleBidding(ui, mousePos, gameState, websocket):
    if ui.passBidding.rect.collidepoint(mousePos) and gameState["bid"] != UNDEFINED:
        await makeBid(websocket, UNDEFINED, TBD)

    if ui.makeBidding.rect.collidepoint(mousePos):
        await makeBid(websocket, gameState["bidRank"], gameState["bidSuit"][0])

    for text in ui.biddingNumbers:
        if text.rect.collidepoint(mousePos) and int(text.value) > gameState["bid"]:
            gameState["bidRank"] = int(text.value)

    for image in ui.biddingSuits:
        if image.rect.collidepoint(mousePos):
            gameState["bidSuit"] = image.value


async def makeBid(websocket, bid, trump):
    await websocket.send(
        json.dumps(
            {
                "Type": ReqType.MAKEBID.value,
                "Data": {"bid": bid, "trump": trump},
            }
        )
    )
