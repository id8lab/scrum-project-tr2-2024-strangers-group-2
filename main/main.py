import pygame
import sys
import os 
import csv
import button
import random
import score

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
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

# Ensure your path is correct for your button images
resume_img = pygame.image.load("images/button_resume.png").convert_alpha()
options_img = pygame.image.load("images/button_options.png").convert_alpha()
quit_img = pygame.image.load("images/button_quit.png").convert_alpha()
video_img = pygame.image.load("images/button_video.png").convert_alpha()
audio_img = pygame.image.load("images/button_audio.png").convert_alpha()
back_img = pygame.image.load("images/button_back.png").convert_alpha()
restart_img = pygame.image.load("images/button_restart.png").convert_alpha()
start_img = pygame.image.load("images/button_start.png").convert_alpha()
mute_img = pygame.image.load("images/button_mute.png").convert_alpha()
unmute_img = pygame.image.load("images/button_unmute.png").convert_alpha()
windows_img = pygame.image.load("images/button_windows.png").convert_alpha()
fullscreen_img = pygame.image.load("images/button_fullscreen.png").convert_alpha()
instruction_img = pygame.image.load("images/button_instruction.png").convert_alpha()


# Calculate center x-coordinate for buttons
button_width = resume_img.get_width()  # Assuming all buttons have the same width
center_x = screen_width // 2

