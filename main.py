import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

screen_width = 800
screen_height = 600

# Config stuff
maxvel = 10
numprey = 50
border = 25

#lists
# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
prey_list = pygame.sprite.Group()

# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()



class Prey(pygame.sprite.Sprite):
    """
    This class represents the ball
    It derives from the "Sprite" class in Pygame
    """
    def __init__(self, x, y):
        # Call the parent class (Sprite) constructor
        super(Prey, self).__init__()

        # Load image as sprite
        prey_image = pygame.image.load("ressources/img/prey.png").convert()
        self.image = prey_image

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

        # Coordinates
        self.rect.x = x
        self.rect.y = y

        # Velocity
        self.x_vel = random.randint(1, 10)/10.0
        self.y_vel = random.randint(1, 10)/10.0

    def getdistance(self, prey):
        distX = self.rect.x - prey.rect.x
        distY = self.rect.y - prey.rect.y
        return math.sqrt(distX * distX + distY * distY)

    def cohesion(self, prey_list):
        if len(prey_list) < 1:
            return

        # calculate the average distances from the other boids
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

        self.x_vel -= (avgX / 100)
        self.y_vel -= (avgY / 100)

    def alignment(self, prey_list):
        if len(prey_list) < 1:
            return
        # calculate the average velocities of the other boids
        avgX = 0
        avgY = 0

        for prey in prey_list:
            avgX += prey.x_vel
            avgY += prey.y_vel

        avgX /= len(prey_list)
        avgY /= len(prey_list)

        # set our velocity towards the others
        self.x_vel += (avgX / 40)
        self.y_vel += (avgY / 40)

    def seperation(self, prey_list, minDistance):
        if len(prey_list) < 1:
            return

        distanceX = 0
        distanceY = 0
        numClose = 0

        for prey in prey_list:
            distance = self.getdistance(prey)
            if distance < minDistance:
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

        self.x_vel -= distanceX / 5
        self.y_vel -= distanceY / 5

    def update(self):
        """ Called each frame. """
        if abs(self.x_vel) > maxvel or abs(self.y_vel) > maxvel:
            scaleFactor = maxvel / max(abs(self.x_vel), abs(self.y_vel))
            self.x_vel *= scaleFactor
            self.y_vel *= scaleFactor

        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

# Set the height and width of the screen
screen = pygame.display.set_mode([screen_width, screen_height])

for i in range(numprey):
    # Create new prey in random location
    prey = Prey(random.randint(0, screen_width), random.randint(0, screen_height))
    # Add the prey to the list of objects
    prey_list.add(prey)
    all_sprites_list.add(prey)

# -------- Main Program Loop -----------
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    for prey in prey_list:
        closeprey = []
        for otherprey in prey_list:
            if otherprey == prey:
                continue
            distance = prey.getdistance(otherprey)
            if distance < 200:
                closeprey.append(otherprey)

        prey.cohesion(closeprey)
        prey.alignment(closeprey)
        prey.seperation(closeprey, 20)

        if prey.rect.x < border and prey.x_vel < 0:
            prey.x_vel = -prey.x_vel * random.random()

        if prey.rect.x > screen_width - border and prey.x_vel > 0:
            prey.x_vel = -prey.x_vel * random.random()

        if prey.rect.y < border and prey.y_vel < 0:
            prey.y_vel = -prey.y_vel * random.random()

        if prey.rect.y > screen_height - border and prey.y_vel > 0:
            prey.y_vel = -prey.y_vel * random.random()

    # Calls update() method on every sprite in the list
    all_sprites_list.update()

    # Clear the screen
    screen.fill(BLACK)

    # Draw all the spites
    all_sprites_list.draw(screen)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    pygame.time.delay(10)
    # Limit to 60 frames per second
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    clock.tick(60)
