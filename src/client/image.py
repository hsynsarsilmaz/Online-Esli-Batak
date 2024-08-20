import pygame
from src.common.common import *


def createBiddingSuits() -> list:
    suits = ["Hearts", "Spades", "Clubs", "Diamonds"]
    biddingSuits = []
    imageSize = 50

    positions = [
        (750, 300),
        (825, 300),
        (750, 380),
        (825, 380),
    ]

    for suit in suits:
        relativePaths = [
            f"res/img/misc/{suit}.png",
            f"res/img/misc/{suit}2.png",
        ]
        paths = [resourcePath(relativePath) for relativePath in relativePaths]
        image = pygame.image.load(
            paths[0] if BUILD else relativePaths[0]
        ).convert_alpha()
        highlighted = pygame.image.load(
            paths[1] if BUILD else relativePaths[1]
        ).convert_alpha()
        image = pygame.transform.scale(image, (imageSize, imageSize))
        highlighted = pygame.transform.scale(highlighted, (imageSize, imageSize))
        rect = image.get_rect(center=(positions[suits.index(suit)]))
        biddingSuits.append((image, highlighted, rect))

    return biddingSuits
