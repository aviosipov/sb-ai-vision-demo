import pygame
from shared import game_settings as settings
from shared.scene import Scene
from shared.font import load_font
from shared.ui import draw_rectangle
from shared.ui import draw_breathing_text
from shared.slideshow import Slideshow

class GameOverConfig:
    def __init__(self):
        self.fade_out_duration = 1000  # Fade out duration in milliseconds
        self.breathing_duration = 1200  # Breathing effect duration in milliseconds
        self.zoom_speed = 0.05
        self.pan_speed = 0.02
        self.max_zoom_level = 1.8

class GameOver(Scene):
    def __init__(self, screen, audio_file, image_files, config):
        super().__init__(screen)  # Call the parent class constructor
        self.bg_music = audio_file  # Set the background music file
        self.breathing_duration = config.breathing_duration
        self.breathing_timer = 0
        self.text_alpha = 255

        self.slideshow = Slideshow(screen, audio_file, image_files, config)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.switch_to_scene("start_game")  # Switch to the start_game scene

    def update(self, dt):
        self.slideshow.update(dt)

        self.breathing_timer = (self.breathing_timer + dt * 1000) % self.breathing_duration
        self.text_alpha = int(255 * (1 - (self.breathing_timer / self.breathing_duration)))

        if self.slideshow.fade_out_alpha == 0:
            self.switch_to_scene("start_game")  # Switch to the start_game scene when the fade out is complete

    def draw(self):
        self.slideshow.draw()

        text_bg_color = (50, 50, 50)  # Dark gray
        draw_rectangle(self.screen, 0, settings.SCREEN_HEIGHT - 75, settings.SCREEN_WIDTH, 50, text_bg_color, opacity=160)
        draw_breathing_text(self.screen, "Press Enter to Try Again", settings.WHITE, (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 50), self.breathing_duration, self.breathing_timer)

    def reset(self):
        super().reset()  # Call the reset method of the parent class
        self.breathing_timer = 0
        self.text_alpha = 255
        self.play_bg_music(loops=0)  # Play the background music only once
        self.next_scene = None  # Reset the next_scene attribute
        self.slideshow.reset()  # Reset the slideshow