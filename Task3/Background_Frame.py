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

# Scale images to fit the screen if necessary (optional)
sky_cloud = pygame.transform.scale(sky_cloud, (screen_width, screen_height))
mountain = pygame.transform.scale(mountain, (screen_width, screen_height))
pine1 = pygame.transform.scale(pine1, (screen_width, screen_height))
pine2 = pygame.transform.scale(pine2, (screen_width, screen_height))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill the screen with a color (RGB format)
    screen.fill((0, 128, 255))
    
    # Blit the images in the correct order
    screen.blit(sky_cloud, (0, 0))  # Top layer
    screen.blit(mountain, (0, 0))   # Middle layer
    screen.blit(pine1, (0, 0))      # Bottom layer (behind)
    screen.blit(pine2, (0, 0))      # Bottom layer (in front)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
