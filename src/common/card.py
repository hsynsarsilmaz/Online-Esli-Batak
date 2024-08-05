import pygame

class card:
    def __init__(self, suit : str, rank : str, image : pygame.Surface):
        self.suit = suit
        self.rank = rank
        self.image = image
        self.player = None
