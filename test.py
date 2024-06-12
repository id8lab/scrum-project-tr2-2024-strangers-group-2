import pygame

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

# HUD settings
font = pygame.font.SysFont('comicsans', 30)
WHITE = (255, 255, 255)
timer = 0
player_lives = 3
level = 1
level_up_timer = 0

# Load and resize heart image for player lives
heart_image = pygame.image.load('heart.png').convert_alpha()
heart_size = (30, 30)
heart_image = pygame.transform.scale(heart_image, heart_size)


# Function to draw HUD
def draw_hud():
    lives_text = font.render(f'Level: {level}  Lives:', True, WHITE)
    timer_text = font.render(f'Time: {int(timer)}', True, WHITE)
    screen.blit(lives_text, (10, 10))
    screen.blit(timer_text, (SCREEN_WIDTH - timer_text.get_width() - 10, 10))

    # Draw hearts for player lives
    heart_spacing = 5
    lives_text_width = lives_text.get_width()
    for i in range(player_lives):
        screen.blit(heart_image, (lives_text_width + 20 + i * (heart_size[0] + heart_spacing), 15))


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
        self.rect.center = (x, GROUND_LEVEL)
        self.base_y = GROUND_LEVEL
        self.ground_level = GROUND_LEVEL  # Set ground level attribute

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

        self.vel_y += GRAVITY

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

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


player_images = [
    '8dd889acea826111937568e2301697c6-removebg-preview.png',
    'Screenshot_2024-06-11_143220-removebg-preview.png',
    'Screenshot_2024-06-11_160603-removebg-preview.png',
    'Screenshot_2024-06-11_143220-removebg-preview.png',
    '8dd889acea826111937568e2301697c6-removebg-preview.png'
]
enemy_image = '72d04ccc6edc0e1bb0a65400ca2671fe-removebg-preview.png'

player = Monster(player_images, 200, 0.15, 5)
enemy = Monster([enemy_image], 400, 0.3, 5)

# Game loop
run = True
while run:
    clock.tick(FPS)
    timer += 1 / FPS  # Timer increment

    # Level up logic
    level_up_timer += 1 / FPS
    if level_up_timer >= 30:  # Increase level every 30 seconds
        level += 1
        level_up_timer = 0

    # Draw background
    screen.fill(BG)

    # Draw HUD
    draw_hud()

    # Draw sprites
    player.draw()
    enemy.update_animation()
    enemy.draw()

    # Move player
    player.move(moving_left, moving_right)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                player.jump = True
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