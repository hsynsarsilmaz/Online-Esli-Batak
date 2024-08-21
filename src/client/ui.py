import pygame
from src.common.common import *

TEXT_COLOR = (200, 200, 200)
TEXT_HIGHLIGHT_COLOR = (200, 0, 0)
TEXT_DISABLED_ALPHA = 50


class UiElement:
    def __init__(
        self,
        value,
        normal,
        rect,
        clickable: bool = False,
        highlighted=None,
        disabled=None,
    ):
        self.value = value
        self.normal = normal
        self.rect = rect
        if clickable:
            self.highlighted = highlighted
            self.disabled = disabled
            self.disabled.set_alpha(TEXT_DISABLED_ALPHA)


class Text(UiElement):
    def __init__(self, value, size: int, position: tuple, clickable: bool):
        normal = pygame.font.Font(None, size).render(value, True, TEXT_COLOR)
        rect = normal.get_rect(center=position)
        if clickable:
            super().__init__(
                value,
                normal,
                rect,
                clickable,
                pygame.font.Font(None, size).render(value, True, TEXT_HIGHLIGHT_COLOR),
                pygame.font.Font(None, size).render(value, True, TEXT_COLOR),
            )
        else:
            super().__init__(value, normal, rect)


class Image(UiElement):
    def __init__(
        self,
        value,
        path: str,
        highlightColor: tuple,
        size: int,
        position: tuple,
        clickable: bool,
    ):
        normal = pygame.image.load(path).convert_alpha()
        normal = pygame.transform.scale(normal, (size, size))
        rect = normal.get_rect(center=position)
        highlighted = pygame.image.load(path).convert_alpha()
        # Fill all the pixels with the highlight color
        highlighted.fill((*highlightColor, 255), special_flags=pygame.BLEND_RGBA_MULT)
        disabled = pygame.image.load(path).convert_alpha()

        if clickable:
            super().__init__(
                value,
                normal,
                rect,
                clickable,
                pygame.transform.scale(highlighted, (size, size)),
                pygame.transform.scale(disabled, (size, size)),
            )
        else:
            super().__init__(value, normal, rect)


class GameUI:
    def __init__(self):
        self.waitingForPlayers = Text(
            "Waiting for players...", 50, (WIDTH // 2, HEIGHT // 2), False
        )
        self.biddingNumbers = self.createBiddingNumbers()
        self.biddingSuits = self.createBiddingSuits()
        self.passBidding = Text("Pass", 60, (1100, 300), True)
        self.makeBidding = Text("Bid", 60, (1100, 375), True)
        self.points = [
            Text("Team A: 0", 35, (1350, 20), False),
            Text("Team B: 0", 35, (1500, 20), False),
        ]
        self.winner = None

    def createBiddingNumbers(self) -> list:
        biddingNumbers = []
        positions = [
            (400, 300),
            (475, 300),
            (550, 300),
            (437, 380),
            (512, 380),
            (475, 460),
            (650, 380),
        ]

        for i in range(8, 14):
            biddingNumbers.append(Text(str(i), 80, positions[i - 8], True))

        biddingNumbers.append(Text(str(7), 80, positions[-1], True))

        return biddingNumbers

    def createWinner(self, winner: int):
        if winner == 0:
            self.winner = Text("Player 1 and 3 has won !", 50, (600, 300), False)
        else:
            self.winner = Text("Player 2 and 4 has won !", 50, (600, 300), False)

    def createBiddingSuits(self) -> list:
        suits = ["Hearts", "Spades", "Diamonds", "Clubs"]
        biddingSuits = []

        positions = [
            (750, 300),
            (825, 300),
            (750, 380),
            (825, 380),
        ]

        for i, suit in enumerate(suits):
            relativePath = f"res/img/misc/{suit}.png"
            path = resourcePath(relativePath)
            image = Image(
                suit,
                path if BUILD else relativePath,
                TEXT_HIGHLIGHT_COLOR if i % 2 == 0 else (0, 0, 0),
                50,
                positions[i],
                True,
            )
            biddingSuits.append(image)

        return biddingSuits

    def updatePoints(self, points: list):
        self.points[0].value = f"Team A: {points[0]}"
        self.points[1].value = f"Team B: {points[1]}"
        self.points[0].normal = pygame.font.Font(None, 35).render(
            self.points[0].value, True, TEXT_COLOR
        )
        self.points[1].normal = pygame.font.Font(None, 35).render(
            self.points[1].value, True, TEXT_COLOR
        )
