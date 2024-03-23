# scenes/start_game.py
import pygame
import numpy as np
from shared import game_settings as settings
from shared.scene import Scene
from shared.font import load_font
from shared.ui import draw_rectangle
from shared.ui import draw_breathing_text
from shared.spaceship_animation import SpaceshipAnimation
from shared.scene_utils import handle_scene_restart

class StartGame(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.screen = screen
        self.background_image = pygame.image.load('assets/start_game/game-intro.png')
        self.background = pygame.transform.scale(self.background_image, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.breathing_duration = 1200
        self.breathing_timer = 0

        self.spaceship_animations = self.create_spaceship_animations()

    def create_spaceship_animations(self):
        spaceship_images = [
            pygame.image.load('assets/spaceships/spaceship1.png'),
            pygame.image.load('assets/spaceships/spaceship2.png'),
            pygame.image.load('assets/spaceships/spaceship3.png')
        ]

        spaceship_paths = [
            np.array([[100, 100], [200, 200], [300, 150], [400, 250]]),
            np.array([[400, 100], [300, 200], [200, 150], [100, 250]]),
            np.array([[200, 50], [300, 100], [400, 200], [300, 300]])
        ]

        spaceship_times = [
            np.array([0, 1000, 2000, 3000]),
            np.array([0, 1500, 2500, 3500]),
            np.array([0, 1200, 2200, 3200])
        ]

        spaceship_durations = [3000, 3500, 3200]

        animations = [
            SpaceshipAnimation(image, path, times, duration)
            for image, path, times, duration in zip(spaceship_images, spaceship_paths, spaceship_times, spaceship_durations)
        ]

        return animations

    def reset(self):
        self.breathing_timer = 0
        for animation in self.spaceship_animations:
            animation.reset()

    def handle_events(self, event):
        handle_scene_restart(event, self.reset)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.next_scene = "spaceship_selection"
        return None

    def update(self, dt):
        self.breathing_timer = (self.breathing_timer + dt * 1000) % self.breathing_duration

        for animation in self.spaceship_animations:
            animation.update(dt)

    def draw(self):
        self.screen.fill(settings.BLACK)
        self.screen.blit(self.background, (0, 0))

        for animation in self.spaceship_animations:
            if animation.scale > 0:
                scaled_image = pygame.transform.scale(
                    animation.image,
                    (int(animation.image.get_width() * animation.scale), int(animation.image.get_height() * animation.scale))
                )
                position = animation.get_position()
                if position is not None:
                    x, y = position
                    rect = scaled_image.get_rect(center=(x, y))
                    self.screen.blit(scaled_image, rect)

        text_bg_color = (50, 50, 50)
        draw_rectangle(self.screen, 0, settings.SCREEN_HEIGHT - 85, settings.SCREEN_WIDTH, 50, text_bg_color, opacity=153)
        draw_breathing_text(self.screen, "Press Enter to Start", settings.WHITE, (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 60), self.breathing_duration, self.breathing_timer)