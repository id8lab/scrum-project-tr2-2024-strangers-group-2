import pygame
import sys

screen_width = 800
screen_height = int(screen_width * 0.8)
screen = pygame.display.set_mode((screen_width, screen_height))

# define color
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# set life stats
max_hp = 100
current_hp = max_hp

# hp bar setting
bar_width = 200
bar_height = 30
bar_x = (screen_width - bar_width) // 2
bar_y = 50


def draw_hp_bar(current_hp, max_hp):
    # calculate current hp ratio
    hp_ratio = current_hp / max_hp
    # draw life bar
    pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (bar_x, bar_y, bar_width * hp_ratio, bar_height))


def main():
    global current_hp

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_hp = min(current_hp + 10, max_hp)
                elif event.key == pygame.K_DOWN:
                    current_hp = max(current_hp - 10, 0)

        screen.fill(WHITE)
        draw_hp_bar(current_hp, max_hp)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
