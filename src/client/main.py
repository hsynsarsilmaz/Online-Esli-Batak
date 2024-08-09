import pygame
import asyncio
import websockets
import json
import random

from ..common.networking import * 
from ..common.card import * 

WIDTH, HEIGHT = 1600, 900
FPS = 60
CARD_WIDTH, CARD_HEIGHT = 125, 182
myId = -1

color = (2, 100, 42)
cards = []
cardSuitAndRank = []
cardReverseVertical = None
cardReverseHorizontal = None

async def handleServerConnection(websocket : websockets.WebSocketClientProtocol):
    global cardSuitAndRank,myId
    async for message in websocket:
        data = json.loads(message)
        
        if(data["Type"] == ReqType.CONNECT.value):
            myId = data["Data"]
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


def loadCards():
    loadCardReverseImages()
    loadCardImages()
    dealCards()

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Online Eşli Batak")
clock = pygame.time.Clock()

async def main():
    
    async with websockets.connect(URI) as websocket:

        message_handler = asyncio.create_task(handleServerConnection(websocket))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

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

            
            pygame.display.flip()

            await asyncio.sleep(0)

        # await websocket.close()

if __name__ == "__main__":
    asyncio.run(main())