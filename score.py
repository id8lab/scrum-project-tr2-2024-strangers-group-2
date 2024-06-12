# Dongfang Keer is working on the score

score = 0

score_text = font.render(f'Score: {score}', True, white)
score_rect = score_text.get_rect()
score_rect.topright = (SCREEN_WIDTH - 10, 10)
screen.blit(score_text, score_rect)