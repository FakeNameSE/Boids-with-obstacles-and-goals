#!/usr/bin/env python
# coding=utf-8
from modules.constants import *


class Obstacle(pygame.sprite.DirtySprite):
    def __init__(self, x, y):
        pygame.sprite.DirtySprite.__init__(self)

        # Draw obstacles (squares)
        self.image = pygame.Surface([30, 30])
        self.image.fill(RED)

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

        # Coordinates
        self.rect.x = x
        self.rect.y = y

        # Actual coordinates (center of block)
        self.real_x = self.rect.x + 15
        self.real_y = self.rect.y + 15

        self.dirty = 0

    def update(self):
        """Just in case I want to expand this"""
        pass
