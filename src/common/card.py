import pygame

class card:
    def __init__(self, suit : str, rank : str, image : pygame.Surface):
        self.suit = suit
        self.rank = rank
        self.image = image
        self.reverse = None
        self.player = None
        self.xPos = 0
        self.yPos = 0
        self.visible = False
