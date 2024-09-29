import pygame
import asyncio
import websockets

from src.common.common import *
from src.client.networking import *
from src.client.rendering import *
from src.client.events import *
from src.client.card import *
from src.client.ui import *
from src.client.round import *


async def main():

    pygame.init()
    pygame.display.set_caption("Online Eşli Batak")

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    round = Round()
    cardPlayAnimations = []
    cardDestoryAnimations = []
    ui = GameUI()
    running = True

    async with websockets.connect(URI) as websocket:

        message_handler = asyncio.create_task(
            handleServerConnection(websocket, round, ui, cardPlayAnimations)
        )

        while running:
            for event in pygame.event.get():
                if await handleEvents(
                    event, round.gameState, round.decks, ui, websocket
                ):
                    running = False

            screen.fill(BGCOLOR)
            clock.tick(FPS)

            if round.gameState["stage"] == GameStage.WAITING.value:
                screen.blit(ui.waitingForPlayers.normal, ui.waitingForPlayers.rect)

            elif round.gameState["stage"] == GameStage.BIDDING.value:
                renderBidding(screen, ui, round.gameState)
                renderCards(round.decks, screen, False)

            elif round.gameState["stage"] == GameStage.PLAYING.value:
                renderCards(round.decks, screen, True)
                renderCardPlayAnimations(
                    cardPlayAnimations, cardDestoryAnimations, screen, round.gameState
                )
                renderCardDestroyAnimations(
                    cardDestoryAnimations, screen, round.gameState
                )

            renderPoints(ui, screen)

            if round.gameState["newRound"]:
                round.startNewRound(ui)

            pygame.display.flip()
            await asyncio.sleep(0)

        message_handler.cancel()
        await websocket.close()
        pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
