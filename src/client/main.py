import pygame
import asyncio
import websockets
import re

from src.common.common import *
from src.client.networking import *
from src.client.rendering import *
from src.client.events import *
from src.client.card import *
from src.client.ui import *
from src.client.round import *


def readIpFromFile(path):
    try:
        with open(path, "r") as file:
            ip_address = file.readline().strip()
            if isValidIp(ip_address):
                return ip_address
            else:
                print("Invalid IP address in file.")
                return None
    except FileNotFoundError:
        print(f"File not found: {path}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def isValidIp(ip_address):
    pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    if pattern.match(ip_address):
        parts = ip_address.split(".")
        if all(0 <= int(part) <= 255 for part in parts):
            return True
    return False


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
    IP = readIpFromFile("ip.txt")
    if not IP:
        print("No valid IP address found. Exiting...")
        return
    URI = f"ws://{IP}:{PORT}"

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
                round.loadNextRound(ui)

            pygame.display.flip()
            await asyncio.sleep(0)

        message_handler.cancel()
        await websocket.close()
        pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
