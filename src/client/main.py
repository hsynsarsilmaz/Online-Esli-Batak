import pygame
import asyncio
import websockets

from src.common.common import *

from src.client.text import *
from src.client.networking import *
from src.client.rendering import *
from src.client.events import *
from src.client.gamelogic import *
from src.client.card import *
from src.client.image import *


async def main():

    pygame.init()
    pygame.display.set_caption("Online Eşli Batak")

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    gameState = getDefaultGameState()
    decks = {}
    cardPlayAnimations = []
    cardDestoryAnimations = []
    texts = GameText()
    biddingSuits = createBiddingSuits()
    running = True

    async with websockets.connect(URI) as websocket:

        message_handler = asyncio.create_task(
            handleServerConnection(
                websocket, decks, gameState, texts, cardPlayAnimations
            )
        )

        while running:
            for event in pygame.event.get():
                if await handleEvents(
                    event, gameState, decks, texts, biddingSuits, websocket
                ):
                    running = False

            screen.fill(BGCOLOR)
            clock.tick(FPS)

            if gameState["stage"] == GameStage.WAITING.value:
                screen.blit(texts.waitingForPlayers[0], texts.waitingForPlayers[1])

            elif gameState["stage"] == GameStage.BIDDING.value:
                renderBidding(screen, texts, biddingSuits, gameState)
                renderCards(decks, screen, False)

            elif gameState["stage"] == GameStage.PLAYING.value:
                screen.blit(texts.bidValues[0], texts.bidValues[1])
                renderCards(decks, screen, True)
                renderCardPlayAnimations(
                    cardPlayAnimations, cardDestoryAnimations, screen, gameState
                )
                renderCardDestroyAnimations(cardDestoryAnimations, screen, gameState)

            elif gameState["stage"] == GameStage.END.value:
                screen.blit(texts.winner[0], texts.winner[1])

            pygame.display.flip()
            await asyncio.sleep(0)

        message_handler.cancel()
        await websocket.close()
        pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
