import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
GROUND_LEVEL = SCREEN_HEIGHT - 70  # Adjust this value based on your character's height and desired ground level

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')

clock = pygame.time.Clock()
FPS = 60

GRAVITY = 0.75

moving_left = False
moving_right = False

BG = (144, 201, 120)
# placeholder
def draw_bg():
    screen.fill(BG)

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

run = True
while run:
    clock.tick(FPS)
    draw_bg()

    player.draw()
    enemy.update_animation()
    enemy.draw()

    player.move(moving_left, moving_right)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # button press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False
        # button release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    pygame.display.update()

pygame.quit()
