#!/usr/bin/env python
# coding=utf-8
from modules import pygame

pygame.init()
flags = pygame.DOUBLEBUF
# === constants ===

infoObject = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h - 40
pygame.quit()

BLACK = (0, 0, 0)
RED = (255, 0, 0)

MAX_BOID_VELOCITY = 8
NUM_BOIDS = 55
NUM_PREY = 70
NUM_PREDATORS = 5
MAX_PREY_VELOCITY = 8
MAX_PREDATOR_VELOCITY = 8.5
NUM_OBSTACLES = 17
BORDER = 30
FIELD_OF_VIEW = 70
