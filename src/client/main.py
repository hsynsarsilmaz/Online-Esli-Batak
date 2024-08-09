import pygame
import asyncio
import websockets
import json
import random

from ..common.networking import * 
from ..common.card import * 
from ..common.gamelogic import *
from ..common.text import *


myId = -1
cards = []
gameState = GameState.WAITING.value
turn = 1

async def handleServerConnection(websocket : websockets.WebSocketClientProtocol):
    global myId, gameState
    async for message in websocket:
        data = json.loads(message)

        if(data["Type"] == ReqType.CONNECT.value):
            myId = data["Data"]["id"]
            gameState = data["Data"]["gameState"]
            print("Connected: ", myId)

        elif(data["Type"] == ReqType.START.value):
            loadCards(data["Data"],cards)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Online Eşli Batak")
clock = pygame.time.Clock()
initTexts()

def renderBidding():
    for text, highligtedText, rect in biddingNumbers:
        if rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(highligtedText, rect)
        else:
            screen.blit(text, rect)
    
    for text, highligtedText, rect in biddingSuites:
        if rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(highligtedText, rect)
        else:
            screen.blit(text, rect)

def renderCards():
    if len(cards) == 0:
        screen.blit(waitingForPlayers[0], waitingForPlayers[1])
    else:
        for card in cards:
            if card.visible:
                screen.blit(card.image, (card.xPos, card.yPos))
            else:
                screen.blit(card.reverse, (card.xPos, card.yPos))

async def main():
    
    async with websockets.connect(URI) as websocket:

        message_handler = asyncio.create_task(handleServerConnection(websocket))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for text, highligtedText, rect in biddingNumbers:
                        if rect.collidepoint(mouse_pos):
                            pass

                    for text, highligtedText, rect in biddingSuites:
                        if rect.collidepoint(mouse_pos):
                            pass

            screen.fill(BGCOLOR)
            clock.tick(FPS)

            renderCards()

            if gameState == GameState.BIDDING.value:
                renderBidding()
            
            pygame.display.flip()
            await asyncio.sleep(0)

        # await websocket.close()

if __name__ == "__main__":
    asyncio.run(main())