import pygame
import asyncio
import websockets
import json

from ..common.networking import * 
from ..common.card import * 
from ..common.gamelogic import *
from ..common.text import *

async def handleServerConnection(websocket : websockets.WebSocketClientProtocol, cards : list, gameState : dict):
    async for message in websocket:
        data = json.loads(message)

        if(data["Type"] == ReqType.CONNECT.value):
            gameState["myId"] = data["Data"]
            print("Connected: ", gameState)

        elif(data["Type"] == ReqType.START.value):
            loadCards(data["Data"],cards)
            gameState["stage"] = GameStage.BIDDING.value

def renderBidding(screen : pygame.Surface, texts : GameText, gameState : dict):
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

    #Temporary
    if gameState["turn"] == gameState["myId"]:
        screen.blit(texts.skipBidding[0], texts.skipBidding[1])

def renderCards(cards : list, screen : pygame.Surface, texts : GameText):
    for card in cards:
        if card.visible:
            screen.blit(card.image, (card.xPos, card.yPos))
        else:
            screen.blit(card.reverse, (card.xPos, card.yPos))

async def main():

    pygame.init()
    pygame.display.set_caption("Online Eşli Batak")

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    gameState = {
        "myId" : -1,
        "turn" : 1,
        "stage" : GameStage.WAITING.value
    }
    cards = []
    texts = GameText()    

    async with websockets.connect(URI) as websocket:

        message_handler = asyncio.create_task(handleServerConnection(websocket,cards,gameState))

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

                    #temporary
                    if gameState["turn"] == gameState["myId"] and  texts.skipBidding[1].collidepoint(mouse_pos):
                        pass

            screen.fill(BGCOLOR)
            clock.tick(FPS)

            renderCards(cards,screen,texts)

            if gameState["stage"] == GameStage.WAITING.value:
                screen.blit(texts.waitingForPlayers[0], texts.waitingForPlayers[1])

            elif gameState["stage"] == GameStage.BIDDING.value:
                renderBidding(screen,texts,gameState)
            
            pygame.display.flip()
            await asyncio.sleep(0)

        # await websocket.close()

if __name__ == "__main__":
    asyncio.run(main())