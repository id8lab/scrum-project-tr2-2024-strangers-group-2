import pygame

# Initialize Pygame
pygame.init()

# Set screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set title
pygame.display.set_caption("Pygame Screen")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
brown = (165, 42, 42)
orange = (255, 165, 0)

# Load images![](images/sky.png)
desertsky_img = pygame.image.load("sky.png").convert_alpha() #(images/sky.png)
desert_img = pygame.image.load("desert.png").convert_alpha()


# Define new heights for mountain
desertsky_img_height = screen_height // 1.5  # Adjust this value as needed

# HUD settings
font = pygame.font.SysFont('comicsans', 50)
WHITE = (255, 255, 255)
timer = 0
player_lives = 3
score = 0
level = 1

# Load player images for animation
player_images = [
    r'img_character\Screenshot_2024-06-14_163851-removebg-preview.png',
    r'img_character\Screenshot_2024-06-14_164717-removebg-preview.png',
    r'img_character\Screenshot_2024-06-14_164033-removebg-preview.png',
    r'img_character\Screenshot_2024-06-14_164605-removebg-preview.png',
    r'img_character\Screenshot_2024-06-14_164820-removebg-preview.png'
]


# Load and resize player images
player_imgs = [pygame.transform.scale(pygame.image.load(img).convert_alpha(), (20, 32)) for img in player_images]

# Game variables
mario_x = 50
mario_y = 450
mario_speed = 5
goomba_x = 300
goomba_y = 450
goomba_speed = 2

# Animation variables
animation_index = 0
animation_speed = 0.1
animation_counter = 0

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        mario_x -= mario_speed
    if keys[pygame.K_RIGHT]:
        mario_x += mario_speed
    if keys[pygame.K_UP]:
        mario_y -= mario_speed
    if keys[pygame.K_DOWN]:
        mario_y += mario_speed

    # Move goomba
    goomba_x += goomba_speed
    if goomba_x > screen_width - 20 or goomba_x < 0:
        goomba_speed *= -1

    # Update animation
    animation_counter += animation_speed
    if animation_counter >= 1:
        animation_counter = 0
        animation_index = (animation_index + 1) % len(player_imgs)

    # Draw background
    screen.fill(yellow)

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
