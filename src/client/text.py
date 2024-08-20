import pygame
from src.common.common import *

TEXT_COLOR = (200, 200, 200)
TEXT_HIGHLIGHT_COLOR = (200, 0, 0)


class GameText:
    def __init__(self):
        self.waitingForPlayers = self.createWaitingForPlayers()
        self.biddingNumbers = self.createBiddingNumbers()
        self.biddingSuites = self.createBiddingSuites()
        self.bidValues = []
        # Temporary
        self.skipBidding = self.createSkipBidding()
        self.winner = None

    def createBiddingNumbers(self) -> list:
        biddingNumbers = []
        font = pygame.font.Font(None, 80)

        positions = [
            (400, 300),  # 8
            (475, 300),  # 9
            (550, 300),  # 10
            (437, 380),  # 11
            (512, 380),  # 12
            (475, 460),  # 13
        ]

        for i in range(8, 14):
            text = font.render(str(i), True, TEXT_COLOR)
            highlightedText = font.render(str(i), True, TEXT_HIGHLIGHT_COLOR)
            rect = text.get_rect(center=(positions[i - 8]))
            biddingNumbers.append((text, highlightedText, rect))

        return biddingNumbers

    def createBiddingSuites(self) -> list:
        suites = ["H", "S", "D", "C"]
        biddingSuites = []
        font = pygame.font.Font(None, 80)

        # Manually defined positions for a 2x2 rectangle, with a slight gap from the numbers
        positions = [
            (750, 300),  # H (top-left)
            (825, 300),  # S (top-right)
            (750, 380),  # D (bottom-left)
            (825, 380),  # C (bottom-right)
        ]

        for i in range(4):
            text = font.render(suites[i], True, TEXT_COLOR)
            highlightedText = font.render(suites[i], True, TEXT_HIGHLIGHT_COLOR)
            rect = text.get_rect(center=positions[i])
            biddingSuites.append((text, highlightedText, rect))

        return biddingSuites

    def createWaitingForPlayers(self) -> tuple:
        font = pygame.font.Font(None, 36)
        text = font.render("Waiting for other players...", True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (WIDTH // 2, HEIGHT // 2)

        return (text, textRect)

    # temporary
    def createSkipBidding(self) -> tuple:
        font = pygame.font.Font(None, 60)
        text = font.render("Pass", True, TEXT_COLOR)
        highligtedText = font.render("Pass", True, TEXT_HIGHLIGHT_COLOR)
        textRect = text.get_rect()
        textRect.center = (1100, 300)

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
