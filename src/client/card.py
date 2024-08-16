import pygame

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
    cardReverseVertical = pygame.image.load("res/img/cards/RV.png").convert_alpha()
    cardReverseVertical = pygame.transform.scale(
        cardReverseVertical, (CARD_WIDTH, CARD_HEIGHT)
    )
    cardReverseHorizontal = pygame.image.load("res/img/cards/RV.png").convert_alpha()
    cardReverseHorizontal = pygame.transform.scale(
        cardReverseHorizontal, (CARD_WIDTH, CARD_HEIGHT)
    )
    cardReverseHorizontal = pygame.transform.rotate(cardReverseHorizontal, 90)

    return cardReverseVertical, cardReverseHorizontal


def loadCardImages(SuitsAndRanks, cards):
    for suit, rank in SuitsAndRanks:
        image = pygame.image.load(f"res/img/cards/{rank}{suit}.png").convert_alpha()
        image = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
        cards.append(Card(suit, rank, image))
