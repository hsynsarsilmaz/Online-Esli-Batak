import pygame
import asyncio
import websockets

from ..common.networking import *
from ..common.card import *
from ..common.gamelogic import *
from ..common.text import *

from .networking import *
from .rendering import *
from .events import *

async def main():

    pygame.init()
    pygame.display.set_caption("Online Eşli Batak")

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    gameState = getDefaultGameState()
    decks = {}
    animations = []
    texts = GameText()
    running = True

    async with websockets.connect(URI) as websocket:

        message_handler = asyncio.create_task(
            handleServerConnection(websocket, decks, gameState, texts, animations)
        )

        while running:
            for event in pygame.event.get():
                if await handleEvents(event, gameState, decks, texts, websocket):
                    running = False

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

        await websocket.close()

if __name__ == "__main__":
    asyncio.run(main())
