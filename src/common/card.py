import pygame

CARD_WIDTH, CARD_HEIGHT = 125, 182


class Card:

    def __init__(self, suit: str, rank: str, image: pygame.Surface):
        self.suit = suit
        self.rank = rank
        self.image = image
        self.reverse = None
        self.player = None
        self.visible = False
        self.xVel = 0
        self.yVel = 0
        self.frame = 0
        self.rect = self.image.get_rect()

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
