#!/usr/bin/env python
# coding=utf-8
from __future__ import division  # required in Python 2.7

import math
# import pygame
import random
from operator import itemgetter

from modules.constants import *

# Cohesion, separation, alignment, and update methods and basic boid class design initially based off of http://www.coderholic.com/boids/
# Boid behavior algorithms and velocity normalization largely from http://www.vergenet.net/~conrad/boids/pseudocode.html

class Boid(pygame.sprite.DirtySprite):
    def __init__(self, x, y, cohesion_weight, alignment_weight, separation_weight,
                 obstacle_avoidance_weight, goal_weight, field_of_view, max_speed, image):
        # super(Boid, self).__init__()
        pygame.sprite.DirtySprite.__init__(self)

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
        self.max_speed = max_speed


    '''
    Return the distance from another sprite.
    '''
    def distance(self, other):
        if not other:
            return -1

        dist = (self.rect.x - other.rect.x, self.rect.y - other.rect.y)
        return math.sqrt(dist[0] ** 2 + dist[1] ** 2)

    '''
    Boids want to stay close to each other, have them move towards the center of mass of the flock.

    Note that boid_list is the list of boids to take into consideration when applying this rule and does not contain the current boid.

    Note that we can account for limited vision of each boid by limiting which boids get added to boid_list (for instance only boids within a certain distance). This gives each boid a "perceived flock".
    '''
    def cohesion(self, boid_list):
        # Nothing to do if no other boids nearby.
        if len(boid_list) == 0:
            return

        # Calculate the center of mass of boid_list (the center of mass of the flock as perceived by our boid).
        center = find_center_of_mass(boid_list)

        # We want to move in the direction of the vector from the current boid's position to this center of mass.
        cohesion_velocity_change = (center[0] - self.rect.x, center[1] - self.rect.y)

        # set our velocity towards the others
        self.velocityX += (cohesion_velocity_change[0] / self.cohesion_weight)
        self.velocityY += (cohesion_velocity_change[1] / self.cohesion_weight)


    '''
    Boids want to move in the same direction, have them move along direction of average velocity vector.

    Note that boid_list is the list of boids to take into consideration when applying this rule and does not contain the current boid.

    Note that we can account for limited vision of each boid by limiting which boids get added to boid_list (for instance only boids within a certain distance). This gives each boid a "perceived flock".
    '''
    def alignment(self, boid_list):
        if len(boid_list) == 0:
            return

        # calculate the average velocities of the other prey_list
        average_velocity = [0, 0]

        for boid in boid_list:
            average_velocity[0] += boid.velocityX
            average_velocity[1] += boid.velocityY

        average_velocity[0] /= len(boid_list)
        average_velocity[1] /= len(boid_list)

        # set our velocity towards the others
        self.velocityX += (average_velocity[0] / self.alignment_weight)
        self.velocityY += (average_velocity[1] / self.alignment_weight)

    '''
    Boids want to maintain some distance with respect to each other. Have them move in opposite direction of nearby boids.

    Note that boid_list is the list of boids to take into consideration when applying this rule and does not contain the current boid.

    Note that we can account for limited vision of each boid by limiting which boids get added to boid_list (for instance only boids within a certain distance). This gives each boid a "perceived flock".
    '''
    def separation(self, boid_list, min_distance):
        if len(boid_list) == 0:
            return

        separation_velocity_change = [0, 0]

        for boid in boid_list:
            if self.distance(boid) < min_distance:
                separation_velocity_change[0] += self.rect.x - boid.rect.x
                separation_velocity_change[1] += self.rect.y - boid.rect.y

        self.velocityX += separation_velocity_change[0] / self.separation_weight
        self.velocityY += separation_velocity_change[1] / self.separation_weight

    '''
    Updates velocity to move boid away from a single obstacle.

    Note: This should be called for each nearby obstacle that the boid should avoid.
    '''
    def obstacle_avoidance(self, obstacle):
        # Avoid collision with obstacles at all cost
        if self.distance(obstacle) < 45:
			self.velocityX = -1 * (obstacle.real_x - self.rect.x)
			self.velocityY = -1 * (obstacle.real_y - self.rect.y)

        else:
			self.velocityX += -1 * (obstacle.real_x - self.rect.x) / self.obstacle_avoidance_weight
			self.velocityY += -1 * (obstacle.real_y - self.rect.y) / self.obstacle_avoidance_weight

    '''
    Updates velocity to move boid towards a goal (basically the opposite of obstacle avoidance).
    '''
    def goal(self, mouse_x, mouse_y):
        self.velocityX += (mouse_x - self.rect.x) / self.goal_weight
        self.velocityY += (mouse_y - self.rect.y) / self.goal_weight

    '''Predatory behavior, updates velocity to move boid towards the nearby prey which is furthest from its visible flock.'''
    def attack(self, visible_prey):
        if len(visible_prey) == 0:
            self.go_to_middle()
            return

        center = find_center_of_mass(visible_prey)
        target_ids = []

        # Create a 2d array containing all nearby prey and their distance from the center of mass
        for target in visible_prey:
            dist_x = center[0] - target.rect.x
            dist_y = center[1] - target.rect.y
            distance = math.sqrt(dist_x * dist_x + dist_y * dist_y)
            target_ids.append([target, distance])

        # Create an list holding the prey furthest from the center of mass of its flock
        target_id = sorted(target_ids, key=itemgetter(0))
        del target_ids

        # Update velocity with vector on intercept with where the prey the furthest from the center of mass of the prey flock is going.
        self.velocityX += ((target_id[0][0].rect.x +
                            (target_id[0][0].velocityX * 2)) - self.rect.x) / self.goal_weight
        self.velocityY += ((target_id[0][0].rect.y +
                            (target_id[0][0].velocityY * 2)) - self.rect.y) / self.goal_weight

        del target_id

    '''
    Prey behavior, avoid the predator by moving in opposite direction of projected predator location. Move in a direction randomized a little from that so that the predator does not just need to outrun the prey in a straight line.
    '''
    def flee(self, predator):
        self.velocityX += -(((predator.rect.x + (2 * predator.velocityX)) - self.rect.x) /
                            self.obstacle_avoidance_weight) * random.randint(1, 2)
        self.velocityY += -(((predator.rect.y + (2 * predator.velocityY)) - self.rect.y) /
                            self.obstacle_avoidance_weight) * random.randint(1, 2)

    '''
    Update velocity to move boid towards middle of window.
    '''
    def go_to_middle(self):
        self.velocityX += (SCREEN_WIDTH / 2 - self.rect.x) / 150
        self.velocityY += (SCREEN_HEIGHT / 2 - self.rect.y) / 150

    '''
    Normalizes the velocity vector with respect to the maximum speed.
    '''
    def limit_speed(self):
        speed = math.sqrt(self.velocityX**2 + self.velocityY**2)
        if speed > self.max_speed:
            scale_factor = self.max_speed / speed
            self.velocityX *= scale_factor
            self.velocityY *= scale_factor

    '''
    Update position based off of velocity of boid.
    '''
    def update(self, wrap):
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
        # Bounce off the walls to stay on screen. We lose a random amount of velocity along the axis we collided on.
        else:
            if self.rect.x < 0 and self.velocityX < 0:
                self.velocityX = -self.velocityX * random.random()
            if self.rect.x > SCREEN_WIDTH and self.velocityX > 0:
                self.velocityX = -self.velocityX * random.random()
            if self.rect.y < 0 and self.velocityY < 0:
                self.velocityY = -self.velocityY * random.random()
            if self.rect.y > SCREEN_HEIGHT and self.velocityY > 0:
                self.velocityY = -self.velocityY * random.random()

        # Go to middle if the boid is not moving much.
        if abs(math.sqrt(self.velocityX**2 + self.velocityY**2)) < 2:
			self.go_to_middle()

        self.limit_speed()

        self.rect.x += self.velocityX
        self.rect.y += self.velocityY

        # Since the boids should always be moving, we don't have to worry about whether or not they have a dirty rect
        self.dirty = 1

'''
Utility function to compute the center of mass of a list of boids.
'''
def find_center_of_mass(boid_list):
    if len(boid_list) == 0:
        return None

    center = [0, 0]
    for boid in boid_list:
        center[0] += boid.rect.x
        center[1] += boid.rect.y
    center[0] /= len(boid_list)
    center[1] /= len(boid_list)

    return center
