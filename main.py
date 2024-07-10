import pygame


pygame.init()
# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

def draw_text(text,font,text_col, x,y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x,y))


#game loop
run = True
while run:


  screen.fil((52,78, 91))

# event.handler
for