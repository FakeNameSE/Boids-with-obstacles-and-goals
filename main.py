#!/usr/bin/env python
# Prey implementation in Python using PyGame

import sys, pygame, random, math

pygame.init()

size = width, height = 800, 600
black = 0, 0, 0

maxVelocity = 10
numBoids = 50

# lists
# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
prey_list = pygame.sprite.Group()

# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

class Prey(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Prey, self).__init__()

        # Load image as sprite
        prey_image = pygame.image.load("ressources/img/prey.png").convert()
        self.image = prey_image

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

        # Coordinates
        self.rect.x = x
        self.rect.y = y

        self.velocityX = random.randint(1, 10) / -10.0
        self.velocityY = random.randint(1, 10) / -10.0

    "Return the distance from another prey"
    def distance(self, prey):
        distX = self.rect.x - prey.rect.x
        distY = self.rect.y - prey.rect.y
        return math.sqrt(distX * distX + distY * distY)

    "Move closer to a set of prey_list"
    def moveCloser(self, prey_list):
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

    "Move with a set of prey_list"
    def moveWith(self, prey_list):
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

    "Move away from a set of prey_list. This avoids crowding"
    def moveAway(self, prey_list, minDistance):
        if len(prey_list) < 1: return

        distanceX = 0
        distanceY = 0
        numClose = 0

        for prey in prey_list:
            distance = self.distance(prey)
            if  distance < minDistance:
                numClose += 1
                xdiff = (self.rect.x - prey.rect.x)
                ydiff = (self.rect.y - prey.rect.y)

                if xdiff >= 0: xdiff = math.sqrt(minDistance) - xdiff
                elif xdiff < 0: xdiff = -math.sqrt(minDistance) - xdiff

                if ydiff >= 0: ydiff = math.sqrt(minDistance) - ydiff
                elif ydiff < 0: ydiff = -math.sqrt(minDistance) - ydiff

                distanceX += xdiff
                distanceY += ydiff

        if numClose == 0:
            return

        self.velocityX -= distanceX / 5
        self.velocityY -= distanceY / 5

    "Perform actual movement based on our velocity"
    def update(self):
        if abs(self.velocityX) > maxVelocity or abs(self.velocityY) > maxVelocity:
            scaleFactor = maxVelocity / max(abs(self.velocityX), abs(self.velocityY))
            self.velocityX *= scaleFactor
            self.velocityY *= scaleFactor

        self.rect.x += self.velocityX
        self.rect.y += self.velocityY

screen = pygame.display.set_mode(size)

# create prey_list at random positions
for i in range(numBoids):
    prey = Prey(random.randint(0, width), random.randint(0, height))
    # Add the prey to the list of objects
    prey_list.add(prey)
    all_sprites_list.add(prey)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    for prey in prey_list:
        closeBoids = []
        for otherBoid in prey_list:
            if otherBoid == prey: continue
            distance = prey.distance(otherBoid)
            if distance < 200:
                closeBoids.append(otherBoid)


        prey.moveCloser(closeBoids)
        prey.moveWith(closeBoids)
        prey.moveAway(closeBoids, 20)

        # ensure they stay within the screen space
        # if we roubound we can lose some of our velocity
        border = 25
        if prey.rect.x < border and prey.velocityX < 0:
            prey.velocityX = -prey.velocityX * random.random()
        if prey.rect.x > width - border and prey.velocityX > 0:
            prey.velocityX = -prey.velocityX * random.random()
        if prey.rect.y < border and prey.velocityY < 0:
            prey.velocityY = -prey.velocityY * random.random()
        if prey.rect.y > height - border and prey.velocityY > 0:
            prey.velocityY = -prey.velocityY * random.random()


    screen.fill(black)
    # Calls update() method on every sprite in the list
    all_sprites_list.update()

    # Draw all the spites
    all_sprites_list.draw(screen)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    pygame.time.delay(10)
    # Limit to 60 frames per second
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    clock.tick(60)
    pygame.display.flip()
    pygame.time.delay(10)
