import pygame
import numpy as np
from scipy.interpolate import interp1d
from shared import game_settings as settings
from shared.scene import Scene
from shared.font import load_font
from shared.ui import draw_rectangle
from shared.ui import draw_breathing_text
from shared.spaceship_animation import SpaceshipAnimation
from shared.scene_utils import handle_scene_restart
from scipy.interpolate import splprep, splev
from shared.path_utils import create_smooth_path


class AnimationEditor(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.screen = screen
        self.background_image = pygame.image.load('assets/start_game/game-intro.png')
        self.background = pygame.transform.scale(self.background_image, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.breathing_duration = 1200
        self.breathing_timer = 0

        self.spaceship_animations = self.create_spaceship_animations()
        self.selected_animation = 0
        self.editing_mode = False
        self.waypoints = []


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

        for animation in animations:
            animation.smooth_path = create_smooth_path(animation.path)  # Initialize the smooth_path attribute

        return animations
    

    def reset(self):
        self.breathing_timer = 0
        for animation in self.spaceship_animations:
            animation.reset()
        self.waypoints = []

    def handle_events(self, event):
        handle_scene_restart(event, self.reset)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.next_scene = "start_game"
            elif event.key == pygame.K_e:
                self.editing_mode = not self.editing_mode
            elif event.key == pygame.K_LEFT:
                self.selected_animation = (self.selected_animation - 1) % len(self.spaceship_animations)
            elif event.key == pygame.K_RIGHT:
                self.selected_animation = (self.selected_animation + 1) % len(self.spaceship_animations)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.editing_mode:
                self.add_waypoint(event.pos)

    def update(self, dt):
        self.breathing_timer = (self.breathing_timer + dt * 1000) % self.breathing_duration

        for animation in self.spaceship_animations:
            animation.update(dt)

    def draw(self):
        self.screen.fill(settings.BLACK)
        self.screen.blit(self.background, (0, 0))

        for i, animation in enumerate(self.spaceship_animations):
            if animation.scale > 0:
                scaled_image = pygame.transform.scale(
                    animation.image,
                    (int(animation.image.get_width() * animation.scale), int(animation.image.get_height() * animation.scale))
                )
                position = animation.get_position()
                x, y = position
                rect = scaled_image.get_rect(center=(x, y))
                self.screen.blit(scaled_image, rect)

            self.draw_path(i)

            if animation.scale > 0:
                current_position = animation.get_position()
                pygame.draw.line(self.screen, settings.WHITE, animation.prev_position, current_position, 1)
                animation.prev_position = current_position

            self.draw_waypoints(i)




        text_bg_color = (50, 50, 50)
        draw_rectangle(self.screen, 0, settings.SCREEN_HEIGHT - 85, settings.SCREEN_WIDTH, 50, text_bg_color, opacity=153)
        draw_breathing_text(self.screen, "Press Enter to Return to Start", settings.WHITE, (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 60), self.breathing_duration, self.breathing_timer)

    def add_waypoint(self, pos):
        self.spaceship_animations[self.selected_animation].path = np.append(self.spaceship_animations[self.selected_animation].path, [pos], axis=0)
        self.spaceship_animations[self.selected_animation].smooth_path = create_smooth_path(self.spaceship_animations[self.selected_animation].path)  # Update the smooth_path attribute

    def update_animation_path(self):
        self.smooth_path = self.create_smooth_path(self.path)  # Assuming create_smooth_path is your spline generation method


    def create_smooth_path(self, path):
        if len(path) > 2:  # We need at least 3 points to create a smooth spline
            tck, u = splprep(path.T, u=None, s=0.0)  # You may adjust the s parameter for smoothing
            u_new = np.linspace(u.min(), u.max(), 1000)
            x_new, y_new = splev(u_new, tck, der=0)
            smooth_path = np.vstack((x_new, y_new)).T
            return smooth_path
        else:
            return path



    def draw_path(self, animation_index):
        animation = self.spaceship_animations[animation_index]
        if len(animation.path) >= 2:
            pygame.draw.lines(self.screen, settings.WHITE, False, animation.smooth_path, 2)

    def draw_waypoints(self, animation_index):
        animation = self.spaceship_animations[animation_index]
        for waypoint in animation.path:
            pygame.draw.circle(self.screen, settings.YELLOW, waypoint, 5)
