import pygame as pg
import sys

# Initialize pg
pg.init()

# Set up display
width, height = 800, 600
screen = pg.display.set_mode((width, height))
pg.display.set_caption("My pg Template")

# Set up game loop variables
clock = pg.time.Clock()
running = True

# Main game loop
while running:
    # Handle events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Update game state

    # Draw to the screen
    screen.fill((255, 255, 255))  # Fill the screen with a white color

    # Refresh the display
    pg.display.flip()

    # Cap the frame rate
    clock.tick(60)  # Adjust the value to control the frame rate

# Quit pg
pg.quit()
sys.exit()