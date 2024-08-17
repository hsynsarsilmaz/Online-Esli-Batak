import pygame
import os
import sys

from src.common.common import BUILD

CARD_WIDTH, CARD_HEIGHT = 125, 182
WIDTH, HEIGHT = 1600, 900


class Card:

    def __init__(self, suit: str, rank: str, image: pygame.Surface):
        self.suit = suit
        self.rank = rank
        self.image = image
        self.grayImage = self.createGrayImage()
        self.reverse = None
        self.player = None
        self.visible = False
        self.xVel = 0
        self.yVel = 0
        self.frame = 0
        self.playable = False
        self.rect = self.image.get_rect()
        self.destroy = False

    def createGrayImage(self):
        grayImage = pygame.Surface(self.image.get_size(), flags=pygame.SRCALPHA)
        grayImage.fill((128, 128, 128, 255))
        grayImage.blit(self.image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return grayImage

    def calculateWinnerVelocities(self, winner: int, myId: int):
        targetX, targetY = 0, 0
        if winner == myId:
            targetX = WIDTH // 2
            targetY = HEIGHT + 200
        elif winner == (myId + 1) % 4:
            targetX = WIDTH + 200
            targetY = HEIGHT // 2
        elif winner == (myId + 2) % 4:
            targetX = WIDTH // 2
            targetY = -200
        elif winner == (myId + 3) % 4:
            targetX = -200
            targetY = HEIGHT // 2

        self.xVel = (targetX - self.rect.center[0]) / 60
        self.yVel = (targetY - self.rect.center[1]) / 60


def loadCardReverseImages():
    relativePath = "res/img/cards/RV.png"
    path = resourcePath(relativePath)
    cardReverseVertical = pygame.image.load(
        path if BUILD else relativePath
    ).convert_alpha()
    cardReverseVertical = pygame.transform.scale(
        cardReverseVertical, (CARD_WIDTH, CARD_HEIGHT)
    )
    cardReverseHorizontal = pygame.image.load(
        path if BUILD else relativePath
    ).convert_alpha()
    cardReverseHorizontal = pygame.transform.scale(
        cardReverseHorizontal, (CARD_WIDTH, CARD_HEIGHT)
    )
    cardReverseHorizontal = pygame.transform.rotate(cardReverseHorizontal, 90)

    return cardReverseVertical, cardReverseHorizontal


def resourcePath(relativePath):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relativePath)


def loadCardImages(SuitsAndRanks, cards):
    for suit, rank in SuitsAndRanks:
        relativePath = f"res/img/cards/{rank}{suit}.png"
        path = resourcePath(relativePath)
        image = pygame.image.load(path if BUILD else relativePath).convert_alpha()
        image = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
        cards.append(Card(suit, rank, image))
