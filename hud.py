import pygame
from hud import draw_hud

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
GROUND_LEVEL = SCREEN_HEIGHT - 70
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')

# Clock settings
clock = pygame.time.Clock()
FPS = 60

# Game variables
GRAVITY = 0.75
moving_left = False
moving_right = False
BG = (144, 201, 120)

# Game loop
run = True
while run:
    clock.tick(FPS)

    # Draw background
    screen.fill(BG)

    # Draw HUD
    draw_hud(screen)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_ESCAPE:
                run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    # Update display
    pygame.display.update()

pygame.quit()