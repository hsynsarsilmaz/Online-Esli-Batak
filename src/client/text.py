import pygame
from src.common.common import *

TEXT_COLOR = (200, 200, 200)
TEXT_HIGHLIGHT_COLOR = (200, 0, 0)


class GameText:
    def __init__(self):
        self.waitingForPlayers = self.createWaitingForPlayers()
        self.biddingNumbers = self.createBiddingNumbers()
        self.bidValues = []
        self.passBidding = self.createPassBidding()
        self.makeBidding = self.createMakeBidding()
        self.winner = None

    def createBiddingNumbers(self) -> list:
        biddingNumbers = []
        font = pygame.font.Font(None, 80)

        positions = [
            (400, 300),
            (475, 300),
            (550, 300),
            (437, 380),
            (512, 380),
            (475, 460),
        ]

        for i in range(8, 14):
            text = font.render(str(i), True, TEXT_COLOR)
            highlightedText = font.render(str(i), True, TEXT_HIGHLIGHT_COLOR)
            rect = text.get_rect(center=(positions[i - 8]))
            biddingNumbers.append((text, highlightedText, rect))

        return biddingNumbers

    def createWaitingForPlayers(self) -> tuple:
        font = pygame.font.Font(None, 36)
        text = font.render("Waiting for other players...", True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (WIDTH // 2, HEIGHT // 2)

        return (text, textRect)

    def createPassBidding(self) -> tuple:
        font = pygame.font.Font(None, 60)
        text = font.render("Pass", True, TEXT_COLOR)
        highligtedText = font.render("Pass", True, TEXT_HIGHLIGHT_COLOR)
        disabledText = font.render("Pass", True, TEXT_COLOR)
        disabledText.set_alpha(50)
        textRect = text.get_rect()
        textRect.center = (1100, 300)

        return (text, highligtedText, textRect)

    def createMakeBidding(self) -> tuple:
        font = pygame.font.Font(None, 60)
        text = font.render("Bid", True, TEXT_COLOR)
        highligtedText = font.render("Bid", True, TEXT_HIGHLIGHT_COLOR)
        disabledText = font.render("Pass", True, TEXT_COLOR)
        disabledText.set_alpha(50)
        textRect = text.get_rect()
        textRect.center = (1100, 375)

        return (text, highligtedText, textRect)

    def createBidValues(self, bid: int, trump: str):
        font = pygame.font.Font(None, 50)
        text = font.render(f"Bid : {bid} {trump}", True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.topleft = (20, 20)

        self.bidValues = (text, textRect)

    def createWinner(self, winner: int):
        font = pygame.font.Font(None, 50)
        if winner == 0:
            text = font.render(f"Player 1 and 3 has won !", True, (255, 255, 255))
        else:
            text = font.render(f"Player 2 and 4 has won !", True, (255, 255, 255))

        textRect = text.get_rect()
        textRect.topleft = (20, 20)

        self.winner = (text, textRect)
