class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_paths, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.direction = 1
        self.animation_list = []
        self.index = 0
        self.update_time = pygame.time.get_ticks()
        self.flip = False
        self.on_ground = True  
        self.vel_y = 0

        for image_path in image_paths:
            image = pygame.image.load(image_path).convert_alpha()
            width = int(image.get_width() * scale)
            height = int(image.get_height() * scale)
            image = pygame.transform.scale(image, (width, height))
            self.animation_list.append(image)

        self.image = self.animation_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.move_counter = 0

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