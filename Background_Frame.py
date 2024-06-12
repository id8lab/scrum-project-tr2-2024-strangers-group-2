import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 1400
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pygame Screen')

# Load images
sky_cloud = pygame.image.load('sky_cloud.png').convert_alpha()
mountain = pygame.image.load('mountain.png').convert_alpha()
pine1 = pygame.image.load('pine1.png').convert_alpha()
pine2 = pygame.image.load('pine2.png').convert_alpha()
heart_image = pygame.image.load('minecraft-story-mode-pixel-art-video-games-minecraft-heart-removebg-preview.png').convert_alpha()

# Define new heights for sky
sky_height = screen_height // 1.5  # Adjust this value as needed
sky_cloud = pygame.transform.scale(sky_cloud, (screen_width, sky_height))

# Define new heights for mountain
mountain_height = screen_height // 1.5  # Adjust this value as needed
mountain = pygame.transform.scale(mountain, (screen_width, mountain_height))

# Reduce the height of the pine images
pine_height = screen_height // 1.8  # Adjust this value as needed
pine1 = pygame.transform.scale(pine1, (screen_width, pine_height))
pine2 = pygame.transform.scale(pine2, (screen_width, pine_height))

# Scale heart image
heart_size = (40, 40)
heart_image = pygame.transform.scale(heart_image, heart_size)

# HUD settings
font = pygame.font.SysFont('comicsans', 50)
WHITE = (255, 255, 255)
timer = 0
player_lives = 3

# Function to draw HUD
def draw_hud():
    timer_text = font.render(f'Time: {int(timer)}', True, WHITE)
    lives_text = font.render(f'Lives:', True, WHITE)
    screen.blit(timer_text, (screen_width - timer_text.get_width() - 10, 10))  # Top right corner
    screen.blit(lives_text, (10, 10))  # Top left corner
    heart_x = lives_text.get_width() + 20  # Calculate heart position relative to life text
    heart_y = 10 + (font.size(" ")[1] - heart_size[1]) // 2  # Center heart vertically with text
    for i in range(player_lives):
        screen.blit(heart_image, (heart_x + i * (heart_size[0] + 10), heart_y))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Increment timer
    timer += 1 / 60  # Assuming 60 FPS
    
    # Fill the screen with a color (RGB format)
    screen.fill((0, 128, 255))
    
    # Blit the images in the correct order
    screen.blit(sky_cloud, (0, 0))  # Top layer
    screen.blit(mountain, (0, 0))   # Middle layer
    screen.blit(pine1, (0, screen_height - pine_height))  # Bottom layer (behind)
    screen.blit(pine2, (0, screen_height - pine_height))  # Bottom layer (in front)

    # Draw HUD
    draw_hud()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
