import pygame

class Monster(pygame.sprite.Sprite):
    def __init__(self, image_paths, x, scale, speed, world):  # Accept `world` as a parameter
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
        self.world = world  # Store `world` as an instance variable

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
            self.vel_y = -11
            self.jump = False
            self.on_ground = False

        self.vel_y += 0.75  # GRAVITY

        dy += self.vel_y 

        # Check for ground collision
        self.rect.x += dx
        for tile in self.world.floor_list:  # Use self.world.floor_list instead of world.floor_list
            if tile.colliderect(self.rect):
                if dx > 0:
                    self.rect.right = tile.left
                if dx < 0:
                    self.rect.left = tile.right
        self.rect.y += dy
        for tile in self.world.floor_list:  # Use self.world.floor_list instead of world.floor_list
            if tile.colliderect(self.rect):
                if dy > 0:
                    self.rect.bottom = tile.top
                    self.vel_y = 0
                    self.on_ground = True
                if dy < 0:
                    self.rect.top = tile.bottom

        # Check collision with obstacles
        for obstacle in self.world.obstacle_list:  # Use self.world.obstacle_list instead of world.obstacle_list
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