# Create button instances
resume_button = button.Button(center_x - button_width // 2, 200, resume_img, 1)
options_button = button.Button(center_x - button_width // 2, 400, options_img, 1)
quit_button = button.Button(center_x - button_width // 2, 500, quit_img, 1)
video_button = button.Button(center_x - button_width // 2, 300, video_img, 1)
audio_button = button.Button(center_x - button_width // 2, 400, audio_img, 1)
back_button = button.Button(center_x - button_width // 2, 500, back_img, 1)
restart_button = button.Button(center_x - button_width // 2, 350, restart_img, 1)
start_button = button.Button(center_x - button_width // 2, 200, start_img, 1)
mute_button = button.Button(center_x - button_width // 2, 300, mute_img, 1)
unmute_button = button.Button(center_x - button_width // 2, 400, unmute_img, 1)
windows_button = button.Button(center_x - button_width // 2, 300, windows_img, 1)
fullscreen_button = button.Button(center_x - button_width // 2, 400, fullscreen_img, 1)
instruction_button = button.Button(center_x - button_width // 2, 300, instruction_img, 1)

# Game variables
game_paused = False
game_won = False
menu_state = "main"
game_state = "start"
previous_state = 'start'
final_time = 0

# Helper function to draw text
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

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

# Background positions
sky_x = 0
mountain_x = 0
pine1_x = 0
pine2_x = 0

# Load sound effects
shooting_sound = pygame.mixer.Sound('sounds/shooting.wav')
jump_sound = pygame.mixer.Sound('sounds/jump.wav')
game_over_sound = pygame.mixer.Sound('sounds/game-over-arcade-6435.mp3')

game_over_sound_flag = False

# List of sound effects
sound_effects = [shooting_sound, jump_sound, game_over_sound]

# Game over screen
def game_over_screen():

    global game_over_sound_flag, running

    # Fill screen with black
    screen.fill((0,0,0))
    
    # Render game over text
    game_over_text = font.render('Game Over', True, TEXT_COL)
    screen.blit(game_over_text, ((screen_width - game_over_text.get_width()) // 2, (screen_height - game_over_text.get_height()) // 3.75))

    if not game_over_sound_flag:
        game_over_sound.play()
        game_over_sound_flag = True
    
    if restart_button.draw(screen):
        restart_game()
    if quit_button.draw(screen):
        running = False

    # Update display
    pygame.display.flip()


# Game start screen
def start_screen():
    global running, game_state, menu_state

    screen.fill((0,0,0))
    
    game_title = font.render('Ranger shooting', True, TEXT_COL)
    screen.blit(game_title, ((screen_width - game_title.get_width()) // 2, (screen_height - game_title.get_height()) // 9))

    if start_button.draw(screen):
        start_game()
    elif instruction_button.draw(screen):
        menu_state = "instruction"
        game_state = "menu"
    elif options_button.draw(screen):
        menu_state = "options"
        game_state = "menu"
    elif quit_button.draw(screen):
        running = False

def options():
    global running, menu_state, game_paused, game_state
    if menu_state == "main":
        if resume_button.draw(screen):
            game_paused = False
            game_state = "play"
        elif instruction_button.draw(screen):
            menu_state = "instruction"
        elif options_button.draw(screen):
            menu_state = "options"
        elif quit_button.draw(screen):
            running = False
    elif menu_state == "options":
        if video_button.draw(screen):
            menu_state = "video"
        if audio_button.draw(screen):
            menu_state = "audio"
        if back_button.draw(screen):
            menu_state = "main"
            if previous_state == "start":
                game_state = "start"
                print('back to start')
            else:
                game_state = "play"
                print('back to play')
    elif menu_state == "instruction":
        how_to_play()
    elif menu_state == "video":
        video_settings()
    elif menu_state == "audio":
        audio_settings()

def start_game():
    global level, player_lives, score, timer, scroll, moving_left, moving_right, game_paused, menu_state, game_state, enemies_killed, start_time

    level = 1
    player_lives = 3
    score = 0
    timer = 0
    scroll = 0
    moving_left = False
    moving_right = False
    game_paused = False
    menu_state = "main"
    game_state = "play"

    # Clear any existing enemies and lasers
    enemies.empty()
    laser_group.empty()

    # Generate new enemies for the new level
    enemies.add(generate_enemies(enemy_images, 10, common_width, common_height, 2))

    enemies_killed = 0  # Reset the counter
    start_time = pygame.time.get_ticks()  # Reset the start time

    # Reset player position
    player.rect.center = (200, screen_height - 70)
    player.rect.x = 200
    player.rect.y = screen_height - 70

# Function to restart the game back in the first level
def restart_game():
    global player_lives, score, game_over_sound_flag, scroll, moving_left, moving_right
    player_lives = 3
    score = 0
    game_over_sound_flag = False
    scroll = 0
    moving_left = False
    moving_right = False
    player.reset_position()  # Use the new reset_position method
    player.animation_state = "idle"  # Reset animation state
    player.lives = 3  # Reset player lives
    player.score = 0  # Reset player score
    enemies.empty()  # Clear existing enemies
    enemies.add(generate_enemies(enemy_images, 10, common_width, common_height, 2))  # Generate new enemies
    laser_group.empty() 

# Setting for user to mute and unmute audio
def audio_settings():

    global menu_state, sound_effects

    if mute_button.draw(screen):
        for sound in sound_effects:
            sound.set_volume(0) 
        print("muted")
    if unmute_button.draw(screen):
        for sound in sound_effects:
            sound.set_volume(1) 
        print('unmuted')
    if back_button.draw(screen) :
        menu_state = "options"
        print("switch back to options")

# Function to resize screen to full screen or windows
def video_settings():
    global menu_state, screen

    if windows_button.draw(screen):
        pygame.display.set_mode((1400, 800), pygame.RESIZABLE)  # Change to your default window size
        print("Switched to windowed mode")
    if fullscreen_button.draw(screen):
        pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        print("Switched to fullscreen mode")
    if back_button.draw(screen):
        menu_state = "options"
        print("switch back to options")

# How to play screen
def how_to_play():
    global menu_state, game_state

    movement_text = font.render('W, A and D to move', True, TEXT_COL)
    screen.blit(movement_text, ((screen_width - movement_text.get_width()) // 2, (screen_height - movement_text.get_height()) // 3.75))

    shooting_text = font.render('J to shoot', True, TEXT_COL)
    screen.blit(shooting_text, ((screen_width - shooting_text.get_width()) // 2,(screen_height - movement_text.get_height()) // 3))

    menu_text = font.render('Space bar for menu', True, TEXT_COL)
    screen.blit(menu_text, ((screen_width - menu_text.get_width()) // 2,(screen_height - menu_text.get_height()) // 2.25))

    if back_button.draw(screen):
        menu_state = "main"
        if previous_state == "start":
            game_state = "start"
        else:
            game_state = "play"

def game_win():
    global running, game_won, final_time, menu_state, game_state

    # Fill screen with black
    screen.fill((0,0,0))

    # Render win text
    win_text = font.render('You Win!', True, TEXT_COL)
    screen.blit(win_text, ((screen_width - win_text.get_width()) // 2, (screen_height - win_text.get_height()) // 3.75 - 150))

    # Calculate and render time taken
    minutes = int(final_time) // 60
    seconds = int(final_time) % 60
    time_text = font.render(f'Time: {minutes:02}:{seconds:02}', True, TEXT_COL)
    screen.blit(time_text, ((screen_width - time_text.get_width()) // 2, (screen_height - time_text.get_height()) // 2 - 150))

    # Render enemies killed text
    killed_text = font.render(f'Enemies Killed: {enemies_killed}', True, TEXT_COL)
    screen.blit(killed_text, ((screen_width - killed_text.get_width()) // 2, (screen_height - killed_text.get_height()) // 2))

    if back_button.draw(screen):
        game_state = "start"
        menu_state = "main"
        game_won = False
        restart_game()  # Reset the game state

    # Update display
    pygame.display.flip()

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
    def check_laser_collisions(self, laser_group):
        for laser in laser_group:
            # Check collision with ground tiles
            for tile in self.floor_list:
                if is_collision_for_block(tile.right, laser.rect.left, tile.left, laser.rect.right, tile,laser.rect, scroll):
                    laser.kill()  # Remove the laser if it hits a ground tile
                    break
class Laser(pygame.sprite.Sprite):
    def __init__(self, player, scroll,is_player,is_enemy ):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 2))
        self.image.fill((255, 0, 0))  # Red laser
        self.rect = self.image.get_rect()
        self.player = player  # Reference to the player object
        self.rect.centerx = self.player.rect.centerx+scroll  # Initialize laser's x-position to player's center x
        self.rect.centery = self.player.rect.centery  # Initialize laser's y-position to player's center y
        self.speed = 9 * self.player.direction  # Set speed based on player's facing direction
        self.is_player = is_player
        self.is_enemy= is_enemy
        shooting_sound.play() # PLay shooting sound

    def update(self, screen_width):
        self.rect.x += self.speed
        if self.rect.right < 0 or self.rect.left > screen_width:
            self.kill()  # Remove the laser if it goes off-screen

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_paths, x, y, common_width, common_height, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.direction = 1
        self.animation_list = []
        self.index = 0
        self.update_time = pygame.time.get_ticks()
        self.flip = False
        self.on_ground = True  
        self.vel_y = 0
        self.detect_range = 300
        self.detect_shoot = False
        self.shoot_cooldown = 1000
        self.last_shot_time = pygame.time.get_ticks()
        self.hit_points = 0  # Track how many times the enemy has been hit

        # Load the images and scale them to the common size
        for image_path in image_paths:
            image = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.scale(image, (common_width, common_height))
            self.animation_list.append(image)

        self.image = self.animation_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.move_counter = 0

    def detect_player(self, player_rect):
        # Calculate distance between enemy and player
        distance = abs(self.rect.centerx - player_rect.centerx)
        if distance <= self.detect_range:
            self.can_shoot = True
        else:
            self.can_shoot = False

        # Check player's position relative to enemy's direction
        if self.direction == 1 and player_rect.centerx > self.rect.centerx:
            self.can_shoot = True
        elif self.direction == -1 and player_rect.centerx < self.rect.centerx:
            self.can_shoot = True
        else:
            self.can_shoot = False

    def shoot_laser(self, scroll):
        current_time = pygame.time.get_ticks()
        if self.can_shoot and current_time - self.last_shot_time > self.shoot_cooldown:
            self.last_shot_time = current_time
            laser = Laser(self, scroll,False,True)
            laser_group.add(laser)
            shooting_sound.play()  # Play shooting sound

    def handle_hit(self):
        self.hit_points += 1
        if self.hit_points >= 3:
            self.kill()  # Remove the enemy from the group if hit three times

    def resume_movement(self):
        self.can_shoot = False

    def update(self):
        self.move()
        self.update_animation()

    def move(self):
        dx = self.direction * self.speed
        dy = self.vel_y
        self.vel_y += 0.75  # GRAVITY

        # Move the enemy
        self.rect.x += dx
        self.rect.y += dy

        # Check for ground collision and adjust position
        for tile in world.floor_list:
            if tile.colliderect(self.rect):
                if dy > 0:
                    self.rect.bottom = tile.top
                    self.vel_y = 0
                    self.on_ground = True
                elif dy < 0:
                    self.rect.top = tile.bottom

        # Check for collisions with blocks and change direction
        for tile in world.floor_list:
            if tile.colliderect(self.rect):
                if dx > 0:
                    self.rect.right = tile.left
                    self.direction = -1
                    self.flip = True
                elif dx < 0:
                    self.rect.left = tile.right
                    self.direction = 1
                    self.flip = False

        # Change direction when hitting an obstacle or edge of platform
        edge_x = self.rect.right if self.direction > 0 else self.rect.left
        edge_y = self.rect.bottom + 1
        if not any(tile.collidepoint(edge_x, edge_y) for tile in world.floor_list):
            self.direction *= -1
            self.flip = not self.flip

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
    def check_collisions(self, laser_group,scroll):
            for laser in laser_group:
                if is_collision_for_enemy(self.rect.right, laser.rect.left,self.rect.left, laser.rect.right, laser,self.rect,laser.rect, scroll) and laser.is_enemy != True:
                    laser.kill()
                    self.kill()
                    print("Got hit!")


def is_collision_for_enemy(right, left, left1, right1,laser, rect1, rect2, scroll):
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    # right+=scroll
    left-=scroll
    # left1+=scroll
    right1-=scroll
    # Calculate the actuadl top and bottom edges of the rectangles
    top1 = y1
    bottom1 = y1 + h1
    top2 = y2
    bottom2 = y2 + h2
    # print("right of player ", right, " left of the laser ", left)
    # Check for overlap based on the x and y coordinates
    if right >= left and left1 <= right1 and bottom1 >= top2 and top1 <= bottom2:
        # laser.kill()
        return True
    else:
        return False


def generate_enemies(image_paths, num_enemies, common_width, common_height, speed):
    enemies = pygame.sprite.Group()
    segment_width = COLS * TILE_SIZE // num_enemies

    for i in range(num_enemies):
        # Compute the x-position for the enemy within its segment
        x = i * segment_width + random.randint(0, segment_width - common_width)
        y = screen_height - TILE_SIZE * 2  # Assume ground level for simplicity
        
        # Find the correct y-position based on the world data
        for row in world_data[::-1]:  # Start from the bottom row
            if row[x // TILE_SIZE] != -1:
                y = world_data.index(row) * TILE_SIZE
                break
        
        enemy = Enemy(image_paths, x, y, common_width, common_height, speed)
        enemies.add(enemy)
    return enemies

common_width = 64
common_height = 64
enemy_images = [
    r'img_character/enemy_sprite1.png',
    r'img_character/enemy_sprite2.png',
    r'img_character/enemy_sprite3.png',
    r'img_character/enemy_sprite4.png',
    r'img_character/enemy_sprite5.png',
    r'img_character/enemy_sprite6.png',
    r'img_character/enemy_sprite7.png'
]

enemies = generate_enemies(enemy_images, 10, common_width, common_height, 2)

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
        self.is_falling = False

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
        # self.rect.width/=2
        # self.base_y = screen_height - 70
        # self.ground_level = screen_height - 70  # Set ground level attribute
        self.start_x = x  # Store the starting x position
        self.start_y = screen_height - 70  # Store the starting y position
        
    def reset_position(self):
        self.rect.center = (self.start_x, self.start_y)
        self.vel_y = 0
        self.on_ground = True
        self.is_falling = False

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

        self.vel_y += 0.65  # GRAVITY

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

        # Check if the player has fallen off the screen
        if self.rect.top > screen_height:
            self.is_falling = True

        return dx  # Return the amount of horizontal movement

    def check_collisions(self, laser_group, scroll):
        global player_lives, enemies_killed
        for laser in laser_group:
            if is_collision(self.rect.right, laser.rect.left, self.rect.left, laser.rect.right, laser, self.rect, laser.rect, scroll, self.jump) and laser.is_player != True:
                laser.kill()
                player_lives -= 1
                enemies_killed += 1  # Increment the killed enemies counter
                print("Got hit!")
                if player_lives <= 0:
                    # Handle game over logic here if necessary
                    pass

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

def is_collision(right, left, left1, right1,laser, rect1, rect2, scroll, jump):
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    # right+=scroll
    left-=scroll
    # left1+=scroll
    right1-=scroll
    # Calculate the actuadl top and bottom edges of the rectangles
    top1 = y1
    bottom1 = y1 + h1
    top2 = y2
    bottom2 = y2 + h2
    # print("right of player ", right, " left of the laser ", left)
    # Check for overlap based on the x and y coordinates
    if jump :
        bottom1+=20
        top1+=20
    if right >= left and left1 <= right1 and bottom1 >= top2 and top1 <= bottom2:
        # laser.kill()
        return True
    else:
        return False

def is_collision_for_block(right, left, left1, right1,rect1, rect2, scroll):
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    # right+=scroll
    left-=scroll
    # left1+=scroll
    right1-=scroll
    # Calculate the actuadl top and bottom edges of the rectangles
    top1 = y1
    bottom1 = y1 + h1
    top2 = y2
    bottom2 = y2 + h2
    # Check for overlap based on the x and y coordinates
    if right >= left and left1 <= right1 and bottom1 >= top2 and top1 <= bottom2:
        # laser.kill()
        return True
    else:
        return False
    
# Load player images
player_images = [
    r'img_character\Screenshot_2024-06-14_163851-removebg-preview.png', 
    r'img_character\Screenshot_2024-06-14_164717-removebg-preview.png',
    r'img_character\Screenshot_2024-06-14_164033-removebg-preview.png',
    r'img_character\Screenshot_2024-06-14_164605-removebg-preview.png',
    r'img_character\Screenshot_2024-06-14_164820-removebg-preview.png'
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

def draw_pause_background():
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

while running:
    if game_state == "start":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        previous_state = "start"  # Set previous state when entering start screen
        start_screen()

    elif game_state == "menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if previous_state == "start":
                        game_state = "start"
                    else:
                        game_state = "play"
                    game_paused = False

        screen.fill((0, 0, 0))  # Clear screen
        options()

    elif game_state == "play":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_paused = not game_paused
                    if game_paused:
                        game_state = "menu"
                        menu_state = "main"
                        previous_state = "play"
                elif event.key == pygame.K_a:
                    moving_left = True
                elif event.key == pygame.K_d:
                    moving_right = True
                elif event.key == pygame.K_w:
                    player.jump = True
                    jump_sound.play()
                elif event.key == pygame.K_j:
                    direction = player.direction
                    laser = Laser(player, scroll, True, False)
                    laser_group.add(laser)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    moving_left = False
                elif event.key == pygame.K_d:
                    moving_right = False

        if not game_paused and player_lives > 0 and not game_won:
            # Clear the screen
            screen.fill((0, 128, 255))

            # Move the player
            dx = player.move(moving_left, moving_right)
            
            if player.is_falling:
                player_lives = 0  # Set lives to 0 to trigger game over
           
            if player.rect.right >= world.floor_list[-1].right:
                game_state = "win"
                game_won = True
                final_time = timer  # Store the final time when the game is won
            
            # Detect player and handle shooting for each enemy
            for enemy in enemies:
                enemy.detect_player(player.rect)
                enemy.shoot_laser(scroll)
            
            # Resume normal movement for enemies
            for enemy in enemies:
                if not enemy.can_shoot:
                    enemy.update()

            # Adjust scroll
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

            # Update and draw background
            sky_x = scroll * 0.1 % screen_width
            mountain_x = scroll * 0.2 % screen_width
            pine1_x = scroll * 0.6 % screen_width
            pine2_x = scroll * 0.8 % screen_width

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

            # Update and draw enemies
            enemies.update()
            for enemy in enemies:
                enemy.draw(screen, scroll)
                enemy.check_collisions(laser_group, scroll)

            laser_group.update(screen_width)
            laser_group.draw(screen)
            player.check_collisions(laser_group, scroll)
            world.check_laser_collisions(laser_group)

            # Draw HUD elements
            draw_time()
            draw_score()
            draw_level()
            draw_lives()

            # Update timer only if the game hasn't been won
            timer += 1/60  # Assuming 60 FPS

        elif game_paused:
            draw_pause_background()
            options()
        elif player_lives <= 0:
            game_over_screen()
    elif game_state == "win":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        game_win()

    # Update display
    pygame.display.flip()
    clock.tick(60)
