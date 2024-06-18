import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))

jump_sound = pygame.mixer.Sound("sounds\jump.wav")
shoot_sound = pygame.mixer.Sound("sounds\shooting.wav")
losehp_sound = pygame.mixer.Sound("sounds\losehp.wav")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jump_sound.play()
            elif event.key == pygame.K_s:
                shoot_sound.play()
            elif event.key == pygame.K_h:
                losehp_sound.play()

    screen.fill((255, 255, 255))

    pygame.display.flip()

pygame.quit()
sys.exit()

