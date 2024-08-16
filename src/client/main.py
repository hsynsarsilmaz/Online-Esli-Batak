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
            if gameState["myId"] == gameState["currentPlayer"]:
                decks["my"].markPlayableCards(True, "", 0, gameState["trump"])

            texts.createBidValues(gameState["bid"], gameState["trump"])

        elif data["Type"] == ReqType.PLAYTURN.value:
            gameState["currentPlayer"] = data["Data"]["currentPlayer"]
            if gameState["currentPlayer"] != gameState["myId"]:
                decks["my"].unMarkMyCards()
            else:
                decks["my"].markPlayableCards(
                    data["Data"]["isFirstTurn"],
                    data["Data"]["suit"],
                    data["Data"]["rank"],
                    gameState["trump"],
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

            animations.append(card)
            gameState["winner"] = data["Data"]["winner"]
            gameState["champion"] = data["Data"]["champion"]

            if gameState["champion"] != UNDEFINED:
                gameState["champion"] = data["Data"]["champion"]
                texts.createWinner(gameState["champion"])


def renderText(items: list, screen: pygame.Surface):
    for text, highligtedText, rect in items:
        if rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(highligtedText, rect)
        else:
            screen.blit(text, rect)


def renderBidding(screen: pygame.Surface, texts: GameText, gameState: dict):
    renderText(texts.biddingNumbers, screen)
    renderText(texts.biddingSuites, screen)

    # Temporary
    if gameState["currentPlayer"] == gameState["myId"]:
        renderText([texts.skipBidding], screen)


def renderCards(decks: dict, screen: pygame.Surface, playingStage: bool):
    selectedCard = None
    if playingStage:
        for card in reversed(decks["my"].cards):
            if card.rect.collidepoint(pygame.mouse.get_pos()):
                selectedCard = card
                break

    for deck in decks.values():
        for card in deck.cards:
            if card.visible:
                if not playingStage:
                    screen.blit(card.image, card.rect)
                elif card.playable:
                    if selectedCard and card == selectedCard:
                        screen.blit(card.image, card.rect.move(0, -20))
                    else:
                        screen.blit(card.image, card.rect)
                else:
                    screen.blit(card.grayImage, card.rect)

            else:
                screen.blit(card.reverse, card.rect)


def renderAnimations(animations: list, screen: pygame.Surface, gameState: dict):
    if gameState["winner"] != UNDEFINED:
        if len(animations) == 4 and animations[3].frame == 61:
            for i, animation in enumerate(animations):
                animation.calculateWinnerVelocities(
                    gameState["myId"], gameState["winner"]
                )
                animation.frame = -15 * i
                animation.destroy = True

    for animation in animations:
        if animation.frame < 0:
            animation.frame += 1
        elif animation.frame < 60:
            animation.rect.x += animation.xVel
            animation.rect.y += animation.yVel
            animation.frame += 1
        elif animation.frame == 60:
            if animation.destroy:
                animations.remove(animation)
                if gameState["champion"] != UNDEFINED and len(animations) == 0:
                    gameState["stage"] = GameStage.END.value
            else:
                animation.xVel = 0
                animation.yVel = 0
                animation.rect.center = (WIDTH // 2, HEIGHT // 2)
                animation.frame += 1

        screen.blit(animation.image, animation.rect)


async def playCard(
    decks: dict, websocket: websockets.WebSocketClientProtocol, mousePos: tuple
):
    for card in reversed(decks["my"].cards):
        if card.playable and card.rect.collidepoint(mousePos):
            await sendRequest(
                websocket,
                {
                    "Type": ReqType.PLAYCARD.value,
                    "Data": {
                        "suit": card.suit,
                        "rank": card.rank,
                    },
                },
            )
            break


async def main():

    pygame.init()
    pygame.display.set_caption("Online Eşli Batak")

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    gameState = getDefaultGameState()
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
                    if gameState["currentPlayer"] == gameState[
                        "myId"
                    ] and texts.skipBidding[2].collidepoint(mousePos):
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
                renderCards(decks, screen, False)

            elif gameState["stage"] == GameStage.PLAYING.value:
                screen.blit(texts.bidValues[0], texts.bidValues[1])
                renderCards(decks, screen, True)
                renderAnimations(animations, screen, gameState)

            elif gameState["stage"] == GameStage.END.value:
                screen.blit(texts.winner[0], texts.winner[1])

            pygame.display.flip()
            await asyncio.sleep(0)

        # await websocket.close()


if __name__ == "__main__":
    asyncio.run(main())
