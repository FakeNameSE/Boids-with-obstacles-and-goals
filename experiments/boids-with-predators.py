#!/usr/bin/env python
# coding=utf-8
# Boid implementation in Python using PyGame

from __future__ import division  # required in Python 2.7
# Necessary to import modules with relative path
import sys, os.path as path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from modules.boid import *

# === main === (lower_case names)

# --- init ---

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)

# Set the title of the window
pygame.display.set_caption('Boids with predators')

# Fill background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(BLACK)

# sprite lists
prey_list = pygame.sprite.Group()
close_prey = pygame.sprite.Group()
predator_list = pygame.sprite.Group()
# This is a list of every sprite.
all_sprites_list = pygame.sprite.LayeredDirty()

# --- create boids and obstacles at random positions on the screen ---

# Place boids
for i in xrange(NUM_PREY):
    prey = Boid(random.randint(BORDER, SCREEN_WIDTH - BORDER), random.randint(BORDER, SCREEN_HEIGHT - BORDER),
                100, 40, 5, 15, 0, FIELD_OF_VIEW, MAX_PREY_SPEED, "experiments/resources/img/boid.png")
    # Add the prey to the lists of objects
    prey_list.add(prey)
    all_sprites_list.add(prey)

for i in xrange(NUM_PREDATORS):
    predator = Boid(random.randint(BORDER, SCREEN_WIDTH - BORDER), random.randint(BORDER, SCREEN_HEIGHT - BORDER),
                    100, 40, 5, 0, 50, FIELD_OF_VIEW, MAX_PREDATOR_SPEED, "experiments/resources/img/predator.png")
    # Add the predator to the lists of objects
    predator_list.add(predator)
    all_sprites_list.add(predator)

clock = pygame.time.Clock()
running = True

# Clear old sprites and replace with background
all_sprites_list.clear(screen, background)

# --- mainloop ---

while running:

    # --- events ---

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    text = "Boids Simulation with Predators: FPS: {0:.2f}".format(clock.get_fps())
    pygame.display.set_caption(text)

    # --- updates ---

    # Scan for boids and predators to pay attention to
    for prey in prey_list:
        closeboid = []
        avoid = False
        for otherboid in prey_list:
            if otherboid == prey:
                continue
            distance = prey.distance(otherboid)
            if distance < 200:
                closeboid.append(otherboid)
        for predator in predator_list:
            distance = prey.distance(predator)
            if distance < prey.field_of_view:
                avoid = True

        # Apply the rules of the boids
        prey.cohesion(closeboid)
        prey.alignment(closeboid)
        prey.separation(closeboid, 20)
        if avoid:
            prey.flee(predator)
        else:
            prey.go_to_middle()
        prey.update(True)

    for predator in predator_list:
        closeboid = []
        close_prey.empty()
        for otherboid in predator_list:
            if otherboid == predator:
                continue
            distance = predator.distance(otherboid)
            if distance < predator.field_of_view:
                closeboid.append(otherboid)
        for prey in prey_list:
            distance = prey.distance(prey)
            if distance < predator.field_of_view:
                close_prey.add(prey)

        # Apply the rules of the boids
        predator.cohesion(closeboid)
        predator.alignment(closeboid)
        predator.separation(closeboid, 20)
        predator.attack(close_prey)
        predator.update(True)

        # If a predator manages to touch a prey, the prey gets eaten!
        collisions = pygame.sprite.spritecollide(predator, close_prey, True)
        # for prey in collisions:
        # print "munch!"

    # --- draws ---

    # Create list of dirty sprites
    rects = all_sprites_list.draw(screen)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.update(rects)
    # pygame.time.delay(10)
    # Used to manage how fast the screen updates
    clock.tick(60)

# --- the end ---
pygame.quit()
sys.exit()
