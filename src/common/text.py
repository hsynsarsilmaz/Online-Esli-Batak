import pygame
from .gamelogic import WIDTH, HEIGHT

TEXT_COLOR = (200,200,200)
TEXT_HIGHLIGHT_COLOR = (200,0,0)

class GameText:
    def __init__(self):
        self.waitingForPlayers = self.createWaitingForPlayers()
        self.biddingNumbers = self.createBiddingNumbers()
        self.biddingSuites = self.createBiddingSuites()
        self.bidValues = []
        #Temporary
        self.skipBidding = self.createSkipBidding()

    def createBiddingNumbers(self) -> list:
        biddingNumbers = []
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

        return biddingNumbers

    def createBiddingSuites(self) -> list:
        suites= ["H", "S", "D", "C"]
        biddingSuites = []
        font = pygame.font.Font(None, 80)

        for i in range(4):
            text = font.render(suites[i], True, TEXT_COLOR)
            highligtedText = font.render(suites[i], True, TEXT_HIGHLIGHT_COLOR)
            xPos = 800 + 75 * i
            yPos = 300
            rect = text.get_rect(center=(xPos,yPos))
            biddingSuites.append((text, highligtedText, rect))

        return biddingSuites

    def createWaitingForPlayers(self) -> tuple:
        font = pygame.font.Font(None, 36)
        text = font.render("Waiting for other players...", True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (WIDTH // 2, HEIGHT // 2)
        
        return (text, textRect)
    
    def createSkipBidding(self) -> tuple:
        font = pygame.font.Font(None, 36)
        text = font.render("Skip Bidding", True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (WIDTH // 2, HEIGHT // 2)
        
        return (text, textRect)
    
    def createBidValues(self,bid : int, trump : str):
        font = pygame.font.Font(None, 50)
        text = font.render(f"Bid : {bid} {trump}", True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.topleft = (20, 20)
        
        self.bidValues = (text, textRect)