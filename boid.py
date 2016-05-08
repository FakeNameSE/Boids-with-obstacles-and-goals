from __future__ import division  # required in Python 2.7

import math
import pygame
import random
from operator import itemgetter

from constants import *


class Boid(pygame.sprite.Sprite):
    def __init__(self, x, y, cohesion_weight, alignment_weight, separation_weight,
                 obstacle_avoidance_weight, goal_weight, field_of_view, max_velocity, image):
        super(Boid, self).__init__()

        # Load image as sprite
        self.image = pygame.image.load(image).convert_alpha()

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

        # Coordinates
        self.rect.x = x
        self.rect.y = y

        self.velocityX = random.randint(1, 10) / 10.0
        self.velocityY = random.randint(1, 10) / 10.0

        # === Attributes ===

        # Weights
        self.cohesion_weight = cohesion_weight
        self.alignment_weight = alignment_weight
        self.separation_weight = separation_weight
        self.obstacle_avoidance_weight = obstacle_avoidance_weight
        self.goal_weight = goal_weight

        self.field_of_view = field_of_view
        self.max_velocity = max_velocity
    def distance(self, entity, obstacle):
        """Return the distance from another boid"""

        if obstacle:
            dist_x = self.rect.x - entity.real_x
            dist_y = self.rect.y - entity.real_y

        else:
            dist_x = self.rect.x - entity.rect.x
            dist_y = self.rect.y - entity.rect.y

        return math.sqrt(dist_x * dist_x + dist_y * dist_y)

    def cohesion(self, boid_list):
        """Move closer to a set of boid_list"""

        if len(boid_list) < 1:
            return

        # calculate the average distances from the other prey_list
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
        self.velocityX -= (average_x / self.cohesion_weight)
        self.velocityY -= (average_y / self.cohesion_weight)

    def alignment(self, boid_list):
        """Move with a set of boid_list"""

        if len(boid_list) < 1:
            return

        # calculate the average velocities of the other prey_list
        average_x = 0
        average_y = 0

        for boid in boid_list:
            average_x += boid.velocityX
            average_y += boid.velocityY

        average_x /= len(boid_list)
        average_y /= len(boid_list)

        # set our velocity towards the others
        self.velocityX += (average_x / self.alignment_weight)
        self.velocityY += (average_x / self.alignment_weight)

    def separation(self, boid_list, min_distance):
        """Move away from a set of boid_list. This avoids crowding"""

        if len(boid_list) < 1:
            return

        distance_x = 0
        distance_y = 0
        num_close = 0

        for boid in boid_list:
            distance = self.distance(boid, False)

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

        self.velocityX -= distance_x / self.separation_weight
        self.velocityY -= distance_y / self.separation_weight

    def obstacle_avoidance(self, obstacle):
        """Avoid obstacles"""
        self.velocityX += -1 * (obstacle.real_x - self.rect.x) / self.obstacle_avoidance_weight
        self.velocityY += -1 * (obstacle.real_y - self.rect.y) / self.obstacle_avoidance_weight

    def goal(self, mouse_x, mouse_y):
        """Seek goal"""
        self.velocityX += (mouse_x - self.rect.x) / self.goal_weight
        self.velocityY += (mouse_y - self.rect.y) / self.goal_weight

    def attack(self, target_list):
        """Predatory behavior"""
        if len(target_list) < 1:
            self.velocityX += (SCREEN_WIDTH - self.rect.x)
            self.velocityY += (SCREEN_WIDTH - self.rect.y)
            return

        # Calculate the center of mass of target_list
        target_ids = []
        average_x = 0
        average_y = 0
        for target in target_list:
            average_x += target.rect.x
            average_y += target.rect.y

        average_x /= len(target_list)
        average_y /= len(target_list)

        # Create a 2d array containing all nearby prey and their distance from the center of mass
        for target in target_list:
            dist_x = average_x - target.rect.x
            dist_y = average_y - target.rect.y
            distance = math.sqrt(dist_x * dist_x + dist_y * dist_y)
            target_ids.append([target, distance])

        # Sort array by distance from center of mass
        target_ids = sorted(target_ids, key=itemgetter(0))

        # Set vector on intercept toward where the prey the furthest from us is going
        self.velocityX += ((target_ids[0][0].rect.x + target_ids[0][0].velocityX) - self.rect.x) / self.goal_weight
        self.velocityY += ((target_ids[0][0].rect.y + target_ids[0][0].velocityY) - self.rect.y) / self.goal_weight

    def flee(self, predator):
        """Prey behavior, avoid the predators"""
        self.velocityX += -1 * (predator.rect.x - self.rect.x) / self.obstacle_avoidance_weight
        self.velocityY += -1 * (predator.rect.y - self.rect.y) / self.obstacle_avoidance_weight

    def update(self, wrap):
        """Perform actual movement based on our velocity"""
        if wrap:
            # If we leave the screen we reappear on the other side.
            if self.rect.x < 0 and self.velocityX < 0:
                self.rect.x = SCREEN_WIDTH
            if self.rect.x > SCREEN_WIDTH and self.velocityX > 0:
                self.rect.x = 0
            if self.rect.y < 0 and self.velocityY < 0:
                self.rect.y = SCREEN_HEIGHT
            if self.rect.y > SCREEN_HEIGHT and self.velocityY > 0:
                self.rect.y = 0

        else:
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
        if abs(self.velocityX) > self.max_velocity or abs(self.velocityY) > self.max_velocity:
            scale_factor = self.max_velocity / max(abs(self.velocityX), abs(self.velocityY))
            self.velocityX *= scale_factor
            self.velocityY *= scale_factor

        self.rect.x += self.velocityX
        self.rect.y += self.velocityY
