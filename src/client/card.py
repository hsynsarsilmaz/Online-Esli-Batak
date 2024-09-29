import pygame

from src.common.common import BUILD, resourcePath

CARD_WIDTH, CARD_HEIGHT = 125, 182
WIDTH, HEIGHT = 1600, 900

WINNER_TARGET_POSITIONS = [
    (WIDTH // 2, HEIGHT + 200),  # Self
    (WIDTH + 200, HEIGHT // 2),  # Right Player
    (WIDTH // 2, -200),  # Mate
    (-200, HEIGHT // 2),  # Left Player
]


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
        self.rect = None

    def createGrayImage(self):
        grayImage = pygame.Surface(self.image.get_size(), flags=pygame.SRCALPHA)
        grayImage.fill((128, 128, 128, 255))
        grayImage.blit(self.image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return grayImage

    def calculateWinnerVelocities(self, winner: int, myId: int):
        targetX, targetY = WINNER_TARGET_POSITIONS[(winner - myId) % 4]

        self.xVel = (targetX - self.rect.center[0]) / 60
        self.yVel = (targetY - self.rect.center[1]) / 60


def loadCardReverseImages():
    relativePath = "res/img/cards/RV.png"
    path = resourcePath(relativePath)

    cardReverse = pygame.image.load(path if BUILD else relativePath).convert_alpha()
    cardReverse = pygame.transform.scale(cardReverse, (CARD_WIDTH, CARD_HEIGHT))

    return cardReverse, pygame.transform.rotate(cardReverse, 90)


def loadCardImages(SuitsAndRanks, cards):
    for suit, rank in SuitsAndRanks:
        relativePath = f"res/img/cards/{rank}{suit}.png"
        path = resourcePath(relativePath)
        image = pygame.image.load(path if BUILD else relativePath).convert_alpha()
        image = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
        cards.append(Card(suit, rank, image))
