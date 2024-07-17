# import pygame

# pygame.init()

# class Laser(pygame.sprite.Sprite):
    # def __init__(self, x, y, direction, scroll):
    #     pygame.sprite.Sprite.__init__(self)
    #     self.image = pygame.Surface((10, 2))
    #     self.image.fill((255, 0, 0))  # Red laser
    #     self.rect = self.image.get_rect()
    #     self.rect.center = (x, y)
    #     self.speed = 5 * direction
    #     self.direction = direction
    #     self.scroll = scroll

    # def update(self, screen_width, scroll):
    #     # self.rect.x += self.speed
    #     self.rect.x += self.speed - self.scroll[0] + scroll[0]
    #     self.rect.y -= self.scroll[1] - scroll[1]
    #     if self.rect.right < 0 or self.rect.left > screen_width:
    #         self.kill()  # Remove the laser if it goes off-screen

import pygame

pygame.init()

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 2))
        self.image.fill((255, 0, 0))  # Red laser
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5 * direction  # direction should be 1 for right, -1 for left
        self.initial_x = x  # Store the initial x position in the game world

    def update(self, scroll):
        # Move the laser based on its speed
        self.initial_x += self.speed
        
        # Update the laser's position relative to the scroll
        self.rect.centerx = self.initial_x - scroll

        # Remove the laser if it goes off-screen
        if self.rect.right < 0 or self.rect.left > pygame.display.get_surface().get_width():
            self.kill()
