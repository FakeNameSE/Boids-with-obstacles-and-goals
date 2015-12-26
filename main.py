import pygame
import random
import math
import sys

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

screen_width = 700
screen_height = 400

# Config stuff
maxvel = 10

#lists
closeprey = []

class Prey(pygame.sprite.Sprite):
    """
    This class represents the ball
    It derives from the "Sprite" class in Pygame
    """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super(Prey, self).__init__()

        # Load image as sprite
        prey_image = pygame.image.load("ressources/img/prey.png").convert()
        self.image = prey_image
        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values 
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

        # Velocity
        self.x_vel = random.randint(1, 10)/10.0
        self.y_vel = random.randint(1, 10)/10.0

    def getdistance(self, flockmate):
        distX = self.rect.x - flockmate.rect.x
        distY = self.rect.y - flockmate.rect.y
        return math.sqrt(distX * distX + distY * distY)

    def cohesion(self, flockmates):
        if len(flockmates) <= 1:
            return

        # calculate the average distances from the other boids
        avgX = 0
        avgY = 0
        for flockmate in flockmates:
            if flockmate.rect.x == self.rect.x and flockmate.rect.y == self.rect.y:
                continue

            avgX += (self.rect.x - flockmate.rect.x)
            avgY += (self.rect.y - flockmate.rect.y)

        avgX /= len(flockmates)
        avgY /= len(flockmates)

        # set our velocity towards the others
        distance = math.sqrt((avgX * avgX) + (avgY * avgY)) * -1.0

        self.x_vel -= (avgX / 100)
        self.y_vel -= (avgY / 100)

    def alignment(self, flockmates):
        if len(flockmates) <= 1:
            return
        # calculate the average velocities of the other boids
        avgX = 0
        avgY = 0

        for flockmate in flockmates:
            avgX += flockmate.x_vel
            avgY += flockmate.y_vel

        avgX /= len(flockmates)
        avgY /= len(flockmates)

        # set our velocity towards the others
        self.x_vel += (avgX / 40)
        self.y_vel += (avgY / 40)

    def seperation(self, flockmates, minDistance):
        if len(flockmates) <= 1: return

        distanceX = 0
        distanceY = 0
        numClose = 0

        for flockmate in flockmates:
            distance = self.getdistance(flockmate)
            if distance < minDistance:
                numClose += 1
                xdiff = (self.rect.x - flockmate.rect.x)
                ydiff = (self.rect.y - flockmate.rect.y)

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

        if abs(self.x_vel) >= maxvel or abs(self.y_vel) >= maxvel:
            scaleFactor = maxvel / max(abs(self.x_vel), abs(self.y_vel))
            self.x_vel *= scaleFactor
            self.y_vel *= scaleFactor

        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

# Initialize Pygame
pygame.init()
 
# Set the height and width of the screen
screen = pygame.display.set_mode([screen_width, screen_height])
 
# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
prey_list = pygame.sprite.Group()

# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

for i in range(10):
    prey = Prey()
    # Set a random location for the prey
    prey.rect.y = random.randrange(10, screen_height - 10)
    prey.rect.x = random.randrange(10, screen_width - 10)
    
    # Add the prey to the list of objects
    prey_list.add(prey)
    all_sprites_list.add(prey)
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
score = 0
 
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    for prey in prey_list:
        for otherprey in prey_list:
            if otherprey == prey:
                continue

            distance = prey.getdistance(otherprey)
            if distance < 200:
                closeprey.append(otherprey)

        prey.cohesion(closeprey)
        prey.alignment(closeprey)
        prey.seperation(closeprey, 20)

        border = 25
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
    screen.fill(BLUE)

    # Draw all the spites
    all_sprites_list.draw(screen)
 
    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
pygame.quit()
sys.exit()
