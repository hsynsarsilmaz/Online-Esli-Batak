import pygame
import asyncio
import websockets
import json
import random

from ..common.networking import * 
from ..common.card import * 
from ..common.gamelogic import *

WIDTH, HEIGHT = 1600, 900
FPS = 60
CARD_WIDTH, CARD_HEIGHT = 125, 182
myId = -1

color = (2, 100, 42)
cards = []
cardSuitAndRank = []
cardReverseVertical = None
cardReverseHorizontal = None
gameState = GameState.WAITING.value
turn = 1

biddingNumbers = []
biddingSuites = []

async def handleServerConnection(websocket : websockets.WebSocketClientProtocol):
    global cardSuitAndRank,myId, gameState
    async for message in websocket:
        data = json.loads(message)

        if(data["Type"] == ReqType.CONNECT.value):
            myId = data["Data"]["id"]
            gameState = data["Data"]["gameState"]
            print("Connected: ", myId)

        elif(data["Type"] == ReqType.START.value):
            cardSuitAndRank = data["Data"]
            loadCards()

def loadCardReverseImages():
    global cardReverseVertical, cardReverseHorizontal
    cardReverseVertical = pygame.image.load("res/img/cards/RV.png").convert_alpha()
    cardReverseVertical = pygame.transform.scale(cardReverseVertical, (CARD_WIDTH, CARD_HEIGHT))
    cardReverseHorizontal = pygame.image.load("res/img/cards/RV.png").convert_alpha()
    cardReverseHorizontal = pygame.transform.scale(cardReverseHorizontal, (CARD_WIDTH, CARD_HEIGHT))
    cardReverseHorizontal = pygame.transform.rotate(cardReverseHorizontal, 90)

def loadCardImages():
    global cards
    for suit,rank in cardSuitAndRank:
        image = pygame.image.load(f"res/img/cards/{rank}{suit}.png").convert_alpha()
        image = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
        cards.append(Card(suit, rank ,image))
    random.shuffle(cards)

def dealCards():
     for i in range(4):
        for j in range(13):
            c = cards[j + i*13]
            if(i == 0):
                c.xPos = 317 + j * 70
                c.yPos = 668
                c.reverse = cardReverseVertical
                c.visible = True
            elif(i == 1):
                c.xPos = 68 
                c.yPos = 88  + j * 50
                c.reverse = cardReverseHorizontal
            elif(i == 2):
                c.xPos = 317 + j * 70
                c.yPos = 50
                c.reverse = cardReverseVertical
            elif(i == 3):
                c.xPos = 1350 
                c.yPos = 88  + j * 50
                c.reverse = cardReverseHorizontal

def getBiddingNumbersAndSuites():
    global biddingNumbers, biddingSuites
    font = pygame.font.Font(None, 80)
    for i in range(7,14):
        text = font.render(str(i), True, (200,200,200))
        highligtedText = font.render(str(i), True, (200,0,0))
        row = (i - 7) // 3 
        col = (i - 7) % 3 + (1 if i == 13 else 0)
        xPos = 400 + 75 * col
        yPos = 300 + 80 * row  
        rect = text.get_rect(center=(xPos,yPos))
        biddingNumbers.append((text, highligtedText, rect))

    suites= ["H", "S", "D", "C"]

    for i in range(4):
        text = font.render(suites[i], True, (200,200,200))
        highligtedText = font.render(suites[i], True, (200,0,0))
        xPos = 800 + 75 * i
        yPos = 300
        rect = text.get_rect(center=(xPos,yPos))
        biddingSuites.append((text, highligtedText, rect))


def loadCards():
    loadCardReverseImages()
    loadCardImages()
    dealCards()

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Online Eşli Batak")
clock = pygame.time.Clock()
getBiddingNumbersAndSuites()

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

            screen.fill(color)
            
            clock.tick(FPS)

            if len(cards) == 0:
                font = pygame.font.Font(None, 36)
                text = font.render("Waiting for other players...", True, (255, 255, 255))
                textRect = text.get_rect()
                textRect.center = (WIDTH // 2, HEIGHT // 2)
                screen.blit(text, textRect)
            else:
                for card in cards:
                    if card.visible:
                        screen.blit(card.image, (card.xPos, card.yPos))
                    else:
                        screen.blit(card.reverse, (card.xPos, card.yPos))

            if gameState == GameState.BIDDING.value:
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


            
            pygame.display.flip()

            await asyncio.sleep(0)

        # await websocket.close()

if __name__ == "__main__":
    asyncio.run(main())