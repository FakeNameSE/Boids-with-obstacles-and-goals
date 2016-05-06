#!/usr/bin/env python
# Boid implementation in Python using PyGame

from __future__ import division  # required in Python 2.7

import sys

from boid import *
from obstacle import *

# === main ===

# --- init ---

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the title of the window
pygame.display.set_caption('Boids')

# --- objects ---

# lists
boid_list = pygame.sprite.Group()
obstacle_list = pygame.sprite.Group()
# This is a list of every sprite.
all_sprites_list = pygame.sprite.Group()

# --- create boids and obstacles at random positions on the screen ---

# Place boids
for i in range(NUM_BOIDS):
    boid = Boid(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
    # Add the boid to the lists of objects
    boid_list.add(boid)
    all_sprites_list.add(boid)

# Place obstacles
for i in range(NUM_OBSTACLES):
    obstacle = Obstacle(random.randint(0 + BORDER, SCREEN_WIDTH - BORDER),
                        random.randint(0 + BORDER, SCREEN_HEIGHT - BORDER))
    # Add the obstacle to the lists of objects
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

    # Scan for boids and obstacles to pay attention to
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

        # Apply the rules of the boids
        boid.cohesion(closeboid)
        boid.alignment(closeboid)
        boid.separation(closeboid, 20)
        if avoid:
            boid.obstacle_avoidance(obstacle)
        boid.goal(mouse_x, mouse_y)
        boid.update()

    # Check for collisions
    for boid in boid_list:
        collisions = pygame.sprite.spritecollide(boid, obstacle_list, False)
        for obstacle in collisions:
            boid.velocityX = -1 * boid.velocityX * random.uniform(0.1, 0.9)
            boid.velocityY = -1 * boid.velocityY * random.uniform(0.1, 0.9)

    # --- draws ---

    # Background colour
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
