import pygame

pygame.init()

# === constants ===

infoObject = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h - 40
pygame.quit()

BLACK = (0, 0, 0)
RED = (255, 0, 0)

MAX_BOID_VELOCITY = 8
NUM_BOIDS = 55
NUM_OBSTACLES = 17
BORDER = 30
