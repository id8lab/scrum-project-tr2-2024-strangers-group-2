import pygame

def draw_time(screen, font, timer, color, screen_width, screen_height):
    minutes = int(timer) // 60
    seconds = int(timer) % 60
    timer_text = font.render(f'{minutes:02}:{seconds:02}', True, color)
    screen.blit(timer_text, (screen_width - timer_text.get_width() - 10, screen_height - timer_text.get_height() - 10))

def draw_score(screen, font, score, color, screen_width):
    score_text = font.render(f'Score: {score}', True, color)
    screen.blit(score_text, (screen_width - score_text.get_width() - 10, 10))

def draw_level(screen, font, level, color, screen_width):
    level_text = font.render(f'Level: {level}', True, color)
    level_x = (screen_width - level_text.get_width()) // 2
    screen.blit(level_text, (level_x, 10))

def draw_lives(screen, font, lives, color, x, y):
    lives_text = font.render(f'Lives:', True, color)
    screen.blit(lives_text, (x, y))
    heart_size = (40, 40)
    heart_y = y + (lives_text.get_height() - heart_size[1]) // 2
    for i in range(lives):
        heart_x = x + lives_text.get_width() + 20 + i * (heart_size[0] + 10)
        heart_pos = (heart_x, heart_y)
        screen.blit(pygame.transform.scale("img_element\heart.png", heart_size), heart_pos)
