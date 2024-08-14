import pygame
import asyncio
import websockets
import json

from ..common.networking import *
from ..common.card import *
from ..common.gamelogic import *
from ..common.text import *


async def handleServerConnection(
    websocket: websockets.WebSocketClientProtocol,
    decks: dict,
    gameState: dict,
    texts: GameText,
    animations: list,
):
    async for message in websocket:
        data = json.loads(message)
        cards = []

        if data["Type"] == ReqType.CONNECT.value:
            gameState["myId"] = data["Data"]

        elif data["Type"] == ReqType.START.value:
            loadCardImages(data["Data"], cards)
            dealCards(cards, decks, gameState["myId"])
            gameState["stage"] = GameStage.BIDDING.value

        elif data["Type"] == ReqType.GAMESTART.value:
            gameState["bid"] = data["Data"]["bid"]
            gameState["trump"] = data["Data"]["trump"]
            gameState["bidder"] = data["Data"]["bidder"]
            gameState["stage"] = GameStage.PLAYING.value

            texts.createBidValues(gameState["bid"], gameState["trump"])

        elif data["Type"] == ReqType.ANIMATION.value:
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

            animations.append(card)


def renderBidding(screen: pygame.Surface, texts: GameText, gameState: dict):
    for text, highligtedText, rect in texts.biddingNumbers:
        if rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(highligtedText, rect)
        else:
            screen.blit(text, rect)

    for text, highligtedText, rect in texts.biddingSuites:
        if rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(highligtedText, rect)
        else:
            screen.blit(text, rect)

    # Temporary
    if gameState["turn"] == gameState["myId"]:
        screen.blit(texts.skipBidding[0], texts.skipBidding[1])


def renderCards(decks: dict, screen: pygame.Surface, texts: GameText, animations: list):
    selectedCard = None
    for card in reversed(decks["my"].cards):
        if card.rect.collidepoint(pygame.mouse.get_pos()):
            selectedCard = card
            break

    for key, deck in decks.items():
        for card in deck.cards:
            if card.visible:
                if card.playable:
                    if selectedCard and card == selectedCard:
                        screen.blit(card.image, card.rect.move(0, -20))
                    else:
                        screen.blit(card.image, card.rect)
                else:
                    screen.blit(card.grayImage, card.rect)

            else:
                screen.blit(card.reverse, card.rect)

    for animation in animations:
        if animation.frame < 60:
            animation.rect.x += animation.xVel
            animation.rect.y += animation.yVel
            animation.frame += 1
        elif animation.frame == 60:
            animation.xVel = 0
            animation.yVel = 0
            animation.rect.center = (WIDTH // 2, HEIGHT // 2)
            animation.frame += 1

        screen.blit(animation.image, animation.rect)


async def main():

    pygame.init()
    pygame.display.set_caption("Online Eşli Batak")

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    gameState = {
        "myId": -1,
        "turn": 0,
        "stage": GameStage.WAITING.value,
        "bid": 0,
        "trump": "",
        "bidder": 0,
    }
    decks = {}
    animations = []
    texts = GameText()

    async with websockets.connect(URI) as websocket:

        message_handler = asyncio.create_task(
            handleServerConnection(websocket, decks, gameState, texts, animations)
        )

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for text, highligtedText, rect in texts.biddingNumbers:
                        if rect.collidepoint(mouse_pos):
                            pass

                    for text, highligtedText, rect in texts.biddingSuites:
                        if rect.collidepoint(mouse_pos):
                            pass

                    for card in reversed(decks["my"].cards):
                        if card.rect.collidepoint(mouse_pos):
                            await sendRequest(
                                websocket,
                                {
                                    "Type": ReqType.PLAY.value,
                                    "Data": {
                                        "suit": card.suit,
                                        "rank": card.rank,
                                    },
                                },
                            )
                            break

                    # temporary
                    if gameState["turn"] == gameState["myId"] and texts.skipBidding[
                        1
                    ].collidepoint(mouse_pos):
                        await sendRequest(
                            websocket,
                            {
                                "Type": ReqType.BIDSKIP.value,
                                "Data": {"bid": 7, "trump": "S"},
                            },
                        )

            screen.fill(BGCOLOR)
            clock.tick(FPS)

            if gameState["stage"] == GameStage.WAITING.value:
                screen.blit(texts.waitingForPlayers[0], texts.waitingForPlayers[1])

            elif gameState["stage"] == GameStage.BIDDING.value:
                renderBidding(screen, texts, gameState)
                renderCards(decks, screen, texts, animations)

            elif gameState["stage"] == GameStage.PLAYING.value:
                screen.blit(texts.bidValues[0], texts.bidValues[1])
                renderCards(decks, screen, texts, animations)

            pygame.display.flip()
            await asyncio.sleep(0)

        # await websocket.close()


if __name__ == "__main__":
    asyncio.run(main())
