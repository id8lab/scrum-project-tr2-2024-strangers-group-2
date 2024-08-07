class Score:
    def __init__(self):
        self.score = 0

    def increase_score(self, amount):
        """Increase the score by the specified amount."""
        self.score += amount

    def decrease_score(self, amount):
        """Decrease the score by the specified amount (e.g., when losing a life)."""
        self.score -= amount
        if self.score < 0:
            self.score = 0

    def get_score(self):
        """Return the current score."""
        return self.score

    def reset_score(self):
        """Reset the score to zero."""
        self.score = 0

    def draw_score(self, screen, font):
        """Draw the score on the screen."""
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        screen.blit(score_text, (screen.get_width() - score_text.get_width() - 10, 10))


# Usage example
if __name__ == "__main__":
    import pygame

    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.SysFont('comicsans', 50)

    score = Score()

    # Simulate increasing and decreasing score
    score.increase_score(10)
    score.decrease_score(5)

    # Main loop to draw score
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        score.draw_score(screen, font)
        pygame.display.flip()

    pygame.quit()
