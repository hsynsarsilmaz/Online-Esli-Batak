import pygame
import asyncio
import websockets

from src.common.common import *
from src.client.networking import *
from src.client.rendering import *
from src.client.events import *
from src.client.gamelogic import *
from src.client.card import *
from src.client.ui import *


async def main():

    pygame.init()
    pygame.display.set_caption("Online Eşli Batak")

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    gameState = getDefaultGameState()
    decks = {}
    cardPlayAnimations = []
    cardDestoryAnimations = []
    ui = GameUI()
    running = True

    async with websockets.connect(URI) as websocket:

        message_handler = asyncio.create_task(
            handleServerConnection(websocket, decks, gameState, ui, cardPlayAnimations)
        )

        while running:
            for event in pygame.event.get():
                if await handleEvents(event, gameState, decks, ui, websocket):
                    running = False

            screen.fill(BGCOLOR)
            clock.tick(FPS)

            if gameState["stage"] == GameStage.WAITING.value:
                screen.blit(ui.waitingForPlayers.normal, ui.waitingForPlayers.rect)

            elif gameState["stage"] == GameStage.BIDDING.value:
                renderBidding(screen, ui, gameState)
                renderCards(decks, screen, False)

            elif gameState["stage"] == GameStage.PLAYING.value:
                renderCards(decks, screen, True)
                renderCardPlayAnimations(
                    cardPlayAnimations, cardDestoryAnimations, screen, gameState
                )
                renderCardDestroyAnimations(cardDestoryAnimations, screen, gameState)

            renderPoints(ui, screen)

            if gameState["newRound"]:
                startNewRound(gameState, decks, ui)

            pygame.display.flip()
            await asyncio.sleep(0)

        message_handler.cancel()
        await websocket.close()
        pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
