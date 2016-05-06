import pygame

from constants import *


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Obstacle, self).__init__()

        # Draw obstacles (squares)
        self.image = pygame.Surface([30, 30])
        self.image.fill(RED)

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

        # Coordinates
        self.rect.x = x
        self.rect.y = y

    def update(self):
        """Just in case I want to expand this"""
        pass
