import pygame
from config import TILE_SIZE

class World:
    def __init__(self):
        self.obstacle_list = []
        self.floor_list = []

    def process_data(self, data):
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(img_rect)
                        self.floor_list.append(img_rect)

    def draw(self, screen, scroll):
        for tile in self.obstacle_list:
            tile_rect = tile.move(scroll, 0)
            pygame.draw.rect(screen, (144, 201, 120), tile_rect)
            pygame.draw.rect(screen, (0, 0, 0), tile_rect, 2)
