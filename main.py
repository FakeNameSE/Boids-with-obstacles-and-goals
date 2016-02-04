#!/usr/bin/env python
# Prey implementation in Python using PyGame

from __future__ import division # required in Python 2.7

import sys
import pygame
import random
import math

# === constants === (UPPER_CASE names)

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 1024

BLACK = (0, 0, 0)

MAX_PREY_VELOCITY = 10
MAX_PREDATOR_VELOCITY = 12
NUM_PREY = 50
NUM_PREDATORS = 10

BORDER = 25

# === classes === (CamelCase names for classes / lower_case names for method)

class Prey(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super(Prey, self).__init__()

        # Load image as sprite
        self.image = pygame.image.load("ressources/img/prey.png").convert()

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

        # Coordinates
        self.rect.x = x
        self.rect.y = y

#        self.velocityX = random.randint(-10, 10) / 10.0
#        self.velocityY = random.randint(-10, 10) / 10.0

        self.velocityX = random.randint(1, 10) / 10.0
        self.velocityY = random.randint(1, 10) / 10.0

    def distance(self, prey):
        '''Return the distance from another prey'''

        distX = self.rect.x - prey.rect.x
        distY = self.rect.y - prey.rect.y

        return math.sqrt(distX * distX + distY * distY)

    def move_closer(self, prey_list):
        '''Move closer to a set of prey_list'''

        if len(prey_list) < 1:
            return

        # calculate the average distances from the other prey_list
        avgX = 0
        avgY = 0
        for prey in prey_list:
            if prey.rect.x == self.rect.x and prey.rect.y == self.rect.y:
                continue

            avgX += (self.rect.x - prey.rect.x)
            avgY += (self.rect.y - prey.rect.y)

        avgX /= len(prey_list)
        avgY /= len(prey_list)

        # set our velocity towards the others
        distance = math.sqrt((avgX * avgX) + (avgY * avgY)) * -1.0

        self.velocityX -= (avgX / 100)
        self.velocityY -= (avgY / 100)


    def move_with(self, prey_list):
        '''Move with a set of prey_list'''

        if len(prey_list) < 1:
            return

        # calculate the average velocities of the other prey_list
        avgX = 0
        avgY = 0

        for prey in prey_list:
            avgX += prey.velocityX
            avgY += prey.velocityY

        avgX /= len(prey_list)
        avgY /= len(prey_list)

        # set our velocity towards the others
        self.velocityX += (avgX / 40)
        self.velocityY += (avgY / 40)

    def move_away(self, prey_list, minDistance):
        '''Move away from a set of prey_list. This avoids crowding'''

        if len(prey_list) < 1:
            return

        distanceX = 0
        distanceY = 0
        numClose = 0

        for prey in prey_list:
            distance = self.distance(prey)

            if  distance < minDistance:
                numClose += 1
                xdiff = (self.rect.x - prey.rect.x)
                ydiff = (self.rect.y - prey.rect.y)

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

        self.velocityX -= distanceX / 5
        self.velocityY -= distanceY / 5

    def defend(self, predator_list):
        nearest_predator = None
        shortest_distance = None

        for predator in predator_list:
            distX = self.rect.x - predator.rect.x
            distY = self.rect.y - predator.rect.y
            d = distX*distX+distY*distY
            if not shortest_distance or d < shortest_distance:
                shortest_distance = d
                nearest_predator = predator

            # do something with nearest_prey, shortest_distance
            trajectory_x = self.rect.x - nearest_predator.rect.x
            trajectory_y = self.rect.y - nearest_predator.rect.y

            self.velocityX += trajectory_x
            self.velocityY += trajectory_y

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

class Predator(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super(Predator, self).__init__()

        # Load image as sprite
        self.image = pygame.image.load("ressources/img/predator.png").convert()

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

        # Coordinates
        self.rect.x = x
        self.rect.y = y

#        self.velocityX = random.randint(-10, 10) / 10.0
#        self.velocityY = random.randint(-10, 10) / 10.0

        self.velocityX = random.randint(1, 10) / 10.0
        self.velocityY = random.randint(1, 10) / 10.0

    def distance(self, predator):
        '''Return the distance from another prey'''

        distX = self.rect.x - predator.rect.x
        distY = self.rect.y - predator.rect.y

        return math.sqrt(distX * distX + distY * distY)

    def move_closer(self, predator_list):
        '''Move closer to a set of prey_list'''

        if len(predator_list) < 1:
            return

        # calculate the average distances from the other prey_list
        avgX = 0
        avgY = 0
        for predator in predator_list:
            if predator.rect.x == self.rect.x and predator.rect.y == self.rect.y:
                continue

            avgX += (self.rect.x - predator.rect.x)
            avgY += (self.rect.y - predator.rect.y)

        avgX /= len(predator_list)
        avgY /= len(predator_list)

        # set our velocity towards the others
        distance = math.sqrt((avgX * avgX) + (avgY * avgY)) * -1.0

        self.velocityX -= (avgX / 100)
        self.velocityY -= (avgY / 100)


    def move_with(self, predator_list):
        '''Move with a set of prey_list'''

        if len(predator_list) < 1:
            return

        # calculate the average velocities of the other prey_list
        avgX = 0
        avgY = 0

        for predator in predator_list:
            avgX += predator.velocityX
            avgY += predator.velocityY

        avgX /= len(predator_list)
        avgY /= len(predator_list)

        # set our velocity towards the others
        self.velocityX += (avgX / 40)
        self.velocityY += (avgY / 40)

    def move_away(self, predator_list, minDistance):
        '''Move away from a set of prey_list. This avoids crowding'''

        if len(prey_list) < 1:
            return

        distanceX = 0
        distanceY = 0
        numClose = 0

        for predator in predator_list:
            distance = self.distance(predator)

            if  distance < minDistance:
                numClose += 1
                xdiff = (self.rect.x - predator.rect.x)
                ydiff = (self.rect.y - predator.rect.y)

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

        self.velocityX -= distanceX / 5
        self.velocityY -= distanceY / 5


    def attack(self, prey_list):
        nearest_prey = None
        shortest_distance = None

        for prey in prey_list:
            distX = self.rect.x - prey.rect.x
            distY = self.rect.y - prey.rect.y
            d = distX*distX+distY*distY
            if not shortest_distance or d < shortest_distance:
                shortest_distance = d
                nearest_prey = prey

            # do something with nearest_prey, shortest_distance
            trajectory_x = self.rect.x - nearest_prey.rect.x
            trajectory_y = self.rect.y - nearest_prey.rect.y

            self.velocityX -= trajectory_x
            self.velocityY -= trajectory_y

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

        if abs(self.velocityX) > MAX_PREDATOR_VELOCITY or abs(self.velocityY) > MAX_PREDATOR_VELOCITY:
            scaleFactor = MAX_PREDATOR_VELOCITY / max(abs(self.velocityX), abs(self.velocityY))
            self.velocityX *= scaleFactor
            self.velocityY *= scaleFactor

        self.rect.x += self.velocityX
        self.rect.y += self.velocityY

# === main === (lower_case names)

# --- init ---

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
#screen_rect = screen.get_rect()

# --- objects ---

# lists
# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
prey_list = pygame.sprite.Group()
predator_list = pygame.sprite.Group()

# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

# create prey_list at random positions
for i in range(NUM_PREY):
    prey = Prey(random.randint(0, SCREEN_WIDTH - 100), random.randint(0, SCREEN_HEIGHT - 100))
    # Add the prey to the list of objects
    prey_list.add(prey)
    all_sprites_list.add(prey)

# create predators at random positions
for i in range(NUM_PREDATORS):
    predator = Predator(random.randint(SCREEN_WIDTH - 100, SCREEN_WIDTH), random.randint(SCREEN_HEIGHT - 100, SCREEN_HEIGHT))
    # Add the prey to the list of objects
    predator_list.add(predator)
    all_sprites_list.add(predator)

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

    # --- updates ---

    for prey in prey_list:
        closeprey = []
        for otherprey in prey_list:
            if otherprey == prey:
                continue
            distance = prey.distance(otherprey)
            if distance < 200:
                closeprey.append(otherprey)

        prey.move_closer(closeprey)
        prey.move_with(closeprey)
        prey.move_away(closeprey, 20)
        prey.defend(predator_list)
        prey.update()

    for predator in predator_list:
        closepredator = []
        for otherpredator in predator_list:
            if otherpredator == predator:
                continue
            distance = predator.distance(otherpredator)
            if distance < 200:
                closepredator.append(otherpredator)

        predator.move_closer(closepredator)
        predator.move_with(closepredator)
        predator.move_away(closepredator, 20)
        predator.attack(prey_list)

        predator.update()

    # Calls update() method on every sprite in the list
    #all_sprites_list.update()

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
