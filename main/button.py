import pygame

# button class
# class Button():
#     def __init__(self, x, y, image, scale):
#         width = image.get_width()
#         height = image.get_height()
#         self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (x, y)
#         self.clicked = False

#     def draw(self, surface):
#         # draw button on screen
#         # surface.blit(self.image, (self.rect.x, self.rect.y))
#         # ation = False
#         # return action
    
#     # def click(self):
#         action = False
#         # get mouse position
#         pos = pygame.mouse.get_pos()

#         # check mouseover and clicked conditions
#         if self.rect.collidepoint(pos):
#             if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
#                 action = True
#                 self.clicked = True
#                 print(f"Button at {self.rect.topleft} clicked")

#         if pygame.mouse.get_pressed()[0] == 0:
#             self.clicked = False

#         surface.blit(self.image, (self.rect.x, self.rect.y))
        
#         return action

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.pressed = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.pressed:
                self.pressed = True
            if pygame.mouse.get_pressed()[0] == 0 and self.pressed:
                self.pressed = False
                action = True

        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action
