#!/usr/bin/env python
# Boid implementation in Python using PyGame

from __future__ import division # required in Python 2.7

import sys
import pygame
import random
import math

# === constants ===

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 900
BLACK = (0, 0, 0)
RED   = (255, 0, 0)

MAX_PREY_VELOCITY = 8
MAX_PREDATOR_VELOCITY = 12
NUM_BOIDS = 50
NUM_OBSTACLES = 15
BORDER = 25

# === weights ===

COHESION_WEIGHT = 100
ALIGNMENT_WEIGHT = 40
SEPERATION_WEIGHT = 5
OBSTACLE_AVOIDANCE_WEIGHT = 10
GOAL_WEIGHT = 100

# === classes ===

class Boid(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super(Boid, self).__init__()

        # Load image as sprite
        self.image = pygame.image.load("ressources/img/boid.png").convert()

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

        # Coordinates
        self.rect.x = x
        self.rect.y = y
        
        self.velocityX = random.randint(1, 10) / 10.0
        self.velocityY = random.randint(1, 10) / 10.0

    def distance(self, boid):
        '''Return the distance from another boid'''

        distX = self.rect.x - boid.rect.x
        distY = self.rect.y - boid.rect.y

        return math.sqrt(distX * distX + distY * distY)

    def cohesion(self, boid_list):
        '''Move closer to a set of boid_list'''

        if len(boid_list) < 1:
            return

        # calculate the average distances from the other boid_list
        avgX = 0
        avgY = 0
        for boid in boid_list:
            if boid.rect.x == self.rect.x and boid.rect.y == self.rect.y:
                continue

            avgX += (self.rect.x - boid.rect.x)
            avgY += (self.rect.y - boid.rect.y)

        avgX /= len(boid_list)
        avgY /= len(boid_list)

        # set our velocity towards the others
        distance = math.sqrt((avgX * avgX) + (avgY * avgY)) * -1.0

        self.velocityX -= (avgX / COHESION_WEIGHT)
        self.velocityY -= (avgY / COHESION_WEIGHT)


    def alignment(self, boid_list):
        '''Move with a set of boid_list'''

        if len(boid_list) < 1:
            return

        # calculate the average velocities of the other boid_list
        avgX = 0
        avgY = 0

        for boid in boid_list:
            avgX += boid.velocityX
            avgY += boid.velocityY

        avgX /= len(boid_list)
        avgY /= len(boid_list)

        # set our velocity towards the others
        self.velocityX += (avgX / ALIGNMENT_WEIGHT)
        self.velocityY += (avgY / ALIGNMENT_WEIGHT)

    def seperation(self, boid_list, minDistance):
        '''Move away from a set of boid_list. This avoids crowding'''

        if len(boid_list) < 1:
            return

        distanceX = 0
        distanceY = 0
        numClose = 0

        for boid in boid_list:
            distance = self.distance(boid)

            if  distance < minDistance:
                numClose += 1
                xdiff = (self.rect.x - boid.rect.x)
                ydiff = (self.rect.y - boid.rect.y)

                if xdiff >= 0:
                    xdiff = math.sqrt(minDistance) - xdiff
                elif xdiff < 0:
                    xdiff = -math.sqrt(minDistance) - xdiff

                if ydiff >= 0:
                    ydiff = math.sqrt(minDistance) - ydiff
                elif ydiff < 0:
                    ydiff = -math.sqrt(minDistance) - ydiff

                distanceX += xdiff
                distanceY += ydiff

        if numClose == 0:
            return

        self.velocityX -= distanceX / SEPERATION_WEIGHT
        self.velocityY -= distanceY / SEPERATION_WEIGHT
        
    def obstacle_avoidance(self, obstacle):
        '''Avoid obstacles'''
        self.velocityX += -1 * (obstacle.rect.x - self.rect.x) / OBSTACLE_AVOIDANCE_WEIGHT
        self.velocityY += -1 * (obstacle.rect.y - self.rect.y) / OBSTACLE_AVOIDANCE_WEIGHT

    def goal(self, mouse_x, mouse_y):
        self.velocityX += (mouse_x - self.rect.x) / GOAL_WEIGHT
        self.velocityY += (mouse_y - self.rect.y) / GOAL_WEIGHT

    def update(self):
        '''Perform actual movement based on our velocity'''

        # ensure they stay within the screen space
        # if we roubound we can lose some of our velocity
        if self.rect.x < BORDER and self.velocityX < 0:
            self.velocityX = -self.velocityX * random.random()
        if self.rect.x > SCREEN_WIDTH - BORDER and self.velocityX > 0:
            self.velocityX = -self.velocityX * random.random()
        if self.rect.y < BORDER and self.velocityY < 0:
            self.velocityY = -self.velocityY * random.random()
        if self.rect.y > SCREEN_HEIGHT - BORDER and self.velocityY > 0:
            self.velocityY = -self.velocityY * random.random()

        if abs(self.velocityX) > MAX_PREY_VELOCITY or abs(self.velocityY) > MAX_PREY_VELOCITY:
            scaleFactor = MAX_PREY_VELOCITY / max(abs(self.velocityX), abs(self.velocityY))
            self.velocityX *= scaleFactor
            self.velocityY *= scaleFactor

        self.rect.x += self.velocityX
        self.rect.y += self.velocityY

class Obstacle(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super(Obstacle, self).__init__()

        # Load image as sprite
        #self.image = pygame.image.load("ressources/img/predator.png").convert()
        self.image = pygame.Surface([30, 30])
        self.image.fill(RED)

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

        # Coordinates
        self.rect.x = x
        self.rect.y = y
        
    def update(self):
        pass

# === main === (lower_case names)

# --- init ---

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)

# Set the title of the window
pygame.display.set_caption('Boids')

# --- objects ---

# lists
boid_list = pygame.sprite.Group()
obstacle_list = pygame.sprite.Group()
# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

# create boids and obstacles at random positions on the screen
for i in range(NUM_BOIDS):
    boid = Boid(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
    # Add the boid to the list of objects
    boid_list.add(boid)
    all_sprites_list.add(boid)

for i in range(NUM_OBSTACLES):
    obstacle = Obstacle(random.randint(0 + BORDER, SCREEN_WIDTH - BORDER), random.randint(0 + BORDER, SCREEN_HEIGHT - BORDER))
    obstacle_list.add(obstacle)
    all_sprites_list.add(obstacle)

# --- mainloop ---

clock = pygame.time.Clock()

running = True

while running:

    # --- events ---

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    pos = pygame.mouse.get_pos()
    mouse_x = pos[0]
    mouse_y = pos[1]

    # --- updates ---
    for boid in boid_list:
        closeboid = []
        obstacles = []
        avoid = False
        for otherboid in boid_list:
            if otherboid == boid:
                continue
            distance = boid.distance(otherboid)
            if distance < 200:
                closeboid.append(otherboid)
        for obstacle in obstacle_list:
            distance = boid.distance(obstacle)
            if distance < 50:
                avoid = True
                
        boid.cohesion(closeboid)
        boid.alignment(closeboid)
        boid.seperation(closeboid, 20)
        if avoid == True:
            boid.obstacle_avoidance(obstacle)
        boid.goal(mouse_x, mouse_y)
        boid.update()
        
    for boid in boid_list:
		collisions = pygame.sprite.spritecollide(boid, obstacle_list, False)
		for obstacle in collisions:
			boid.velocityX *= -1
			boid.velocityY *= -1
	
    # --- draws ---

    screen.fill(BLACK)

    # Draw all the spites
    all_sprites_list.draw(screen)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    pygame.time.delay(10)
    # Used to manage how fast the screen updates
    clock.tick(120)

# --- the end ---
pygame.quit()
sys.exit()
