import pygame
import sys
import csv

# Initialize Pygame
pygame.init()

#define game variables
ROWS = 16
COLS = 150
TILE_SIZE = 50
TILE_TYPES = 21
level = 1

# Set up the display
screen_width = 1400
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pygame Screen')

#create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)

#load in level data and create world
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

# Load images
sky_cloud = pygame.image.load('img_background/sky_cloud.png').convert_alpha()
mountain = pygame.image.load('img_background/mountain.png').convert_alpha()
pine1 = pygame.image.load('img_background/pine1.png').convert_alpha()
pine2 = pygame.image.load('img_background/pine2.png').convert_alpha()
heart_image = pygame.image.load('img_element/minecraft-story-mode-pixel-art-video-games-minecraft-heart-removebg-preview.png').convert_alpha()

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
score = 0
level = 1

# Function to draw time
def draw_time():
    minutes = int(timer) // 60
    seconds = int(timer) % 60
    timer_text = font.render(f'{minutes:02}:{seconds:02}', True, WHITE)
    screen.blit(timer_text, (screen_width - timer_text.get_width() - 10, screen_height - timer_text.get_height() - 10))  # Bottom right corner

# Function to draw score
def draw_score():
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (screen_width - score_text.get_width() - 10, 10))  # Top right corner

# Function to draw level
def draw_level():
    level_text = font.render(f'Level: {level}', True, WHITE)
    level_x = (screen_width - level_text.get_width()) // 2
    screen.blit(level_text, (level_x, 10))  # Top middle

# Function to draw lives
def draw_lives():
    lives_text = font.render(f'Lives:', True, WHITE)
    screen.blit(lives_text, (10, 10))  # Top left corner
    heart_y = 10 + (lives_text.get_height() - heart_size[1]) // 2  # Center the hearts vertically
    for i in range(player_lives):
        screen.blit(heart_image, (lives_text.get_width() + 20 + i * (heart_size[0] + 10), heart_y))

class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        # Process level data
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(img_rect)

    def draw(self, screen):
        # Draw blocks and floor
        for tile in self.obstacle_list:
            pygame.draw.rect(screen, (144, 201, 120), tile)
            pygame.draw.rect(screen, (0, 0, 0), tile, 2)

class Monster(pygame.sprite.Sprite):
    def __init__(self, image_paths, x, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.direction = 1
        self.jump = False
        self.vel_y = 0
        self.flip = False
        self.animation_list = []
        self.index = 0
        self.update_time = pygame.time.get_ticks()

        # Define a common size for the images
        common_width = 64
        common_height = 64

        # Load the images and scale them to the common size
        for image_path in image_paths:
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (common_width, common_height))
            self.animation_list.append(image)
        
        self.image = self.animation_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, screen_height - 70)
        self.base_y = screen_height - 70
        self.ground_level = screen_height - 70  # Set ground level attribute

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0

        if moving_left or moving_right:
            self.update_animation()

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1

        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        if self.jump:
            self.vel_y = -11
            self.jump = False

        self.vel_y += 0.75  # GRAVITY

        dy += self.vel_y 

        # Check for ground collision
        if self.rect.bottom + dy > self.ground_level:
            dy = self.ground_level - self.rect.bottom
            self.vel_y = 0

        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        ANIMATION_COOLDOWN = 100  # milliseconds

        # Update animation only
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.index = (self.index + 1) % len(self.animation_list)
            self.image = self.animation_list[self.index]

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

# Load player images
player_images = [
    'img_character\8dd889acea826111937568e2301697c6-removebg-preview.png', 
    'img_character\Screenshot_2024-06-11_143220-removebg-preview.png',
    'img_character\Screenshot_2024-06-11_160603-removebg-preview.png',
    'img_character\Screenshot_2024-06-11_143220-removebg-preview.png',
    'img_character\8dd889acea826111937568e2301697c6-removebg-preview.png'
]

player = Monster(player_images, 200, 0.15, 5)

# Main loop
clock = pygame.time.Clock()
world = World()
world.process_data(world_data)

moving_left = False
moving_right = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # button press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                running = False
        # button release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
    
    # Increment timer
    timer += clock.get_time() / 1000  # Convert milliseconds to seconds
    
    # Fill the screen with a color (RGB format)
    screen.fill((0, 128, 255))
    
    # Blit the images in the correct order
    screen.blit(sky_cloud, (0, 0))  # Top layer
    screen.blit(mountain, (0, 0))   # Middle layer
    screen.blit(pine1, (0, screen_height - pine_height))  # Bottom layer (behind)
    screen.blit(pine2, (0, screen_height - pine_height))  # Bottom layer (in front)

    # Draw HUD
    world.draw(screen)
    draw_time()
    draw_score()
    draw_level()
   
    draw_lives()

    # Update and draw the player
    player.move(moving_left, moving_right)
    player.draw(screen)

    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate at 60 FPS
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
