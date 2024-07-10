import pygame
import button

pygame.init()

# create game window with increased size
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

# Initialize the screen with the new size
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

# Define constants
TEXT_COL = (255, 255, 255)  # White color
font_size = 36

# game variable
game_paused = False
menu_state = "main"

# Load the font
font = pygame.font.Font(None, font_size)  # None means default font

# load button images
resume_img = pygame.image.load("C:/Users/ADMIN/Downloads/scrum-project-tr2-2024-strangers-group-2-4/Setting_page/images/button_resume.png").convert_alpha()
options_img = pygame.image.load("C:/Users/ADMIN/Downloads/scrum-project-tr2-2024-strangers-group-2-4/Setting_page/images/button_options.png").convert_alpha()
quit_img = pygame.image.load("C:/Users/ADMIN/Downloads/scrum-project-tr2-2024-strangers-group-2-4/Setting_page/images/button_quit.png").convert_alpha()
video_img = pygame.image.load("C:/Users/ADMIN/Downloads/scrum-project-tr2-2024-strangers-group-2-4/Setting_page/images/button_video.png").convert_alpha()
audio_img = pygame.image.load("C:/Users/ADMIN/Downloads/scrum-project-tr2-2024-strangers-group-2-4/Setting_page/images/button_audio.png").convert_alpha()
keys_img = pygame.image.load("C:/Users/ADMIN/Downloads/scrum-project-tr2-2024-strangers-group-2-4/Setting_page/images/button_keys.png").convert_alpha()
back_img = pygame.image.load("C:/Users/ADMIN/Downloads/scrum-project-tr2-2024-strangers-group-2-4/Setting_page/images/button_back.png").convert_alpha()

# create button instances with adjusted positions for larger screen
resume_button = button.Button(412, 200, resume_img, 1)
options_button = button.Button(412, 300, options_img, 1)
quit_button = button.Button(412, 400, quit_img, 1)
video_button = button.Button(312, 200, video_img, 1)
audio_button = button.Button(312, 300, audio_img, 1)
keys_button = button.Button(312, 400, keys_img, 1)
back_button = button.Button(412, 500, back_img, 1)
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))
# Main loop
running = True
while running:
    screen.fill((52, 78, 91))

    # check if game is paused
    if game_paused:
        # check menu state
        if menu_state == "main":
            # draw pause screen buttons
            if resume_button.draw(screen):
                game_paused = False
            if options_button.draw(screen):
                menu_state = "options"
            if quit_button.draw(screen):
                running = False
        elif menu_state == "options":
            if video_button.draw(screen):
                pass  # Placeholder for actual video settings action
            if audio_button.draw(screen):
                pass  # Placeholder for actual audio settings action
            if keys_button.draw(screen):
                pass  # Placeholder for actual keys settings action
            if back_button.draw(screen):
                menu_state = "main"
    else:
        draw_text("Press SPACE to pause", font, TEXT_COL, 412, 375)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_paused = not game_paused
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
