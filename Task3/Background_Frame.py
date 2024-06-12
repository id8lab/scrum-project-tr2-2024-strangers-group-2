import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pygame Screen')

# Load images
sky_cloud = pygame.image.load('sky_cloud.png').convert_alpha()
mountain = pygame.image.load('mountain.png').convert_alpha()
pine1 = pygame.image.load('pine1.png').convert_alpha()
pine2 = pygame.image.load('pine2.png').convert_alpha()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill the screen with a color (RGB format)
    screen.fill((0, 128, 255))
    
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
