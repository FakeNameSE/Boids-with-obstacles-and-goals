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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the title of the window
pygame.display.set_caption('Boids')

# Fill background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(BLACK)

# --- objects ---

# lists
# This is a list of every boid
boid_list = pygame.sprite.Group()
# This is a list of every sprite.
all_sprites_list = pygame.sprite.LayeredDirty()

# --- create boids and obstacles at random positions on the screen ---

# Place boids
for i in range(NUM_BOIDS):
    boid = Boid(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT),
                100, 40, 5, 10, 100, 200, MAX_BOID_SPEED, "experiments/resources/img/boid.png")
    # Add the boid to the lists of objects
    boid_list.add(boid)
    all_sprites_list.add(boid)

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

    text = "Boids Simulation: FPS: {0:.2f}".format(clock.get_fps())
    pygame.display.set_caption(text)
    # --- updates ---

    # Scan for boids to pay attention to
    for boid in boid_list:
        closeboid = []
        for otherboid in boid_list:
            if otherboid == boid:
                continue
            distance = boid.distance(otherboid)
            if distance < boid.field_of_view:
                closeboid.append(otherboid)

        # Apply the rules of the boids
        boid.cohesion(closeboid)
        boid.alignment(closeboid)
        boid.separation(closeboid, 20)
        boid.update(False)

        # --- draws ---

    # Create list of dirty rects
    rects = all_sprites_list.draw(screen)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.update(rects)
    clock.tick(120)

# --- the end ---
pygame.quit()
sys.exit()
