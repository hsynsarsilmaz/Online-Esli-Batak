import pygame
from .gamelogic import WIDTH, HEIGHT

TEXT_COLOR = (200,200,200)
TEXT_HIGHLIGHT_COLOR = (200,0,0)
biddingNumbers = []
biddingSuites = []
waitingForPlayers = []


def initTexts():
    getWaitingForPlayersText(waitingForPlayers)
    getBiddingNumbersAndSuites(biddingNumbers, biddingSuites)

def getBiddingNumbersAndSuites(biddingNumbers, biddingSuites):
    font = pygame.font.Font(None, 80)
    for i in range(7,14):
        text = font.render(str(i), True, TEXT_COLOR)
        highligtedText = font.render(str(i), True, TEXT_HIGHLIGHT_COLOR)
        row = (i - 7) // 3 
        col = (i - 7) % 3 + (1 if i == 13 else 0)
        xPos = 400 + 75 * col
        yPos = 300 + 80 * row  
        rect = text.get_rect(center=(xPos,yPos))
        biddingNumbers.append((text, highligtedText, rect))

    suites= ["H", "S", "D", "C"]

    for i in range(4):
        text = font.render(suites[i], True, TEXT_COLOR)
        highligtedText = font.render(suites[i], True, TEXT_HIGHLIGHT_COLOR)
        xPos = 800 + 75 * i
        yPos = 300
        rect = text.get_rect(center=(xPos,yPos))
        biddingSuites.append((text, highligtedText, rect))

def getWaitingForPlayersText(waitingForPlayers):
    font = pygame.font.Font(None, 36)
    text = font.render("Waiting for other players...", True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (WIDTH // 2, HEIGHT // 2)
    waitingForPlayers.append(text)
    waitingForPlayers.append(textRect)
