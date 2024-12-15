import pygame
class Sounds:

    def __init__(self):

        pygame.mixer.init()

        self.jump_sound = pygame.mixer.Sound(r"sounds\jump.wav")
        self.shoot_sound = pygame.mixer.Sound(r"sounds\shooting.wav")
        self.losehp_sound = pygame.mixer.Sound(r"sounds\losehp.wav")
        self.ui_sound = pygame.mixer.Sound(r"sounds\ui 1.wav")
        self.game_over_sound = pygame.mixer.Sound(r"sounds\game-over-arcade-6435.mp3")
        self.enemy_spawn_sound = pygame.mixer.Sound(r"sounds\enemyspawn.wav")
        
        self.bg_music = {
            3: r"sounds\arabic-desert-196240.mp3",
            2: r"sounds\6- The Veil of Night.mp3",
            1: r"sounds\Pixel 1.wav"}

    def play_jump_sound(self):
        self.jump_sound.play()

    def play_shoot_sound(self):
        self.shoot_sound.play()

    def play_losehp_sound(self):
        self.losehp_sound.play()

    def play_ui_sound(self):
        self.ui_sound.play()

    def play_game_over_sound(self):
        self.game_over_sound.play()

    def play_enemy_spawn_sound(self):
        self.enemy_spawn_sound.play()

    def play_bg_music_for_level(self, level):
        pygame.mixer.music.load(self.bg_music[level])
        pygame.mixer.music.play(-1)
        
    def stop_bg_music(self):
        pygame.mixer.music.stop()

    def pause_bg_music(self):
        pygame.mixer.music.pause()

    def unpause_bg_music(self):
        pygame.mixer.music.unpause()