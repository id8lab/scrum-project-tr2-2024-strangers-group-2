import pygame
import sys
from sounds import Sounds

pygame.init()

sounds = Sounds()



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
            if event.key == pygame.K_1:
                sounds.play_bg_music_for_level(1)
            elif event.key == pygame.K_2:
                sounds.play_bg_music_for_level(2)
            elif event.key == pygame.K_3:
                sounds.play_bg_music_for_level(3)
            elif event.key == pygame.K_p:
                sounds.pause_bg_music()
            elif event.key == pygame.K_u:
                sounds.unpause_bg_music()
            elif event.key == pygame.K_q:
                running = False

    screen.fill((255, 255, 255))

    pygame.display.flip()

pygame.quit()
sys.exit()

