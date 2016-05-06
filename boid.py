from __future__ import division  # required in Python 2.7

import math
import pygame
import random

from constants import *

# === weights ===

COHESION_WEIGHT = 100
ALIGNMENT_WEIGHT = 40
SEPARATION_WEIGHT = 5
OBSTACLE_AVOIDANCE_WEIGHT = 10
GOAL_WEIGHT = 100


class Boid(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Boid, self).__init__()

        # Load image as sprite
        self.image = pygame.image.load("resources/img/boid.png").convert()

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

        # Coordinates
        self.rect.x = x
        self.rect.y = y

        self.velocityX = random.randint(1, 10) / 10.0
        self.velocityY = random.randint(1, 10) / 10.0

    def distance(self, boid):
        """Return the distance from another boid"""

        dist_x = self.rect.x - boid.rect.x
        dist_y = self.rect.y - boid.rect.y

        return math.sqrt(dist_x * dist_x + dist_y * dist_y)

    def cohesion(self, boid_list):
        """Move closer to a set of boid_list"""

        if len(boid_list) < 1:
            return

        # calculate the average distances from the other boid_list
        average_x = 0
        average_y = 0
        for boid in boid_list:
            if boid.rect.x == self.rect.x and boid.rect.y == self.rect.y:
                continue

            average_x += (self.rect.x - boid.rect.x)
            average_y += (self.rect.y - boid.rect.y)

        average_x /= len(boid_list)
        average_y /= len(boid_list)

        # set our velocity towards the others
        self.velocityX -= (average_x / COHESION_WEIGHT)
        self.velocityY -= (average_y / COHESION_WEIGHT)

    def alignment(self, boid_list):
        """Move with a set of boid_list"""

        if len(boid_list) < 1:
            return

        # calculate the average velocities of the other boid_list
        average_x = 0
        average_y = 0

        for boid in boid_list:
            average_x += boid.velocityX
            average_y += boid.velocityY

        average_x /= len(boid_list)
        average_y /= len(boid_list)

        # set our velocity towards the others
        self.velocityX += (average_x / ALIGNMENT_WEIGHT)
        self.velocityY += (average_x / ALIGNMENT_WEIGHT)

    def separation(self, boid_list, min_distance):
        """Move away from a set of boid_list. This avoids crowding"""

        if len(boid_list) < 1:
            return

        distance_x = 0
        distance_y = 0
        num_close = 0

        for boid in boid_list:
            distance = self.distance(boid)

            if distance < min_distance:
                num_close += 1
                xdiff = (self.rect.x - boid.rect.x)
                ydiff = (self.rect.y - boid.rect.y)

                if xdiff >= 0:
                    xdiff = math.sqrt(min_distance) - xdiff
                elif xdiff < 0:
                    xdiff = -math.sqrt(min_distance) - xdiff

                if ydiff >= 0:
                    ydiff = math.sqrt(min_distance) - ydiff
                elif ydiff < 0:
                    ydiff = -math.sqrt(min_distance) - ydiff

                distance_x += xdiff
                distance_y += ydiff

        if num_close == 0:
            return

        self.velocityX -= distance_x / SEPARATION_WEIGHT
        self.velocityY -= distance_y / SEPARATION_WEIGHT

    def obstacle_avoidance(self, obstacle):
        """Avoid obstacles"""
        self.velocityX += -1 * (obstacle.rect.x - self.rect.x) / OBSTACLE_AVOIDANCE_WEIGHT
        self.velocityY += -1 * (obstacle.rect.y - self.rect.y) / OBSTACLE_AVOIDANCE_WEIGHT

    def goal(self, mouse_x, mouse_y):
        """Seek goal"""
        self.velocityX += (mouse_x - self.rect.x) / GOAL_WEIGHT
        self.velocityY += (mouse_y - self.rect.y) / GOAL_WEIGHT

    def update(self):
        """Perform actual movement based on our velocity"""

        # ensure they stay within the screen space
        # if we rebound we can lose some of our velocity
        if self.rect.x < BORDER and self.velocityX < 0:
            self.velocityX = -self.velocityX * random.random()
        if self.rect.x > SCREEN_WIDTH - BORDER and self.velocityX > 0:
            self.velocityX = -self.velocityX * random.random()
        if self.rect.y < BORDER and self.velocityY < 0:
            self.velocityY = -self.velocityY * random.random()
        if self.rect.y > SCREEN_HEIGHT - BORDER and self.velocityY > 0:
            self.velocityY = -self.velocityY * random.random()

        # Obey speed limit
        if abs(self.velocityX) > MAX_BOID_VELOCITY or abs(self.velocityY) > MAX_BOID_VELOCITY:
            scale_factor = MAX_BOID_VELOCITY / max(abs(self.velocityX), abs(self.velocityY))
            self.velocityX *= scale_factor
            self.velocityY *= scale_factor

        self.rect.x += self.velocityX
        self.rect.y += self.velocityY
