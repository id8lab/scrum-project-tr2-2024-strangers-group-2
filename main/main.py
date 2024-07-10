import pygame
import sys
import os 
import csv
import button

# Initialize Pygame
pygame.init()

#define game variables
ROWS = 16
COLS = 150
TILE_SIZE = 50
TILE_TYPES = 21
TEXT_COL = (255, 255, 255) 
level = 1

# Set up the display
screen_width = 1400
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pygame Screen')

# Create a laser group
laser_group = pygame.sprite.Group()

#create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)

#load in level data and create world
with open(f'C:/Users/ADMIN/Downloads/scrum-project-tr2-2024-strangers-group-2-5/main/level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

# Ensure your path is correct for your button images
resume_img = pygame.image.load("C:/Users/ADMIN/Downloads/scrum-project-tr2-2024-strangers-group-2-5/Setting_page/images/button_resume.png").convert_alpha()
options_img = pygame.image.load("C:/Users/ADMIN/Downloads/scrum-project-tr2-2024-strangers-group-2-5/Setting_page/images/button_options.png").convert_alpha()
quit_img = pygame.image.load("C:/Users/ADMIN/Downloads/scrum-project-tr2-2024-strangers-group-2-5/Setting_page/images/button_quit.png").convert_alpha()
video_img = pygame.image.load("C:/Users/ADMIN/Downloads/scrum-project-tr2-2024-strangers-group-2-5/Setting_page/images/button_video.png").convert_alpha()
audio_img = pygame.image.load("C:/Users/ADMIN/Downloads/scrum-project-tr2-2024-strangers-group-2-5/Setting_page/images/button_audio.png").convert_alpha()
keys_img = pygame.image.load("C:/Users/ADMIN/Downloads/scrum-project-tr2-2024-strangers-group-2-5/Setting_page/images/button_keys.png").convert_alpha()
back_img = pygame.image.load("C:/Users/ADMIN/Downloads/scrum-project-tr2-2024-strangers-group-2-5/Setting_page/images/button_back.png").convert_alpha()

# Calculate center x-coordinate for buttons
button_width = resume_img.get_width()  # Assuming all buttons have the same width
center_x = screen_width // 2

# Create button instances
resume_button = button.Button(center_x - button_width // 2, 200, resume_img, 1)
options_button = button.Button(center_x - button_width // 2, 300, options_img, 1)
quit_button = button.Button(center_x - button_width // 2, 400, quit_img, 1)
video_button = button.Button(center_x - button_width // 2, 200, video_img, 1)
audio_button = button.Button(center_x - button_width // 2, 300, audio_img, 1)
keys_button = button.Button(center_x - button_width // 2, 400, keys_img, 1)
back_button = button.Button(center_x - button_width // 2, 500, back_img, 1)

# Game variables
game_paused = False
menu_state = "main"

# Helper function to draw text
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Load images
sky_cloud = pygame.image.load('C:/Users/ADMIN/Downloads/scrum-project-tr2-2024-strangers-group-2-5/img_background/sky_cloud.png').convert_alpha()
mountain = pygame.image.load('C:/Users/ADMIN/Downloads/scrum-project-tr2-2024-strangers-group-2-5/img_background/mountain.png').convert_alpha()
pine1 = pygame.image.load('C:/Users/ADMIN/Downloads/scrum-project-tr2-2024-strangers-group-2-5/img_background/pine1.png').convert_alpha()
pine2 = pygame.image.load('C:/Users/ADMIN/Downloads/scrum-project-tr2-2024-strangers-group-2-5/img_background/pine2.png').convert_alpha()
heart_image = pygame.image.load('C:/Users/ADMIN/Downloads/scrum-project-tr2-2024-strangers-group-2-5/img_element/minecraft-story-mode-pixel-art-video-games-minecraft-heart-removebg-preview.png').convert_alpha()

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

# Background positions
sky_x = 0
mountain_x = 0
pine1_x = 0
pine2_x = 0

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
        self.floor_list = []

    def process_data(self, data):
        # Process level data
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(img_rect)
                        self.floor_list.append(img_rect)

    def draw(self, screen, scroll):
        # Draw blocks and floor
        for tile in self.obstacle_list:
            tile_rect = tile.move(scroll, 0)
            pygame.draw.rect(screen, (144, 201, 120), tile_rect)
            pygame.draw.rect(screen, (0, 0, 0), tile_rect, 2)

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 2))
        self.image.fill((255, 0, 0))  # Red laser
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10 * direction

    def update(self, screen_width):
        self.rect.x += self.speed
        if self.rect.right < 0 or self.rect.left > screen_width:
            self.kill()  # Remove the laser if it goes off-screen

class Monster(pygame.sprite.Sprite):
    def __init__(self, image_paths, x, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.direction = 1
        self.on_ground = True  
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

        if self.jump and self.on_ground:
            self.vel_y = -13
            self.jump = False
            self.on_ground = False

        self.vel_y += 0.75  # GRAVITY

        dy += self.vel_y 

        # Check for ground collision
        self.rect.x += dx
        for tile in world.floor_list:
            if tile.colliderect(self.rect):
                if dx > 0:
                    self.rect.right = tile.left
                if dx < 0:
                    self.rect.left = tile.right
        self.rect.y += dy
        for tile in world.floor_list:
            if tile.colliderect(self.rect):
                if dy > 0:
                    self.rect.bottom = tile.top
                    self.vel_y = 0
                    self.on_ground = True
                if dy < 0:
                    self.rect.top = tile.bottom

        # Check collision with obstacles
        for obstacle in world.obstacle_list:
            if obstacle.colliderect(self.rect):
                self.collided = True
                break
        else:
            self.collided = False
        
        return dx  # Return the amount of horizontal movement

    def update_animation(self):
        ANIMATION_COOLDOWN = 100  # milliseconds

        # Update animation only
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.index = (self.index + 1) % len(self.animation_list)
            self.image = self.animation_list[self.index]

    def draw(self, screen, scroll):
        rect_with_scroll = self.rect.move(scroll, 0)
        screen.blit(pygame.transform.flip(self.image, self.flip, False), rect_with_scroll)

# Load player images
player_images = [
    r'C:/Users/ADMIN/Downloads/scrum-project-tr2-2024-strangers-group-2-5/img_character\Screenshot_2024-06-14_163851-removebg-preview.png', 
    r'C:/Users/ADMIN/Downloads/scrum-project-tr2-2024-strangers-group-2-5/img_character\Screenshot_2024-06-14_164717-removebg-preview.png',
    r'C:/Users/ADMIN/Downloads/scrum-project-tr2-2024-strangers-group-2-5/img_character\Screenshot_2024-06-14_164033-removebg-preview.png',
    r'C:/Users/ADMIN/Downloads/scrum-project-tr2-2024-strangers-group-2-5/img_character\Screenshot_2024-06-14_164605-removebg-preview.png',
    r'C:/Users/ADMIN/Downloads/scrum-project-tr2-2024-strangers-group-2-5/img_character\Screenshot_2024-06-14_164820-removebg-preview.png'
]

player = Monster(player_images, 200, 0.15, 5)

# Main loop
clock = pygame.time.Clock()
world = World()
world.process_data(world_data)

moving_left = False
moving_right = False
running = True
scroll = 0
scroll_speed = 5
scroll_threshold = screen_width // 4
    
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    # Reset game variables
                    game_over = False
                    player.rect.x = 200  # Reset player position
                    player.rect.y = screen_height - 70
                    player_lives = 3
                    score = 0
                    level = 1
                    laser_group.empty()  # Clear any active lasers
                    # Reset any other variables or game states as needed
                else:
                    game_paused = not game_paused  # Toggle pause state or other actions
            elif event.key == pygame.K_a:
                moving_left = True
            elif event.key == pygame.K_d:
                moving_right = True
            elif event.key == pygame.K_w:
                player.jump = True
            elif event.key == pygame.K_j:  # Left Control key to shoot
                direction = player.direction
                laser = Laser(player.rect.centerx + (direction * player.rect.width), player.rect.centery, direction)
                laser_group.add(laser)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            elif event.key == pygame.K_d:
                moving_right = False

    # Game over logic
    if player.rect.top > screen_height:
        game_over = True

    # Clear the screen
    screen.fill((0, 128, 255))

    if game_paused:
        if menu_state == "main":
            if resume_button.draw(screen):
                game_paused = False
            if options_button.draw(screen):
                menu_state = "options"
            if quit_button.draw(screen):
                running = False
        elif menu_state == "options":
            if video_button.draw(screen):
                pass  # Placeholder for video settings action
            if audio_button.draw(screen):
                pass  # Placeholder for audio settings action
            if keys_button.draw(screen):
                pass  # Placeholder for key settings action
            if back_button.draw(screen):
                menu_state = "main"
    elif game_over:
        # Display game over screen
        screen.fill((0, 0, 0))  # Fill the screen with black
        draw_text("GAME OVER", font, TEXT_COL, screen_width // 2 - 150, screen_height // 2 - 50)
        draw_text("Press SPACE to restart", font, TEXT_COL, screen_width // 2 - 200, screen_height // 2 + 50)
    else:
        # Draw gameplay elements
        draw_text("Game in progress", font, TEXT_COL, 10, 10)
        # Move player, update game state, draw other elements

        # Move the player
        dx = player.move(moving_left, moving_right)
        
        # Adjust scroll to keep player in fixed position
        if moving_right:
            scroll -= scroll_speed
        if moving_left:
            scroll += scroll_speed

        # Prevent scrolling beyond the world's bounds
        max_scroll = -TILE_SIZE * (COLS - screen_width // TILE_SIZE)
        if scroll < max_scroll:
            scroll = max_scroll
        elif scroll > 0:
            scroll = 0

        # Update background positions
        sky_x = scroll * 0.1 % screen_width
        mountain_x = scroll * 0.2 % screen_width
        pine1_x = scroll * 0.6 % screen_width
        pine2_x = scroll * 0.8 % screen_width

        # Draw the background images
        screen.blit(sky_cloud, (sky_x, 0))
        screen.blit(sky_cloud, (sky_x - screen_width, 0))
        screen.blit(mountain, (mountain_x, screen_height - mountain_height))
        screen.blit(mountain, (mountain_x - screen_width, screen_height - mountain_height))
        screen.blit(pine1, (pine1_x, screen_height - pine_height))
        screen.blit(pine1, (pine1_x - screen_width, screen_height - pine_height))
        screen.blit(pine2, (pine2_x, screen_height - pine_height))
        screen.blit(pine2, (pine2_x - screen_width, screen_height - pine_height))
        
        # Draw the world
        world.draw(screen, scroll)

        # Draw the player
        player.draw(screen, scroll)

        laser_group.update(screen_width)
        laser_group.draw(screen)

        # Draw HUD elements
        draw_time()
        draw_score()
        draw_level()
        draw_lives()

    # Update display
    pygame.display.update()
    clock.tick(60)