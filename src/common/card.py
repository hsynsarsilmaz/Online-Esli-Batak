import pygame

CARD_WIDTH, CARD_HEIGHT = 125, 182
class Card:
    def __init__(self, suit : str, rank : str, image : pygame.Surface):
        self.suit = suit
        self.rank = rank
        self.image = image
        self.reverse = None
        self.player = None
        self.xPos = 0
        self.yPos = 0
        self.visible = False

def loadCardReverseImages():
    cardReverseVertical = pygame.image.load("res/img/cards/RV.png").convert_alpha()
    cardReverseVertical = pygame.transform.scale(cardReverseVertical, (CARD_WIDTH, CARD_HEIGHT))
    cardReverseHorizontal = pygame.image.load("res/img/cards/RV.png").convert_alpha()
    cardReverseHorizontal = pygame.transform.scale(cardReverseHorizontal, (CARD_WIDTH, CARD_HEIGHT))
    cardReverseHorizontal = pygame.transform.rotate(cardReverseHorizontal, 90)

    return cardReverseVertical, cardReverseHorizontal

def loadCardImages(SuitsAndRanks,cards):
    for suit,rank in SuitsAndRanks:
        image = pygame.image.load(f"res/img/cards/{rank}{suit}.png").convert_alpha()
        image = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
        cards.append(Card(suit, rank ,image))

def dealCards(cardReverseVertical,cardReverseHorizontal, cards):
     for i in range(4):
        for j in range(13):
            c = cards[j + i*13]
            if(i == 0):
                c.xPos = 317 + j * 70
                c.yPos = 668
                c.reverse = cardReverseVertical
                c.visible = True
            elif(i == 1):
                c.xPos = 68 
                c.yPos = 88  + j * 50
                c.reverse = cardReverseHorizontal
            elif(i == 2):
                c.xPos = 317 + j * 70
                c.yPos = 50
                c.reverse = cardReverseVertical
            elif(i == 3):
                c.xPos = 1350 
                c.yPos = 88  + j * 50
                c.reverse = cardReverseHorizontal

def loadCards(SuitsAndRanks, cards):
    cardReverseVertical, cardReverseHorizontal = loadCardReverseImages()
    loadCardImages(SuitsAndRanks,cards)
    dealCards(cardReverseVertical,cardReverseHorizontal, cards)